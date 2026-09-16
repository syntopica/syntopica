"""The component menu: what each one needs and which checkouts it brings."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from types import MappingProxyType


@dataclass(frozen=True)
class Component:
    """One installable component."""

    requires: tuple[str, ...]
    engines: tuple[str, ...]


COMPONENTS: Mapping[str, Component] = MappingProxyType(
    {
        "brain": Component(requires=(), engines=("brain",)),
        "clips": Component(requires=("brain",), engines=("clips",)),
        # atrium indexes the archive that the agents transport exports.
        "atrium": Component(requires=("brain",), engines=("atrium", "agents")),
    }
)

ENGINE_ORDER: tuple[str, ...] = ("brain", "clips", "atrium", "agents")
