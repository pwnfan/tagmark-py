import os
import click

from pathlib import Path

from dotenv import load_dotenv

from tagmark.core.convert import BaseConverter
from tagmark.tool.convert import diigo, tagmark as tagmark_


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
    github_token: str,
):
    converter: BaseConverter = None
    match format:
        case "diigo_chrome":
            converter = diigo.ChromeConverter()
        case "tagmark_jsonlines":
            converter = tagmark_.JsonLinesConverer()
        case _:
            raise ValueError(f"unsupported format: {format}")
    _items: list[dict] = converter.load_original_items(
        data_source=Path(input_file_path)
    )
    converter.convert_to_tagmark(items=_items)
    converter.tagmark.get_github_repo_infos(access_token=github_token)
    converter.tagmark.dump_to_json_lines(
        output_path=Path(output_file_path), keep_empty_keys=keep_empty_keys
    )
