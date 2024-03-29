import json
import os
import warnings
from datetime import datetime
from pathlib import Path

import click
from dotenv import find_dotenv, load_dotenv

from tagmark.core.convert import BaseConverter
from tagmark.core.export import BaseExporter
from tagmark.core.log import LogHandler, LogLevel, get_level_logger
from tagmark.tools.autotagdef import AutoTagDefinitionMarker, AutoTagMakeStats
from tagmark.tools.checktag import TagsChecker
from tagmark.tools.convert import diigo as convert_diigo
from tagmark.tools.convert import tagmark as convert_tagmark
from tagmark.tools.export import diigo as export_diigo
from tagmark.tools.maketagdoc import TagDocMaker

load_dotenv(dotenv_path=find_dotenv(usecwd=True))


class TagInfoUnusedWarning(Warning):
    pass


class TagInfoMissingError(Exception):
    pass


__logger = get_level_logger(
    name="tagmark.cli",
    level=LogLevel.INFO,
    handlers=[
        LogHandler.CONSOLE,
    ],
)
__logger.bind(scope="cli")


class NaturalOrderGroup(click.Group):
    def list_commands(self, ctx):
        return self.commands.keys()


@click.group(
    cls=NaturalOrderGroup,
    context_settings=dict(help_option_names=["-h", "--help"]),
)
def cli():
    pass


@cli.command(
    name="export",
    context_settings=dict(help_option_names=["-h", "--help"]),
    help="export tagged bookmarked data from third party services into jsonlines file",
)
@click.option(
    "-f",
    "--format",
    type=click.Choice(
        [
            "diigo_web",
        ]
    ),
    default="diigo_web",
    show_default=True,
    show_choices=True,
    help="third party service",
)
@click.option(
    "-m",
    "--max-sleep-seconds-between-requests",
    type=click.FLOAT,
    default=3,
    show_default=True,
    help="if multiple requests are needed to retrieve the data, in order to prevent excessive load on the target server, a random time sleep is necessary, this option set the maximum sleep seconds",
)
@click.option(
    "-o",
    "--output-file-path",
    type=click.Path(exists=False, file_okay=True, dir_okay=False),
    default="diigo_web_exported.jsonl",
    show_default=True,
    help="output file path",
)
def export(
    format: str,
    max_sleep_seconds_between_requests: float,
    output_file_path: str,
):
    exporter: BaseExporter = None
    match format:
        case "diigo_web":
            exporter = export_diigo.WebExporter(
                max_sleep_seconds_between_requests=max_sleep_seconds_between_requests
            )
            _cookie = os.environ.get("DIIGO_COOKIE", "")
            if not _cookie.strip():
                __logger.error(
                    msg="Diigo web Cookie is missing, please specify it as DIIGO_COOKIE in the .env file or in shell environment variable"
                )
                raise ValueError(f"Cookie value: {_cookie}")
            try:
                exporter.export(cookie=_cookie)
            except Exception:
                __logger.error(
                    msg="export data failed",
                    exc_info=True,
                )
        case _:
            raise ValueError(f"unsupported format: {format}")

    output_file_path: Path = Path(output_file_path)
    exporter.dump_to_json_lines(output_path=output_file_path)
    if output_file_path.exists():
        __logger.info(
            msg="data has been exported",
            counts_exported_items=len(exporter.items),
            output_file_path=output_file_path.absolute(),
        )
    else:
        __logger.warn(
            msg="no data has been exported",
        )


@cli.command(
    name="convert",
    context_settings=dict(help_option_names=["-h", "--help"]),
    no_args_is_help=True,
    help="convert other bookmark formats into TagMark format (json-lines)",
)
@click.option(
    "-i",
    "--input-file-path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    help="input file path",
)
@click.option(
    "-f",
    "--format",
    type=click.Choice(
        ["diigo_web_exported", "diigo_exported_chrome_format", "tagmark_jsonlines"]
    ),
    default="diigo_web_exported",
    show_default=True,
    show_choices=True,
    help="format of the input file",
)
@click.option(
    "-o",
    "--output-file-path",
    type=click.Path(exists=False, file_okay=True, dir_okay=False),
    default="tagmarks.jsonl",
    show_default=True,
    help="output tagmark jsonlines data file path",
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
@click.option(
    "-u",
    "--update-github-info-after-hours",
    type=float,
    default=23,
    show_default=True,
    help="update github info only when user specified number of hours has passed since the last update",
)
def convert(
    input_file_path: str,
    format: str,
    output_file_path: str,
    keep_empty_keys: bool,
    condition_json_path: str,
    is_ban_condition: bool,
    github_token: str,
    update_github_info_after_hours: float,
):
    converter: BaseConverter = None
    match format:
        case "diigo_web_exported":
            converter = convert_diigo.WebExportedJsonlinesConverter()
        case "diigo_exported_chrome_format":
            converter = convert_diigo.ExportedChromeFormatConverter()
        case "tagmark_jsonlines":
            converter = convert_tagmark.JsonLinesConverter()
        case _:
            raise ValueError(f"unsupported format: {format}")
    _items: list[dict] = converter.load_original_items(
        data_source=Path(input_file_path)
    )
    converter.convert_to_tagmark(items=_items)
    with open(Path(condition_json_path), "r") as _f:
        condition: dict = json.load(_f)
        converter.tagmark.get_github_repo_infos(
            access_token=github_token,
            condition=condition,
            after_hours=update_github_info_after_hours,
            is_ban_condition=is_ban_condition,
        )
        converter.tagmark.dump_to_json_lines(
            output_path=Path(output_file_path),
            keep_empty_keys=keep_empty_keys,
            condition=condition,
            is_ban_condition=is_ban_condition,
        )
        __logger.info(
            msg="new tagmark data file has been generated",
            tagmark_data=Path(output_file_path).absolute(),
        )


@cli.command(
    name="checktag",
    context_settings=dict(help_option_names=["-h", "--help"]),
    no_args_is_help=True,
    help="check tag consistency in tagmark data file (json-lines) and tags info file (json)",
)
@click.option(
    "-d",
    "--tagmark-jsonlines-data-path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    help="the tagmark jsonlines data file path, which may be the output file generated by the `-o` parameter of the `convert` subcommand",
)
@click.option(
    "-t",
    "--tags-json-path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    help="tags.json file path",
)
@click.option(
    "-c",
    "--condition-json-path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    default=Path(__file__).absolute().parent.joinpath("condition_example.json"),
    show_default=True,
    help="json file containing the condition for filtering TagmarkItem, here only the value of `tags` field in the file will be used, and this condition must be a ban condition",
)
@click.option(
    "-a",
    "--add-new-tags",
    type=bool,
    default=True,
    show_default=True,
    help="if set to `True`, a new tags.json file will be generated, which includes old tags in tag.json file, and new tags in the tagmark data file(specified by -t).",
)
def check_tag(
    tagmark_jsonlines_data_path: str,
    tags_json_path: str,
    condition_json_path: str,
    add_new_tags: bool,
):
    tags_checker: TagsChecker = TagsChecker(
        tagmark_jsonlines_data_path=tagmark_jsonlines_data_path,
        tags_json_path=tags_json_path,
        condition_json_path=condition_json_path,
    )
    tags_checker.check_tag_duplicated_formatted_names()
    tags_checker.check_tags()
    __logger.info(tags_count=tags_checker.check_result.count)

    if tags_checker.check_result.tags_only_in_tags_json:
        __logger.warn(
            msg="tags only in tags.json(unused tags) found",
            tags_unused=tags_checker.check_result.tags_only_in_tags_json,
        )
        warnings.warn(
            message=f"tags only in tags.json(unused tags) found: {sorted(tags_checker.check_result.tags_only_in_tags_json)}",
            category=TagInfoUnusedWarning,
        )

    if tags_checker.check_result.tags_only_in_data_source:
        __logger.warn(
            msg="tags only in data source(undefined tags) found",
            tags_only_in_data_source=sorted(
                tags_checker.check_result.tags_only_in_data_source
            ),
        )

        if not add_new_tags:
            raise TagInfoMissingError(
                f"tags only in data source(undefined tags) found: {sorted(tags_checker.check_result.tags_only_in_data_source)}"
            )
        else:
            tags_json_path: Path = Path(tags_json_path)
            new_tags_json_file: Path = tags_json_path.parent.joinpath(
                f"new-{datetime.now().strftime('%Y%m%d%H%M%S')}-{tags_json_path.name}"
            )
            tags_checker.generate_new_tag_infos()
            with open(new_tags_json_file, "w") as f:
                json.dump(
                    obj=tags_checker.new_tag_infos,
                    fp=f,
                    sort_keys=True,
                    indent=4,
                    ensure_ascii=False,
                )
                __logger.info(
                    msg="new tags information file has been generated",
                    new_tags_information_file=new_tags_json_file.absolute(),
                )


@cli.command(
    name="autotagdef",
    context_settings=dict(help_option_names=["-h", "--help"]),
    no_args_is_help=True,
    help="get tag definition automatically with ChatGPT",
)
@click.option(
    "-d",
    "--tags-info-json-path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    help="tags.json (tags information) file path",
)
@click.option(
    "-c",
    "--gpt-config-file-path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    default="~/.config/revChatGPT/config.json",
    help="the config file for invoking ChatGPT API, we sugguest setting `access_token` in the config file, see https://github.com/acheong08/ChatGPT#--access-token for details.",
)
@click.option(
    "-i",
    "--gpt-conversation-id",
    type=str,
    default=None,
    show_default=True,
    help="the id of conversation in which to (continue to) interact with ChatGPT, if set to `None` a new conversation will be created. See https://github.com/acheong08/ChatGPT/wiki/V1#ask for details.",
)
@click.option(
    "-t",
    "--gpt-timeout",
    type=int,
    default=60,
    show_default=True,
    help="the timeout that GPT answers one question (get one tag definition)",
)
@click.option(
    "-l",
    "--little-info-tag-is-ok",
    type=click.BOOL,
    default=False,
    show_default=True,
    help="",
)
def auto_tag_def(
    tags_info_json_path,
    gpt_config_file_path,
    gpt_conversation_id,
    gpt_timeout,
    little_info_tag_is_ok,
):
    # load tag definitions from file
    _tags_info_json_path: Path = Path(tags_info_json_path)
    with open(Path(_tags_info_json_path)) as _f:
        _tags_info: dict[str:dict] = json.load(_f)

    # loag gpt config from file
    with open(Path(gpt_config_file_path)) as _f:
        _gpt_config = json.load(_f)

    # auto make tag definitions
    _auto_tag_def_maker: AutoTagDefinitionMarker = AutoTagDefinitionMarker(
        gpt_config=_gpt_config,
        conversation_id=gpt_conversation_id,
        timeout=gpt_timeout,
    )

    _new_tag_definitions: dict[str:str]
    _auto_tag_make_stats: AutoTagMakeStats
    (
        _new_tag_definitions,
        _auto_tag_make_stats,
    ) = _auto_tag_def_maker.auto_define_tags(
        tag_infos=_tags_info,
        little_info_tag_is_ok=little_info_tag_is_ok,
    )
    if _new_tag_definitions:
        __logger.info(
            msg="no definition tags found!",
            no_definition_tags=_new_tag_definitions.keys(),
        )

    new_tags_info: dict[str:dict] = _tags_info.copy()
    for _tag, _definition in _new_tag_definitions.items():
        new_tags_info[_tag]["definition"] = _definition

    # write new tag infos into file
    new_tags_info_json_path: Path = _tags_info_json_path.parent.joinpath(
        f"new-{datetime.now().strftime('%Y%m%d%H%M%S')}-{_tags_info_json_path.name}"
    )
    with open(new_tags_info_json_path, "w") as f:
        json.dump(
            obj=new_tags_info,
            fp=f,
            sort_keys=True,
            indent=4,
            ensure_ascii=False,
        )
        __logger.info(
            msg="new tags.json has been generated",
            new_tags_definition_file=new_tags_info_json_path.absolute(),
        )
        __logger.info(
            msg="statistics",
            auto_tag_make_stats=_auto_tag_make_stats,
        )


@cli.command(
    name="maketagdoc",
    context_settings=dict(help_option_names=["-h", "--help"]),
    no_args_is_help=True,
    help="make document from a template containing tag related syntaxes",
)
@click.option(
    "-d",
    "--tagmark-jsonlines-data-path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    help="the tagmark jsonlines data file path, which may be the output file generated by the `-o` parameter of the `convert` subcommand",
)
@click.option(
    "-t",
    "--tags-json-path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    help="tags.json file path",
)
@click.option(
    "-s",
    "--config-path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    default=Path(__file__)
    .absolute()
    .parent.joinpath(
        "tools",
        "maketagdoc.toml.default",
    ),
    show_default=True,
    help="(formatter) configuration file path",
)
@click.option(
    "-u",
    "--url-base",
    type=str,
    default="./",
    show_default=True,
    help="url base for generating formatted links",
)
@click.option(
    "-c",
    "--condition-json-path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    default=Path(__file__).absolute().parent.joinpath("condition_example.json"),
    show_default=True,
    help="json file containing the condition for filtering TagmarkItem, here only the value of `tags` field in the file will be used, and this condition must be a ban condition",
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
    "-m",
    "--template-path",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
    help="template file path",
)
@click.option(
    "-o",
    "--output-file-path",
    type=click.Path(exists=False, file_okay=True, dir_okay=False),
    default=Path.cwd().absolute().joinpath("formatted_tag_doc.md"),
    show_default=True,
    help="the output file (formatted according to the template file) path",
)
def make_tag_doc(
    tagmark_jsonlines_data_path,
    tags_json_path,
    config_path,
    url_base,
    condition_json_path,
    is_ban_condition,
    template_path,
    output_file_path,
):
    tag_doc_maker: TagDocMaker = TagDocMaker(
        tagmark_jsonlines_data_path=Path(tagmark_jsonlines_data_path),
        tags_json_path=Path(tags_json_path),
        config_path=Path(config_path),
        url_base=url_base,
        condition_json_path=Path(condition_json_path),
        is_ban_condition=is_ban_condition,
    )
    with open(template_path) as ft, open(output_file_path, "w") as fo:
        fo.write(tag_doc_maker.make(cheat_sheet_template=ft.read()))
        __logger.info(
            msg="tag formatted document has been generated",
            output_file_path=Path(output_file_path).absolute(),
        )


if __name__ == "__main__":
    cli()
