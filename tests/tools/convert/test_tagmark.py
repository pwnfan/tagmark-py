import json
from pathlib import Path

from tagmark.core.convert import TagsCheckResult
from tagmark.tools.convert.tagmark import JsonLinesConverter


class TestJsonlinesConverter:
    jsonlines_converter: JsonLinesConverter = JsonLinesConverter()
    test_data_file: Path = Path("tests/data/tagmark_ui_data_1682298863.158216.jsonl")
    test_tag_definition_file: Path = Path("tests/data/tag_definitions.json")
    test_ban_condition_file: Path = Path("tests/data/ban-condition.json")

    def test_load_items(
        self,
    ):
        for item in self.jsonlines_converter.load_original_items(
            data_source=self.test_data_file
        ):
            assert item.get("url")

    def test_convert(self):
        items: list[dict] = self.jsonlines_converter.load_original_items(
            data_source=self.test_data_file
        )
        self.jsonlines_converter.convert_to_tagmark(items=items)
        for _tagmark_item in self.jsonlines_converter.tagmark.tagmark_items:
            assert _tagmark_item.url

    def test_check_tags(self):
        with open(Path(self.test_tag_definition_file)) as _f_tag_definition:
            _tags_with_definition: set = set(json.load(_f_tag_definition).keys())
        with open(Path(self.test_ban_condition_file)) as _f_ban_condition:
            _tags_in_ban_condition: set = set(
                json.load(_f_ban_condition).get("tags", [])
            )
        check_result: TagsCheckResult = self.jsonlines_converter.check_tags(
            tags_with_definition=_tags_with_definition,
            tags_in_ban_condition=_tags_in_ban_condition,
        )
        assert check_result.tags_without_definition == {"oss"}
        assert check_result.tags_definition_unused == {"test"}
        assert check_result.count == {
            "tags_in_data_source": 7,
            "tags_with_definition": 7,
            "tags_without_definition": 1,
            "tags_definition_unused": 1,
        }
