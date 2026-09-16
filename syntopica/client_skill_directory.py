"""Where each client discovers personal skills."""

from pathlib import Path

CLIENT_DIRECTORIES = {"claude": ".claude", "codex": ".codex"}


def client_skill_directory(client: str, home: Path) -> Path:
    """The documented per-user skills directory, plus this skill's name."""
    return home / CLIENT_DIRECTORIES[client] / "skills" / "syntopica"
