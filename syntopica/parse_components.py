"""Turn the --with argument into an ordered component tuple."""

from syntopica.components import COMPONENTS


def parse_components(spec: str) -> tuple[str, ...]:
    """Validate names, imply brain, and keep menu order."""
    names = [name.strip() for name in spec.split(",")]
    if spec.strip() == "":
        raise ValueError("no component named; choose from " + ", ".join(COMPONENTS))
    unknown = [name for name in names if name not in COMPONENTS]
    if unknown:
        raise ValueError(f"unknown component {unknown[0]!r}; choose from " + ", ".join(COMPONENTS))
    chosen = set(names)
    for name in names:
        chosen.update(COMPONENTS[name].requires)
    return tuple(name for name in COMPONENTS if name in chosen)
