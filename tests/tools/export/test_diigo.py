import os
import tempfile
from pathlib import Path
from typing import TextIO

import requests_mock

from tagmark.tools.export.diigo import WebExporter


class TestWebExporter:
    web_exporter: WebExporter = WebExporter()
    response1: dict = {
        "items": [
            {
                "comments": [],
                "ouliner_id": [],
                "created_at": 1690507197,
                "annotations": [],
                "c_count": 0,
                "text_view_link": "https://www.diigo.com/text_view?url=https%3A%2F%2Fgithub.com%2Ffuture-architect%2Fvuls",
                "pub_a_count": 0,
                "real_name": "pwnfan",
                "type_name": "bookmark",
                "is_attached_item": True,
                "user_id": 16400249,
                "first_by": "ronansandford",
                "pri_sticky_count": 0,
                "updated_at": 1690507197,
                "first_by_real_name": "ronansandford",
                "readed": 1,
                "pub_sticky_count": 0,
                "groups": [],
                "pri_c_count": 0,
                "hasDetails": "false",
                "private": True,
                "description": "",
                "pub_c_count": 0,
                "t_name": "sec,tool,enterprise,blue-team,scan-vul,vul-management,oss,golang",
                "title": "future-architect/vuls: Agent-less vulnerability scanner for Linux, FreeBSD, Container, WordPress, Programming language libraries, Network devices",
                "outliners_id": [],
                "tags": "sec,tool,enterprise,blue-team,scan-vul,vul-management,oss,golang",
                "mode": 2,
                "url": "https://github.com/future-architect/vuls",
                "pri_a_count": 0,
                "u_name": "pwnfan",
                "link_id": 309886765,
            },
            {
                "comments": [],
                "ouliner_id": [],
                "created_at": 1690507119,
                "annotations": [],
                "c_count": 0,
                "text_view_link": "https://www.diigo.com/text_view?url=https%3A%2F%2Fwww.jpcert.or.jp",
                "pub_a_count": 0,
                "real_name": "pwnfan",
                "type_name": "bookmark",
                "is_attached_item": True,
                "user_id": 16400249,
                "first_by": "anonymous",
                "pri_sticky_count": 0,
                "updated_at": 1690507119,
                "first_by_real_name": "anonymous",
                "readed": 1,
                "pub_sticky_count": 0,
                "groups": [],
                "pri_c_count": 0,
                "hasDetails": "false",
                "private": True,
                "description": "",
                "pub_c_count": 0,
                "t_name": "sec,vul-alert,cert,japanese",
                "title": "JPCERT コーディネーションセンター",
                "outliners_id": [],
                "tags": "sec,vul-alert,cert,japanese",
                "mode": 2,
                "url": "https://www.jpcert.or.jp",
                "pri_a_count": 0,
                "u_name": "pwnfan",
                "link_id": 330145969,
            },
        ],
        "total": 2,
        "rss_link": "",
        "unread_total": 1,
        "adsInfo": {
            "search": {
                "hints": "blue-team,issue",
                "bottom": True,
                "top": True,
            }
        },
    }
    response2: dict = {
        "items": [],
        "adsInfo": {"search": {"bottom": False, "top": False}},
        "total": 0,
        "rss_link": "",
    }

    def test_export_dump(self, mocker):
        # test export
        with requests_mock.Mocker() as mocker:
            mocker.get(
                url=requests_mock.ANY,
                response_list=[
                    {
                        "json": self.response1,
                    },
                    {
                        "json": self.response2,
                    },
                ],
            )
            assert self.web_exporter.export() == len(self.response1["items"])
            assert self.web_exporter.items == self.response1["items"]

        # test dump
        with open("tests/data/diigo_web_exported.jsonl") as f_right:
            output_f: TextIO = tempfile.NamedTemporaryFile(mode="w", delete=False)
            output_f.close()
            self.web_exporter.dump_to_json_lines(output_path=Path(output_f.name))
            with open(output_f.name) as output_f:
                assert output_f.read() == f_right.read()
            os.unlink(output_f.name)
