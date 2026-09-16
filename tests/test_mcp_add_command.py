from pathlib import Path

from syntopica.mcp_add_command import mcp_add_command


def test_claude_registers_at_user_scope_with_absolute_paths() -> None:
    argv = mcp_add_command("claude", Path("/data"), Path("/data/engines/atrium"))
    assert argv == (
        "claude",
        "mcp",
        "add",
        "--scope",
        "user",
        "--env",
        "SYNTOPICA_DATA=/data",
        "atrium",
        "--",
        "uv",
        "run",
        "--project",
        "/data/engines/atrium",
        "atrium-mcp",
    )


def test_codex_has_no_scope_flag() -> None:
    argv = mcp_add_command("codex", Path("/data"), Path("/data/engines/atrium"))
    assert argv == (
        "codex",
        "mcp",
        "add",
        "atrium",
        "--env",
        "SYNTOPICA_DATA=/data",
        "--",
        "uv",
        "run",
        "--project",
        "/data/engines/atrium",
        "atrium-mcp",
    )
