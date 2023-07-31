import pytest

from tagmark.core.tag import TagItem
from tagmark.tools.checktag import DuplicatedTagFormattedNameError, TagsChecker


class TestTagsChecker:
    @classmethod
    @pytest.fixture(autouse=True)
    def setup(cls, test_input_file_paths):
        cls.tags_checker: TagsChecker = TagsChecker(
            tagmark_data_json_path=test_input_file_paths["tagmark_data_json"],
            tags_json_path=test_input_file_paths["tags_json"],
            condition_json_path=test_input_file_paths["condition_json"],
        )

    def test_check_tags(
        self,
    ):
        self.tags_checker.check_tags()
        assert self.tags_checker.check_result.tags_only_in_data_source == {"oss"}
        assert self.tags_checker.check_result.tags_only_in_tags_json == {"test"}
        assert self.tags_checker.check_result.count == {
            "tags_in_data_source": 7,
            "tags_in_tags_json": 7,
            "tags_only_in_data_source": 1,
            "tags_only_in_tags_json": 1,
        }

    def test_generate_new_tag_infos(
        self,
    ):
        self.tags_checker.check_tags()
        self.tags_checker.generate_new_tag_infos()

        new_tags_infos_expected: dict = self.tags_checker.tag_infos.copy()

        for _tag in self.tags_checker.check_result.tags_only_in_data_source:
            new_tags_infos_expected[_tag] = TagItem(tag=_tag).as_tags_json_data_value()

        assert self.tags_checker.new_tag_infos == new_tags_infos_expected

    def test_check_tag_duplicated_formatted_names(
        self,
    ):
        with pytest.raises(DuplicatedTagFormattedNameError):
            self.tags_checker.check_tag_duplicated_formatted_names()
