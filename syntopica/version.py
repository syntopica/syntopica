"""The installed package version, read from metadata so it is written once."""

from importlib.metadata import PackageNotFoundError, version


def package_version() -> str:
    """Return the distribution version, or a marker when run from a bare checkout."""
    try:
        return version("syntopica")
    except PackageNotFoundError:
        return "0.0.0+unpackaged"
