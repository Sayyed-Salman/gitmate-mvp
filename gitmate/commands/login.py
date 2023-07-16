import click
from utils import check_login_status, check_remote_login_status
from utils import set_login_status, set_remote_login_status
from utils import set_git_config


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

    # Set login status
    set_login_status()

    # Print success message
    click.echo("Successfully logged in!")


@click.command(name="remote")
@click.option("--host", "-H", default="https://github.com", help="Host URL of remote repository")
@click.option("--token", "-t", help="Access token for remote repository", required=True)
def remote(host, token):
    """Login to remote repository"""
    # Check if already logged in
    if check_remote_login_status():
        click.echo("Already logged in!")
        return


login.add_command(remote)
login.add_command(local)
