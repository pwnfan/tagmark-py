import os

import pytest

from tagmark.core.github import (
    GithubRepoNotFoundError,
    GithubUrl,
    InvalidGithubAccessTokenError,
    NotGithubUrlError,
    get_github_api_remaining,
)


class TestGithubUrl:
    def test_NotGithubUrlError(
        self,
    ):
        url = "https://www.google.com"
        with pytest.raises(NotGithubUrlError):
            GithubUrl(url=url)

    def test_InvalidGithubAccessTokenError(
        self,
    ):
        url = "https://github.com/not-extists_user-12345/not-exists-repo-54321"
        with pytest.raises(InvalidGithubAccessTokenError):
            github_url: GithubUrl = GithubUrl(url=url)
            github_url.get_repo_info(access_token="invalid_access_token")

    def test_GithubRepoNotFoundError(
        self,
    ):
        url = "https://github.com/not-extists_user-12345/not-exists-repo-54321"
        with pytest.raises(GithubRepoNotFoundError):
            github_url: GithubUrl = GithubUrl(url=url)
            github_url.get_repo_info(access_token=os.environ.get("GITHUB_TOKEN"))

    def test_is_github_url(
        self,
    ):
        url1 = "https://www.google.com"
        assert GithubUrl.is_github_url(url1) is False
        url2 = "https://github.com/olifolkerd/tabulator"
        assert GithubUrl.is_github_url(url2) is True

    def test_get_repo_info(
        self,
    ):
        access_token = os.environ.get("GITHUB_TOKEN")
        url = "https://github.com/olifolkerd/tabulator"

        github_url = GithubUrl(url=url)
        assert github_url.url == url
        assert github_url.owner == "olifolkerd"
        assert github_url.repo == "tabulator"

        github_url.get_repo_info(access_token=access_token)
        assert github_url.repo_info.url is not None
        assert github_url.repo_info.owner is not None
        assert github_url.repo_info.name is not None
        assert github_url.repo_info.is_archived is not None
        assert github_url.repo_info.description is not None
        assert github_url.repo_info.time_created is not None
        assert github_url.repo_info.time_last_commit is not None
        assert github_url.repo_info.time_last_release is None  # TODO
        assert github_url.repo_info.count_star is not None
        assert github_url.repo_info.count_fork is not None
        assert github_url.repo_info.count_watcher is not None
        assert github_url.repo_info.count_branch is None  # TODO
        assert github_url.repo_info.count_tag is None  # TODO
        assert github_url.repo_info.count_release is None  # TODO
        assert github_url.repo_info.count_conributor is None  # TODO
        assert len(github_url.repo_info.topics) >= 0


def test_get_github_api_remaining():
    access_token = os.environ.get("GITHUB_TOKEN")
    github_api_remaining: int = get_github_api_remaining(access_token=access_token)
    assert github_api_remaining > 0
