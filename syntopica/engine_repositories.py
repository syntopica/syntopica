"""Where each engine checkout is cloned from."""

from collections.abc import Mapping
from types import MappingProxyType

ENGINE_REPOSITORIES: Mapping[str, str] = MappingProxyType(
    {
        "brain": "https://github.com/syntopica/brain.git",
        "clips": "https://github.com/syntopica/clips.git",
        "atrium": "https://github.com/syntopica/atrium.git",
        "scribe": "https://github.com/syntopica/scribe.git",
    }
)
