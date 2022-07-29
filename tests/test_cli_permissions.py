from typer.testing import CliRunner

from .fixture_cli import env_gitlab_token
from gitlabtree.main import app

runner = CliRunner()


def test_help() -> None:
    result = runner.invoke(app, ["permissions", "--help"])
    assert result.exit_code == 0
    assert "permissions" in result.stdout
    assert "Show granted permissions" in result.stdout


def test_no_command() -> None:
    result = runner.invoke(app, ["permissions"])
    assert result.exit_code == 2
    assert "Missing argument 'START'" in result.output
