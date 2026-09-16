"""One installable component and what it brings."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Component:
    """A menu entry: the components it requires and the engine checkouts it needs."""

    requires: tuple[str, ...]
    engines: tuple[str, ...]
