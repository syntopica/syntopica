"""Read the tracked configuration document as written, without overlays."""

import json
from pathlib import Path
from typing import cast


def read_config_document(data: Path) -> dict[str, object]:
    """The hub only needs section presence and engine paths; overlays belong to engines."""
    path = data / "syntopica.config.json"
    return cast(dict[str, object], json.loads(path.read_text(encoding="utf-8")))
