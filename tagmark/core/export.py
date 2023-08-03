import json
from abc import ABC, abstractmethod
from pathlib import Path


class BaseExporter(ABC):
    def __init__(self, max_sleep_seconds_between_requests=3):
        self.max_sleep_seconds_between_requests = 3
        self.items: list[dict] = []

    @abstractmethod
    def export(
        self,
    ) -> int:
        """
        export data

        Returns:
            int: the number of exported data items
        """
        raise NotImplementedError

    def dump_to_json_lines(
        self,
        output_path: Path,
    ):
        if len(self.items) > 0:
            with open(output_path, "w") as f:
                f.writelines(
                    f"{json.dumps(_item, ensure_ascii=False, separators=(',', ':'))}\n"
                    for _item in self.items
                )
