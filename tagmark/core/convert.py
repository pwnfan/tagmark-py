from abc import ABC, abstractmethod
from typing import Any, Iterable

from tagmark.core.data import TagmarkItem, Tagmark


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
