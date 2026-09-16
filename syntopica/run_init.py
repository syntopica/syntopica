"""init: refuse what cannot work, validate against the engine, then write."""

import sys
from pathlib import Path

from syntopica.build_config_document import build_config_document
from syntopica.engine_repositories import ENGINE_REPOSITORIES
from syntopica.engines_for_components import engines_for_components
from syntopica.ensure_repository import ensure_repository
from syntopica.missing_engine_checkouts import missing_engine_checkouts
from syntopica.parse_components import parse_components
from syntopica.read_engine_schema import read_engine_schema
from syntopica.validate_document import validate_document
from syntopica.write_instance import write_instance


def run_init(components: str, data: str, engines: str) -> int:
    """Return 0 after writing syntopica.config.json, 1 with the reason on stderr."""
    root = Path(data).resolve()
    engines_dir = (root / engines).resolve()
    try:
        chosen = parse_components(components)
    except ValueError as error:
        print(f"init: {error}", file=sys.stderr)
        return 1
    if (root / "syntopica.config.json").exists():
        print(f"init: {root / 'syntopica.config.json'} already exists", file=sys.stderr)
        return 1
    missing = missing_engine_checkouts(engines_dir, engines_for_components(chosen))
    if missing:
        for name in missing:
            print(
                f"init: missing checkout {engines}/{name}; run: "
                f"git clone {ENGINE_REPOSITORIES[name]} {engines_dir / name}",
                file=sys.stderr,
            )
        return 1
    document = build_config_document(chosen, engines)
    try:
        validate_document(document, read_engine_schema(engines_dir / "brain"))
    except (FileNotFoundError, ValueError) as error:
        print(f"init: {error}", file=sys.stderr)
        return 1
    root.mkdir(parents=True, exist_ok=True)
    initialised = ensure_repository(root)
    write_instance(root, document)
    print(f"wrote {root / 'syntopica.config.json'} for {', '.join(chosen)}")
    if initialised:
        print(f"initialised a Git repository at {root}")
    print("next: syntopica doctor")
    return 0
