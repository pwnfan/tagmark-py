from pathlib import Path

import pytest

from tagmark.tools.maketagdoc import TagDocMaker


class TestTagDocMaker:
    @classmethod
    @pytest.fixture(autouse=True)
    def setup(cls, test_input_file_paths):
        cls.tag_doc_maker: TagDocMaker = TagDocMaker(
            tagmark_data_json_path=test_input_file_paths["tagmark_data_json"],
            tags_json_path=test_input_file_paths["tags_json"],
            config_path=Path("tagmark/tools/maketagdoc.toml.default").absolute(),
            url_base="https://pwnfan.github.io/tagmark/",
            condition_json_path=test_input_file_paths["condition_json"],
            is_ban_condition=True,
        )

    def test_format_line(self):
        error_line = "* test error line: {{xxx:yyy}}"
        with pytest.raises(ValueError):
            self.tag_doc_maker._format_line(line=error_line)

    def test_make(self):
        with open("tests/data/maketagdoc_template.md") as ft, open(
            "tests/data/maketagdoc_result.md"
        ) as fr:
            assert self.tag_doc_maker.make(ft.read()) == fr.read()
