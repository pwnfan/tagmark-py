import json
from dataclasses import dataclass, field
from pathlib import Path

from tagmark.core.tag import TagItem
from tagmark.tools.convert import tagmark as tagmark_convert


@dataclass
class TagsCheckResult:
    tags_in_data_source: set[str] = field(default_factory=set[str])
    tags_in_tags_json: set[str] = field(default_factory=set[str])
    tags_only_in_data_source: set[str] = field(default_factory=set[str])
    tags_only_in_tags_json: set[str] = field(default_factory=set[str])

    def __post_init__(self):
        self.tags_only_in_data_source = (
            self.tags_in_data_source - self.tags_in_tags_json
        )
        self.tags_only_in_tags_json = self.tags_in_tags_json - self.tags_in_data_source

    @property
    def count(self) -> dict[str:int]:
        _count: dict[str:int] = dict()
        for _k in self.__class__.__annotations__.keys():
            _v = getattr(self, _k)
            _count[_k] = len(_v)
        return _count


class TagsChecker:
    def __init__(
        self,
        tagmark_data_json_path: Path,
        tags_json_path: Path,
        condition_json_path: Path | None = None,
    ):
        self._tagmark_data_json_path = tagmark_data_json_path
        self._tags_json_path = tags_json_path
        self._condition_json_path = condition_json_path

        self.__load_tagmark_data()
        self.__load_tag_infos()
        self.__load_condition()

    def __load_tagmark_data(
        self,
    ):
        self.converter: tagmark_convert.JsonLinesConverter = (
            tagmark_convert.JsonLinesConverter()
        )

        _items: list[dict] = self.converter.load_original_items(
            data_source=self._tagmark_data_json_path
        )
        self.converter.convert_to_tagmark(items=_items)
        self.tags_in_data_source = self.converter.tagmark.all_tags

    def __load_tag_infos(
        self,
    ):
        with open(self._tags_json_path) as _f_tags_json:
            self.tag_infos: dict = json.load(_f_tags_json)
            self.tags_in_json_file: set = set(self.tag_infos.keys())

    def __load_condition(
        self,
    ):
        self.tags_in_ban_condition: set[str] = {}
        if self._condition_json_path:
            with open(self._condition_json_path) as _f_ban_condition:
                self.tags_in_ban_condition = set(
                    json.load(_f_ban_condition).get("tags", [])
                )

    def check_tags(
        self,
    ) -> TagsCheckResult:
        self.check_result: TagsCheckResult = TagsCheckResult(
            tags_in_data_source=self.tags_in_data_source - self.tags_in_ban_condition,
            tags_in_tags_json=self.tags_in_json_file - self.tags_in_ban_condition,
        )
        return self.check_result

    def generate_new_tag_infos(self) -> dict[str:dict]:
        self.new_tag_infos: dict[str:dict] = self.tag_infos.copy()
        self.new_tag_infos.update(
            {
                _tag: TagItem(
                    tag=_tag,
                ).as_tags_json_data_value()
                for _tag in self.check_result.tags_only_in_data_source
            }
        )
        return self.new_tag_infos
