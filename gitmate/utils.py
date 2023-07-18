import os
import re
import json
import subprocess
from errors import FileNotFoundError


root_path = os.path.dirname(os.path.abspath(__file__))


def check_status_file() -> bool:
    """
    Check if status.json file exists.
    """
    if os.path.exists(os.path.join(root_path, "status.json")):
        return True
    else:
        return False


@ staticmethod
def check_login_status():
    """
    Check if user is logged in.
    """
    if not check_status_file():
        return FileNotFoundError(message="status.json file not found.")

    with open(os.path.join(root_path, "status.json"), "r") as f:
        status = json.load(f)

    print(status)

    if status["loggedIn"] == True:
        return True


@ staticmethod
def check_remote_login_status():
    """
    Check if user is logged in with github via PAT.
    """
    with open(os.path.join(root_path, "status.json"), "r") as f:
        status = json.load(f)
    if status["remoteLoggedIn"] == True:
        return True


@ staticmethod
def set_login_status(status_update: bool = True):
    """
    Set login status to True or False.
    """
    with open(os.path.join(root_path, "status.json"), "r") as f:
        status = json.load(f)

    status["loggedIn"] = f"{status_update}"

    with open(os.path.join(root_path, "status.json"), "w") as f:
        json.dump(status, f, indent=4)


@ staticmethod
def set_remote_login_status(status_update: bool = True):
    """
    Set remote login status to True or False.
    """
    with open(os.path.join(root_path, "status.json"), "r") as f:
        status = json.load(f)

    status["remoteLoggedIn"] = f"{status_update}"

    with open(os.path.join(root_path, "status.json"), "w") as f:
        json.dump(status, f, indent=4)


@ staticmethod
def unset_git_config(name, email):
    """
    Unset git config.
    """
    subprocess.run(['git', 'config', '--global',
                   '--unset', 'user.name', name])
    subprocess.run(['git', 'config', '--global',
                   '--unset', 'user.email', email])


@ staticmethod
def set_git_config(name, email):
    """
    Set git config.
    """
    subprocess.run(['git', 'config', '--global',
                   'user.name', name])
    subprocess.run(['git', 'config', '--global',
                   'user.email', email])


@staticmethod
def add_remote_credentials(username, password, url="https://github.com"):
    """
    Add remote credentials.
    """
    command = ['git', 'credential', 'approve']
    input_data = f'url={url}\nusername={username}\npassword={password}\n\n'

    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    process.communicate(input_data.encode())


@staticmethod
def remove_remote_credentials(username, url="https://github.com"):
    """
    Remove remote credentials.
    """
    command = ['git', 'credential', 'reject']
    input_data = f'url={url}\nusername={username}\n\n'

    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    process.communicate(input_data.encode())


@staticmethod
def set_git_credential_helper():
    """
    Set git credential helper.
    """
    subprocess.run(['git', 'config', '--global', 'credential.helper', 'store'])


if __name__ == "__main__":
    print(check_status_file())
