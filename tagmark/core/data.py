import json

from dataclasses import dataclass, field
from pathlib import Path
from typing import NewType, Iterable

from tagmark.core.github import (
    get_github_api_remaining,
    GithubUrl,
    GithubRepoInfo,
    GithubApiLimitReachedError,
    NotGithubUrlError,
)
from tagmark.core.log import get_level_logger, LogLevel, LogHandler

Timestamp: type = NewType("Timestamp", float)


@dataclass
class TagmarkItem:
    url: str
    id: int | None = None
    valid: str = True
    title: str | None = None
    tags: list[str] = field(default_factory=list)
    description: str | None = None
    comment: str | None = None
    is_github_url: bool = False
    github_repo_info: GithubRepoInfo | None = field(default=None, init=False)
    extra_info: dict | None = None
    time_added: Timestamp | None = None
    time_updated: Timestamp | None = None

    def __post_init__(self):
        if GithubUrl.is_github_url(self.url):
            self.is_github_url = True

    def get_github_repo_info(self, access_token):
        if not self.is_github_url:
            raise NotGithubUrlError(f"{self.url} is not a github url")
        _github_url: GithubUrl = GithubUrl(url=self.url)
        _github_url.get_repo_info(access_token=access_token)
        self.github_repo_info = _github_url.repo_info

    def to_dict(self, keep_empty_keys=False) -> dict:
        dict_item: dict = {}
        for _k in self.__class__.__annotations__.keys():
            _v = getattr(self, _k)

            if _k == "github_repo_info" and _v:
                dict_item[_k] = _v.to_dict(keep_empty_keys=keep_empty_keys)
            else:
                if _v or keep_empty_keys:
                    dict_item[_k] = _v
        return dict_item


class Tagmark:
    def __init__(self) -> None:
        self.tagmark_items: list[TagmarkItem] = []
        self._logger = get_level_logger(
            name="tagmark",
            level=LogLevel.INFO,
            handlers=[
                LogHandler.CONSOLE,
            ],
        )
        self._logger.bind(scope="Tagmark")

    def add(
        self,
        new_tagmark_items: Iterable[TagmarkItem],
        check_dup_on: list[str] = ["url"],
    ) -> int:
        count_added: int = 0
        for _new_tagmark_item in new_tagmark_items:
            # check duplicate
            for _column in check_dup_on:
                _new_value = getattr(_new_tagmark_item, _column)
                if _new_value is None:
                    continue
                if any(
                    getattr(tagmark_item, _column) == _new_value
                    for tagmark_item in self.tagmark_items
                ):
                    raise ValueError(
                        f"Duplicate value {_new_value} on column {_column}"
                    )

            _next_id: int = self.max_id + 1
            _new_tagmark_item.id = _next_id
            self.tagmark_items.append(_new_tagmark_item)
            count_added += 1
        return count_added

    @property
    def max_id(self) -> int:
        if not self.tagmark_items:
            return 0
        return max(_.id for _ in self.tagmark_items)

    def sort(self, key="id", reverse=False):
        return sorted(
            self.tagmark_items, key=lambda _: getattr(_, key), reverse=reverse
        )

    @property
    def count_github_url(self) -> int:
        count: int = 0
        for _item in self.tagmark_items:
            if _item.is_github_url:
                count += 1
        return count

    def get_github_repo_infos(self, access_token: str):
        _github_api_remaining: int = get_github_api_remaining(access_token=access_token)
        self._logger.info(_github_api_remaining=_github_api_remaining)
        if self.count_github_url > _github_api_remaining:
            raise GithubApiLimitReachedError(
                f"API limit reached, needs {self.count_github_url}, remaining {_github_api_remaining}"
            )
        for _tag_mark_item in self.tagmark_items:
            if not _tag_mark_item.is_github_url:
                continue
            else:
                try:
                    _tag_mark_item.get_github_repo_info(access_token=access_token)
                except Exception as err:
                    self._logger.warning(url=_tag_mark_item.url, msg=err, exc_info=True)

    def dump_to_json_lines(self, output_path: Path, keep_empty_keys=False):
        if len(self.tagmark_items) > 0:
            with open(output_path, "w") as f:
                f.writelines(
                    f"{json.dumps(_item.to_dict(keep_empty_keys=keep_empty_keys))}\n"
                    for _item in self.tagmark_items
                )
