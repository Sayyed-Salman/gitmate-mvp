import click
import logging

from utils import check_login_status, check_remote_login_status
from utils import set_login_status, set_remote_login_status
from utils import set_git_config, setup_git_credential_helper, set_username
from utils import add_remote_credentials, get_username
from constants import PROVIDERS

logger = logging.getLogger(__name__)


@click.group("login")
def login():
    """Login to GitMate."""
    pass


@click.command(name="local")
@click.option("--username", "-u", help="Username for local repository", required=True)
@click.option("--email", "-e", help="Email for local repository", required=True)
def local(username, email):
    """Login to local repository"""

    # Check if already logged in
    if check_login_status():
        click.echo("Already logged in!")
        return

    # Set git config
    set_git_config(username, email)
    set_username(username)
    # Set login status
    set_login_status()

    # Print success message
    logger.log(logging.INFO, "Successfully logged in!")
    click.echo("Successfully logged in!")


@click.command(name="remote")
@click.option("--host", "-H", default="github", help="Host URL of remote repository (select one from {})".format(PROVIDERS), type=click.Choice(PROVIDERS), show_default=True)
@click.option("--custom-host-name", "-c", help="Custom host name for remote repository")
@click.option("--custom-host-url", "-u", help="Custom host url for remote repository")
@click.option("--token", "-t", help="Access token for remote repository", required=True)
def remote(host, token, custom_host_name, custom_host_url):
    """Login to remote repository"""
    # Check if already logged in
    if check_remote_login_status():
        click.echo("Already logged in!")
        return

    if custom_host_name and not custom_host_url:
        custom_host_url = click.prompt(
            "Enter custom host url for remote repository : ", type=str)
    elif custom_host_url and not custom_host_name:
        custom_host_name = click.prompt(
            "Enter custom host name for remote repository : ", type=str)

    if custom_host_name and custom_host_url:
        do_something = True
        """
        1. create a new entry in status.json file with custom_host to true
        2. create a new file 'custom.json' with host name and url 

        3. later in code check if custom_host is true then read from custom.json file
        """

    # Setup git credential helper
    credentials_ = setup_git_credential_helper()

    username = get_username()
    add_remote_credentials(username, token, host)

    if not credentials_ == 1:
        click.echo("Something went wrong!")
        return


login.add_command(remote)
login.add_command(local)
