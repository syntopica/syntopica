"""The entry point answers --version without touching any instance."""

import pytest

from syntopica.cli import main


def test_version_flag_prints_the_package_version(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as raised:
        main(["--version"])
    assert raised.value.code == 0
    assert capsys.readouterr().out.strip().startswith("syntopica 0.")


def test_no_command_is_usage_error() -> None:
    with pytest.raises(SystemExit) as raised:
        main([])
    assert raised.value.code == 2
