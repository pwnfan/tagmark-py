import json
from pathlib import Path
from typing import Iterable

from tagmark.core.convert import BaseConverter
from tagmark.core.data import TagmarkItem
from tagmark.core.github import GithubRepoInfo


class JsonLinesConverer(BaseConverter):
    def _convert_to_tagmark_item(self, item: dict) -> TagmarkItem:
        item.pop("github_repo_info", None)
        return TagmarkItem(**item)

    def load_original_items(self, data_source: Path) -> Iterable[dict]:
        with open(data_source, "r") as _f:
            for _json_line in _f:
                yield json.loads(_json_line.strip())
