from csv import DictReader
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable

from tagmark.core.convert import BaseConverter
from tagmark.core.data import TagmarkItem, Timestamp


class ChromeConverter(BaseConverter):
    class ChromeParser(HTMLParser):
        def __init__(self):
            super().__init__()
            self.bookmarks = []
            self.current_bookmark = None
            self.current_title = None

        def handle_starttag(self, tag, attrs):
            if tag == "a":
                bookmark = dict(attrs)
                self.bookmarks.append(bookmark)
                self.current_bookmark = bookmark
                self.current_title = ""
            elif tag == "dd" and self.current_bookmark is not None:
                self.current_bookmark["description"] = ""

        def handle_data(self, data):
            if self.current_title is not None:
                self.current_title += data.strip()
            if (
                self.current_bookmark is not None
                and "description" in self.current_bookmark
            ):
                self.current_bookmark["description"] += data.strip()

        def handle_endtag(self, tag):
            if tag == "a":
                self.current_bookmark["title"] = self.current_title
                self.current_title = None

    def load_original_items(self, data_source: Path) -> Iterable[dict]:
        with open(data_source, "r") as f:
            _parser: self.ChromeParser = self.ChromeParser()
            _parser.feed(f.read())
            return _parser.bookmarks

    def _convert_to_tagmark_item(self, item: dict) -> TagmarkItem:
        _raw_tags: str = item.get("tags").strip()
        _tags: list[str] = []
        if _raw_tags:
            _tags = _raw_tags.split(",")

        _description: str | None = item.get("description") or None
        return TagmarkItem(
            url=item.get("href"),
            valid=True,
            title=item.get("title"),
            tags=_tags,
            comment=_description,  # the `description` in diigo is actually the comment added by myself
            time_added=Timestamp(item.get("add_date")),
        )


# TODO
class CsvConverter(BaseConverter):
    def load_original_items(self, data_source: Path) -> Iterable[dict]:
        with open(data_source, newline="") as csvfile:
            for _row in DictReader(csvfile):
                yield _row

    def _convert_to_tagmark_item(self, item: dict) -> TagmarkItem:
        # TODO
        pass
