"""Copy the packaged skill into a client's skills directory, marking it as ours."""

import shutil
from importlib.resources import as_file, files
from pathlib import Path

MARKER = ".syntopica-hub"


def install_skill(target: Path, version: str) -> str:
    """Return 'installed' or 'updated'; refuse a directory without our marker."""
    existed = target.exists()
    if existed and not (target / MARKER).is_file():
        raise FileExistsError(f"{target} exists and was not written by syntopica client")
    with as_file(files("syntopica").joinpath("skills/syntopica")) as source:
        if existed:
            shutil.rmtree(target)
        shutil.copytree(source, target)
    (target / MARKER).write_text(f"{version}\n", encoding="utf-8")
    return "updated" if existed else "installed"
