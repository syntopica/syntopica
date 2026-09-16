"""Assemble syntopica.config.json for a component set, with schema defaults spelled out."""

from syntopica.engines_for_components import engines_for_components


def build_config_document(components: tuple[str, ...], engines_relative: str) -> dict[str, object]:
    """Return the document; every path is relative to the file that will hold it."""
    engines = {
        name: {"path": f"{engines_relative}/{name}", "apiVersion": 1}
        for name in engines_for_components(components)
    }
    document: dict[str, object] = {
        "schemaVersion": 1,
        "instanceId": "mine",
        "brain": {
            "pages": ["pages"],
            "sources": "sources",
            "index": "index.md",
            "ledger": ".ingest",
        },
        "engines": engines,
    }
    if "clips" in components:
        document["clips"] = {"archive": "clips", "inbox": None, "inboxRepositoryUrl": None}
        # Which model runs each stage is the person's decision; null means
        # "not chosen yet", and the clips doctor names it.
        document["runners"] = {
            "synthesis": None,
            "grade": None,
            "triage": None,
            "triageRefiner": None,
        }
    if "atrium" in components:
        document["atrium"] = {"path": "atrium"}
        document["conversations"] = {"path": "conversations"}
    return document
