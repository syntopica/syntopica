"""How each engine's doctor is invoked from its own checkout."""

from pathlib import Path


def engine_doctor_command(name: str, checkout: Path) -> tuple[str, ...]:
    """Return argv; the caller sets cwd to the checkout and SYNTOPICA_DATA."""
    commands = {
        "brain": (str(checkout / "bin" / "brain"), "doctor"),
        "clips": (str(checkout / "clips.sh"), "doctor"),
        "atrium": ("uv", "run", "--project", str(checkout), "atrium", "doctor"),
    }
    return commands[name]
