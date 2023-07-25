from dataclasses import dataclass

from revChatGPT.V1 import Chatbot
from tqdm import tqdm

from tagmark.core.log import LogHandler, LogLevel, get_level_logger
from tagmark.core.tag import NoEnoughTagInfoForGptPromptException, TagItem


@dataclass
class AutoTagMakeStats:
    count_total_tags: int = 0
    count_auto_made_success: int = (
        0  # has a prompt and succeeded to get a definition by chatgpt
    )
    count_auto_made_fail: int = (
        0  # has a prompt but failed to get a definition by chatgpt
    )
    count_no_gpt_prompt: int = (
        0  # the value is still TagItem.gpt_prompt_context is an empty value
    )
    count_already_defined: int = 0  # already has a definition


class AutoTagDefinitionMarker:
    def __init__(
        self, gpt_config: dict, timeout: int = 60, conversation_id: str = None
    ):
        self.chatbot = Chatbot(config=gpt_config)
        self._conversation_id = conversation_id or gpt_config.get("conversation_id")
        self._timeout = timeout
        self._logger = get_level_logger(
            name="tagmark",
            level=LogLevel.INFO,
            handlers=[
                LogHandler.CONSOLE,
            ],
        )
        self._logger.bind(scope=self.__class__.__name__)

    def _get_definition_by_chatgpt(
        self,
        prompt: str,
    ) -> str | None:
        response: str = ""

        for data in self.chatbot.ask(
            prompt=prompt,
            conversation_id=self._conversation_id,
            timeout=self._timeout,
        ):
            response = data["message"]

        return response

    def auto_define_tags(
        self,
        tag_infos: dict[str:dict],
        little_info_tag_is_ok=False,
    ) -> tuple[dict[str:str], AutoTagMakeStats]:
        auto_tag_make_stats: AutoTagMakeStats = AutoTagMakeStats()
        auto_tag_make_stats.count_total_tags = len(tag_infos)
        new_tag_definitions: dict[str:str] = {}
        for _tag, _tag_value in tqdm(tag_infos.items()):
            _tag_item: TagItem = TagItem(tag=_tag, **_tag_value)

            if _tag_item.definition:
                auto_tag_make_stats.count_already_defined += 1
                continue
            else:
                try:
                    _gpt_prompt: str = _tag_item.generate_gpt_prompt(
                        little_info_is_ok=little_info_tag_is_ok,
                    )
                except NoEnoughTagInfoForGptPromptException:
                    auto_tag_make_stats.count_no_gpt_prompt += 1
                    self._logger.error(
                        msg=f"Error occurs when getting the definition of {_tag_item} from gpt",
                        exc_info=True,
                    )
                    continue

                try:
                    _tag_definition: str | None = self._get_definition_by_chatgpt(
                        prompt=_gpt_prompt
                    )
                    if not _tag_definition or not _tag_definition.strip():
                        auto_tag_make_stats.count_auto_made_fail += 1
                    else:
                        auto_tag_make_stats.count_auto_made_success += 1
                        new_tag_definitions[_tag] = _tag_definition
                except Exception:
                    self._logger.error(
                        msg=f"Error occurs when getting the definition tag {_tag} from gpt",
                        exc_info=True,
                    )
                    auto_tag_make_stats.count_auto_made_fail += 1

        return new_tag_definitions, auto_tag_make_stats
