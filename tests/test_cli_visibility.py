from typer.testing import CliRunner

from .fixture_cli import env_gitlab_token
from gitlabtree.main import app

runner = CliRunner()


def test_help() -> None:
    result = runner.invoke(app, ["visibility", "--help"])
    assert result.exit_code == 0
    assert "visibility" in result.stdout
    assert "Show the visibility of each project and group" in result.stdout
    assert "public, intern, private" in result.stdout


def test_no_command() -> None:
    result = runner.invoke(app, ["visibility"])
    assert result.exit_code == 2
    assert "Missing argument 'START'" in result.output
