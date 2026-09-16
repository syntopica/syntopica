from typing import cast

from syntopica.build_config_document import build_config_document
from syntopica.engines_for_components import engines_for_components


def test_brain_only_names_one_engine() -> None:
    document = build_config_document(("brain",), "engines")
    assert document["engines"] == {"brain": {"path": "engines/brain", "apiVersion": 1}}
    assert "clips" not in document and "atrium" not in document
    assert document["brain"] == {
        "pages": ["pages"],
        "sources": "sources",
        "index": "index.md",
        "ledger": ".ingest",
    }


def test_clips_adds_its_section_engine_and_null_runners() -> None:
    document = build_config_document(("brain", "clips"), "engines")
    engines = cast(dict[str, object], document["engines"])
    assert document["clips"] == {"archive": "clips", "inbox": None, "inboxRepositoryUrl": None}
    assert engines["clips"] == {"path": "engines/clips", "apiVersion": 1}
    assert document["runners"] == {
        "synthesis": None,
        "grade": None,
        "triage": None,
        "triageRefiner": None,
    }


def test_atrium_adds_state_sections_and_two_checkouts() -> None:
    document = build_config_document(("brain", "atrium"), "engines")
    assert document["atrium"] == {"path": "atrium"}
    assert document["conversations"] == {"path": "conversations"}
    assert set(cast(dict[str, object], document["engines"])) == {"brain", "atrium", "agents"}


def test_engines_for_components_is_ordered() -> None:
    assert engines_for_components(("brain", "atrium", "clips")) == (
        "brain",
        "clips",
        "atrium",
        "agents",
    )
