import json
import plistlib
import subprocess
from pathlib import Path

import pytest

from syntopica.run_schedule import run_schedule


def _instance(tmp_path: Path, engines: dict[str, dict[str, str]], **sections: object) -> Path:
    data = tmp_path / "my data"
    data.mkdir()
    document = {"brain": {}, "engines": engines, **sections}
    (data / "syntopica.config.json").write_text(json.dumps(document))
    return data


def test_both_jobs_are_written_with_absolute_paths_and_loaded(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    engines = {name: {"path": f"engines/{name}"} for name in ("brain", "atrium", "scribe")}
    data = _instance(tmp_path, engines, atrium={}, conversations={})
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setattr("sys.platform", "darwin")
    calls: list[tuple[str, ...]] = []

    def run(argv: tuple[str, ...]) -> subprocess.CompletedProcess[str]:
        calls.append(argv)
        return subprocess.CompletedProcess(argv, 0, "", "")

    monkeypatch.setattr("syntopica.run_schedule.run_client_command", run)
    assert run_schedule(str(data)) == 0
    agents = tmp_path / "home" / "Library" / "LaunchAgents"
    refresh = plistlib.loads((agents / "dev.syntopica.atrium-refresh.plist").read_bytes())
    context = plistlib.loads((agents / "dev.syntopica.atrium-context.plist").read_bytes())
    checkout = data.resolve() / "engines" / "atrium"
    # The data directory has a space in it: the shell line must survive that.
    assert refresh["ProgramArguments"][2] == f"exec '{checkout}/bin/atrium-refresh'"
    assert refresh["EnvironmentVariables"] == {
        "SYNTOPICA_DATA": str(data.resolve()),
        "SCRIBE_CHECKOUT": str(data.resolve() / "engines" / "scribe"),
    }
    assert context["ProgramArguments"] == [f"{checkout}/bin/atrium", "serve-context"]
    assert (data / "atrium").is_dir()
    assert [argv[1] for argv in calls] == ["bootout", "bootstrap", "bootout", "bootstrap"]
    assert capsys.readouterr().out.count("loaded dev.syntopica.atrium-") == 2


def test_an_instance_without_atrium_is_refused(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], monkeypatch: pytest.MonkeyPatch
) -> None:
    data = _instance(tmp_path, {"brain": {"path": "engines/brain"}})
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setattr("sys.platform", "darwin")
    assert run_schedule(str(data)) == 1
    assert "no atrium component" in capsys.readouterr().err
    assert not (tmp_path / "home" / "Library").exists()
