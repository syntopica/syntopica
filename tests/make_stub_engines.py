"""Stub engine checkouts: repositories with only what the hub reads."""

import shutil
import subprocess
from pathlib import Path

FIXTURE_SCHEMA = Path(__file__).resolve().parent / "fixtures" / "syntopica-config.schema.json"


def make_stub_engines(root: Path, names: tuple[str, ...]) -> Path:
    engines = root / "engines"
    for name in names:
        checkout = engines / name
        checkout.mkdir(parents=True)
        subprocess.run(["git", "init", "-q", "--template=", str(checkout)], check=True)
        if name == "brain":
            (checkout / "schema").mkdir()
            shutil.copy(FIXTURE_SCHEMA, checkout / "schema" / "syntopica-config.schema.json")
    return engines
