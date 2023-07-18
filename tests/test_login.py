import click
from click.testing import CliRunner
import subprocess

from gitmate.commands import login


def test_login_local():
    username = "test"
    email = "test@gmail.com"

    runner = CliRunner()
    result = runner.invoke(
        login.local, ["-u", f"{username}", "-e", f"{email}"])

    def get_git_username():
        """Get local git username."""
        return subprocess.check_output(['git', 'config', '--global', 'user.name']).decode('utf-8').strip()

    def get_git_email():
        """Get local git email."""
        return subprocess.check_output(['git', 'config', '--global', 'user.email']).decode('utf-8').strip()

    system_username = get_git_username()
    system_email = get_git_email()

    assert username == system_username
    assert email == system_email
    assert result.exit_code == 0
