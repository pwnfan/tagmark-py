import json
import os
import time
from pathlib import Path

import pytest

from tagmark.core.data import Tagmark, TagmarkFilter, TagmarkItem
from tagmark.core.github import GithubRepoInfo


class TestTagmark:
    tagmark_obj: Tagmark = Tagmark()
    count_added: int = 0

    @classmethod
    def setup_class(cls):
        cls.count_added += cls.tagmark_obj.add(
            [
                TagmarkItem(
                    url="https://github.com/olifolkerd/tabulator",
                    tags=[
                        "dev",
                        "frontend",
                        "javascript",
                        "library",
                        "module",
                    ],
                ),
                TagmarkItem(
                    url="https://github.com/yairEO/tagify",
                    tags=[
                        "dev",
                        "frontend",
                        "javascript",
                        "tag",
                        "library",
                        "module",
                    ],
                ),
                TagmarkItem(
                    url="https://www.runoob.com/w3cnote/open-source-license.html",
                    tags=[
                        "dev",
                        "oss",
                        "license",
                    ],
                ),
            ]
        )
        ban_condition: dict = {
            "tags": [
                "oss",
            ],
        }

        assert cls.tagmark_obj._count_need_update_github_repo_info(after_hours=1) == 2
        _access_token = os.environ.get("GITHUB_TOKEN")
        cls.tagmark_obj.get_github_repo_infos(
            access_token=_access_token, condition=ban_condition, is_ban_condition=True
        )
        assert cls.tagmark_obj._count_need_update_github_repo_info(after_hours=1) == 0

    def test_add(
        self,
    ):
        assert self.tagmark_obj.tagmark_items[0].id == 1
        assert self.tagmark_obj.tagmark_items[1].id == 2
        assert self.tagmark_obj.tagmark_items[2].id == 3
        assert self.count_added == 3

        # test add duplicated data
        with pytest.raises(ValueError):
            self.tagmark_obj.add(
                [
                    TagmarkItem(
                        url="https://github.com/olifolkerd/tabulator",
                        tags=[
                            "dev",
                            "frontend",
                            "javascript",
                            "library",
                            "module",
                        ],
                    ),
                ]
            )

    def test_sort(
        self,
    ):
        _sorted_tagit_items: list[TagmarkItem] = self.tagmark_obj.sort(
            key="url", reverse=True
        )
        assert list(_.url for _ in _sorted_tagit_items) == list(
            reversed([_.url for _ in self.tagmark_obj.tagmark_items])
        )

    def test_count_github_url(self):
        assert self.tagmark_obj.count_github_url == 2

    def test_all_tags(self):
        assert len(self.tagmark_obj.all_tags) == 8

    def test_get_github_repo_infos(
        self,
    ):
        github_repo_info: GithubRepoInfo = self.tagmark_obj.tagmark_items[
            0
        ].github_repo_info
        assert github_repo_info.url is not None
        assert github_repo_info.owner is not None
        assert github_repo_info.name is not None
        assert github_repo_info.is_archived is not None
        assert github_repo_info.description is not None
        assert github_repo_info.time_created is not None
        assert github_repo_info.time_last_commit is not None
        assert github_repo_info.time_last_release is None  # TODO
        assert github_repo_info.count_star is not None
        assert github_repo_info.count_fork is not None
        assert github_repo_info.count_watcher is not None
        assert github_repo_info.count_branch is None  # TODO
        assert github_repo_info.count_tag is None  # TODO
        assert github_repo_info.count_release is None  # TODO
        assert github_repo_info.count_contributor is None  # TODO

        github_repo_info: GithubRepoInfo = self.tagmark_obj.tagmark_items[
            -1
        ].github_repo_info
        assert not github_repo_info

    def test_dump_to_json_lines(
        self,
    ):
        # test keep_empty_keys==True
        output_path: Path = Path(f"/tmp/tagit_test_{time.time()}.jsonl")
        self.tagmark_obj.dump_to_json_lines(
            output_path=output_path, keep_empty_keys=True
        )
        dict_items: list[dict] = []

        with open(output_path, "r") as _f:
            for _line in _f:
                dict_items.append(json.loads(_line.strip()))
        for _dict_item in dict_items:
            for _k in TagmarkItem.__annotations__.keys():
                assert _k in _dict_item.keys()

        os.remove(output_path)

        # test keep_empty_keys==False
        output_path: Path = Path(f"/tmp/tagit_test_{time.time()}.jsonl")
        self.tagmark_obj.dump_to_json_lines(
            output_path=output_path, keep_empty_keys=False
        )
        dict_items: list[dict] = []

        with open(output_path, "r") as _f:
            for _line in _f:
                dict_items.append(json.loads(_line.strip()))
        assert "github_repo_info" not in dict_items[-1].keys()

        os.remove(output_path)

        # test condition and ban_condition==True
        output_path: Path = Path(f"/tmp/tagit_test_{time.time()}.jsonl")
        self.tagmark_obj.dump_to_json_lines(
            output_path=output_path,
            keep_empty_keys=False,
            condition={
                "tags": ["frontend", "xxx"],
                "valid": True,
            },
            is_ban_condition=True,
        )
        dict_items: list[dict] = []

        with open(output_path, "r") as _f:
            for _line in _f:
                dict_items.append(json.loads(_line.strip()))
        assert len(dict_items) == 1
        assert dict_items[0]["url"] == self.tagmark_obj.tagmark_items[-1].url

        # test condition and ban_condition==False
        output_path: Path = Path(f"/tmp/tagit_test_{time.time()}.jsonl")
        self.tagmark_obj.dump_to_json_lines(
            output_path=output_path,
            keep_empty_keys=False,
            condition={
                "tags": ["frontend", "xxx"],
                "valid": True,
            },
            is_ban_condition=False,
        )
        dict_items: list[dict] = []

        with open(output_path, "r") as _f:
            for _line in _f:
                dict_items.append(json.loads(_line.strip()))
        assert len(dict_items) == 2
        for _dict_item in dict_items:
            assert _dict_item["url"] != self.tagmark_obj.tagmark_items[-1].url


class TestTagmarkFilter:
    tagmark_obj: Tagmark = Tagmark()

    @classmethod
    def setup_class(cls):
        cls.tagmark_obj.add(
            [
                TagmarkItem(
                    url="https://github.com/CERT-Polska/Artemis",
                    tags=["sec", "misc-tool", "recon", "scan-vul", "oss", "python"],
                ),
                TagmarkItem(
                    url="https://github.com/moonD4rk/HackBrowserData",
                    tags=[
                        "sec",
                        "tool",
                        "sensitive-info",
                        "recon",
                        "browser",
                        "oss",
                        "golang",
                        "post-exploitation",
                    ],
                ),
                TagmarkItem(
                    url="https://www.runoob.com/w3cnote/open-source-license.html",
                    tags=[
                        "dev",
                        "oss",
                        "license",
                    ],
                ),
                TagmarkItem(
                    url="https://www.lifars.com/knowledge-center/python-penetration-testing-cheat-sheet",
                    tags=["sec", "dev", "python", "code-example", "penetration"],
                ),
            ]
        )

    def test_filter(self):
        filter_value1: str = "sec AND ((python OR golang))"
        condition: dict = {
            "tags": [
                "golang",
            ],
        }

        tagmark_filter1: TagmarkFilter = TagmarkFilter(filter_value=filter_value1)
        tagmark_filter1.filter(
            tagmark=self.tagmark_obj,
            condition=condition,
            is_ban_condition=True,
        )
        assert tagmark_filter1.count_total == 2
        assert tagmark_filter1.count_github == 1

        tagmark_filter2: TagmarkFilter = TagmarkFilter(filter_value=filter_value1)
        tagmark_filter2.filter(
            tagmark=self.tagmark_obj,
            condition=condition,
            is_ban_condition=False,
        )
        assert tagmark_filter2.count_total == 1
        assert tagmark_filter2.count_github == 1

        filter_value2: str = "sec AND ( NOT  golang)"
        tagmark_filter3: TagmarkFilter = TagmarkFilter(filter_value=filter_value2)
        tagmark_filter3.filter(tagmark=self.tagmark_obj)
        assert tagmark_filter3.count_total == 2
        assert tagmark_filter3.count_github == 1

        tagmark_filter4: TagmarkFilter = TagmarkFilter(filter_value="")
        tagmark_filter4.filter(tagmark=self.tagmark_obj)
        assert tagmark_filter4.count_total == 4
        assert tagmark_filter4.count_github == 2
