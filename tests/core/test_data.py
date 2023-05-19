import json
import os
import time
from pathlib import Path

import pytest

from tagmark.core.data import Tagmark, TagmarkItem
from tagmark.core.github import GithubRepoInfo


class TestTagit:
    tagit: Tagmark = Tagmark()
    count_added: int = 0

    @classmethod
    def setup_class(cls):
        cls.count_added += cls.tagit.add(
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
        _access_token = os.environ.get("GITHUB_TOKEN")
        cls.tagit.get_github_repo_infos(
            access_token=_access_token, condition=ban_condition, is_ban_condition=True
        )

    def test_add(
        self,
    ):
        assert self.tagit.tagmark_items[0].id == 1
        assert self.tagit.tagmark_items[1].id == 2
        assert self.tagit.tagmark_items[2].id == 3
        assert self.count_added == 3

        # test add duplicated data
        with pytest.raises(ValueError):
            self.tagit.add(
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

    def test_count_github_url(self):
        assert self.tagit.count_github_url == 2

    def test_all_tags(self):
        assert len(self.tagit.all_tags) == 8

    def test_sort(
        self,
    ):
        _sorted_tagit_items: list[TagmarkItem] = self.tagit.sort(
            key="url", reverse=True
        )
        assert list(_.url for _ in _sorted_tagit_items) == list(
            reversed([_.url for _ in self.tagit.tagmark_items])
        )

    def test_get_github_repo_infos(
        self,
    ):
        github_repo_info: GithubRepoInfo = self.tagit.tagmark_items[0].github_repo_info
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
        assert github_repo_info.count_conributor is None  # TODO
        
        github_repo_info: GithubRepoInfo = self.tagit.tagmark_items[-1].github_repo_info
        assert not github_repo_info

    def test_dump_to_json_lines(
        self,
    ):
        # test keep_empty_keys==True
        output_path: Path = Path(f"/tmp/tagit_test_{time.time()}.jsonl")
        self.tagit.dump_to_json_lines(output_path=output_path, keep_empty_keys=True)
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
        self.tagit.dump_to_json_lines(output_path=output_path, keep_empty_keys=False)
        dict_items: list[dict] = []

        with open(output_path, "r") as _f:
            for _line in _f:
                dict_items.append(json.loads(_line.strip()))
        assert "github_repo_info" not in dict_items[-1].keys()

        os.remove(output_path)

        # test condition and ban_condition==True
        output_path: Path = Path(f"/tmp/tagit_test_{time.time()}.jsonl")
        self.tagit.dump_to_json_lines(
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
        assert dict_items[0]["url"] == self.tagit.tagmark_items[-1].url

        # test condition and ban_condition==False
        output_path: Path = Path(f"/tmp/tagit_test_{time.time()}.jsonl")
        self.tagit.dump_to_json_lines(
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
            assert _dict_item["url"] != self.tagit.tagmark_items[-1].url
