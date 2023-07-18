import click
import os


@click.group("destroy")
def destroy():
    """Delete credentials from GitMate."""
    creds_path = os.path.join(os.path.expanduser("~"), ".git-credentials")
    if os.path.exists(creds_path):
        os.remove(creds_path)
    else:
        click.echo("No credentials found!")
    click.echo("Successfully deleted credentials!")
    return
