from pathlib import Path

import pytest

from syntopica.engine_doctor_command import engine_doctor_command


def test_each_engine_runs_from_its_checkout() -> None:
    checkout = Path("/x")
    assert engine_doctor_command("brain", checkout) == ("/x/bin/brain", "doctor")
    assert engine_doctor_command("clips", checkout) == ("/x/clips.sh", "doctor")
    assert engine_doctor_command("atrium", checkout) == (
        "uv",
        "run",
        "--project",
        "/x",
        "atrium",
        "doctor",
    )


def test_agents_has_no_doctor() -> None:
    with pytest.raises(KeyError):
        engine_doctor_command("agents", Path("/x"))
