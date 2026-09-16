"""client: install the skill; register the atrium server when the instance has it."""

import os
import sys
from pathlib import Path
from typing import cast

from syntopica.client_skill_directory import client_skill_directory
from syntopica.find_data_directory import find_data_directory
from syntopica.install_skill import install_skill
from syntopica.mcp_add_command import mcp_add_command
from syntopica.mcp_server_listed import mcp_server_listed
from syntopica.package_version import package_version
from syntopica.read_config_document import read_config_document
from syntopica.run_client_command import run_client_command
from syntopica.selected_components import selected_components


def run_client(client: str, data: str | None) -> int:
    """Return 0 when the client can use the instance after a restart."""
    try:
        root = find_data_directory(data, os.environ, Path.cwd())
    except FileNotFoundError as error:
        print(f"client: {error}", file=sys.stderr)
        return 1
    home = Path(os.environ.get("HOME", Path.home()))
    target = client_skill_directory(client, home)
    try:
        outcome = install_skill(target, package_version())
    except FileExistsError as error:
        print(f"client: {error}", file=sys.stderr)
        return 1
    print(f"{outcome} skill at {target}")
    document = read_config_document(root)
    if "atrium" in selected_components(document):
        engines = cast(dict[str, dict[str, str]], document["engines"])
        checkout = (root / engines["atrium"]["path"]).resolve()
        if mcp_server_listed(client, run_client_command):
            print(f"{client} mcp atrium: already registered")
        else:
            run_client_command(mcp_add_command(client, root, checkout))
            print(f"registered mcp server atrium for {client} ({checkout})")
    print(f"restart your {client} session so it discovers the skill and any new server")
    return 0
