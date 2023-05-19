import json
import os
import warnings
from datetime import datetime
from pathlib import Path

import click
from dotenv import find_dotenv, load_dotenv

from tagmark.core.convert import BaseConverter, TagsCheckResult
from tagmark.core.log import LogHandler, LogLevel, get_level_logger
from tagmark.tools.convert import diigo
from tagmark.tools.convert import tagmark as tagmark_convert

load_dotenv(dotenv_path=find_dotenv(usecwd=True))


class TagDefinitionUnusedWarning(Warning):
    pass


class TagDefinitionMissingError(Exception):
    pass


@click.group()
def cli():
    pass


@cli.command(help="covert other format of bookmarks into Tagmark format(json-lines)")
@click.option(
    "-i",
    "--input-file-path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    help="input file path",
)
@click.option(
    "-f",
    "--format",
    type=click.Choice(["diigo_chrome", "tagmark_jsonlines"]),
    default="diigo_chrome",
    show_default=True,
    show_choices=True,
    help="format of the input file",
)
@click.option(
    "-o",
    "--output-file-path",
    type=click.Path(exists=False, file_okay=True, dir_okay=False),
    default="tagmark_ui_data.jsonl",
    show_default=True,
    help="output file path",
)
@click.option(
    "-k",
    "--keep_empty_keys",
    type=click.BOOL,
    default=False,
    show_default=True,
    help="whether keep keys with empty values",
)
@click.option(
    "-c",
    "--condition-json-path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    default=Path(__file__).absolute().parent.joinpath("condition_example.json"),
    show_default=True,
    help="json file containing the condition for fitlering TagmarkItem",
)
@click.option(
    "-b",
    "--is-ban-condition",
    type=click.BOOL,
    default=True,
    show_default=True,
    help="If set to True, a TagmarkItem hits the `condition` will be banned, or it will be remained",
)
@click.option(
    "-t",
    "--github_token",
    type=str,
    default=os.environ.get("GITHUB_TOKEN"),
    show_default=False,
    help="the GITHUB_TOKEN to access Github API, default will read from the .env file of the root dir of this project",
)
def convert(
    input_file_path: str,
    format: str,
    output_file_path: str,
    keep_empty_keys: bool,
    condition_json_path: str,
    is_ban_condition: bool,
    github_token: str,
):
    converter: BaseConverter = None
    match format:
        case "diigo_chrome":
            converter = diigo.ChromeConverter()
        case "tagmark_jsonlines":
            converter = tagmark_convert.JsonLinesConverer()
        case _:
            raise ValueError(f"unsupported format: {format}")
    _items: list[dict] = converter.load_original_items(
        data_source=Path(input_file_path)
    )
    converter.convert_to_tagmark(items=_items)
    converter.tagmark.get_github_repo_infos(access_token=github_token)
    with open(Path(condition_json_path), "r") as _f:
        condition: dict = json.load(_f)
        converter.tagmark.dump_to_json_lines(
            output_path=Path(output_file_path),
            keep_empty_keys=keep_empty_keys,
            condition=condition,
            is_ban_condition=is_ban_condition,
        )


@cli.command(help="verify every tag has a definition")
@click.option(
    "-t",
    "--tagmark-data-file-path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    help="the tagmark data file path, which may be the value the `-o` parameter of the `convert` sub command",
)
@click.option(
    "-d",
    "--tag-definition-file-path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    help="tag definition file path",
)
@click.option(
    "-c",
    "--condition-json-path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    default=None,
    show_default=True,
    help="json file containing the condition for fitlering TagmarkItem, here only the value of `tags` field in the file will be used, and this condition is a determinate ban condition",
)
@click.option(
    "-a",
    "--add-no-def-tag",
    type=bool,
    default=True,
    show_default=True,
    help="if set to `True`, the tags in the input file(bookmark file) without a tag definition will be added into the tag definition file, with a placeholder value specified by `added_missing_tag_value_placeholder`. If set to `Flase` and any tag without definition exists, an error will be raised",
)
@click.option(
    "-p",
    "--no-def-tag-value-placeholder",
    type=str,
    default="!!!NO DEFINITION FOR THIS TAG, PLEASE ADD HERE!!!",
    show_default=True,
    help="explained in the `-a` parameter",
)
def checktag(
    tagmark_data_file_path: str,
    tag_definition_file_path: str,
    condition_json_path: str,
    add_no_def_tag: bool,
    no_def_tag_value_placeholder: str,
):
    _converter: tagmark_convert.JsonLinesConverer = tagmark_convert.JsonLinesConverer()
    _items: list[dict] = _converter.load_original_items(
        data_source=Path(tagmark_data_file_path)
    )
    _converter.convert_to_tagmark(items=_items)
    tag_definition_file: Path = Path(tag_definition_file_path)
    with open(tag_definition_file) as _f_tag_definition:
        tag_definitions: dict = json.load(_f_tag_definition)
        _tags_with_definition: set = set(tag_definitions.keys())

    _tags_in_ban_condition: set[str] = {}
    if condition_json_path:
        with open(Path(condition_json_path)) as _f_ban_condition:
            _tags_in_ban_condition: set = set(
                json.load(_f_ban_condition).get("tags", [])
            )

    tags_check_result: TagsCheckResult = _converter.check_tags(
        tags_with_definition=_tags_with_definition,
        tags_in_ban_condition=_tags_in_ban_condition,
    )
    _logger = get_level_logger(
        name="tagmark.cli",
        level=LogLevel.INFO,
        handlers=[
            LogHandler.CONSOLE,
        ],
    )
    _logger.bind(scope="checktag")
    _logger.info(tags_count=tags_check_result.count)

    if tags_check_result.tags_definition_unused:
        _logger.warn(
            msg="unused definition found",
            tags_definition_unused=tags_check_result.tags_definition_unused,
        )
        warnings.warn(
            message=f"unused definition found: {sorted(tags_check_result.tags_definition_unused)}",
            category=TagDefinitionUnusedWarning,
        )

    if tags_check_result.tags_without_definition:
        if not add_no_def_tag:
            _logger.error(
                msg="tags without definition found",
                tags_without_definition=tags_check_result.tags_without_definition,
            )
            raise TagDefinitionMissingError(
                f"tags without definition found{sorted(tags_check_result.tags_without_definition)}"
            )
        else:
            if not no_def_tag_value_placeholder.strip():
                raise ValueError(
                    f"invalid value for `no_def_tag_value_placeholder`: {no_def_tag_value_placeholder}"
                )
            new_tags_definition_file: Path = tag_definition_file.parent.joinpath(
                f"new-{datetime.now().strftime('%Y%m%d%H%M%S')}-{tag_definition_file.name}"
            )
            new_tags_definition: dict[str:str] = tag_definitions.copy()
            new_tags_definition.update(
                {
                    _tag: no_def_tag_value_placeholder
                    for _tag in tags_check_result.tags_without_definition
                }
            )
            with open(new_tags_definition_file, "w") as f:
                json.dump(
                    obj=new_tags_definition,
                    fp=f,
                    sort_keys=True,
                    indent=4,
                    ensure_ascii=False,
                )
                _logger.info(
                    msg="new tags definition file has been generated",
                    new_tags_definition_file=new_tags_definition_file.absolute(),
                )
