"""The component menu: what each one needs and which checkouts it brings."""

from collections.abc import Mapping
from types import MappingProxyType

from syntopica.component import Component

COMPONENTS: Mapping[str, Component] = MappingProxyType(
    {
        "brain": Component(requires=(), engines=("brain",)),
        "clips": Component(requires=("brain",), engines=("clips",)),
        # atrium indexes the archive that the agents transport exports.
        "atrium": Component(requires=("brain",), engines=("atrium", "agents")),
    }
)

ENGINE_ORDER: tuple[str, ...] = ("brain", "clips", "atrium", "agents")
