from dataclasses import asdict, dataclass


class NoEnoughTagInfoForGptPromptException(Exception):
    pass


@dataclass
class TagItem:
    tag: str
    abbr: str | None = None
    full_name: str | None = None
    alias: str | None = None
    definition: str | None = None
    prefer_format: str | None = None
    gpt_prompt_context: str | None = None

    @property
    def has_little_info_for_gpt(
        self,
    ) -> bool:
        return (
            not self.definition
            and not self.abbr
            and not self.full_name
            and not self.gpt_prompt_context
        )

    @property
    def formatted_name(self) -> str:
        formatted_name: str = ""

        if self.prefer_format:
            formatted_name = self.prefer_format.format(**asdict(self))
        else:
            if self.full_name:
                formatted_name += self.full_name
                if self.abbr:
                    formatted_name += f" (abbr. {self.abbr})"
            elif self.abbr:
                formatted_name += f"{self.abbr}"
            else:
                formatted_name += f"{self.tag}"

            if self.alias:
                formatted_name += f", aka {self.alias}"

        return formatted_name

    def generate_gpt_prompt(self, little_info_is_ok=False) -> str:
        if not little_info_is_ok and self.has_little_info_for_gpt:
            raise NoEnoughTagInfoForGptPromptException(self)

        prompt: str = ""
        _name_in_prompt: str = ""

        if not self.abbr and not self.full_name:
            _name_in_prompt += self.tag
        elif self.full_name:
            _name_in_prompt += self.full_name
            if self.abbr:
                _name_in_prompt += f" ({self.abbr})"
        elif self.abbr:
            _name_in_prompt += self.abbr

        # if self.alias:
        #     _name_in_prompt += f", aka {self.alias}"

        if self.gpt_prompt_context:
            prompt += f"in {self.gpt_prompt_context}, "
        prompt += f"what is {_name_in_prompt}?"

        return prompt

    def as_tags_json_data_value(
        self,
    ):
        """
        As tag data structure in tags.json is key-value, in which the
        `key` equals TagItem.tag, `value` is a json object likes:
            {
                "abbr": null,
                "full_name": null,
                "alias": null,
                "definition": null,
                "prefer_format": null,
                "gpt_prompt_context": null
            }
        this function generate the value part as a python dict
        """
        data_value: dict[str : str | None] = asdict(self)
        data_value.pop("tag")
        return data_value
