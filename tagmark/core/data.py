import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

from tqdm import tqdm

from tagmark.core import Timestamp
from tagmark.core.github import (
    GithubApiLimitReachedError,
    GithubRepoInfo,
    GithubRepoNotFoundError,
    GithubUrl,
    InvalidGithubAccessTokenError,
    NotGithubUrlError,
    get_github_api_remaining,
)
from tagmark.core.log import LogHandler, LogLevel, get_level_logger


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
    github_repo_info: GithubRepoInfo | None = field(default=None, init=True)
    extra_info: dict | None = None
    time_added: Timestamp | None = None

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
                if _v is not None or keep_empty_keys:
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

    def _count_need_update_github_repo_info(self, after_hours: float) -> int:
        count: int = 0
        for _item in self.tagmark_items:
            if _item.is_github_url:
                if not _item.github_repo_info or _item.github_repo_info.need_update(
                    after_hours=after_hours
                ):
                    count += 1
        return count

    def get_github_repo_infos(
        self,
        access_token: str,
        condition: dict = {},
        after_hours: float = 48,
        is_ban_condition=True,
    ):
        _count_need_update: int = self._count_need_update_github_repo_info(
            after_hours=after_hours
        )
        if _count_need_update <= 0:
            return
        self._logger.info(_count_need_update=_count_need_update)

        _github_api_remaining: int = get_github_api_remaining(access_token=access_token)
        self._logger.info(_github_api_remaining=_github_api_remaining)
        if _count_need_update > _github_api_remaining:
            raise GithubApiLimitReachedError(
                f"API limit reached, needs {_count_need_update}, remaining {_github_api_remaining}"
            )
        for _tagmark_item in tqdm(
            iterable=self.tagmark_items,
            desc="retrieving Github repository information",
        ):
            if not _tagmark_item.is_github_url:
                continue
            elif (
                _tagmark_item.github_repo_info
                and not _tagmark_item.github_repo_info.need_update(
                    after_hours=after_hours
                )
            ):
                continue
            elif (
                is_ban_condition and _tagmark_item.hits_condition(condition=condition)
            ) or (
                (not is_ban_condition)
                and (not _tagmark_item.hits_condition(condition=condition))
            ):
                continue
            else:
                try:
                    _tagmark_item.get_github_repo_info(access_token=access_token)
                except InvalidGithubAccessTokenError as err:
                    self.logger.error(url=_tagmark_item.url, msg=err, exc_info=True)
                    raise
                except GithubRepoNotFoundError as err:
                    self._logger.warning(url=_tagmark_item.url, msg=err, exc_info=True)
                    _tagmark_item.valid = False
                except Exception as err:
                    self._logger.warning(url=_tagmark_item.url, msg=err, exc_info=True)

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
            condition (dict, optional): the condition for filtering TagmarkItem. Defaults to {}.
            is_ban_condition (bool, optional): If set to True, a TagmarkItem hits the `condition`
                will be banned, or it will be remained. Defaults to True.
        """
        if len(self.tagmark_items) > 0:
            with open(output_path, "w") as f:
                f.writelines(
                    f"{json.dumps(obj=_item.to_dict(keep_empty_keys=keep_empty_keys), ensure_ascii=False)}\n"
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


class TagmarkFilter:
    def __init__(self, filter_value: str):
        self.filter_value: str = filter_value
        self.filtered_tagmark: Tagmark = Tagmark()

    @property
    def count_total(self):
        return len(self.filtered_tagmark.tagmark_items)

    @property
    def count_github(self):
        return self.filtered_tagmark.count_github_url

    def filter(
        self,
        tagmark: Tagmark,
        condition: dict = {},
        is_ban_condition=True,
    ):
        _tagmark_item: Tagmark
        _filtered_items: list[Tagmark] = []
        for _tagmark_item in tagmark.tagmark_items:
            if self._hits_tagmark_item(
                tagmark_item=_tagmark_item,
                condition=condition,
                is_ban_condition=is_ban_condition,
            ):
                _filtered_items.append(_tagmark_item)
        self.filtered_tagmark.add(_filtered_items)

    def _hits_tagmark_item(
        self, tagmark_item: TagmarkItem, condition: dict = {}, is_ban_condition=True
    ) -> bool:
        if (is_ban_condition and tagmark_item.hits_condition(condition)) or (
            not is_ban_condition and not tagmark_item.hits_condition(condition)
        ):
            return False

        self.filter_value = self.filter_value.strip()

        if not self.filter_value:
            return True

        _filter_value_parts: list[str] = []
        for _filter_value_part in re.split(r"\b(OR|AND|NOT)\b", self.filter_value):
            _filter_value_part = _filter_value_part.strip()
            if _filter_value_part in ("AND", "OR", "NOT"):
                _filter_value_parts.append(_filter_value_part.lower())
            elif set(_filter_value_part) == set("("):
                _filter_value_parts.append(_filter_value_part)
            else:
                _tag_keyword: str = self.__extract_tag_keyword(_filter_value_part)
                if not _tag_keyword.strip():
                    return False
                _filter_value_parts.append(
                    _filter_value_part.replace(
                        _tag_keyword, str(_tag_keyword.lower() in tagmark_item.tags)
                    )
                )

        return eval(" ".join(_filter_value_parts))

    def __extract_tag_keyword(self, _filter_value_part: str) -> str:
        _start_index: int = (
            0
            if _filter_value_part.rfind("(") == -1
            else _filter_value_part.rfind("(") + 1
        )
        _end_index: int = (
            len(_filter_value_part)
            if _filter_value_part.find(")") == -1
            else _filter_value_part.find(")")
        )
        return _filter_value_part[_start_index:_end_index]
