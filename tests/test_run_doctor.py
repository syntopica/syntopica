import json
import stat
from pathlib import Path

import pytest

from syntopica.run_doctor import run_doctor


def _fake_engine(engines: Path, name: str, relative: str, body: str) -> None:
    script = engines / name / relative
    script.parent.mkdir(parents=True, exist_ok=True)
    (engines / name / ".git").mkdir(parents=True, exist_ok=True)
    script.write_text("#!/bin/sh\n" + body)
    script.chmod(script.stat().st_mode | stat.S_IXUSR)


def _instance(tmp_path: Path, document: dict[str, object]) -> Path:
    data = tmp_path / "data"
    data.mkdir()
    (data / "syntopica.config.json").write_text(json.dumps(document))
    return data


@pytest.fixture
def quiet_clients(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setattr("syntopica.run_doctor.mcp_server_listed", lambda client, run: False)


def test_all_selected_engines_pass(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], quiet_clients: None
) -> None:
    engines = tmp_path / "engines"
    _fake_engine(engines, "brain", "bin/brain", 'echo "PASS configuration: valid"\n')
    _fake_engine(engines, "clips", "clips.sh", 'echo "PASS paths: all present"\n')
    data = _instance(
        tmp_path,
        {
            "brain": {},
            "clips": {},
            "engines": {
                "brain": {"path": "../engines/brain"},
                "clips": {"path": "../engines/clips"},
            },
        },
    )
    assert run_doctor(str(data)) == 0
    out = capsys.readouterr().out
    assert "== brain ==" in out and "== clips ==" in out
    assert "PASS brain doctor" in out and "PASS clips doctor" in out
    assert "INFO claude skill: not installed" in out


def test_one_failing_engine_fails_the_run(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], quiet_clients: None
) -> None:
    engines = tmp_path / "engines"
    _fake_engine(engines, "brain", "bin/brain", 'echo "FAIL paths: 1 missing (pages)"; exit 1\n')
    data = _instance(tmp_path, {"brain": {}, "engines": {"brain": {"path": "../engines/brain"}}})
    assert run_doctor(str(data)) == 1
    out = capsys.readouterr().out
    assert "FAIL paths: 1 missing (pages)" in out and "FAIL brain doctor" in out


def test_missing_checkout_is_named(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], quiet_clients: None
) -> None:
    data = _instance(tmp_path, {"brain": {}, "engines": {"brain": {"path": "../engines/brain"}}})
    assert run_doctor(str(data)) == 1
    assert "FAIL brain checkout missing" in capsys.readouterr().out


def test_atrium_reports_the_agents_checkout_and_mcp(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    engines = tmp_path / "engines"
    _fake_engine(engines, "brain", "bin/brain", "echo PASS\n")
    _fake_engine(engines, "atrium", "unused", "")
    (engines / "agents" / ".git").mkdir(parents=True)
    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    uv = fake_bin / "uv"
    uv.write_text('#!/bin/sh\necho "PASS index: reachable"\n')
    uv.chmod(uv.stat().st_mode | stat.S_IXUSR)
    monkeypatch.setenv("PATH", f"{fake_bin}:{tmp_path}")
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setattr(
        "syntopica.run_doctor.mcp_server_listed", lambda client, run: client == "codex"
    )
    data = _instance(
        tmp_path,
        {
            "brain": {},
            "atrium": {},
            "conversations": {},
            "engines": {
                "brain": {"path": "../engines/brain"},
                "atrium": {"path": "../engines/atrium"},
                "agents": {"path": "../engines/agents"},
            },
        },
    )
    assert run_doctor(str(data)) == 0
    out = capsys.readouterr().out
    assert "PASS atrium doctor" in out and "PASS agents checkout present" in out
    assert "INFO codex mcp atrium: registered" in out
    assert "INFO claude mcp atrium: not registered" in out


def test_no_instance_is_reported(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("SYNTOPICA_DATA", raising=False)
    assert run_doctor(None) == 1
    assert "no syntopica.config.json" in capsys.readouterr().err
