import click
import logging

from utils import check_login_status, check_remote_login_status
from utils import set_login_status, set_remote_login_status, set_host
from utils import set_git_config, setup_git_credential_helper, set_username
from utils import add_remote_credentials, get_username, set_status_custom_host, use_custom_host_file_
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
@click.option("--host", "-H", help="Host URL of remote repository (select one from {})".format(PROVIDERS), type=click.Choice(PROVIDERS), required=True)
@click.option("--custom-host-name", "-c", help="Custom host name for remote repository")
@click.option("--custom-host-url", "-u", help="Custom host url for remote repository")
@click.option("--token", "-t", help="Access token for remote repository", required=True)
def remote(host, token, custom_host_name, custom_host_url):
    """Login to remote repository"""
    # Check if already logged in
    try:
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
            set_status_custom_host()
            use_custom_host_file_(custom_host_name, custom_host_url)
            """
            1. in status.json file set custom_host to true
            2. create a new file 'custom.json' with host name and url 
            3. later in code check if custom_host is true then read from custom.json file
            """

        # Setup git credential helper
        credentials_ = setup_git_credential_helper()

        def _resolve_host_(host) -> str:
            if host in PROVIDERS:
                return PROVIDERS[host]
            else:
                hostname = click.prompt(
                    "Enter hostname for remote repository : ", type=str)
                host_url = click.prompt(
                    "Enter host url for remote repository : ", type=str)
                set_status_custom_host()
                use_custom_host_file_(hostname, host_url)
                return host_url

        username = get_username()
        add_remote_credentials(username, token, _resolve_host_(host))
        set_host(_resolve_host_(host))
        set_remote_login_status()

        if not credentials_ == 1:
            click.echo("Something went wrong!")
            click.echo("[!] Remote login failed!")
            return

    except Exception as e:
        click.echo(e)
        click.echo("[!] Remote login failed!")
        return


login.add_command(remote)
login.add_command(local)
