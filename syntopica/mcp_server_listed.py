"""Ask a client whether the atrium server is already registered."""

from collections.abc import Callable


def mcp_server_listed(client: str, run: Callable[[tuple[str, ...]], str]) -> bool:
    """True when a line of `<client> mcp list` names atrium."""
    output = run((client, "mcp", "list"))
    return any(line.strip().startswith("atrium") for line in output.splitlines())
