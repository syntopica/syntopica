import json
import subprocess
from pathlib import Path

import pytest

from syntopica.run_client import run_client


def _result(
    returncode: int, stdout: str = "", stderr: str = ""
) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess((), returncode, stdout, stderr)


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
        "syntopica.run_client.run_client_command",
        lambda argv: calls.append(argv) or _result(1),
    )
    assert run_client("codex", str(data)) == 0
    assert (tmp_path / "home" / ".codex" / "skills" / "syntopica" / "SKILL.md").exists()
    assert calls == []
    out = capsys.readouterr().out
    assert "installed" in out and "restart" in out


def _atrium_instance(tmp_path: Path) -> Path:
    return _instance(
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

    registration = (
        f"atrium:\n  Args: run --project {data / 'engines' / 'atrium'} atrium-mcp\n"
        f"  Environment:\n    SYNTOPICA_DATA={data}\n"
    )

    def run_command(argv: tuple[str, ...]) -> subprocess.CompletedProcess[str]:
        calls.append(argv)
        added = any(call[:3] == ("claude", "mcp", "add") for call in calls[:-1])
        if argv[1:3] == ("mcp", "get") and added:
            return _result(0, registration)
        return _result(1) if argv[1:3] == ("mcp", "get") else _result(0)

    monkeypatch.setattr("syntopica.run_client.run_client_command", run_command)
    assert run_client("claude", str(data)) == 0
    assert calls[0] == ("claude", "mcp", "get", "atrium")
    assert calls[1][:3] == ("claude", "mcp", "add")
    assert str(data / "engines" / "atrium") in calls[1]
    assert run_client("claude", str(data)) == 0
    assert "already registered for this instance" in capsys.readouterr().out
    assert sum(1 for argv in calls if argv[:3] == ("claude", "mcp", "add")) == 1


def test_a_failing_registration_is_reported(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    data = _atrium_instance(tmp_path)
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setattr(
        "syntopica.run_client.run_client_command",
        lambda argv: _result(1, "", "claude: command not found\n"),
    )
    assert run_client("claude", str(data)) == 1
    assert "mcp add failed" in capsys.readouterr().err


def test_a_silent_registration_failure_is_caught(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    data = _atrium_instance(tmp_path)
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setattr(
        "syntopica.run_client.run_client_command",
        lambda argv: _result(1) if argv[1:3] == ("mcp", "get") else _result(0),
    )
    assert run_client("claude", str(data)) == 1
    assert "reported success but no atrium server" in capsys.readouterr().err


def test_a_server_pointing_elsewhere_is_a_conflict(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    data = _atrium_instance(tmp_path)
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setattr(
        "syntopica.run_client.run_client_command",
        lambda argv: (
            _result(0, "atrium:\n  Environment:\n    SYNTOPICA_DATA=/other/wiki\n")
            if argv[1:3] == ("mcp", "get")
            else _result(0)
        ),
    )
    assert run_client("claude", str(data)) == 1
    assert "another instance" in capsys.readouterr().err


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
