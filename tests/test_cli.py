from typer.testing import CliRunner

from gitlabtree.main import app

runner = CliRunner()


def test_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "permissions" in result.stdout
    assert "pipeline" in result.stdout
    assert "visibility" in result.stdout


def test_wrong_command() -> None:
    result = runner.invoke(app, ["nope"])
    assert result.exit_code == 2
    assert "No such command 'nope'" in result.output


def test_no_command() -> None:
    result = runner.invoke(app, [])
    assert result.exit_code == 2
    assert "Missing command" in result.output
