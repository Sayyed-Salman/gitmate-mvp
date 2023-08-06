from utils import create_a_folder_with_readme, get_host
import os
import click
import logging

from utils import get_username

from provider.factory import get_provider

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
    provider = get_provider(host)

    current_user = get_username()

    remote_repo = provider(username="username", token="token")

    remote_repo.create_repo(name=name)

    # link both of them

    # init on local

    # push to remote


create.add_command(repo)
