from dataclasses import dataclass

from revChatGPT.V1 import Chatbot
from tqdm import tqdm

from tagmark.core.log import LogHandler, LogLevel, get_level_logger


@dataclass
class AutoTagMakeStats:
    count_total_tags: int = 0
    count_auto_made_success: int = (
        0  # has a prompt and succeeded to get a definiton by chatgpt
    )
    count_auto_made_fail: int = (
        0  # has a prompt but failed to get a definiton by chatgpt
    )
    count_no_prompt: int = 0  # the value is still `no_def_tag_value_placeholder`
    count_already_defined: int = 0  # already has a definiton


class AutoTagDefinitonMarker:
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
        self._logger.bind(scope="AutoTagDefinitonMarker")

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

    def auto_make_tag_definitions(
        self,
        tag_definitions: dict[str:str],
        gpt_prompt_ending_flag: str = "?",
        no_def_tag_value_placeholder: str = "!!!NO DEFINITION FOR THIS TAG, PLEASE ADD HERE!!!",
    ) -> tuple[dict[str:str], AutoTagMakeStats]:
        auto_tag_make_stats: AutoTagMakeStats = AutoTagMakeStats()
        auto_tag_make_stats.count_total_tags = len(tag_definitions)
        new_tags_definition: dict[str:str] = {}
        for _tag, _tag_value in tqdm(tag_definitions.items()):
            _tag_value: str = _tag_value.strip()
            _new_tag_value: str = _tag_value

            # `_tag_value` is a question(prompt) for gpt to generate definition
            if _tag_value.endswith(gpt_prompt_ending_flag):
                try:
                    _new_tag_value = self._get_definition_by_chatgpt(prompt=_tag_value)
                    auto_tag_make_stats.count_auto_made_success += 1
                except Exception:
                    self._logger.error(
                        msg=f"Error occurs when getting the definition tag {_tag} from gpt",
                        exc_info=True,
                    )
                    auto_tag_make_stats.count_auto_made_fail += 1

            # `_tag_value` is a placeholder
            elif no_def_tag_value_placeholder == _tag_value:
                self._logger.warning(msg=f"placeholder found for tag {_tag}, skip...")
                auto_tag_make_stats.count_no_prompt += 1

            # `_tag_value` is a tag definition
            else:
                auto_tag_make_stats.count_already_defined += 1

            new_tags_definition[_tag] = _new_tag_value
        return new_tags_definition, auto_tag_make_stats
