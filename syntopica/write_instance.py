"""Create the directories and files the engines' doctors require, then the config."""

import json
from collections.abc import Mapping
from pathlib import Path
from typing import cast

# The brain engine applies schema defaults for the newsletter paths even when
# that section is absent, and its doctor requires the defaults to exist.
# Creating them for every component set keeps a brain-only doctor green. The
# clip archive is not one of those: since brain stopped requiring it for an
# instance without the engine, creating it left every brain-only wiki with an
# empty `clips/` nobody could explain.
STATE_ENTRIES = ("engines/", "atrium/", "conversations/", "syntopica.local.json")
CONFIG_FILES = {
    "newsletter-accepted.json": "[]\n",
    "newsletter-rejected.json": "[]\n",
    "newsletter-rejected-booking.json": "[]\n",
    "project-aliases.json": "{}\n",
}


def write_instance(data: Path, document: Mapping[str, object]) -> None:
    """Write directories, .config files, .gitignore entries and the document."""
    brain = cast(Mapping[str, object], document["brain"])
    directories = [
        *cast(list[str], brain["pages"]),
        cast(str, brain["sources"]),
        cast(str, brain["ledger"]),
        ".config",
    ]
    clips = document.get("clips")
    if isinstance(clips, Mapping):
        directories.append(cast(str, clips["archive"]))
    for directory in directories:
        (data / directory).mkdir(parents=True, exist_ok=True)
    for name, text in CONFIG_FILES.items():
        target = data / ".config" / name
        if not target.exists():
            target.write_text(text, encoding="utf-8")
    # The index is a required path too; `brain index` rewrites it from the pages.
    index = data / cast(str, brain["index"])
    if not index.exists():
        index.write_text("# Index\n", encoding="utf-8")
    ignore = data / ".gitignore"
    present = ignore.read_text(encoding="utf-8").splitlines() if ignore.exists() else []
    additions = [entry for entry in STATE_ENTRIES if entry not in present]
    if additions:
        with ignore.open("a", encoding="utf-8") as handle:
            handle.write("".join(f"{entry}\n" for entry in additions))
    (data / "syntopica.config.json").write_text(
        json.dumps(document, indent=2) + "\n", encoding="utf-8"
    )
