"""Select the instance the way the engines do: explicit, environment, bounded walk."""

from collections.abc import Mapping
from pathlib import Path


def find_data_directory(explicit: str | None, environ: Mapping[str, str], start: Path) -> Path:
    """Return the directory holding syntopica.config.json, never crossing a .git."""
    start = start.resolve()
    selected = explicit if explicit is not None else environ.get("SYNTOPICA_DATA")
    if selected is not None:
        candidate = (start / selected).resolve()
        if (candidate / "syntopica.config.json").is_file():
            return candidate
        raise FileNotFoundError(f"no syntopica.config.json in {candidate}")
    for candidate in (start, *start.parents):
        if (candidate / "syntopica.config.json").is_file():
            return candidate
        if (candidate / ".git").exists():
            break
    raise FileNotFoundError(f"no syntopica.config.json found walking upward from {start}")
