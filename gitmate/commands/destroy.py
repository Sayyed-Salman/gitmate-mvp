import os
import click


@click.group("destroy")
def destroy():
    """Delete credentials from GitMate."""
    


@click.command("file")
@click.option("--path","-p", help="Credentials file path.")
def remove_creds_file(path):
    """Delete credentials file"""

    creds_path = os.path.join(os.path.expanduser("~"), ".git-credentials")
    if os.path.exists(creds_path):
        os.remove(creds_path)
    else:
        click.echo("No credentials file found!")
    click.echo("Successfully deleted credentials!")


destroy.add_command(remove_creds_file)