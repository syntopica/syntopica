from syntopica.selected_components import selected_components


def test_brain_only() -> None:
    assert selected_components({"brain": {}, "engines": {"brain": {}}}) == ("brain",)


def test_clips_needs_section_and_engine() -> None:
    assert selected_components({"clips": {"archive": "clips"}, "engines": {"brain": {}}}) == (
        "brain",
    )
    assert selected_components(
        {"clips": {"archive": "clips"}, "engines": {"brain": {}, "clips": {}}}
    ) == ("brain", "clips")


def test_atrium_needs_both_state_sections() -> None:
    assert selected_components({"atrium": {}, "engines": {"brain": {}}}) == ("brain",)
    assert selected_components(
        {"atrium": {}, "conversations": {}, "engines": {"brain": {}, "atrium": {}}}
    ) == ("brain", "atrium")
