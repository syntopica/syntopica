"""The configuration schema is the brain engine's; the hub never carries a copy."""

import json
from pathlib import Path
from typing import cast


def read_engine_schema(brain_checkout: Path) -> dict[str, object]:
    """Read schema/syntopica-config.schema.json from the checkout."""
    path = brain_checkout / "schema" / "syntopica-config.schema.json"
    if not path.is_file():
        raise FileNotFoundError(f"no schema at {path}; is {brain_checkout} a brain checkout?")
    return cast(dict[str, object], json.loads(path.read_text(encoding="utf-8")))
