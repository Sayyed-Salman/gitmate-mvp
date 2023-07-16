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

    with open("status.json", "r",encoding="utf-8") as f:
        status = json.load(f)
    if status["loggedIn"]:
        return True


@ staticmethod
def check_remote_login_status():
    """
    Check if user is logged in with github via PAT.
    """
    with open("status.json", "r") as f:
        status = json.load(f)
    if status["remoteLoggedIn"]:
        return True


@ staticmethod
def set_login_status(status: bool = True):
    """
    Set login status to True or False.
    """
    with open("status.json", "r") as f:
        status = json.load(f)
    status["loggedIn"] = status
    with open("status.json", "w") as f:
        json.dump(status, f)


@ staticmethod
def set_remote_login_status(status: bool = True):
    """
    Set remote login status to True or False.
    """
    with open("status.json", "r") as f:
        status = json.load(f)
    status["remoteLoggedIn"] = status
    with open("status.json", "w") as f:
        json.dump(status, f)


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


if __name__ == "__main__":
    print(check_status_file())
    print(root_path)
    pass
