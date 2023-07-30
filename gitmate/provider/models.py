from abc import ABC, abstractmethod

hosts = {
    "github": "https://api.github.com",
    "gitlab": "https://gitlab.com",
    "azure": "https://dev.azure.com",

}


class Provider(ABC):
    """
    The default provider that all other providers must follow.
    """

    def __init__(self, username, token, data=None, debug=False):
        self.username = username
        self.token = token
        self.data = data
        self.debug = debug

    @abstractmethod
    def create_repo(self):
        pass

    @abstractmethod
    def list_repos(self):
        pass

    @abstractmethod
    def find_if_repo_exists(self):
        pass
