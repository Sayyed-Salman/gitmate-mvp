import os
import re
import json
import subprocess
import logging
from errors import FileNotFoundError

logger = logging.getLogger(__name__)

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

    Returns:
        bool: True if logged in, False otherwise.
    """
    with open(os.path.join(root_path, "status.json"), "r") as f:
        status = json.load(f)
    if status["remoteLoggedIn"] == True:
        return True


@ staticmethod
def set_login_status(status_update: bool = True):
    """
    Set login status to True or False.

    Args:
        status_update (bool, optional): Status to be updated. Defaults to True.
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

    Args:
        status_update (bool, optional): Status to be updated. Defaults to True.
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

    Args:   
        name (str): Name of the user.
        email (str): Email of the user.
    """
    subprocess.run(['git', 'config', '--global',
                   '--unset', 'user.name', name])
    subprocess.run(['git', 'config', '--global',
                   '--unset', 'user.email', email])


@ staticmethod
def set_git_config(name, email):
    """
    Set git config.

    Args:
        name (str): Name of the user.
        email (str): Email of the user.
    """
    subprocess.run(['git', 'config', '--global',
                   'user.name', name])
    subprocess.run(['git', 'config', '--global',
                   'user.email', email])


@staticmethod
def add_remote_credentials(username, password, url="https://github.com"):
    """
    Add remote credentials.

    Args:
        username (str): Username of the user.
        password (str): Password of the user.
        url (str, optional): URL of the remote repository. Defaults to "https://github.com".
    """
    command = ['git', 'credential', 'approve']
    input_data = f'url={url}\nusername={username}\npassword={password}\n\n'

    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    process.communicate(input_data.encode())


@staticmethod
def remove_remote_credentials(username, url="https://github.com"):
    """
    Remove remote credentials.

    Args:
        username (str): Username of the user.
        url (str, optional): URL of the remote repository. Defaults to "https://github.com".
    """
    command = ['git', 'credential', 'reject']
    input_data = f'url={url}\nusername={username}\n\n'

    process = subprocess.Popen(command, stdin=subprocess.PIPE)
    process.communicate(input_data.encode())


@staticmethod
def setup_git_credential_helper(state="store", path=None):
    """
    Set git credential helper to provided state.
    Creates a .git-credentials file in the home directory for default state.

    Args:
        state (str): State of the credential helper. Defaults to "store". [store, manager, CUSTOM]
        path (str, optional): Path of the credential helper. Defaults to None.
    """
    try:
        if state == "store":
            subprocess.run(['git', 'config', '--global',
                            'credential.helper', 'store', "--file", path])
        elif state == "manager":
            subprocess.run(['git', 'config', '--global',
                            'credential.helper', 'manager-core'])
        else:
            subprocess.run(['git', 'config', '--global',
                            'credential.helper', state])
        return 1
    except Exception as e:
        logger.log(logging.ERROR, e)
        return "Error setting up credential helper!"


if __name__ == "__main__":
    print(check_status_file())
