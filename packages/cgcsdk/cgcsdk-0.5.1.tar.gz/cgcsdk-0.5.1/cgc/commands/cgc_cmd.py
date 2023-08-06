import click

from cgc.commands.compute.compute_cmd import compute_delete
from cgc.utils.click_group import CustomCommand


@click.command("rm", cls=CustomCommand)
@click.argument("name", type=click.STRING)
def cgc_rm(name: str):
    """
    Delete an app in user namespace
    \f
    :param name: name of the app to delete
    :type name: str
    """
    compute_delete(name)
