"""The launchd jobs that keep an atrium instance fresh and its context resident."""

import shlex
from pathlib import Path


def launch_agents(data: Path, atrium: Path, scribe: Path) -> dict[str, dict[str, object]]:
    """Return each job's property list by label; every path in it is absolute.

    The refresh runs through a login shell because launchd starts jobs with a
    bare PATH and the export needs the person's own pnpm and node. The label is
    the name the session-end hook in the atrium checkout kicks, so it is fixed.
    """
    state = data / "atrium"
    return {
        "dev.syntopica.atrium-refresh": {
            "Label": "dev.syntopica.atrium-refresh",
            "ProgramArguments": [
                "/bin/zsh",
                "-lc",
                f"exec {shlex.quote(str(atrium / 'bin' / 'atrium-refresh'))}",
            ],
            "EnvironmentVariables": {"SYNTOPICA_DATA": str(data), "SCRIBE_CHECKOUT": str(scribe)},
            "StartInterval": 3600,
            "RunAtLoad": False,
            "Nice": 10,
            "StandardOutPath": str(state / "refresh.launchd.log"),
            "StandardErrorPath": str(state / "refresh.launchd.log"),
        },
        "dev.syntopica.atrium-context": {
            "Label": "dev.syntopica.atrium-context",
            "ProgramArguments": [str(atrium / "bin" / "atrium"), "serve-context"],
            "EnvironmentVariables": {"SYNTOPICA_DATA": str(data)},
            "RunAtLoad": True,
            "KeepAlive": {"SuccessfulExit": False},
            "ThrottleInterval": 30,
            "StandardOutPath": str(state / "context-service.log"),
            "StandardErrorPath": str(state / "context-service.log"),
        },
    }
