import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable, NewType

from tagmark.core.github import (
    GithubApiLimitReachedError,
    GithubRepoInfo,
    GithubUrl,
    NotGithubUrlError,
    get_github_api_remaining,
)
from tagmark.core.log import LogHandler, LogLevel, get_level_logger

Timestamp: type = NewType("Timestamp", float)


@dataclass
class TagmarkItem:
    url: str
    id: int | None = None
    valid: bool = True
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

    def hits_condition(self, condition: dict = {}):
        if not condition:
            return False
        is_hit: bool = True
        for _k, _v in condition.items():
            _item_value = getattr(self, _k)
            if (_item_value is None) and (_v is None):
                is_hit = is_hit and True
            if (type(_item_value) is bool) and (type(_v) is bool):
                is_hit = is_hit and (_v == _item_value)
            elif (
                type(_item_value)
                in (
                    str,
                    list,
                )
            ) and (type(_v) in (list, tuple, set)):
                is_hit = is_hit and any(_x in _item_value for _x in _v)
            else:
                raise ValueError(
                    f"type {type(_item_value)} with value {_v} is not supported in a condition."
                )
        return is_hit


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

    @property
    def all_tags(self) -> set:
        _all_tags: set = set()
        for _tagmark_item in self.tagmark_items:
            if _tagmark_item.tags:
                _all_tags.update(_tagmark_item.tags)
        return _all_tags

    def get_github_repo_infos(self, access_token: str):
        if self.count_github_url <= 0:
            return
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

    def dump_to_json_lines(
        self,
        output_path: Path,
        keep_empty_keys=False,
        condition: dict = {},
        is_ban_condition=True,
    ):
        """
        dump self.tagmark_items into a json-lines file

        Args:
            output_path (Path): output path of the json-lines file
            keep_empty_keys (bool, optional): whether keep the keys with empty value when dumping.
                Defaults to False.
            condition (dict, optional): the condition for fitlering TagmarkItem. Defaults to {}.
            is_ban_condition (bool, optional): If set to True, a TagmarkItem hits the `condition`
                will be banned, or it will be remained. Defaults to True.
        """
        if len(self.tagmark_items) > 0:
            with open(output_path, "w") as f:
                f.writelines(
                    f"{json.dumps(_item.to_dict(keep_empty_keys=keep_empty_keys))}\n"
                    for _item in self.tagmark_items
                    if (
                        (
                            is_ban_condition
                            and (not _item.hits_condition(condition=condition))
                        )
                        or (
                            (not is_ban_condition)
                            and _item.hits_condition(condition=condition)
                        )
                    )
                )
