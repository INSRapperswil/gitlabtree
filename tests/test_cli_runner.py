from typer.testing import CliRunner

from .fixture_cli import env_gitlab_token
from gitlabtree.main import app

runner = CliRunner()


def test_help() -> None:
    result = runner.invoke(app, ["runner", "--help"])
    assert result.exit_code == 0
    assert "runner" in result.stdout
    assert "Show the available runner" in result.stdout


def test_wrong_command() -> None:
    result = runner.invoke(app, ["pipeline", "nope"])
    assert result.exit_code == 2
    assert "Got unexpected extra argument (nope)" in result.output


def test_no_command() -> None:
    result = runner.invoke(app, ["pipeline"])
    assert result.exit_code == 2
    assert "Missing argument 'START'" in result.output
