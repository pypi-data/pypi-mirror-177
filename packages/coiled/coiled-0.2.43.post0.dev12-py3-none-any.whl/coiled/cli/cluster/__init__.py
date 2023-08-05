import click

from ..utils import CONTEXT_SETTINGS
from .logs import logs
from .ssh import ssh


@click.group(context_settings=CONTEXT_SETTINGS)
def cluster():
    """Commands for managing Coiled clusters"""
    pass


# @click.command(context_settings=CONTEXT_SETTINGS)
# def list():
#     print(f"...pretend this is a list of clusters...")


cluster.add_command(ssh)
cluster.add_command(logs)
