from pathlib import Path

import pytest

from syntopica.find_data_directory import find_data_directory


def _instance(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    (root / "syntopica.config.json").write_text("{}")
    return root


def test_explicit_wins(tmp_path: Path) -> None:
    data = _instance(tmp_path / "data")
    assert find_data_directory(str(data), {"SYNTOPICA_DATA": "/nowhere"}, tmp_path) == data


def test_environment_is_used_without_explicit(tmp_path: Path) -> None:
    data = _instance(tmp_path / "data")
    assert find_data_directory(None, {"SYNTOPICA_DATA": str(data)}, tmp_path) == data


def test_walks_upward_and_stops_at_a_repository(tmp_path: Path) -> None:
    data = _instance(tmp_path / "data")
    nested = data / "pages" / "deep"
    nested.mkdir(parents=True)
    assert find_data_directory(None, {}, nested) == data
    (tmp_path / "other" / ".git").mkdir(parents=True)
    with pytest.raises(FileNotFoundError, match="walking upward"):
        find_data_directory(None, {}, tmp_path / "other")
