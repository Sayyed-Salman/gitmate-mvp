from utils import create_a_folder_with_readme, get_host
import os
import click
import logging

from utils import get_username
from utils import get_remote_credentials_for_current_user

from provider.factory import get_provider

from constants import PROVIDERS

logger = logging.getLogger(__name__)


@click.group("create")
def create():
    """Create a new repository."""
    pass


@click.command("repo")
@click.option("--name", "-n", help="Name of the repository", required=True)
@click.option("--path", "-p", help="Path of the repository", default="")
def repo(name, path):
    """Create a new repository."""

    if not path:
        new_path = os.getcwd()
    else:
        if os.path.exists(path):
            new_path = path
        else:
            click.echo(f"\"{path}\" : Path does not exist!")
            return

    logger.log(logging.INFO, "Creating a new repository...")
    click.echo("Creating a new repository...")
    click.echo("Name: {}".format(name))
    click.echo("Path: {}".format(new_path))

    # Create a folder with a readme file
    folder_path = create_a_folder_with_readme(name, new_path)

    # Create a repo in remote host.
    host = get_host()

    def _resolve_host_name(host):
        for key, value in PROVIDERS.items():
            if host in value:
                return key
        return None

    # Returns a provider object based on the host name
    provider = get_provider(_resolve_host_name(host))

    current_user = get_username()

    creds = get_remote_credentials_for_current_user(current_user)
    token = creds["password"]
    remote_repo = provider(username=current_user, token=token)
    remote_repo.data = {
        "name": f"{name}",
        "description": f"Created by {current_user} from gitmate."
    }
    remote_repo.create_repo()

    # link both of them

    # init on local

    # push to remote


create.add_command(repo)
