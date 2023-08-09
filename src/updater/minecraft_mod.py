import json
from typing import Any
import requests


class MinecraftMod:
    user_name: str
    repo_name: str
    is_pre_release: bool
    download_link: str
    file_name: str

    def __init__(self, user_name: str, repo_name: str,
                 is_pre_release: bool = True) -> None:
        self.user_name = user_name
        self.repo_name = repo_name
        self.is_pre_release = is_pre_release
        response = self.request_releases_json()
        if response is None:
            return
        self.download_link = response["browser_download_url"]
        self.file_name = response["name"]
        print(self.download_link, self.file_name)

    def get_source(self) -> str:
        return ""

    def get_github_url(self) -> str:
        return f"https://github.com/{self.user_name}/{self.repo_name}"

    def get_github_api_url(self) -> str:
        return f"https://api.github.com/repos/{self.user_name}/{self.repo_name}/releases"

    def handle_request_fail(self):
        # TODO: Handle fails
        pass

    def request_releases_json(self) -> Any | None:
        if self.is_pre_release:
            response = requests.get(self.get_github_api_url())
            if response.status_code != 200:
                self.handle_request_fail()
                return None
            return response.json()[0]["assets"][0]

        response = requests.get(self.get_github_api_url() + "/latest")
        if response.status_code != 200:
            self.handle_request_fail()
            return None
        return response.json()["assets"][0]

    def __normalize(self, string: str) -> str:
        string = "".join([char for char in string.lower() if (
            char not in {"-", ".", " ", "_"}
            and
            not char.isdigit()
        )])
        string.replace("beta", "")
        string.replace("alpha", "")
        return string

    def is_same_mod(self, file_name: str) -> bool:
        return self.__normalize(file_name) == self.__normalize(self.file_name)

    def should_update_and_replace(self, file_name: str) -> bool:
        if file_name == self.file_name:
            return False
        if self.is_same_mod(file_name):
            return True
        return False
