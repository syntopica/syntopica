import subprocess
from pathlib import Path

from syntopica.mcp_server_status import mcp_server_status

REGISTERED = "atrium:\n  Args: run --project /w/engines/atrium atrium-mcp\n  SYNTOPICA_DATA=/w\n"


def _run(returncode: int, stdout: str = ""):
    return lambda argv: subprocess.CompletedProcess(argv, returncode, stdout, "")


def test_absent_when_the_client_has_no_such_server() -> None:
    assert mcp_server_status("claude", _run(1), Path("/w"), Path("/w/engines/atrium")) == "absent"


def test_matches_this_instance_and_checkout() -> None:
    status = mcp_server_status("claude", _run(0, REGISTERED), Path("/w"), Path("/w/engines/atrium"))
    assert status == "matches"


def test_a_server_for_another_wiki_is_a_conflict() -> None:
    status = mcp_server_status(
        "codex", _run(0, REGISTERED), Path("/other"), Path("/other/engines/atrium")
    )
    assert status == "conflict"
