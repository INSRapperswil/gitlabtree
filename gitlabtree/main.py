"""
GitLabTree CLI tool
"""

from typing import Callable, NamedTuple
from urllib.parse import quote

import typer
from requests.exceptions import RequestException
from rich.console import Console

from .models import Group
from .gitlab_helper import GitLabHelper
from .rich_helper import error, render_tree
from .visibility import get_tree_with_visibility
from .runner import get_tree_with_runner
from .pipeline import get_tree_with_pipeline
from .permissions import get_tree_with_permissions

console = Console()
error_console = Console()

app = typer.Typer()


class Config(NamedTuple):
    """
    Settings to store as typer context obj
    """

    gitlab: GitLabHelper
    pager: bool


def _get_tree(
    start: str,
    config: Config,
    get_tree_function: Callable[[GitLabHelper, str], Group],
) -> None:
    try:
        with console.status("Loading...", spinner="monkey"):
            tree = get_tree_function(config.gitlab, quote(start, safe=""))
        if config.pager:
            with console.pager():
                console.print(render_tree(tree))
        else:
            console.print(render_tree(tree))
        raise typer.Exit(0)
    except RequestException as exc:
        error_console.print(error(str(exc), "API Error"))
        raise typer.Exit(10)


@app.callback()
def callback(
    ctx: typer.Context,
    api_url: str = typer.Option(..., help="GitLab API URL", envvar="GITLAB_API"),
    token: str = typer.Option(
        ...,
        help="GitLab API token",
        envvar="GITLAB_TOKEN",
        prompt="GitLab Token",
        hide_input=True,
    ),
    pager: bool = typer.Option(False, help="Using a pager for the output"),
) -> None:
    """
    GitLab🌲 to get a quick GitLab 🌲-view in your console
    """
    ctx.obj = Config(gitlab=GitLabHelper(api_url=api_url, token=token), pager=pager)


@app.command()
def permissions(
    ctx: typer.Context, start: str = typer.Argument(..., help="Group to start the tree")
) -> None:
    """
    Show granted permissions

    Starting at a group level and traveling down to the repositories
    """
    _get_tree(start=start, config=ctx.obj, get_tree_function=get_tree_with_permissions)


@app.command()
def pipeline(
    ctx: typer.Context, start: str = typer.Argument(..., help="Group to start the tree")
) -> None:
    """
    Show the status of the last pipeline run for each project

    Starting at a group level and traveling down to the repositories
    """
    _get_tree(start=start, config=ctx.obj, get_tree_function=get_tree_with_pipeline)


@app.command()
def visibility(
    ctx: typer.Context, start: str = typer.Argument(..., help="Group to start the tree")
) -> None:
    """
    Show the visibility of each project and group

    Starting at a group level traveling down to the repositories and
    showing the visibility (public, intern, private)
    """
    _get_tree(start=start, config=ctx.obj, get_tree_function=get_tree_with_visibility)


@app.command()
def runners(
    ctx: typer.Context, start: str = typer.Argument(..., help="Group to start the tree")
) -> None:
    """
    Show the available runner

    Starting at a group level and traveling down to the repositories
    """
    _get_tree(start=start, config=ctx.obj, get_tree_function=get_tree_with_runner)
