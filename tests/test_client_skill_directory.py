from pathlib import Path

from syntopica.client_skill_directory import client_skill_directory


def test_directories_follow_each_client_contract(tmp_path: Path) -> None:
    assert client_skill_directory("claude", tmp_path) == (
        tmp_path / ".claude" / "skills" / "syntopica"
    )
    assert client_skill_directory("codex", tmp_path) == tmp_path / ".codex" / "skills" / "syntopica"
