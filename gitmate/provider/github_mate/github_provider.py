from models import Provider
from models import hosts

from github import Github
from github import Auth

from github import enable_console_debug_logging


class GithubProvider(Provider):

    HOST = hosts["github"]

    def __init__(self, username, token, data=None, debug=False):
        super().__init__(username, token, data)
        self.auth = Auth(username, token)
        self.github = Github(self.auth)

        if debug:
            enable_console_debug_logging()

    def create_repo(self):
        user = self.github.get_user()

        try:
            repo = user.create_repo(self.data.name)
            return repo
        except Exception as e:
            return e

    def list_repos(self):
        user = self.github.get_user()
        repos = user.get_repos()
        return repos

    def find_if_repo_exists(self, repo_name):

        return "yes"
