import click
import logging
from commands import login
from commands import destroy
from commands import create


@click.group("gitmate")
def cli():
    """GitMate CLI."""
    pass


cli.add_command(login.login)
cli.add_command(destroy.destroy)
cli.add_command(create.create)

if __name__ == "__main__":
    cli()
