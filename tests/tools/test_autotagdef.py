from tagmark.tools.autotagdef import AutoTagDefinitonMarker


class TestAutoTagDefinitonMarker:
    auto_tag_def_maker: AutoTagDefinitonMarker = AutoTagDefinitonMarker(
        gpt_config={"access_token": "fake_test_token"},
    )

    def test_auto_make_tag_definitions(self, mocker):
        tag_definitions: dict[str:str] = {
            # already has a definition
            "active-directory": "Active Directory (AD) is a directory service developed by Microsoft that is used in Windows-based networks.",
            # a prompt has been set for auto marking definition by GPT (the ending `?` is the flag)
            "adfs": "what is ADFS?",
            # a prompt has been set for auto marking definition by GPT
            "adversary-emulation": "in cybersecurity, what is Adversary Emulation?",
            # a prompt has been set for auto marking definition by GPT
            "aggregator-site": "what is a aggregator site?",
            # no definition, and no prompt has been set
            "ai": "!!!NO DEFINITION FOR THIS TAG, PLEASE ADD HERE!!!",
            # no definition, and no prompt has been set
            "alibaba-cloud": "!!!NO DEFINITION FOR THIS TAG, PLEASE ADD HERE!!!",
        }
        mocker.patch.object(
            self.auto_tag_def_maker,
            "_get_definition_by_chatgpt",
            side_effect=[
                "dummy GPT generated definiton",
                "",
                Exception("Something went wrong"),
            ],
        )

        (
            new_tag_definitions,
            auto_tag_make_stats,
        ) = self.auto_tag_def_maker.auto_make_tag_definitions(
            tag_definitions=tag_definitions,
        )
        assert auto_tag_make_stats.count_total_tags == len(tag_definitions)
        assert auto_tag_make_stats.count_auto_made_success == 1
        assert auto_tag_make_stats.count_auto_made_fail == 2
        assert auto_tag_make_stats.count_already_defined == 1
        assert auto_tag_make_stats.count_no_prompt == 2
        _gpt_results: list[str] = [
            new_tag_definitions.get("adfs"),
            new_tag_definitions.get("adversary-emulation"),
            new_tag_definitions.get("aggregator-site"),
        ]
        assert any(
            [
                tag_definitions.get("adfs") in _gpt_results,
                tag_definitions.get("adversary-emulation") in _gpt_results,
                tag_definitions.get("aggregator-site") in _gpt_results,
            ]
        )
        assert not all(
            [
                tag_definitions.get("adfs") in _gpt_results,
                tag_definitions.get("adversary-emulation") in _gpt_results,
                tag_definitions.get("aggregator-site") in _gpt_results,
            ]
        )
