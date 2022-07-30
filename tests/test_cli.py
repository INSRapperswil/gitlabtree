import sys
import subprocess
import pytest
import typer
from typer.testing import CliRunner

from gitlabtree.models import Group

from .fixture_cli import env_gitlab_token
from .fixture_helper import *
from gitlabtree.main import app, Config, _get_tree

runner = CliRunner()


def test_help() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "permissions" in result.stdout
    assert "pipeline" in result.stdout
    assert "visibility" in result.stdout
    assert "runners" in result.stdout


def test_wrong_command() -> None:
    result = runner.invoke(app, ["nope"])
    assert result.exit_code == 2
    assert "No such command 'nope'" in result.output


def test_no_command() -> None:
    result = runner.invoke(app, [])
    assert result.exit_code == 2
    assert "Missing command" in result.output


def test_run_python_module() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "gitlabtree", "--help"], capture_output=True, text=True
    )
    assert result.returncode == 0
    assert "permissions" in result.stdout
    assert "pipeline" in result.stdout
    assert "visibility" in result.stdout


def test_get_tree(gitlab_helper: GitLabHelper) -> None:
    def get_fake_tree(gitlab: GitLabHelper, start: str) -> Group:
        return Group(name="fake")

    config = Config(gitlab=gitlab_helper, pager=False)
    with pytest.raises(typer.Exit) as exc:
        _get_tree("start", config, get_fake_tree)

    assert exc.value.exit_code == 0


def test_get_tree_exceptoin(gitlab_helper: GitLabHelper) -> None:
    def get_fake_tree(gitlab: GitLabHelper, start: str) -> Group:
        from requests.exceptions import HTTPError

        raise HTTPError("Ups")
        return Group(name="fake")

    config = Config(gitlab=gitlab_helper, pager=False)
    with pytest.raises(typer.Exit) as exc:
        _get_tree("start", config, get_fake_tree)

    assert exc.value.exit_code == 10
