from typer.testing import CliRunner

from .fixture_cli import env_gitlab_token
from gitlabtree.main import app

runner = CliRunner()


def test_help() -> None:
    result = runner.invoke(app, ["pipeline", "--help"])
    assert result.exit_code == 0
    assert "pipeline" in result.stdout
    assert "last pipeline run" in result.stdout


def test_no_command() -> None:
    result = runner.invoke(app, ["pipeline"])
    assert result.exit_code == 2
    assert "Missing argument 'START'" in result.output
