import os
import stat
from pathlib import Path

from syntopica.run_engine_doctor import run_engine_doctor


def _script(path: Path, body: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("#!/bin/sh\n" + body)
    path.chmod(path.stat().st_mode | stat.S_IXUSR)
    return path


def test_passing_doctor_reports_output_and_sees_the_instance(tmp_path: Path) -> None:
    script = _script(tmp_path / "engine" / "doctor", 'echo "PASS in $SYNTOPICA_DATA"; pwd\n')
    passed, output = run_engine_doctor(
        (str(script),), tmp_path / "engine", tmp_path / "data", os.environ
    )
    assert passed
    assert f"PASS in {tmp_path / 'data'}" in output
    assert str((tmp_path / "engine").resolve()) in output


def test_failing_doctor_is_reported_with_stderr(tmp_path: Path) -> None:
    script = _script(tmp_path / "engine" / "doctor", 'echo "FAIL paths" >&2; exit 1\n')
    passed, output = run_engine_doctor(
        (str(script),), tmp_path / "engine", tmp_path / "data", os.environ
    )
    assert not passed and "FAIL paths" in output


def test_missing_executable_is_a_failure_not_a_crash(tmp_path: Path) -> None:
    passed, output = run_engine_doctor((str(tmp_path / "absent"),), tmp_path, tmp_path, os.environ)
    assert not passed and "absent" in output
