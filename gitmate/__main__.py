import click
import logging
from commands import login
from commands import destroy


@click.group("gitmate")
def cli():
    """GitMate CLI."""
    pass


cli.add_command(login.login)
cli.add_command(destroy.destroy)

if __name__ == "__main__":
    cli()
