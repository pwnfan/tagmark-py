import json
import os
from pathlib import Path

import click
from dotenv import load_dotenv

from tagmark.core.convert import BaseConverter
from tagmark.tools.convert import diigo
from tagmark.tools.convert import tagmark as tagmark_convert

load_dotenv()


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
    help="If set to True, a TagmarkItem hits the `condition` will be banned, or it will be remained.",
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
