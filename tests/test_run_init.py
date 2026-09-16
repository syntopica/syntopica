import json
from pathlib import Path

import pytest

from syntopica.run_init import run_init
from tests.make_stub_engines import make_stub_engines


def test_brain_only_writes_a_valid_instance(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    make_stub_engines(tmp_path, ("brain",))
    assert run_init("brain", str(tmp_path), "engines") == 0
    document = json.loads((tmp_path / "syntopica.config.json").read_text())
    assert document["engines"] == {"brain": {"path": "engines/brain", "apiVersion": 1}}
    for directory in ("pages", "sources", ".ingest", "clips", ".config"):
        assert (tmp_path / directory).is_dir(), directory
    assert (tmp_path / ".config" / "project-aliases.json").read_text() == "{}\n"
    assert (tmp_path / ".git").is_dir()
    ignored = (tmp_path / ".gitignore").read_text().splitlines()
    assert {"engines/", "atrium/", "conversations/", "syntopica.local.json"} <= set(ignored)
    assert "syntopica doctor" in capsys.readouterr().out


def test_all_components_need_all_four_checkouts(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    make_stub_engines(tmp_path, ("brain", "clips"))
    assert run_init("brain,clips,atrium", str(tmp_path), "engines") == 1
    err = capsys.readouterr().err
    assert "engines/atrium" in err and "engines/agents" in err
    assert "git clone https://github.com/syntopica/atrium.git" in err
    assert not (tmp_path / "syntopica.config.json").exists()


def test_existing_configuration_is_never_overwritten(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    make_stub_engines(tmp_path, ("brain",))
    (tmp_path / "syntopica.config.json").write_text("{}")
    assert run_init("brain", str(tmp_path), "engines") == 1
    assert "already exists" in capsys.readouterr().err
    assert (tmp_path / "syntopica.config.json").read_text() == "{}"


def test_unknown_component_is_reported(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert run_init("brain,capture", str(tmp_path), "engines") == 1
    assert "unknown component 'capture'" in capsys.readouterr().err


def test_document_is_validated_against_the_engine_schema(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    engines = make_stub_engines(tmp_path, ("brain",))
    schema = engines / "brain" / "schema" / "syntopica-config.schema.json"
    schema.write_text(json.dumps({"type": "object", "required": ["nonexistent"]}))
    assert run_init("brain", str(tmp_path), "engines") == 1
    assert "nonexistent" in capsys.readouterr().err
