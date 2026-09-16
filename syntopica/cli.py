"""Command-line entry point: init, doctor and client."""

from __future__ import annotations

import argparse
import sys

from syntopica.version import package_version


def main(argv: list[str] | None = None) -> int:
    """Parse the command line and dispatch to one command."""
    parser = argparse.ArgumentParser(prog="syntopica", description=__doc__)
    parser.add_argument("--version", action="version", version=f"syntopica {package_version()}")
    commands = parser.add_subparsers(dest="command", required=True)

    init = commands.add_parser("init", help="write syntopica.config.json for the chosen components")
    init.add_argument(
        "--with", dest="components", required=True, help="comma-separated: brain,clips,atrium"
    )
    init.add_argument("--data", default=".", help="the data directory (default: current directory)")
    init.add_argument(
        "--engines", default="engines", help="where the engine checkouts live, relative to --data"
    )

    doctor = commands.add_parser("doctor", help="run every selected engine's doctor")
    doctor.add_argument("--data", default=None)

    client = commands.add_parser("client", help="install the skill and register the MCP server")
    client.add_argument("name", choices=("claude", "codex"))
    client.add_argument("--data", default=None)

    args = parser.parse_args(argv)
    # Lazy on purpose: --version and --help never load a command's dependencies.
    if args.command == "init":
        from syntopica.run_init import run_init

        return run_init(args.components, args.data, args.engines)
    if args.command == "doctor":
        from syntopica.run_doctor import run_doctor

        return run_doctor(args.data)
    from syntopica.run_client import run_client

    return run_client(args.name, args.data)


if __name__ == "__main__":
    sys.exit(main())
