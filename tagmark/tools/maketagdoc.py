import json
import re
import tomllib
from enum import Enum
from pathlib import Path

from tqdm import tqdm

from tagmark.core.data import TagmarkFilter
from tagmark.core.log import LogHandler, LogLevel, get_level_logger
from tagmark.core.tag import TagItem
from tagmark.tools.convert import tagmark as convert_tagmark

FormatterNamesInTemplate: Enum
FormatExpressions: Enum


class FormatterType(Enum):
    total = "total"
    tag = "tag"
    filter = "filter"
    tag_filter_counts = "tag_filter_counts"
    tag_filter = "tag_filter"
    filter_counts = "filter_counts"


class TagDocMaker:
    def __init__(
        self,
        tagmark_data_json_path: Path,
        tags_json_path: Path,
        config_path: Path,
        url_base: str,
        condition_json_path: Path | None = None,
        is_ban_condition: bool = True,
    ):
        self._logger = get_level_logger(
            name="tagmark",
            level=LogLevel.INFO,
            handlers=[
                LogHandler.CONSOLE,
            ],
        )
        self._logger.bind(scope="TagDocMaker")

        self._tagmark_data_json_path: Path = tagmark_data_json_path
        self._tags_json_path: Path = tags_json_path
        self._config_path: Path = config_path
        self._condition_json_path: Path = condition_json_path
        self._is_ban_condition: bool = is_ban_condition
        self.url_base: str = url_base.rstrip("/")

        self.converter: convert_tagmark.JsonLinesConverter
        self.__load_tagmark_data()

        self.tag_infos: dict
        self.__load_tag_infos()

        self.condition: dict
        self.__load_condition()

        self.config: dict
        self.FormatterTypeNameAbbr: Enum
        self.FormatExpressions: Enum
        self.formatter_value_regex: re.Pattern
        self.__load_config()

    def __load_tagmark_data(
        self,
    ):
        self.converter: convert_tagmark.JsonLinesConverter = (
            convert_tagmark.JsonLinesConverter()
        )

        _items: list[dict] = self.converter.load_original_items(
            data_source=self._tagmark_data_json_path
        )
        self.converter.convert_to_tagmark(items=_items)

    def __load_tag_infos(
        self,
    ):
        with open(self._tags_json_path) as f:
            self.tag_infos: dict[str:dict] = json.load(f)

    def __load_condition(
        self,
    ):
        self.condition: dict
        if self._condition_json_path and self._condition_json_path.exists():
            with open(self._condition_json_path) as f:
                self.condition = json.load(f)
        else:
            self.condition = {}

    def __load_config(self):
        with open(self._config_path, "rb") as f:
            config: dict[str:any] = tomllib.load(f)

            self.formatter_value_regex = re.compile(
                config["formatter"]["value"]["regex"]
            )

            # check config
            _type: FormatterType
            for _type in FormatterType:
                assert _type.name in config["formatter"]["type_name_abbr"]
                assert _type.name in config["formatter"]["value"]["format_expression"]

            self.FormatterTypeNameAbbr: Enum = Enum(
                "FormatterTypeNameAbbr", config["formatter"]["type_name_abbr"]
            )
            self.FormatExpressions: Enum = Enum(
                "FormatExpressions", config["formatter"]["value"]["format_expression"]
            )

    def make(self, cheat_sheet_template: str) -> str:
        new_lines: list[str] = []

        _line: str
        for _line in tqdm(
            iterable=cheat_sheet_template.splitlines(keepends=True),
            desc="processing by lines...",
        ):
            try:
                new_lines.append(self._format_line(line=_line))
            except Exception as err:
                self._logger.error(
                    line=_line,
                    msg=err,
                    exc_info=True,
                )
                raise err
        return "".join(new_lines)

    def _format_line(self, line: str) -> str:
        if not line.strip():
            return line

        new_line: str = line
        _match: re.Match
        for _match in self.formatter_value_regex.finditer(line):
            _matched_string: str = _match.group()

            _: str
            _formatter_name_in_template: str
            _formatter_value: str
            _, _formatter_name_in_template, _formatter_value = _match.groups()
            _formatter_type: FormatterType = FormatterType[
                self.FormatterTypeNameAbbr(_formatter_name_in_template).name
            ]

            _tag_item: TagItem | None = None
            _tagmark_filter: TagmarkFilter | None = None

            # formatter value is a tag
            if _formatter_type in (
                FormatterType.tag,
                FormatterType.tag_filter,
                FormatterType.tag_filter_counts,
            ):
                _tag_item = TagItem(
                    tag=_formatter_value, **self.tag_infos.get(_formatter_value, {})
                )

            _tagmark_filter = TagmarkFilter(value=_formatter_value.strip())
            _tagmark_filter.filter(
                tagmark=self.converter.tagmark,
                condition=self.condition,
                is_ban_condition=self._is_ban_condition,
            )

            _formatter_expression: self.FormatExpressions = self.FormatExpressions[
                _formatter_type.name
            ]
            _formatted_matched_string: str = _formatter_expression.value.format(
                tag_item=_tag_item,
                url_base=self.url_base,
                filter=_tagmark_filter,
            )
            new_line = new_line.replace(_matched_string, _formatted_matched_string)

        return new_line
