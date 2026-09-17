"""Compare the client's registered atrium server with this instance."""

import subprocess
from collections.abc import Callable
from pathlib import Path

Run = Callable[[tuple[str, ...]], subprocess.CompletedProcess[str]]


def mcp_server_status(client: str, run: Run, data: Path, checkout: Path) -> str:
    """'absent', 'matches' or 'conflict' for the server named atrium.

    A name test alone answered yes for a server pointing at another wiki, and
    an entry merely beginning with `atrium` satisfied it too, so the hub
    reported a connection the client did not have. The registration stores the
    two absolute paths that decide which wiki answers, so both are compared.
    """
    result = run((client, "mcp", "get", "atrium"))
    if result.returncode != 0:
        return "absent"
    registered = result.stdout
    if str(checkout) in registered and f"SYNTOPICA_DATA={data}" in registered:
        return "matches"
    return "conflict"
