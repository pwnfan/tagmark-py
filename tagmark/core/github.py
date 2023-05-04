from dataclasses import asdict, dataclass, field
from datetime import datetime
from urllib.parse import ParseResult, urlparse

import requests

github_api_base_url = "https://api.github.com"


class NotGithubUrlError(Exception):
    pass


class GetGithubRepoInfoError(Exception):
    pass


class GetGithubApiLimitError(Exception):
    pass


class GithubApiLimitReachedError(Exception):
    pass


@dataclass
class GithubRepoInfo:
    url: str
    owner: str | None = None
    name: str | None = None
    is_archived: bool | None = None
    description: str | None = None
    time_created: datetime | None = None
    time_last_commit: datetime | None = None
    time_last_release: datetime | None = None
    count_star: int | None = None
    count_fork: int | None = None
    count_watcher: int | None = None
    count_branch: int | None = None
    count_tag: int | None = None
    count_release: int | None = None
    count_conributor: int | None = None
    topics: list[str] = field(default_factory=list)  # tags by github

    def to_dict(self, keep_empty_keys=False) -> dict:
        _dict_item: dict = asdict(self)
        if not keep_empty_keys:
            [_dict_item.pop(_k) for _k, _v in _dict_item.copy().items() if not _v]
        return _dict_item


@dataclass
class GithubUrl:
    url: str
    owner: str | None = None
    repo: str | None = None
    parsed_url: ParseResult | None = None
    repo_info: GithubRepoInfo | None = None

    def __post_init__(self):
        self.parsed_url = urlparse(self.url)

        # check url
        if self.parsed_url.netloc != "github.com":
            raise NotGithubUrlError(f"{self.url} is not a github url")

        _parsed_path = self.parsed_url.path.strip("/").split("/")
        self.owner = _parsed_path[0]
        self.repo = _parsed_path[1]

    def get_repo_info(self, access_token: str):
        assert access_token
        _response = requests.get(
            url=f"{github_api_base_url}/repos/{self.owner}/{self.repo}",
            headers={"Authorization": f"token {access_token}"},
        )
        if _response.status_code != 200:
            raise GetGithubRepoInfoError(
                f"Failed to retrieve github repository information, response status code is {_response.status_code}"
            )
        _raw_repo_info: dict = _response.json()
        self.repo_info = GithubRepoInfo(
            url=f"{self.parsed_url.scheme}://{self.parsed_url.netloc}/{self.owner}/{self.repo}",
            owner=self.owner,
            name=self.repo,
            is_archived=_raw_repo_info.get("archived"),
            description=_raw_repo_info.get("description"),
            time_created=_raw_repo_info.get("created_at"),
            time_last_commit=_raw_repo_info.get("pushed_at"),
            time_last_release=None,  # TODO
            count_star=_raw_repo_info.get("stargazers_count"),
            count_fork=_raw_repo_info.get("forks_count"),
            count_watcher=_raw_repo_info.get("watchers_count"),
            count_branch=None,  # TODO
            count_tag=None,  # TODO
            count_release=None,  # TODO
            count_conributor=None,  # TODO
            topics=_raw_repo_info.get("topics"),
        )

    @classmethod
    def is_github_url(cls, url):
        return urlparse(url).netloc == "github.com"


def get_github_api_remaining(access_token: str) -> int:
    assert access_token
    _response = requests.get(
        url=f"{github_api_base_url}/rate_limit",
        headers={"Authorization": f"token {access_token}"},
    )
    if _response.status_code != 200:
        raise GetGithubApiLimitError(
            f"Failed to retrieve API rate limit, response status code is {_response.status_code}"
        )
    _rate_limit: dict = _response.json()
    return _rate_limit.get("rate", {}).get("remaining", 0)
