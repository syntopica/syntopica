"""Run one of the agent clients' own commands and return its full result."""

import subprocess


def run_client_command(argv: tuple[str, ...]) -> subprocess.CompletedProcess[str]:
    """A client binary that is not installed reads as exit 127, not a crash.

    The status and stderr are part of the answer: discarding them let the hub
    print `registered mcp server atrium` after a registration that never ran.
    """
    try:
        return subprocess.run(argv, capture_output=True, text=True, check=False)
    except OSError as error:
        return subprocess.CompletedProcess(argv, 127, "", f"{argv[0]}: {error}\n")
