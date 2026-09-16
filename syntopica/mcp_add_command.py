"""The client's own registration command for the atrium server."""

from pathlib import Path


def mcp_add_command(client: str, data: Path, atrium_checkout: Path) -> tuple[str, ...]:
    """Absolute paths only: the server starts from any working directory."""
    server = ("--", "uv", "run", "--project", str(atrium_checkout), "atrium-mcp")
    env = ("--env", f"SYNTOPICA_DATA={data}")
    if client == "claude":
        return ("claude", "mcp", "add", "--scope", "user", *env, "atrium", *server)
    return ("codex", "mcp", "add", "atrium", *env, *server)
