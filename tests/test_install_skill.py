from pathlib import Path

import pytest

from syntopica.install_skill import install_skill


def test_installs_with_a_marker(tmp_path: Path) -> None:
    target = tmp_path / "skills" / "syntopica"
    assert install_skill(target, "0.1.0") == "installed"
    assert (target / "SKILL.md").read_text().startswith("---\nname: syntopica")
    assert (target / ".syntopica-hub").read_text() == "0.1.0\n"


def test_updates_its_own_copy(tmp_path: Path) -> None:
    target = tmp_path / "syntopica"
    install_skill(target, "0.1.0")
    (target / "SKILL.md").write_text("stale")
    assert install_skill(target, "0.2.0") == "updated"
    assert "stale" not in (target / "SKILL.md").read_text()
    assert (target / ".syntopica-hub").read_text() == "0.2.0\n"


def test_refuses_a_directory_it_did_not_write(tmp_path: Path) -> None:
    target = tmp_path / "syntopica"
    target.mkdir()
    (target / "SKILL.md").write_text("theirs")
    with pytest.raises(FileExistsError, match="not written by"):
        install_skill(target, "0.1.0")
    assert (target / "SKILL.md").read_text() == "theirs"
