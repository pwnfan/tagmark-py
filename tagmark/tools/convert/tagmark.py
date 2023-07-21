import json
from pathlib import Path
from typing import Iterable

from dacite import from_dict

from tagmark.core.convert import BaseConverter
from tagmark.core.data import TagmarkItem


class JsonLinesConverer(BaseConverter):
    def _convert_to_tagmark_item(self, item: dict) -> TagmarkItem:
        return from_dict(data_class=TagmarkItem, data=item)

    def load_original_items(self, data_source: Path) -> Iterable[dict]:
        with open(data_source, "r") as _f:
            for _json_line in _f:
                yield json.loads(_json_line.strip())
