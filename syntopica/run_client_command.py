"""Run one of the agent clients' own commands and return what it printed."""

import subprocess


def run_client_command(argv: tuple[str, ...]) -> str:
    """A client binary that is not installed reads as empty output, not a crash."""
    try:
        return subprocess.run(argv, capture_output=True, text=True, check=False).stdout
    except OSError:
        return ""
