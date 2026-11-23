"""The client's own registration command for the atrium server."""

from pathlib import Path


def mcp_add_command(client: str, data: Path, atrium_checkout: Path) -> tuple[str, ...]:
    """Absolute paths only: the server starts from any working directory.

    The name precedes `--env`: Claude Code reads that option as variadic, so a
    name placed after it was taken for a second variable and the registration
    failed with `Invalid environment variable format: atrium`.
    """
    server = ("--", "uv", "run", "--project", str(atrium_checkout), "atrium-mcp")
    registration = ("atrium", "--env", f"SYNTOPICA_DATA={data}", *server)
    if client == "claude":
        return ("claude", "mcp", "add", "--scope", "user", *registration)
    return ("codex", "mcp", "add", *registration)
