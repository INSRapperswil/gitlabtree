from typer.testing import CliRunner

from gitlabtree.main import app

runner = CliRunner()


def test_help() -> None:
    result = runner.invoke(app, ["pipeline", "--help"])
    assert result.exit_code == 0
    assert "pipeline" in result.stdout
    assert "last pipeline run" in result.stdout


def test_wrong_command() -> None:
    result = runner.invoke(app, ["pipeline", "nope"])
    assert result.exit_code == 2
    assert "Got unexpected extra argument (nope)" in result.output


def test_no_command() -> None:
    result = runner.invoke(app, ["pipeline"])
    assert result.exit_code == 1
    assert "Not implemented yet. But comming soon" in result.output
