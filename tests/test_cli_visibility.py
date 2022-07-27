from typer.testing import CliRunner

from .fixture_cli import env_gitlab_token
from gitlabtree.main import app

runner = CliRunner()


def test_help() -> None:
    result = runner.invoke(app, ["visibility", "--help"])
    assert result.exit_code == 0
    assert "visibility" in result.stdout
    assert "Show the visibility of for each project and group" in result.stdout
    assert "public, intern, private" in result.stdout


def test_wrong_command() -> None:
    result = runner.invoke(app, ["visibility", "nope"])
    assert result.exit_code == 2
    assert "Got unexpected extra argument (nope)" in result.output


def test_no_command() -> None:
    result = runner.invoke(app, ["visibility"])
    assert result.exit_code == 1
    assert "Not implemented yet. But comming soon" in result.output
