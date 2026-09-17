"""doctor: every selected engine's own doctor, then how the clients see the instance."""

import os
import sys
from pathlib import Path
from typing import cast

from syntopica.client_skill_directory import client_skill_directory
from syntopica.engine_doctor_command import engine_doctor_command
from syntopica.engines_for_components import engines_for_components
from syntopica.find_data_directory import find_data_directory
from syntopica.mcp_server_status import mcp_server_status
from syntopica.read_config_document import read_config_document
from syntopica.run_client_command import run_client_command
from syntopica.run_engine_doctor import run_engine_doctor
from syntopica.selected_components import selected_components

CLIENTS = ("claude", "codex")
STATUS_REPORT = {
    "matches": "registered for this instance",
    "conflict": "registered for another instance or checkout",
    "absent": "not registered",
}


def run_doctor(data: str | None) -> int:
    """Print per-engine output and a summary; exit 1 if any selected engine fails."""
    try:
        root = find_data_directory(data, os.environ, Path.cwd())
    except FileNotFoundError as error:
        print(f"doctor: {error}", file=sys.stderr)
        return 1
    document = read_config_document(root)
    engines = cast(dict[str, dict[str, str]], document.get("engines", {}))
    components = selected_components(document)
    summary: list[tuple[bool, str]] = []
    for name in engines_for_components(components):
        checkout = (root / engines[name]["path"]).resolve()
        if not (checkout / ".git").exists():
            summary.append((False, f"{name} checkout missing ({checkout})"))
            continue
        if name == "agents":
            summary.append((True, "agents checkout present"))
            continue
        print(f"== {name} ==")
        passed, output = run_engine_doctor(
            engine_doctor_command(name, checkout), checkout, root, os.environ
        )
        print(output, end="" if output.endswith("\n") else "\n")
        summary.append((passed, f"{name} doctor"))
    print("== summary ==")
    for passed, line in summary:
        print(f"{'PASS' if passed else 'FAIL'} {line}")
    home = Path(os.environ.get("HOME", Path.home()))
    for client in CLIENTS:
        installed = client_skill_directory(client, home).is_dir()
        print(f"INFO {client} skill: {'installed' if installed else 'not installed'}")
        if "atrium" in components:
            checkout = (root / engines["atrium"]["path"]).resolve()
            status = mcp_server_status(client, run_client_command, root, checkout)
            print(f"INFO {client} mcp atrium: {STATUS_REPORT[status]}")
    return int(any(not passed for passed, _ in summary))
