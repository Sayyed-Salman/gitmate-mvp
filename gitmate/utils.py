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


def get_username() -> str:
    """
    Get username from status.json file.
    """
    if not check_status_file():
        return FileNotFoundError(message="status.json file not found.")

    with open(os.path.join(root_path, "status.json"), 'r') as f:
        status = json.load(f)

    username = status["username"]

    return username


def set_username(username):
    """
    set username in status.json file.

    Args:
        username (str): Username of the user.
    """
    if not check_status_file():
        return FileNotFoundError(message="status.json not found")

    with open(os.path.join(root_path, "status.json"), 'r') as f:
        status = json.load(f)

    status["username"] = username

    with open(os.path.join(root_path, "status.json"), 'w') as f:
        json.dump(status, f, indent=4)


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


def set_remote_login_status(status_update: bool = True):
    """
    Set remote login status to True or False.

    Args:
        status_update (bool, optional): Status to be updated. Defaults to True.
    """
    with open(os.path.join(root_path, "status.json"), "r", encoding="utf-8") as f:
        status = json.load(f)

    status["remoteLoggedIn"] = f"{status_update}"

    with open(os.path.join(root_path, "status.json"), "w", encoding="utf-8") as f:
        json.dump(status, f, indent=4)


def unset_git_config(name, email):
    """
    Unset git config.

    Args:   
        name (str): Name of the user.
        email (str): Email of the user.
    """
    subprocess.run(['git', 'config', '--global',
                   '--unset', 'user.name', name], check=False)
    subprocess.run(['git', 'config', '--global',
                   '--unset', 'user.email', email], check=False)


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


def get_remote_credentials_for_current_user():
    """
    Get remote credentials.

    Returns:
        dict: Dictionary containing username and password.
    """
    command = ['git', 'credential', 'fill']
    input_data = 'url=https://github.com\n\n'

    process = subprocess.Popen(
        command, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    output, _ = process.communicate(input_data.encode())

    output = output.decode()
    username = re.search(r'username=(.*)', output).group(1)
    password = re.search(r'password=(.*)', output).group(1)

    return {"username": username, "password": password}


def setup_git_credential_helper(state="store", path=None):
    """
    Set git credential helper to provided state.
    Creates a .git-credentials file in the home directory for default state.

    Args:
        state (str): State of the credential helper. Defaults to "store". [store, manager, CUSTOM]
        path (str, optional): Path of the credential helper. Defaults to None.
    """
    try:
        if state == "store" and path:
            subprocess.run(['git', 'config', '--global',
                            'credential.helper', 'store', "--file", path])
        elif state == "store":
            subprocess.run(['git', 'config', '--global',
                            'credential.helper', 'store'])
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


def create_a_folder_with_readme(name, path):
    """
    Create a folder with a 'readme.md' file inside it.

    Parameters:
        name (str): The name of the folder.
        path (str): The path where the folder will be created.

    Returns:
        str: The absolute path of the created folder.
    """
    folder_path = os.path.join(path, name)
    os.makedirs(folder_path, exist_ok=True)

    readme_content = f"# {name}"
    readme_file_path = os.path.join(folder_path, "readme-mate.md")
    with open(readme_file_path, "w") as readme_file:
        readme_file.write(readme_content)

    return os.path.abspath(folder_path)


def init_and_first_commit(path):
    """
    Run "git init", "git add .", and "git commit -m 'mate commit'" commands.

    Parameters:
        path (str): The path of the directory where the Git repository will be initialized.

    Returns:
        bool: True if the commands executed successfully, False otherwise.
    """
    try:
        # Run "git init" command
        subprocess.run(["git", "init"], cwd=path, check=True)

        # Run "git add ." command
        subprocess.run(["git", "add", "."], cwd=path, check=True)

        # Run "git commit -m 'mate commit'" command
        subprocess.run(["git", "commit", "-m", "mate commit"],
                       cwd=path, check=True)

        return True  # All commands executed successfully
    except subprocess.CalledProcessError:
        return False  # An error occurred while executing the commands


def set_status_custom_host(status_update: bool = True):
    """
    Set status to custom.
    """
    with open(os.path.join(root_path, "status.json"), "r", encoding="utf-8") as f:
        status = json.load(f)

    status["custom_host"] = f"{status_update}"

    with open(os.path.join(root_path, "status.json"), "w", encoding="utf-8") as f:
        json.dump(status, f, indent=4)


def use_custom_host_file_(host_name, host_url):
    """
    Create or update custom host file.
    """
    custom_host = {}
    custom_host["host_name"] = f"{host_name}"
    custom_host["host_url"] = f"{host_url}"

    file_ = os.path.join(root_path, "custom.json")

    if not os.path.exists(file_):
        with open(file_, "w", encoding="utf-8") as f:
            json.dump(custom_host, f, indent=4)

    else:
        with open(file_, "r", encoding="utf-8") as f:
            custom = json.load(f)

        custom["host_name"] = f"{host_name}"
        custom["host_url"] = f"{host_url}"

        with open(file_, "w", encoding="utf-8") as f:
            json.dump(custom, f, indent=4)


def get_host():
    """
    Get host name and url.
    """
    with open(os.path.join(root_path, "status.json"), "r", encoding="utf-8") as f:
        status = json.load(f)

    return status["host"]


if __name__ == "__main__":
    print(check_status_file())
