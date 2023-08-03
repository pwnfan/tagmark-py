import random
import time

import requests
from fake_useragent import UserAgent
from tqdm import tqdm

from tagmark.core.export import BaseExporter


class WebExporter(BaseExporter):
    def export(self, cookie: str = ""):
        # random user-agent from top 10% most used user-agents
        _user_agent: str = UserAgent(min_percentage=10.0).random
        _page_number: int = 0
        _ONCE_EXPORT_COUNT: int = 96  # max is 100
        _session: requests.Session = requests.Session()
        _total_count: int | None = None
        _tqdm: tqdm = tqdm(total=1)
        while True:
            _response: requests.Response = _session.get(
                url=f"https://www.diigo.com/interact_api/load_user_items?page_num={_page_number}&sort=created&count={_ONCE_EXPORT_COUNT}",
                headers={
                    "User-Agent": _user_agent,
                    "Cookie": cookie,
                },
            )
            _page_number += 1

            if not _total_count:
                _total_count = _response.json().get("total")
                _tqdm.total = _total_count

            _new_items: list[dict] = _response.json().get("items", [])
            if len(_new_items) > 0:
                self.items.extend(_new_items)
                _tqdm.update(len(_new_items))
            else:
                _tqdm.close()
                break

            time.sleep(random.uniform(0, self.max_sleep_seconds_between_requests))

        return len(self.items)
