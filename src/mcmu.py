from getpass import getpass
from pathlib import Path
import traceback
from typing import Any
import threading
import requests

CONFIG_PATH = "./mcmu.txt"


class InvalidUrlException(ValueError):
    pass


class MinecraftMod:
    user_name: str
    repo_name: str
    is_pre_release: bool
    download_link: str
    file_name: str

    def __init__(self, user_name: str, repo_name: str,
                 is_pre_release: bool = False) -> None:
        self.user_name = user_name
        self.repo_name = repo_name
        self.is_pre_release = is_pre_release
        response = self.request_releases_json()
        if response is None:
            return
        self.download_link = response["browser_download_url"]
        self.file_name = response["name"]

    def get_source(self) -> str:
        return ""

    def get_github_url(self) -> str:
        return f"https://github.com/{self.user_name}/{self.repo_name}"

    def get_github_api_url(self) -> str:
        return f"https://api.github.com/repos/{self.user_name}/{self.repo_name}/releases"

    def handle_request_fail(self, url: str, code: int):
        raise InvalidUrlException(f"Request failed with code: {code} ({url})")

    def request_releases_json(self) -> Any | None:
        if self.is_pre_release:
            response = requests.get(self.get_github_api_url())
            if response.status_code != 200:
                self.handle_request_fail(
                    self.get_github_api_url(), response.status_code)
                return None
            return response.json()[0]["assets"][0]

        response = requests.get(self.get_github_api_url() + "/latest")
        if response.status_code != 200:
            self.handle_request_fail(
                self.get_github_api_url() + "/latest",
                response.status_code)
            return None
        return response.json()["assets"][0]

    def is_same_mod(self, file_name: str) -> bool:
        return _normalize(file_name) == _normalize(self.file_name)

    def download(self, path: Path) -> None:
        print(f"Downloading {self.file_name} from \"{self.download_link}\"...")
        content = requests.get(
            self.download_link,
            allow_redirects=True).content
        print(f"Finish downloading {self.file_name}")
        with (path / self.file_name).open("wb") as file:
            file.write(content)

    @classmethod
    def from_github_url(cls, github_url: str, is_pre_release=False):
        github_url = github_url.replace("https://", "")
        if not github_url.startswith("github.com/"):
            raise InvalidUrlException(
                f"'{github_url}' is not a valid github link")
        github_url = github_url.replace("github.com/", "")
        try:
            urls = github_url.split("/")
            user = urls[0]
            repo = urls[1]
        except Exception as e:
            raise InvalidUrlException(
                f"'{github_url}' is not a valid github link") from e
        return cls(user, repo, is_pre_release)


def _normalize(string: str) -> str:
    string = "".join([char for char in string.lower() if (
        char not in {"-", ".", " ", "_"}
        and
        not char.isdigit()
    )])
    string = string.replace("beta", "")
    string = string.replace("alpha", "")
    return string


def download_custom(url: str, path: Path) -> None:
    file_name = url.split("/")[-1]
    print(f"Downloading {file_name} from \"{url}\"...")
    content = requests.get(
        url,
        allow_redirects=True).content
    print(f"Finish downloading {file_name}")
    with (path / file_name).open("wb") as file:
        file.write(content)


def get_mods(lines: list[str]) -> list[MinecraftMod]:
    mods: list[MinecraftMod] = []
    for line in lines:
        if (
            line.startswith("pre https://github.com/") or
            line.startswith("https://github.com/") or
            line.startswith("pre github.com/") or
            line.startswith("github.com/")
        ):
            if line.startswith("pre "):
                line = line[4:]
                mods.append(
                    MinecraftMod.from_github_url(
                        line, is_pre_release=True))
            else:
                mods.append(
                    MinecraftMod.from_github_url(
                        line, is_pre_release=False))
            continue
    return mods


def get_custom_urls(lines: list[str]) -> list[str]:
    urls: list[str] = []
    for line in lines:
        if not line.startswith("url "):
            continue
        line = line[4:]
        urls.append(line)
    return urls


def update_from_string(path_string: str, string: list[str]):
    path = Path(path_string)
    if not path.is_dir():
        raise FileNotFoundError(f"{repr(path_string)} is not a path")
    mods = get_mods(string)
    urls = get_custom_urls(string)
    update(path, mods, urls)


def update(mod_folder: Path, mods: list[MinecraftMod], custom_urls: list[str]):
    mod_files = [path for path in mod_folder.iterdir() if path.is_file()]
    download_queue: list[threading.Thread] = []
    mod_count = 0

    def handle_mod(mod: MinecraftMod):
        for mod_file in mod_files:
            if mod.download_link.endswith(mod_file.name):
                print(f"{mod_file.name} is already up to date.")
                break
            if mod.is_same_mod(mod_file.name):
                mod_file.unlink()
                mod_count += 1
                _thread = threading.Thread(
                    target=mod.download,
                    args=(mod_folder,))
                download_queue.append(_thread)
                _thread.start()
                break
        else:
            mod_count += 1
            _thread = threading.Thread(
                target=mod.download,
                args=(mod_folder,))
            download_queue.append(_thread)
            _thread.start()

    for mod in mods:
        handle_mod(mod)

    def handle_url(custom_url: str):
        for mod_file in mod_files:
            if custom_url.endswith(mod_file.name):
                print(f"{mod_file.name} is already up to date.")
                break
            if _normalize(custom_url) == _normalize(mod_file.name):
                mod_file.unlink()
                mod_count += 1
                _thread = threading.Thread(
                    target=download_custom,
                    args=(custom_url, mod_folder))
                download_queue.append(_thread)
                _thread.start()
                break
        else:
            mod_count += 1
            _thread = threading.Thread(
                target=download_custom,
                args=(custom_url, mod_folder))
            download_queue.append(_thread)
            _thread.start()

    for custom_url in custom_urls:
        handle_url(custom_url)

    for thread in download_queue:
        thread.join()

    print(f"Finished updating {len(mods) + len(custom_urls)} mod(s) ({mod_count} downloaded)")


def main():
    try:
        config_file = Path(CONFIG_PATH)
        if not config_file.is_file():
            print("Missing './mcmu.txt'")
            return
        with config_file.open("r") as file:
            lines = file.read().splitlines()
        if not lines:
            raise ValueError("Missing mod folder path in './mcmu.txt'")
        print(lines)
        update_from_string(lines.pop(0), lines)
    except Exception as error:
        traceback.print_exc()

    getpass("")


if __name__ == "__main__":
    main()
