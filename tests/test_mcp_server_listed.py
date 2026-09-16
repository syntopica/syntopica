from syntopica.mcp_server_listed import mcp_server_listed


def test_detects_the_server_by_name() -> None:
    assert mcp_server_listed("claude", lambda argv: "atrium: uv run ... - Connected\n")
    assert not mcp_server_listed("codex", lambda argv: "other: something\n")


def test_uses_each_client_command() -> None:
    seen: list[tuple[str, ...]] = []

    def run(argv: tuple[str, ...]) -> str:
        seen.append(argv)
        return ""

    mcp_server_listed("codex", run)
    assert seen == [("codex", "mcp", "list")]
