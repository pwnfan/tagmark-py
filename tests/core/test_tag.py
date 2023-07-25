import pytest

from tagmark.core.tag import NoEnoughTagInfoForGptPromptException, TagItem


class TestTagItem:
    tag_items: list[TagItem] = [
        # 0
        TagItem(
            tag="2fa",
            abbr="2FA",
            full_name="Two-Factor Authentication",
            prefer_format="{full_name} ({abbr})",
        ),
        # 1
        TagItem(
            tag="alibaba-cloud",
            alias="Aliyun",
            full_name="Alibaba Cloud",
        ),
        # 2
        TagItem(
            tag="auto-completion",
            alias="tab completion",
            gpt_prompt_context="shell",
        ),
        # 3
        TagItem(
            tag="crlf-injection",
            abbr="CRLF injection",
            alias="HTTP response splitting",
            full_name="Carriage Return Line Feed injection",
            gpt_prompt_context="cybersecurity",
        ),
        # 4
        TagItem(
            tag="dev",
            abbr="dev",
            full_name="development",
            prefer_format="{full_name}",
        ),
        # 5
        TagItem(
            tag="frontend",
            gpt_prompt_context="software development",
        ),
        # 6
        TagItem(
            tag="test",
        ),
        # 7
        TagItem(
            tag="adfs",
            abbr="ADFS",
        ),
    ]

    def test_has_little_info_for_gpt(
        self,
    ):
        assert self.tag_items[0].has_little_info_for_gpt is False
        assert self.tag_items[1].has_little_info_for_gpt is False
        assert self.tag_items[2].has_little_info_for_gpt is False
        assert self.tag_items[3].has_little_info_for_gpt is False
        assert self.tag_items[4].has_little_info_for_gpt is False
        assert self.tag_items[5].has_little_info_for_gpt is False
        assert self.tag_items[6].has_little_info_for_gpt is True
        assert self.tag_items[7].has_little_info_for_gpt is False

    def test_format_name(
        self,
    ):
        assert self.tag_items[0].formatted_name == "Two-Factor Authentication (2FA)"
        assert self.tag_items[1].formatted_name == "Alibaba Cloud, aka Aliyun"
        assert self.tag_items[2].formatted_name == "auto-completion, aka tab completion"
        assert (
            self.tag_items[3].formatted_name
            == "Carriage Return Line Feed injection (abbr. CRLF injection), aka HTTP response splitting"
        )
        assert self.tag_items[4].formatted_name == "development"
        assert self.tag_items[5].formatted_name == "frontend"
        assert self.tag_items[6].formatted_name == "test"
        assert self.tag_items[7].formatted_name == "ADFS"

    def test_generate_gpt_prompt(
        self,
    ):
        assert (
            self.tag_items[0].generate_gpt_prompt(little_info_is_ok=False)
            == self.tag_items[0].generate_gpt_prompt(little_info_is_ok=True)
            == "what is Two-Factor Authentication (2FA)?"
        )
        assert (
            self.tag_items[1].generate_gpt_prompt(little_info_is_ok=False)
            == self.tag_items[1].generate_gpt_prompt(little_info_is_ok=True)
            == "what is Alibaba Cloud?"
        )
        assert (
            self.tag_items[2].generate_gpt_prompt(little_info_is_ok=False)
            == self.tag_items[2].generate_gpt_prompt(little_info_is_ok=True)
            == "in shell, what is auto-completion?"
        )
        assert (
            self.tag_items[3].generate_gpt_prompt(little_info_is_ok=False)
            == self.tag_items[3].generate_gpt_prompt(little_info_is_ok=True)
            == "in cybersecurity, what is Carriage Return Line Feed injection (CRLF injection)?"
        )

        assert (
            self.tag_items[5].generate_gpt_prompt(little_info_is_ok=False)
            == self.tag_items[5].generate_gpt_prompt(little_info_is_ok=True)
            == "in software development, what is frontend?"
        )

        assert (
            self.tag_items[6].generate_gpt_prompt(little_info_is_ok=True)
            == "what is test?"
        )
        with pytest.raises(NoEnoughTagInfoForGptPromptException):
            self.tag_items[6].generate_gpt_prompt(little_info_is_ok=False)

        assert (
            self.tag_items[7].generate_gpt_prompt(little_info_is_ok=False)
            == self.tag_items[7].generate_gpt_prompt(little_info_is_ok=True)
            == "what is ADFS?"
        )

    def test_as_tags_json_data_value(
        self,
    ):
        assert self.tag_items[2].as_tags_json_data_value() == dict(
            abbr=None,
            full_name=None,
            alias="tab completion",
            definition=None,
            prefer_format=None,
            gpt_prompt_context="shell",
        )
