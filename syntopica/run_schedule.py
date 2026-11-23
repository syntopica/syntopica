"""schedule: install the launchd jobs that refresh atrium and serve its context."""

import os
import plistlib
import sys
from pathlib import Path
from typing import cast

from syntopica.find_data_directory import find_data_directory
from syntopica.launch_agents import launch_agents
from syntopica.read_config_document import read_config_document
from syntopica.run_client_command import run_client_command
from syntopica.selected_components import selected_components


def run_schedule(data: str | None) -> int:
    """Return 0 when both jobs are loaded for this instance."""
    try:
        root = find_data_directory(data, os.environ, Path.cwd())
    except FileNotFoundError as error:
        print(f"schedule: {error}", file=sys.stderr)
        return 1
    if sys.platform != "darwin":
        print("schedule: only launchd on macOS is supported", file=sys.stderr)
        return 1
    document = read_config_document(root)
    if "atrium" not in selected_components(document):
        print("schedule: this instance has no atrium component to schedule", file=sys.stderr)
        return 1
    engines = cast(dict[str, dict[str, str]], document["engines"])
    atrium = (root / engines["atrium"]["path"]).resolve()
    scribe = (root / engines["scribe"]["path"]).resolve()
    home = Path(os.environ.get("HOME", Path.home()))
    directory = home / "Library" / "LaunchAgents"
    directory.mkdir(parents=True, exist_ok=True)
    # launchd opens the log paths itself and does not create their directory.
    (root / "atrium").mkdir(exist_ok=True)
    domain = f"gui/{os.getuid()}"
    for label, agent in launch_agents(root, atrium, scribe).items():
        path = directory / f"{label}.plist"
        path.write_bytes(plistlib.dumps(agent))
        # Unloading first makes a rerun pick up a moved instance or checkout;
        # it fails when the job was never loaded, which is the first run.
        run_client_command(("launchctl", "bootout", f"{domain}/{label}"))
        result = run_client_command(("launchctl", "bootstrap", domain, str(path)))
        if result.returncode != 0:
            print(
                f"schedule: launchctl bootstrap failed for {label}\n{result.stderr}",
                end="",
                file=sys.stderr,
            )
            return 1
        print(f"loaded {label} ({path})")
    return 0
