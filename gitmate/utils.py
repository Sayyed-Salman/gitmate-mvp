import os
import re
import json
import subprocess


@staticmethod
def check_login_status():
    with open("status.json", "r") as f:
        status = json.load(f)
    if status["loggedIn"]:
        return True


@staticmethod
def check_remote_login_status():
    with open("status.json", "r") as f:
        status = json.load(f)
    if status["remoteLoggedIn"]:
        return True


@staticmethod
def set_login_status(status: bool = True):
    with open("status.json", "r") as f:
        status = json.load(f)
    status["loggedIn"] = status
    with open("status.json", "w") as f:
        json.dump(status, f)


@staticmethod
def set_remote_login_status(status: bool = True):
    with open("status.json", "r") as f:
        status = json.load(f)
    status["remoteLoggedIn"] = status
    with open("status.json", "w") as f:
        json.dump(status, f)


@staticmethod
def unset_git_config(name, email):
    subprocess.run(['git', 'config', '--global',
                   '--unset', 'user.name', name])
    subprocess.run(['git', 'config', '--global',
                   '--unset', 'user.email', email])


@staticmethod
def set_git_config(name, email):
    subprocess.run(['git', 'config', '--global',
                   'user.name', name])
    subprocess.run(['git', 'config', '--global',
                   'user.email', email])


if __name__ == "__main__":
    pass
