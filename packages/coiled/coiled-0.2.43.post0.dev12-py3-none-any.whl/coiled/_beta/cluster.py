from __future__ import annotations

import asyncio
import contextlib
import datetime
import logging
import re
import sys
import time
import uuid
import warnings
import weakref
from contextlib import suppress
from copy import deepcopy
from os import environ
from pathlib import Path
from typing import Dict, Generic, Iterable, List, Optional, Set, Tuple, Union

import dask
import dask.distributed
from coiled import magic
from coiled._beta.core import (
    AWSOptions,
    CloudBeta,
    GCPOptions,
    log_cluster_debug_info,
    setup_logging,
)
from coiled._beta.states import (
    ClusterStateEnum,
    InstanceStateEnum,
    ProcessStateEnum,
    flatten_log_states,
    log_states,
    summarize_status,
)
from coiled._beta.widgets import EXECUTION_CONTEXT, HAS_RICH
from coiled.cluster import Cluster, CredentialsPreferred
from coiled.compatibility import DISTRIBUTED_VERSION
from coiled.context import track_context
from coiled.core import IsAsynchronous
from coiled.errors import ClusterCreationError, DoesNotExist
from coiled.exceptions import ArgumentCombinationError, InstanceTypeError
from coiled.utils import (
    COILED_LOGGER_NAME,
    cluster_firewall,
    get_details_url,
    get_instance_type_from_cpu_memory,
    name_to_version,
    parse_identifier,
    parse_wait_for_workers,
    validate_vm_typing,
)
from IPython.display import display
from typing_extensions import Literal

from .cwi_log_link import cloudwatch_url

logger = logging.getLogger(COILED_LOGGER_NAME)


def use_rich_widget():
    return EXECUTION_CONTEXT in ["ipython_terminal", "notebook"] and HAS_RICH


def use_html_widget():
    return False


BEHAVIOR_TO_LEVEL = {"critical-only": 100, "warning-or-higher": 50, "any": 0}


class ClusterBeta(Cluster, Generic[IsAsynchronous]):
    """Create a Dask cluster with Coiled

    Parameters
    ----------
    n_workers
        Number of workers in this cluster. Defaults to 4.
    name
        Name to use for identifying this cluster. Defaults to ``None``.
    software
        Name of the software environment to use.
    worker_class
        Worker class to use. Defaults to :class:`distributed.nanny.Nanny`.
    worker_options
        Mapping with keyword arguments to pass to ``worker_class``. Defaults
        to ``{}``.
    worker_vm_types
        List of instance types that you would like workers to use, default instance type
        selected contains 2 cores. You can use the command ``coiled.list_instance_types()``
        to see a list of allowed types.
    worker_cpu
        Number, or range, of CPUs requested for each worker. Specify a range by
        using a list of two elements, for example: ``worker_cpu=[2, 8]``.
    worker_memory
        Amount of memory to request for each worker, Coiled will use a +/- 10% buffer
        from the memory that you specify. You may specify a range of memory by using a
        list of two elements, for example: ``worker_memory=["2GiB", "4GiB"]``.
    worker_disk_size
        Non-default size of persistent disk attached to each worker instance, specified
        in GB.
    worker_gpu
        For instance types that don't come with a fixed number of GPUs, the number of
        GPUs to attach. This only applies to GCP, and will default to 1 if you specify
        ``worker_gpu_type``. Coiled currently only supports a single GPU per instance.
    worker_gpu_type
        For instance types that don't always come with GPU, the type of GPU to attach.
        This only applied to GCP. Should match the way the cloud provider specifies the
        GPU, for example: ``worker_gpu_type="nvidia-tesla-t4"``.
    scheduler_class
        Scheduler class to use. Defaults to :class:`distributed.scheduler.Scheduler`.
    scheduler_options
        Mapping with keyword arguments to pass to ``scheduler_class``. Defaults
        to ``{}``.
    scheduler_vm_types
        List of instance types that you would like the scheduler to use, default instances
        type selected contains 2 cores. You can use the command
        ``coiled.list_instance_types()`` to se a list of allowed types.
    scheduler_cpu
        Number, or range, of CPUs requested for the scheduler. Specify a range by
        using a list of two elements, for example: ``scheduler_cpu=[2, 8]``.
    scheduler_memory
        Amount of memory to request for the scheduler, Coiled will use a +/-10%
        buffer from the memory what you specify. You may specify a range of memory by using a
        list of two elements, for example: ``scheduler_memory=["2GiB", "4GiB"]``.
    asynchronous
        Set to True if using this Cloud within ``async``/``await`` functions or
        within Tornado ``gen.coroutines``. Otherwise this should remain
        ``False`` for normal use. Default is ``False``.
    cloud
        Cloud object to use for interacting with Coiled. This object contains user/authentication/account
        information. If this is None (default), we look for a recently-cached Cloud object, and if none
        exists create one.
    account
        Name of Coiled account to use. If not provided, will
        default to the user account for the ``cloud`` object being used.
    shutdown_on_close
        Whether or not to shut down the cluster when it finishes.
        Defaults to True, unless name points to an existing cluster.
    use_scheduler_public_ip
        Boolean value that determines if the Python client connects to the
        Dask scheduler using the scheduler machine's public IP address. The
        default behaviour when set to True is to connect to the scheduler
        using its public IP address, which means traffic will be routed over
        the public internet. When set to False, traffic will be routed over
        the local network the scheduler lives in, so make sure the scheduler
        private IP address is routable from where this function call is made
        when setting this to False.
    credentials
        Which credentials to use for Dask operations and forward to Dask
        clusters -- options are "account", "local", or "none". The default
        behavior is to use local credentials if available.
        NOTE: credential handling currently only works with AWS credentials.
    timeout
        Timeout in seconds to wait for a cluster to start, will use
        ``default_cluster_timeout`` set on parent Cloud by default.
    environ
        Dictionary of environment variables.
    send_dask_config
        Whether to send a frozen copy of local dask.config to the cluster.
    backend_options
        Dictionary of backend specific options.
    tags
        Dictionary of tags.
    wait_for_workers
        Whether to wait for a number of workers before returning control
        of the prompt back to the user. Usually, computations will run better
        if you wait for most workers before submitting tasks to the cluster.
        You can wait for all workers by passing ``True``, or not wait for any
        by passing ``False``. You can pass a fraction of the total number of
        workers requested as a float(like 0.6), or a fixed number of workers
        as an int (like 13). If None, the value from ``coiled.wait-for-workers``
        in your Dask config will be used. Default: 0.3. If the requested number
        of workers don't launch within 10 minutes, the cluster will be shut
        down, then a TimeoutError is raised.
    package_sync
        Attempt to synchronize package versions between your local environment and the cluster.
        Cannot be used with the `software` option. Passing `True` will sync all packages (recommended).
        Passing specific packages as a list of strings will attempt to synchronize only those packages,
        use with caution.
        We strongly recommend reading the additional documentation
        for this feature (see https://docs.coiled.io/user_guide/package_sync.html)!
    package_sync_strict
        Only allow exact packages matches, not recommended unless your client platform/architecture
        matches the cluster platform/architecture
    private_to_creator
        Only allow the cluster creator, not other members of team account, to connect to this cluster.
    scheduler_port
        Specify a port other than the default (8786) for communication with Dask scheduler; this is useful
        if your client is on a network that blocks 8786.
    allow_ingress_from
        Control the CIDR from which cluster firewall allows ingress to scheduler; by default this is open
        to any source address (0.0.0.0/0). You can specify CIDR, or "me" for just your IP address.
    allow_ssh
        Allow connections to scheduler over port 22, used for SSH.
    """

    _instances = weakref.WeakSet()

    def __init__(
        self,
        name: Optional[str] = None,
        *,
        software: str = None,
        n_workers: int = 4,
        worker_class: str = None,
        worker_options: dict = None,
        worker_vm_types: Optional[list] = None,
        worker_cpu: Union[int, List[int]] = None,
        worker_memory: Union[str, List[str]] = None,
        worker_disk_size: Optional[int] = None,
        worker_gpu: int = None,
        worker_gpu_type: Optional[str] = None,
        scheduler_class: str = None,
        scheduler_options: dict = None,
        scheduler_vm_types: Optional[list] = None,
        scheduler_cpu: Union[int, List[int]] = None,
        scheduler_memory: Union[str, List[str]] = None,
        asynchronous: bool = False,
        cloud: CloudBeta = None,
        account: str = None,
        shutdown_on_close=None,
        use_scheduler_public_ip: Optional[bool] = None,
        credentials: Optional[str] = "local",
        timeout: Optional[Union[int, float]] = None,
        environ: Optional[Dict[str, str]] = None,
        tags: Optional[Dict[str, str]] = None,
        send_dask_config: bool = True,
        backend_options: Optional[
            Union[AWSOptions, GCPOptions]
        ] = None,  # intentionally not in the docstring yet
        show_widget: bool = True,
        configure_logging: bool = False,
        wait_for_workers: Optional[Union[int, float, bool]] = None,
        package_sync: Union[bool, List[str]] = False,
        package_sync_strict: bool = False,
        package_sync_fail_on: Literal[
            "critical-only", "warning-or-higher", "any"
        ] = "critical-only",
        private_to_creator: Optional[bool] = None,
        # easier network config
        scheduler_port: Optional[int] = None,
        allow_ingress_from: Optional[str] = None,
        allow_ssh: Optional[bool] = None,
    ):
        type(self)._instances.add(self)
        self.package_sync = bool(
            package_sync
        )  # TODO: this should be mutually exclusive with passing a software env
        if isinstance(package_sync, list):
            # ensure python is always included
            self.package_sync_only = set(package_sync)
            self.package_sync_only.add("python")
        else:
            self.package_sync_only = None
        self.package_sync_strict = package_sync_strict
        self.package_sync_fail_on = BEHAVIOR_TO_LEVEL[package_sync_fail_on]
        self.show_widget = show_widget
        self._cluster_status_logs = []
        if configure_logging:
            setup_logging()

        # Determine consistent sync/async
        if cloud and asynchronous is not None and cloud.asynchronous != asynchronous:
            warnings.warn(
                f"Requested a Cluster with asynchronous={asynchronous}, but "
                f"cloud.asynchronous={cloud.asynchronous}, so the cluster will be"
                f"{cloud.asynchronous}"
            )

            asynchronous = cloud.asynchronous

        self.scheduler_comm: Optional[dask.distributed.rpc] = None

        # It's annoying that the user must pass in `asynchronous=True` to get an async Cluster object
        # But I can't think of a good alternative right now.
        self.cloud: CloudBeta[IsAsynchronous] = cloud or CloudBeta.current(
            asynchronous=asynchronous
        )
        # if cloud:
        #     self.cleanup_cloud = False
        #     self.cloud: CloudBeta[IsAsynchronous] = cloud
        # else:
        #     self.cleanup_cloud = True
        #     self.cloud: CloudBeta[IsAsynchronous] = CloudBeta(asynchronous=asynchronous)

        # As of distributed 2021.12.0, deploy.Cluster has a ``loop`` attribute on the
        # base class. We add the attribute manually here for backwards compatibility.
        # TODO: if/when we set the minimum distributed version to be >= 2021.12.0,
        # remove this check.
        if DISTRIBUTED_VERSION >= "2021.12.0":
            kwargs = {"loop": self.cloud.loop}
        else:
            kwargs = {}
            self.loop = self.cloud.loop

        # we really need to call this first before any of the below code errors
        # out; otherwise because of the fact that this object inherits from
        # deploy.Cloud __del__ (and perhaps __repr__) will have AttributeErrors
        # because the gc will run and attributes like `.status` and
        # `.scheduler_comm` will not have been assigned to the object's instance
        # yet
        super(Cluster, self).__init__(asynchronous, **kwargs)

        self.timeout = (
            timeout if timeout is not None else self.cloud.default_cluster_timeout
        )
        self.private_to_creator = (
            dask.config.get("coiled.private-to-creator")
            if private_to_creator is None
            else private_to_creator
        )
        self.software_environment = software or dask.config.get("coiled.software")
        self.worker_class = worker_class or dask.config.get("coiled.worker.class")
        self.worker_cpu = worker_cpu or dask.config.get("coiled.worker.cpu")

        if isinstance(worker_cpu, int) and worker_cpu <= 1:
            raise ValueError("`worker_cpu` should be at least 2.")

        self.worker_memory = worker_memory or dask.config.get("coiled.worker.memory")
        self.worker_vm_types = worker_vm_types
        self.worker_disk_size = worker_disk_size
        self.worker_gpu_count = worker_gpu
        self.worker_gpu_type = worker_gpu_type
        self.worker_options = {
            **(dask.config.get("coiled.worker-options", {})),
            **(worker_options or {}),
        }

        self.scheduler_class = scheduler_class or dask.config.get(
            "coiled.scheduler.class"
        )

        self.scheduler_class = scheduler_class or dask.config.get(
            "coiled.scheduler.class"
        )

        self.scheduler_class = scheduler_class or dask.config.get(
            "coiled.scheduler.class"
        )
        self.scheduler_cpu = scheduler_cpu or dask.config.get("coiled.scheduler.cpu")
        self.scheduler_memory = scheduler_memory or dask.config.get(
            "coiled.scheduler.memory"
        )
        self.scheduler_vm_types = scheduler_vm_types
        self.scheduler_options = {
            **(dask.config.get("coiled.scheduler-options", {})),
            **(scheduler_options or {}),
        }

        self.name = name or dask.config.get("coiled.name")
        self.account = account
        self._start_n_workers = n_workers
        self._lock = None
        self._asynchronous = asynchronous
        if shutdown_on_close is None:
            shutdown_on_close = dask.config.get("coiled.shutdown-on-close")
        self.shutdown_on_close = shutdown_on_close
        self.environ = {k: str(v) for (k, v) in (environ or {}).items() if v}
        self.tags = {k: str(v) for (k, v) in (tags or {}).items() if v}
        self.frozen_dask_config = (
            deepcopy(dask.config.config) if send_dask_config else {}
        )
        self.credentials = CredentialsPreferred(credentials)
        self._default_protocol = dask.config.get("coiled.protocol", "tls")
        self._wait_for_workers_arg = wait_for_workers
        self._last_logged_state_summary = None

        self.worker_vm_types = worker_vm_types
        self.scheduler_vm_types = scheduler_vm_types

        # these are sets of names of workers, only including workers in states that might eventually reach
        # a "started" state
        # they're used in our implementation of scale up/down (mostly inherited from coiled.Cluster)
        # and their corresponding properties are used in adaptive scaling (at least once we
        # make adaptive work with ClusterBeta).
        #
        # (Adaptive expects attributes `requested` and `plan`, which we implement as properties below.)
        #
        # Some good places to learn about adaptive:
        # https://github.com/dask/distributed/blob/39024291e429d983d7b73064c209701b68f41f71/distributed/deploy/adaptive_core.py#L31-L43
        # https://github.com/dask/distributed/issues/5080
        self._requested: Set[str] = set()
        self._plan: Set[str] = set()

        self._adaptive_options: Dict[str, Union[str, int]] = {}
        self.cluster_id: Optional[int] = None
        self.use_scheduler_public_ip: bool = (
            dask.config.get("coiled.use_scheduler_public_ip", True)
            if use_scheduler_public_ip is None
            else use_scheduler_public_ip
        )

        self.backend_options = backend_options

        if (
            allow_ingress_from is not None
            or allow_ssh is not None
            or scheduler_port is not None
        ):
            if backend_options is not None and "ingress" in backend_options:
                raise ArgumentCombinationError(
                    "You cannot use `allow_ingress_from` or `allow_ssh` or `scheduler_port` when "
                    "`ingress` is also specified in `backend_options`."
                )
            firewall_kwargs = {
                "target": allow_ingress_from or "everyone",
                "ssh": False if allow_ssh is None else allow_ssh,
            }

            if scheduler_port is not None:
                firewall_kwargs["scheduler"] = scheduler_port
                self.scheduler_options["port"] = scheduler_port

            self.backend_options = self.backend_options or {}
            self.backend_options["ingress"] = cluster_firewall(**firewall_kwargs)[  # type: ignore
                "ingress"
            ]  # type: ignore

        if not self.asynchronous:
            # If we don't close the cluster, the user's ipython session gets spammed with
            # messages from distributed.
            #
            # Note that this doesn't solve all such spammy dead clusters (which is probably still
            # a problem), just spam created by clusters who failed initial creation.
            error = None
            try:
                self.sync(self._start)
            except (ClusterCreationError, InstanceTypeError) as e:
                error = e
                self.close()
                if self.cluster_id:
                    log_cluster_debug_info(self.cluster_id, self.account)
                raise e.with_traceback(None)
            except KeyboardInterrupt as e:
                error = e
                if self.cluster_id is not None:
                    logger.warning(
                        f"Received KeyboardInterrupt, deleting cluster {self.cluster_id}"
                    )
                    self.cloud.delete_cluster(self.cluster_id, account=self.account)
                raise
            except Exception as e:
                error = e
                self.close()
                raise e
            finally:
                if error:
                    self.sync(
                        self.cloud.add_interaction,
                        "cluster-create",
                        success=False,
                        additional_data={
                            "error_class": error.__class__.__name__,
                            "error_message": str(error),
                            **self._as_json_compatible(),
                        },
                    )
                else:
                    self.sync(
                        self.cloud.add_interaction,
                        "cluster-create",
                        success=True,
                        additional_data={
                            **self._as_json_compatible(),
                        },
                    )

    @property
    def details_url(self):
        return get_details_url(self.cloud.server, self.account, self.cluster_id)

    def _ipython_display_(self):
        cloud = self.cloud
        widget = None

        if use_html_widget():
            from coiled._beta.widgets.notebook import HTMLClusterWidget

            widget = HTMLClusterWidget()
        elif use_rich_widget():
            from coiled._beta.widgets.rich import RichClusterWidget

            widget = RichClusterWidget(server=self.cloud.server, account=self.account)

        if widget and self.cluster_id:
            # TODO: These synchronous calls may be too slow. They can be done concurrently
            cluster_details = cloud._get_cluster_details_synced(
                cluster_id=self.cluster_id, account=self.account
            )
            self.sync(self._update_cluster_status_logs, asynchronous=False)
            widget.update(cluster_details, self._cluster_status_logs)
            display(widget)

    def _repr_mimebundle_(
        self, include: Iterable[str], exclude: Iterable[str], **kwargs
    ):
        # In IPython 7.x This is called in an ipython terminal instead of
        # _ipython_display_ : https://github.com/ipython/ipython/pull/10249
        # In 8.x _ipython_display has been re-enabled in the terminal to
        # allow for rich outputs: https://github.com/ipython/ipython/pull/12315/files
        # So this function *should* only be calle  when in an ipython context using
        # IPython 7.x.
        cloud = self.cloud
        if use_rich_widget() and self.cluster_id:
            from coiled._beta.widgets.rich import RichClusterWidget

            rich_widget = RichClusterWidget(
                server=self.cloud.server, account=self.account
            )
            cluster_details = cloud._get_cluster_details_synced(
                cluster_id=self.cluster_id, account=self.account
            )
            self.sync(self._update_cluster_status_logs, asynchronous=False)
            rich_widget.update(cluster_details, self._cluster_status_logs)
            return rich_widget._repr_mimebundle_(include, exclude, **kwargs)
        else:
            return {"text/plain": repr(self)}

    @track_context
    async def _start(self):
        did_error = False
        await self.cloud
        try:
            cloud = self.cloud
            self.account = self.account or self.cloud.default_account

            user_provider = (
                None  # We'll only fetch this from the backend if we need it.
            )
            if (self.worker_cpu or self.worker_memory) and not self.worker_vm_types:
                user_provider = await self.cloud.get_account_provider_name(
                    account=self.account
                )
                worker_vm_types_to_use = get_instance_type_from_cpu_memory(
                    self.worker_cpu,
                    self.worker_memory,
                    gpus=self.worker_gpu_count,
                    backend=user_provider,
                )
            elif (self.worker_cpu or self.worker_memory) and self.worker_vm_types:
                raise ArgumentCombinationError(
                    "Argument 'worker_vm_types' used together with 'worker_cpu' or 'worker_memory' only "
                    "'worker_vm_types' or 'worker_cpu'/'worker_memory' should be used."
                )
            else:
                if self.worker_vm_types is None:
                    self.worker_vm_types = dask.config.get("coiled.worker.vm-types")
                if isinstance(self.worker_vm_types, str):
                    self.worker_vm_types = [self.worker_vm_types]
                validate_vm_typing(self.worker_vm_types)
                worker_vm_types_to_use = self.worker_vm_types

            if (
                self.scheduler_cpu or self.scheduler_memory
            ) and not self.scheduler_vm_types:
                # if we already fetched user_provider, don't do it again
                user_provider = (
                    user_provider
                    or await self.cloud.get_account_provider_name(account=self.account)
                )
                scheduler_vm_types_to_use = get_instance_type_from_cpu_memory(
                    self.scheduler_cpu, self.scheduler_memory, backend=user_provider
                )
            elif (
                self.scheduler_cpu or self.scheduler_memory
            ) and self.scheduler_vm_types:
                raise ArgumentCombinationError(
                    "Argument 'scheduler_vm_types' used together with 'scheduler_cpu' or "
                    "'scheduler_memory' only 'scheduler_vm_types' or "
                    "'scheduler_cpu'/'scheduler_memory' should be used."
                )
            else:
                if self.scheduler_vm_types is None:
                    self.scheduler_vm_types = dask.config.get(
                        "coiled.scheduler.vm_types"
                    )
                if isinstance(self.scheduler_vm_types, str):
                    self.scheduler_vm_types = [self.scheduler_vm_types]
                validate_vm_typing(self.scheduler_vm_types)
                scheduler_vm_types_to_use = self.scheduler_vm_types

            if self.name:
                try:
                    self.cluster_id = await cloud._get_cluster_by_name(
                        name=self.name,
                        account=self.account,
                    )
                except DoesNotExist:
                    should_create = True
                else:
                    logger.info(
                        f"Using existing cluster: '{self.name} (id: {self.cluster_id})'"
                    )
                    should_create = False
                    if self.shutdown_on_close is None:
                        self.shutdown_on_close = False
            else:
                should_create = True
                self.name = (
                    self.name
                    or (self.account or cloud.default_account)
                    + "-"
                    + str(uuid.uuid4())[:10]
                )

            # FIXME if should_create is False, there's stuff below that probably should be skipped

            # we could avoid this extra network request if the user provided vm types
            # for both worker and scheduler, but for now I don't care about optimizing that
            default_instance_types = await cloud._get_default_instance_types(
                self.account,
                guest_gpu=bool(self.worker_gpu_count),
            )

            warn_for_unspecified_senv = False
            if self.software_environment is None and not self.package_sync:
                py_version = f"py{''.join(map(str, sys.version_info[:2]))}"
                warn_for_unspecified_senv = True
                try:
                    senvs = await self.cloud.list_software_environments(account="coiled")  # type: ignore
                    runtime_versions = [
                        env
                        for env in senvs
                        if env.endswith(py_version) and "coiled/coiled-runtime" in env
                    ]
                    self.software_environment = max(runtime_versions, key=name_to_version)  # type: ignore
                except ValueError:
                    self.software_environment = f"coiled/default-{py_version}"
                conda_prefix = environ.get("CONDA_PREFIX")
                if conda_prefix:
                    conda_meta = Path(conda_prefix) / "conda-meta"
                    if conda_meta.exists():
                        coiled_runtime = next(
                            conda_meta.glob("coiled-runtime*.json"), None
                        )
                        if coiled_runtime:
                            match = re.match(
                                r"coiled-runtime-(\d+\.\d+.\d+)", coiled_runtime.name
                            )
                            if match:
                                runtime_version = match[1].replace(".", "-")
                                self.software_environment = f"coiled/coiled-runtime-{runtime_version}-{py_version}"
                                warn_for_unspecified_senv = False
            if self.package_sync:
                logger.info("Resolving your local python environment...")
                packageLevels = await self.cloud._fetch_package_levels()
                lookup = {pkg["name"]: pkg["level"] for pkg in packageLevels}

                env = await magic.create_environment_approximation(
                    only=self.package_sync_only,
                    priorities=lookup,
                    strict=self.package_sync_strict,
                )
                self.auto_env_issues: Dict[
                    str, Tuple[magic.ResolvedPackageInfo, int]
                ] = {
                    pkg["name"]: (pkg, lookup.get(pkg["name"], 50))
                    for pkg in env
                    if pkg["issue"]
                }
                halting_failures: List[magic.ResolvedPackageInfo] = []
                if not self.package_sync_only:
                    # if we're not operating on a subset, check
                    # all the coiled defined critical packages are present
                    critical_packages = [
                        pkg["name"] for pkg in packageLevels if pkg["level"] == 100
                    ]
                    combined_env: Dict[str, magic.ResolvedPackageInfo] = {
                        p["name"]: p for p in env
                    }

                    for critical_package in critical_packages:
                        if critical_package not in combined_env:
                            problem: magic.ResolvedPackageInfo = {
                                "name": critical_package,
                                "sdist": None,
                                "source": "pip",
                                "channel": None,
                                "conda_name": critical_package,
                                "client_version": "n/a",
                                "specifier": "n/a",
                                "include": False,
                                "issue": f"Could not detect package locally, please install {critical_package}",
                                "md5": None,
                            }
                            halting_failures.append(problem)
                            self.auto_env_issues[critical_package] = (
                                problem,
                                100,
                            )
                        elif not combined_env[critical_package]["include"]:
                            halting_failures.append(combined_env[critical_package])
                            self.auto_env_issues[critical_package] = (
                                combined_env[critical_package],
                                100,
                            )

                for pkgInfo, level in self.auto_env_issues.values():
                    # FIXME the "issue" could be that we're uploading wheel to use, this is confusing message
                    if level > self.package_sync_fail_on or self.package_sync_strict:
                        halting_failures.append(pkgInfo)
                    if level >= 100 or self.package_sync_strict:
                        logfunc = logger.critical
                    elif level >= 50:
                        logfunc = logger.warn
                    else:
                        logfunc = logger.info
                    logfunc(f"Dropped Package - {pkgInfo['name']}, {pkgInfo['issue']}")

                if self.auto_env_issues and HAS_RICH and self.show_widget:
                    from coiled._beta.widgets.rich import (
                        print_rich_package_warning_table,
                    )

                    print_rich_package_warning_table(pkg_warnings=self.auto_env_issues)
                if halting_failures:
                    failure_str = ", ".join(
                        [
                            f'{pkg["name"]} - {pkg["issue"]}'
                            for pkg in halting_failures
                            if pkg["issue"]
                        ]
                    )
                    raise RuntimeError(f"Issues with critical packages: {failure_str}")
                logger.info("Environment magic complete")
            else:
                env = None
            if should_create:
                # TODO: more sensible logging
                if warn_for_unspecified_senv:
                    logger.warn(
                        f"Using {self.software_environment} as a software environment\n"
                        "It's recommended that you specify a software environment or use the "
                        "`coiled-runtime` package.\n"
                        "For more information visit"
                        " https://docs.coiled.io/user_guide/tutorials/matching_coiled_senvs.html"
                    )
                # Elsewhere (in _wait_until_ready) we actually decide how many workers to wait for,
                # in a way that's unified/correct for both the "should_create" case and the case
                # where a cluster already exists.
                #
                # However, we should check here to make sure _wait_for_workers_arg is valid to
                # avoid creating the cluster if it's not valid.
                #
                # (We can't do this check earlier because we don't know until now if we're
                # creating a cluster, and if we're not then "_start_n_workers" may be the wrong
                # number of workers...)

                parse_wait_for_workers(
                    self._start_n_workers, self._wait_for_workers_arg
                )

                # Validate software environment name, setting `can_have_revision` to False since
                # we don't seem to be using this yet.
                if not self.package_sync:
                    parse_identifier(
                        self.software_environment,
                        property_name="software_environment",
                        can_have_revision=False,
                    )

                self.cluster_id = await cloud._create_cluster(
                    account=self.account,
                    name=self.name,
                    workers=self._start_n_workers,
                    software_environment=self.software_environment,
                    worker_class=self.worker_class,
                    worker_options=self.worker_options,
                    worker_cpu=self.worker_cpu,
                    worker_memory=self.worker_memory,
                    worker_disk_size=self.worker_disk_size,
                    gcp_worker_gpu_type=self.worker_gpu_type,
                    gcp_worker_gpu_count=self.worker_gpu_count,
                    scheduler_class=self.scheduler_class,
                    scheduler_options=self.scheduler_options,
                    scheduler_cpu=self.scheduler_cpu,
                    scheduler_memory=self.scheduler_memory,
                    environ=self.environ,
                    tags=self.tags,
                    dask_config=self.frozen_dask_config,
                    scheduler_vm_types=scheduler_vm_types_to_use
                    or default_instance_types,
                    worker_vm_types=worker_vm_types_to_use or default_instance_types,
                    backend_options=self.backend_options,
                    use_scheduler_public_ip=self.use_scheduler_public_ip,
                    auto_env=env,
                    private_to_creator=self.private_to_creator,
                )
            if not self.cluster_id:
                raise RuntimeError(f"Failed to find/create cluster {self.name}")
            logger.info(
                f"Creating Cluster (name: {self.name}, {self.details_url} ). This might take a few minutes..."
            )

            # update our view of workers in case someone tries scaling
            # it might be better to continually update this while waiting for the
            # cluster in _security below, but this seems OK for now
            await self._set_plan_requested()

            # this is what waits for the cluster to be "ready"
            await self._wait_until_ready(should_create)
            self.security, info = await cloud._security(
                cluster_id=self.cluster_id,
                account=self.account,
            )

            await self._set_plan_requested()  # update our view of workers
            self._proxy = bool(self.security.extra_conn_args)

            self._dashboard_address = info["dashboard_address"]

            if self.use_scheduler_public_ip:
                rpc_address = info["public_address"]
            else:
                rpc_address = info["private_address"]
                logger.info(
                    f"Connecting to scheduler on its internal address: {rpc_address}"
                )

            try:
                self.scheduler_comm = dask.distributed.rpc(
                    rpc_address,
                    connection_args=self.security.get_connection_args("client"),
                )
                await self._send_credentials()
            except IOError as e:
                if "Timed out" in "".join(e.args):
                    raise RuntimeError(
                        "Unable to connect to Dask cluster. This may be due "
                        "to different versions of `dask` and `distributed` "
                        "locally and remotely.\n\n"
                        f"You are using distributed={DISTRIBUTED_VERSION} locally.\n\n"
                        "With pip, you can upgrade to the latest with:\n\n"
                        "\tpip install --upgrade dask distributed"
                    )
                raise

            await super(Cluster, self)._start()

            # Set adaptive maximum value based on available config and user quota
            self._set_adaptive_options(info)
        except Exception as e:
            if self._asynchronous:
                did_error = True
                asyncio.create_task(
                    self.cloud.add_interaction(
                        "cluster-create",
                        success=False,
                        additional_data={
                            "error_class": e.__class__.__name__,
                            "error_message": str(e),
                            **self._as_json_compatible(),
                        },
                    )
                )
            raise
        finally:
            if self._asynchronous and not did_error:
                asyncio.create_task(
                    self.cloud.add_interaction(
                        "cluster-create",
                        success=True,
                        additional_data={
                            **self._as_json_compatible(),
                        },
                    )
                )

    def _as_json_compatible(self):
        # the typecasting here is to avoid accidentally
        # submitting something passed in that is not json serializable
        # (user error may cause this)
        return {
            "name": str(self.name),
            "software_environment": str(self.software_environment),
            "show_widget": bool(self.show_widget),
            "async": bool(self._asynchronous),
            "worker_class": str(self.worker_class),
            "worker_cpu": str(self.worker_cpu),
            "worker_memory": str(self.worker_memory),
            "worker_vm_types": str(self.worker_vm_types),
            "worker_gpu_count": str(self.worker_gpu_count),
            "worker_gpu_type": str(self.worker_gpu_type),
            "scheduler_class": str(self.scheduler_class),
            "scheduler_cpu": str(self.scheduler_class),
            "scheduler_memory": str(self.scheduler_memory),
            "scheduler_vm_types": str(self.scheduler_vm_types),
            "n_workers": int(self._start_n_workers),
            "shutdown_on_close": bool(self.shutdown_on_close),
            "use_scheduler_public_ip": bool(self.use_scheduler_public_ip),
            "package_sync": bool(self.package_sync),
            "execution_context": EXECUTION_CONTEXT,
            "account": self.account,
            "timeout": self.timeout,
            "wait_for_workers": self._wait_for_workers_arg,
            "cluster_id": self.cluster_id,
            "backend_options": self.backend_options,
        }

    def _maybe_log_summary(self, cluster_details):
        now = time.time()
        if (
            self._last_logged_state_summary is None
            or now > self._last_logged_state_summary + 5
        ):
            logger.info(summarize_status(cluster_details))
            self._last_logged_state_summary = now

    @track_context
    async def _wait_until_ready(self, is_new_cluster) -> None:
        cloud = self.cloud
        cluster_id = self._assert_cluster_id()
        timeout_at = (
            datetime.datetime.now() + datetime.timedelta(seconds=self.timeout)
            if self.timeout is not None
            else None
        )
        self._latest_dt_seen = None

        if self.show_widget:
            if use_rich_widget():
                from coiled._beta.widgets.rich import RichClusterWidget

                widget = RichClusterWidget(
                    n_workers=self._start_n_workers,
                    server=self.cloud.server,
                    account=self.account,
                )
                ctx = widget
            elif use_html_widget():
                from coiled._beta.widgets.notebook import HTMLClusterWidget

                # We disable buttons here because we are frequently updating the widget,
                # and that will lose the user's selection of which radio button for
                # status logs they had selected.
                widget = HTMLClusterWidget()
                ctx = widget
            else:
                widget = None
                ctx = contextlib.nullcontext()
        else:
            widget = None
            ctx = contextlib.nullcontext()

        num_workers_to_wait_for = None
        with ctx:
            while True:
                cluster_details = await cloud._get_cluster_details(
                    cluster_id=cluster_id, account=self.account
                )
                # Computing num_workers_to_wait_for inside the while loop is kinda goofy, but I don't want to add an
                # extra _get_cluster_details call right now since that endpoint can be very slow for big clusters.
                # Let's optimize it, and then move this code up outside the loop.

                if num_workers_to_wait_for is None:
                    cluster_desired_workers = cluster_details["desired_workers"]
                    num_workers_to_wait_for = parse_wait_for_workers(
                        cluster_desired_workers, self._wait_for_workers_arg
                    )
                    if not is_new_cluster and (
                        self._start_n_workers != cluster_desired_workers
                    ):
                        logging.warning(
                            f"Ignoring your request for {self._start_n_workers} workers since you are "
                            f"connecting to a cluster that had been requested with {cluster_desired_workers} workers"
                        )

                await self._update_cluster_status_logs()
                self._maybe_log_summary(cluster_details)

                if widget:
                    widget.update(
                        cluster_details,
                        self._cluster_status_logs,
                    )

                cluster_state = ClusterStateEnum(
                    cluster_details["current_state"]["state"]
                )
                reason = cluster_details["current_state"]["reason"]

                scheduler_current_state = cluster_details["scheduler"]["current_state"]
                scheduler_state = ProcessStateEnum(scheduler_current_state["state"])
                if cluster_details["scheduler"].get("instance"):
                    scheduler_instance_state = InstanceStateEnum(
                        cluster_details["scheduler"]["instance"]["current_state"][
                            "state"
                        ]
                    )
                else:
                    scheduler_instance_state = InstanceStateEnum.queued
                worker_current_states = [
                    w["current_state"] for w in cluster_details["workers"]
                ]
                ready_worker_current = [
                    current
                    for current in worker_current_states
                    if ProcessStateEnum(current["state"]) == ProcessStateEnum.started
                ]

                if (
                    scheduler_state == ProcessStateEnum.started
                    and scheduler_instance_state
                    in [InstanceStateEnum.ready, InstanceStateEnum.started]
                ):
                    scheduler_ready = True
                    scheduler_reason_not_ready = ""
                else:
                    scheduler_ready = False
                    scheduler_reason_not_ready = "Scheduler not ready."

                n_workers_ready = len(ready_worker_current)
                final_update = None
                if n_workers_ready >= num_workers_to_wait_for:
                    if n_workers_ready == self._start_n_workers:
                        final_update = "All workers ready."
                    else:
                        final_update = (
                            "Most of your workers have arrived. Cluster ready for use."
                        )

                    workers_ready = True
                    workers_reason_not_ready = ""

                else:
                    workers_ready = False
                    workers_reason_not_ready = (
                        f"Only {len(ready_worker_current)} workers ready "
                        f"(was waiting for at least {num_workers_to_wait_for}). "
                    )
                # TODO -- if all workers are ready *or error* then give final update

                if scheduler_ready and workers_ready:
                    assert final_update is not None
                    if widget:
                        widget.update(
                            cluster_details,
                            self._cluster_status_logs,
                            final_update=final_update,
                        )
                    logger.info(summarize_status(cluster_details))
                    return
                else:
                    reason_not_ready = (
                        scheduler_reason_not_ready
                        if not scheduler_ready
                        else workers_reason_not_ready
                    )
                    if cluster_state in (
                        ClusterStateEnum.error,
                        ClusterStateEnum.stopped,
                    ):
                        # this cluster will never become ready; raise an exception
                        error = f"Cluster status is {cluster_state.value} (reason: {reason})"
                        if widget:
                            widget.update(
                                cluster_details,
                                self._cluster_status_logs,
                                final_update=error,
                            )
                        logger.info(summarize_status(cluster_details))
                        raise ClusterCreationError(
                            error,
                            cluster_id=self.cluster_id,
                        )
                    elif cluster_state == ClusterStateEnum.ready:
                        # (cluster state "ready" means all worked either started or errored, so
                        # this cluster will ever have all the workers we want)
                        if widget:
                            widget.update(
                                cluster_details,
                                self._cluster_status_logs,
                                final_update=reason_not_ready,
                            )
                        logger.info(summarize_status(cluster_details))
                        raise ClusterCreationError(
                            reason_not_ready,
                            cluster_id=self.cluster_id,
                        )
                    elif (
                        timeout_at is not None and datetime.datetime.now() > timeout_at
                    ):
                        error = "User-specified timeout expired: " + reason_not_ready
                        if widget:
                            widget.update(
                                cluster_details,
                                self._cluster_status_logs,
                                final_update=error,
                            )
                        logger.info(summarize_status(cluster_details))
                        raise ClusterCreationError(
                            error,
                            cluster_id=self.cluster_id,
                        )
                    else:
                        await asyncio.sleep(1.0)

    async def _update_cluster_status_logs(self):
        cluster_id = self._assert_cluster_id()
        states_by_type = await self.cloud._get_cluster_states_declarative(
            cluster_id, self.account, start_time=self._latest_dt_seen
        )
        states = flatten_log_states(states_by_type)
        if states:
            if not self.show_widget or EXECUTION_CONTEXT == "terminal":
                log_states(states)
            self._latest_dt_seen = states[-1].updated
            self._cluster_status_logs.extend(states)

    def _assert_cluster_id(self) -> int:
        if self.cluster_id is None:
            raise RuntimeError(
                "'cluster_id' is not set, perhaps the cluster hasn't been created yet"
            )
        return self.cluster_id

    def cwi_logs_url(self):
        if self.cluster_id is None:
            raise ValueError(
                "cluster_id is None. Cannot get CloudWatch link without a cluster"
            )

        # kinda hacky, probably something as important as region ought to be an attribute on the
        # cluster itself already and not require an API call
        cluster_details = self.cloud._get_cluster_details_synced(
            cluster_id=self.cluster_id, account=self.account
        )
        if cluster_details["backend_type"] != "vm_aws":
            raise ValueError("Sorry, the cwi_logs_url only works for AWS clusters.")
        region = cluster_details["cluster_options"]["region_name"]

        return cloudwatch_url(self.account, self.name, region)

    def details(self):
        if self.cluster_id is None:
            raise ValueError("cluster_id is None. Cannot get details without a cluster")
        return self.cloud.cluster_details(
            cluster_id=self.cluster_id, account=self.account
        )

    async def _set_plan_requested(self):
        eventually_maybe_good_statuses = [
            ProcessStateEnum.starting,
            ProcessStateEnum.pending,
            ProcessStateEnum.started,
        ]
        eventually_maybe_good_workers = await self.cloud._get_worker_names(
            account=self.account,
            cluster_id=self.cluster_id,
            statuses=eventually_maybe_good_statuses,
        )
        self._plan = eventually_maybe_good_workers
        self._requested = eventually_maybe_good_workers

    @track_context
    async def _scale(self, n: int) -> None:
        await self._set_plan_requested()  # need to update our understanding of current workers before scaling
        logger.debug(f"current _plan: {self._plan}")
        if not self.cluster_id:
            raise ValueError("No cluster available to scale!")
        recommendations = await self.recommendations(n)
        logger.debug(f"scale recommmendations: {recommendations}")
        status = recommendations.pop("status")
        if status == "same":
            return
        if status == "up":
            return await self.scale_up(**recommendations)
        if status == "down":
            return await self.scale_down(**recommendations)

    @track_context
    async def scale_up(self, n: int) -> None:
        """
        Scales up *to* a target number of ``n`` workers

        It's documented that scale_up should scale up to a certain target, not scale up BY a certain amount:

        https://github.com/dask/distributed/blob/main/distributed/deploy/adaptive_core.py#L60
        """
        if not self.cluster_id:
            raise ValueError(
                "No cluster available to scale! "
                "Check cluster was not closed by another process."
            )
        target = n - len(self.plan)
        response = await self.cloud._scale_up(
            account=self.account,
            cluster_id=self.cluster_id,
            n=target,
        )
        if response:
            self._plan.update(set(response.get("workers", [])))
            self._requested.update(set(response.get("workers", [])))

    def _set_adaptive_options(self, info):
        self._adaptive_options = {
            "interval": "5s",
            "wait_count": 12,
            "target_duration": "5m",
            "minimum": 1,
            # TODO: want a more sensible limit; see _set_adaptive_options in coiled.Cluster
            # for inspiration from the logic there
            "maximum": 200,
        }

    @track_context
    async def _close(self, force_shutdown: bool = False) -> None:
        # My small changes to _close probably make sense for legacy Cluster too, but I don't want to carefully
        # test them, so copying this method over.

        with suppress(AttributeError):
            self._adaptive.stop()

        # Stop here because otherwise we get intermittent `OSError: Timed out` when
        # deleting cluster takes a while and callback tries to poll cluster status.
        for pc in self.periodic_callbacks.values():
            pc.stop()

        if hasattr(self, "cluster_id") and self.cluster_id:
            # If the initial create call failed, we don't have a cluster ID.
            # But the rest of this method (at least calling distributed.deploy.Cluster.close)
            # is important.
            if force_shutdown or self.shutdown_on_close in (True, None):
                await self.cloud._delete_cluster(
                    account=self.account,
                    cluster_id=self.cluster_id,
                )
        await super(Cluster, self)._close()

    # async def __aenter__(
    #     self: ClusterBeta[IsAsynchronous],
    # ) -> ClusterBeta[IsAsynchronous]:
    #     return await super().__aenter__()

    # async def __aexit__(self: ClusterBeta[IsAsynchronous], *args, **kwargs) -> None:
    #     if self.cleanup_cloud:
    #         await self.cloud._close()
    #     return await super().__aexit__()
