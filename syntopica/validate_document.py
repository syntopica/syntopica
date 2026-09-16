"""Validate a document against the engine schema and report one readable error."""

from collections.abc import Mapping

from jsonschema import Draft202012Validator


def validate_document(document: Mapping[str, object], schema: Mapping[str, object]) -> None:
    """Raise ValueError with the JSON path and message of the first error."""
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(document), key=lambda error: list(error.path))
    if errors:
        first = errors[0]
        location = "/".join(str(part) for part in first.path) or "configuration"
        raise ValueError(f"{location}: {first.message}")
