from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Iterable

from tagmark.core.data import Tagmark, TagmarkItem


@dataclass
class TagsCheckResult:
    tags_in_data_source: set[str] = field(default_factory=set[str])
    tags_with_definition: set[str] = field(default_factory=set[str])
    tags_without_definition: set[str] = field(default_factory=set[str])
    tags_definition_unused: set[str] = field(default_factory=set[str])

    def __post_init__(self):
        self.tags_without_definition = (
            self.tags_in_data_source - self.tags_with_definition
        )
        self.tags_definition_unused = (
            self.tags_with_definition - self.tags_in_data_source
        )

    @property
    def count(self) -> dict[str:int]:
        _count: dict[str:int] = dict()
        for _k in self.__class__.__annotations__.keys():
            _v = getattr(self, _k)
            _count[_k] = len(_v)
        return _count


class BaseConverter(ABC):
    def __init__(self):
        self.tagmark = Tagmark()

    @abstractmethod
    def _convert_to_tagmark_item(self, item: Any) -> TagmarkItem:
        raise NotImplementedError

    @abstractmethod
    def load_original_items(self, data_source: Any) -> Iterable[Any]:
        raise NotImplementedError

    def convert_to_tagmark(self, items: list[Any]) -> int:
        count_converted_items: int = self.tagmark.add(
            new_tagmark_items=[self._convert_to_tagmark_item(_item) for _item in items],
            check_dup_on=["id", "url"],
        )
        return count_converted_items

    def check_tags(
        self, tags_with_definition: set[str], tags_in_ban_condition: set[str] = set()
    ) -> TagsCheckResult:
        return TagsCheckResult(
            tags_in_data_source=self.tagmark.all_tags - tags_in_ban_condition,
            tags_with_definition=tags_with_definition - tags_in_ban_condition,
        )
