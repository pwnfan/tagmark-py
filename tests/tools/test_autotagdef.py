from tagmark.tools.autotagdef import AutoTagDefinitionMarker


class TestAutoTagDefinitionMarker:
    auto_tag_def_maker: AutoTagDefinitionMarker = AutoTagDefinitionMarker(
        gpt_config={"access_token": "fake_test_token"},
    )
    dumpy_gpt_generated_definition = "dummy GPT generated definition"

    def test_auto_make_tag_definitions(self, mocker):
        tag_infos: dict[str:dict] = {
            "active-directory": {
                "abbr": "AD",
                "full_name": "Active Directory",
                "definition": "Active Directory (AD) is a directory service developed by Microsoft that is used in Windows-based networks.",
            },
            "adfs": {
                "abbr": "ADFS",
            },
            "adversary-emulation": {
                "full_name": "Adversary Emulation",
                "gpt_prompt_context": "cybersecurity",
            },
            "aggregator-site": {"full_name": "aggregator site"},
            "ai": {},
            "alibaba-cloud": {},
        }

        # test `little_info_tag_is_ok` == False
        mocker.patch.object(
            self.auto_tag_def_maker,
            "_get_definition_by_chatgpt",
            side_effect=[
                self.dumpy_gpt_generated_definition,
                "",
                Exception("Something went wrong"),
            ],
        )
        (
            new_tag_definitions,
            auto_tag_make_stats,
        ) = self.auto_tag_def_maker.auto_define_tags(
            tag_infos=tag_infos,
            little_info_tag_is_ok=False,
        )
        assert auto_tag_make_stats.count_total_tags == len(tag_infos)
        assert auto_tag_make_stats.count_auto_made_success == 1
        assert auto_tag_make_stats.count_auto_made_fail == 2
        assert auto_tag_make_stats.count_no_gpt_prompt == 2
        assert auto_tag_make_stats.count_already_defined == 1

        assert any(
            [
                new_tag_definitions.get("adfs") == self.dumpy_gpt_generated_definition,
                new_tag_definitions.get("adversary-emulation")
                == self.dumpy_gpt_generated_definition,
                new_tag_definitions.get("aggregator-site")
                == self.dumpy_gpt_generated_definition,
            ]
        )
        assert not all(
            [
                new_tag_definitions.get("adfs") == self.dumpy_gpt_generated_definition,
                new_tag_definitions.get("adversary-emulation")
                == self.dumpy_gpt_generated_definition,
                new_tag_definitions.get("aggregator-site")
                == self.dumpy_gpt_generated_definition,
            ]
        )

        # test `little_info_tag_is_ok` == True
        mocker.patch.object(
            self.auto_tag_def_maker,
            "_get_definition_by_chatgpt",
            side_effect=[
                self.dumpy_gpt_generated_definition,
                "",
                Exception("Something went wrong"),
                self.dumpy_gpt_generated_definition,
                self.dumpy_gpt_generated_definition,
            ],
        )
        (
            new_tag_definitions,
            auto_tag_make_stats,
        ) = self.auto_tag_def_maker.auto_define_tags(
            tag_infos=tag_infos,
            little_info_tag_is_ok=True,
        )
        assert auto_tag_make_stats.count_total_tags == len(tag_infos)
        assert auto_tag_make_stats.count_auto_made_success == 3
        assert auto_tag_make_stats.count_auto_made_fail == 2
        assert auto_tag_make_stats.count_no_gpt_prompt == 0
        assert auto_tag_make_stats.count_already_defined == 1

        assert any(
            [
                new_tag_definitions.get("adfs") == self.dumpy_gpt_generated_definition,
                new_tag_definitions.get("adversary-emulation")
                == self.dumpy_gpt_generated_definition,
                new_tag_definitions.get("aggregator-site")
                == self.dumpy_gpt_generated_definition,
                new_tag_definitions.get("ai") == self.dumpy_gpt_generated_definition,
                new_tag_definitions.get("alibaba-cloud")
                == self.dumpy_gpt_generated_definition,
            ]
        )
        assert not all(
            [
                new_tag_definitions.get("adfs") == self.dumpy_gpt_generated_definition,
                new_tag_definitions.get("adversary-emulation")
                == self.dumpy_gpt_generated_definition,
                new_tag_definitions.get("aggregator-site")
                == self.dumpy_gpt_generated_definition,
                new_tag_definitions.get("ai") == self.dumpy_gpt_generated_definition,
                new_tag_definitions.get("alibaba-cloud")
                == self.dumpy_gpt_generated_definition,
            ]
        )
