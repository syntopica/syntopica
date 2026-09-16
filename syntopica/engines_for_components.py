"""The checkouts a component set needs, in the fixed engine order."""

from syntopica.components import COMPONENTS, ENGINE_ORDER


def engines_for_components(components: tuple[str, ...]) -> tuple[str, ...]:
    """Union of every selected component's engines, ordered."""
    wanted = {engine for name in components for engine in COMPONENTS[name].engines}
    return tuple(engine for engine in ENGINE_ORDER if engine in wanted)
