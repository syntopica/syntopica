import pytest

from syntopica.parse_components import parse_components


def test_brain_is_always_first_and_deduplicated() -> None:
    assert parse_components("clips,brain,clips") == ("brain", "clips")


def test_brain_is_implied() -> None:
    assert parse_components("atrium") == ("brain", "atrium")


@pytest.mark.parametrize("spec", ["", "capture", "brain,,clips", "brain, clipper"])
def test_unknown_or_empty_component_is_named(spec: str) -> None:
    with pytest.raises(ValueError, match="unknown component|no component"):
        parse_components(spec)
