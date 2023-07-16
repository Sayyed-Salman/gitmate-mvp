import click
import logging
from commands import login

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename="gitmate.log",
)

logger = logging.getLogger(__name__)


@click.group("gitmate")
def cli():
    pass


cli.add_command(login.login)

if __name__ == "__main__":
    cli()
