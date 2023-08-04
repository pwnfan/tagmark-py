from pathlib import Path

import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def test_input_file_paths() -> dict[str:Path]:
    return {
        "tagmark_jsonlines_data": Path(
            "tests/data/tagmark_ui_data_1682298863.158216.jsonl"
        ).absolute(),
        "tags_json": Path("tests/data/tags.json").absolute(),
        "condition_json": Path("tests/data/ban-condition.json").absolute(),
    }
