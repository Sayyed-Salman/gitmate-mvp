import click
from commands import login


@click.group("gitmate")
def cli():
    pass


cli.add_command(login.login)

if __name__ == "__main__":
    cli()
