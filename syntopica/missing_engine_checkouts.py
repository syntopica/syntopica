"""Name the engine checkouts that are not where the configuration will point."""

from pathlib import Path


def missing_engine_checkouts(engines_dir: Path, names: tuple[str, ...]) -> tuple[str, ...]:
    """A checkout is present when its directory holds a .git entry."""
    return tuple(name for name in names if not (engines_dir / name / ".git").exists())
