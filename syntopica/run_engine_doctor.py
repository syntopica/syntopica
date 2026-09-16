"""Run one engine doctor and return whether it passed and what it said."""

import subprocess
from collections.abc import Mapping
from pathlib import Path


def run_engine_doctor(
    command: tuple[str, ...], checkout: Path, data: Path, environ: Mapping[str, str]
) -> tuple[bool, str]:
    """Never raise: a doctor that cannot start is a failing doctor with a reason."""
    env = {**environ, "SYNTOPICA_DATA": str(data)}
    try:
        result = subprocess.run(  # noqa: S603 -- argv from the engine table, no shell
            command, cwd=checkout, env=env, capture_output=True, text=True, check=False
        )
    except OSError as error:
        return False, f"cannot run {command[0]}: {error}"
    return result.returncode == 0, result.stdout + result.stderr
