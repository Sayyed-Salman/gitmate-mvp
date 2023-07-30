import os
import click

from utils import remove_remote_credentials


@click.group("destroy")
def destroy():
    """Delete credentials from GitMate."""


@click.command("file")
@click.option("--path", "-p", help="Credentials file path.")
def remove_creds_file(path):
    """Delete credentials file"""

    creds_path = os.path.join(os.path.expanduser("~"), ".git-credentials")
    if os.path.exists(creds_path):
        os.remove(creds_path)
    else:
        click.echo("No credentials file found!")
    click.echo("Successfully deleted credentials!")


@click.command("user")
@click.option("--username", "-u", help="Username to remove")
@click.option("--host", "-h", help="Host url (https://github.com)")
def remove_user(username, host):
    """Delete user credentials from system.

    Args:
        username (str): Username to remove.
        host (str): Host url (https://github.com).
    """
    remove_remote_credentials(username, host)
    click.echo("Successfully deleted credentials!")


destroy.add_command(remove_creds_file)
destroy.add_command(remove_user)
