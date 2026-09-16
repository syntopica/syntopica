"""The engines require the data directory to be a Git worktree root."""

import subprocess
from pathlib import Path


def ensure_repository(data: Path) -> bool:
    """Run git init when the directory is not already a repository root."""
    if (data / ".git").exists():
        return False
    subprocess.run(["git", "init", "-q", str(data)], check=True)
    return True
