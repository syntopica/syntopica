"""A component is selected when the sections that make it real are present."""

from collections.abc import Mapping
from typing import cast


def selected_components(document: Mapping[str, object]) -> tuple[str, ...]:
    """Brain always; clips with its section and engine; atrium with both state sections."""
    engines = cast(Mapping[str, object], document.get("engines", {}))
    chosen = ["brain"]
    if "clips" in document and "clips" in engines:
        chosen.append("clips")
    if "atrium" in document and "conversations" in document and "atrium" in engines:
        chosen.append("atrium")
    return tuple(chosen)
