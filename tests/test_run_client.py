import json
from pathlib import Path

import pytest

from syntopica.run_client import run_client


def _instance(tmp_path: Path, document: dict[str, object]) -> Path:
    data = tmp_path / "data"
    data.mkdir()
    (data / "syntopica.config.json").write_text(json.dumps(document))
    return data


def test_brain_only_installs_the_skill_and_no_server(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    data = _instance(tmp_path, {"brain": {}, "engines": {"brain": {"path": "engines/brain"}}})
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    calls: list[tuple[str, ...]] = []
    monkeypatch.setattr(
        "syntopica.run_client.run_client_command", lambda argv: calls.append(argv) or ""
    )
    assert run_client("codex", str(data)) == 0
    assert (tmp_path / "home" / ".codex" / "skills" / "syntopica" / "SKILL.md").exists()
    assert calls == []
    out = capsys.readouterr().out
    assert "installed" in out and "restart" in out


def test_atrium_registers_once(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    data = _instance(
        tmp_path,
        {
            "brain": {},
            "atrium": {},
            "conversations": {},
            "engines": {
                "brain": {"path": "engines/brain"},
                "atrium": {"path": "engines/atrium"},
                "agents": {"path": "engines/agents"},
            },
        },
    )
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    calls: list[tuple[str, ...]] = []

    def run_command(argv: tuple[str, ...]) -> str:
        calls.append(argv)
        added = any(call[:3] == ("claude", "mcp", "add") for call in calls[:-1])
        return "atrium: registered\n" if argv[1:3] == ("mcp", "list") and added else ""

    monkeypatch.setattr("syntopica.run_client.run_client_command", run_command)
    assert run_client("claude", str(data)) == 0
    assert calls[0] == ("claude", "mcp", "list")
    assert calls[1][:3] == ("claude", "mcp", "add")
    assert str(data / "engines" / "atrium") in calls[1]
    assert run_client("claude", str(data)) == 0
    assert "already registered" in capsys.readouterr().out
    assert sum(1 for argv in calls if argv[:3] == ("claude", "mcp", "add")) == 1


def test_foreign_skill_directory_stops_the_command(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    data = _instance(tmp_path, {"brain": {}, "engines": {"brain": {"path": "engines/brain"}}})
    home = tmp_path / "home"
    (home / ".claude" / "skills" / "syntopica").mkdir(parents=True)
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setattr("syntopica.run_client.run_client_command", lambda argv: "")
    assert run_client("claude", str(data)) == 1
    assert "not written by" in capsys.readouterr().err
