"""The vendored skill is generic: it names no person, no host, no home path."""

import os
import subprocess
from importlib.resources import files
from pathlib import Path

import pytest


def test_skill_ships_as_package_data() -> None:
    text = files("syntopica").joinpath("skills/syntopica/SKILL.md").read_text(encoding="utf-8")
    assert text.startswith("---\nname: syntopica\n")
    assert "/Users/" not in text and "/home/" not in text


def test_no_personal_identifier_in_tracked_files() -> None:
    patterns = os.environ.get("SYNTOPICA_PERSONAL_DATA_PATTERNS")
    if not patterns:
        pytest.skip("SYNTOPICA_PERSONAL_DATA_PATTERNS is unset")
    root = Path(__file__).resolve().parents[1]
    listed = subprocess.run(
        ["git", "ls-files", "-z"], cwd=root, capture_output=True, text=True, check=True
    )
    tracked = [
        name
        for name in listed.stdout.split("\0")
        if name and name != "LICENSE" and (root / name).is_file()
    ]
    result = subprocess.run(
        ["rg", "-a", "-l", "-i", "-f", patterns, *tracked],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode in (0, 1), result.stderr
    assert result.stdout == "", f"personal identifiers in:\n{result.stdout}"
