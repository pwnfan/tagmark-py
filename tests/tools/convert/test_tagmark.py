from pathlib import Path

from tagmark.tools.convert.tagmark import JsonLinesConverer

class TestJsonlinesConverter:
    jsonlines_converter: JsonLinesConverer = JsonLinesConverer()
    test_file: Path = Path("tests/data/tagmark_ui_data_1682298863.158216.jsonl")

    def test_load_items(
        self,
    ):
        for item in self.jsonlines_converter.load_original_items(data_source=self.test_file):
            assert item.get("url")

    def test_convert(self):
        items: list[dict] = self.jsonlines_converter.load_original_items(data_source=self.test_file)
        self.jsonlines_converter.convert_to_tagmark(items=items)
        for _tagmark_item in self.jsonlines_converter.tagmark.tagmark_items:
            assert _tagmark_item.url
