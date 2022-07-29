"""
GitLabTree CLI tool
"""

import typer

from urllib.parse import quote

from requests.exceptions import RequestException
from rich.console import Console

from .rich_helper import error, render_tree
from .gitlab_helper import GitLabHelper
from .visibility import get_tree_with_visibility
from .runner import get_tree_with_runner
from .pipeline import get_tree_with_pipeline
from .permissions import get_tree_with_permissions

console = Console()
error_console = Console()

app = typer.Typer()


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
) -> None:
    """
    GitLab🌲 to get a quick GitLab 🌲-view in your console
    """
    ctx.obj = GitLabHelper(api_url=api_url, token=token)


@app.command()
def permissions(
    ctx: typer.Context, start: str = typer.Argument(..., help="Group to start the tree")
) -> None:
    """
    Show granted permissions

    Starting at a group level and traveling down to the repositories
    """
    try:
        with console.status("Loading...", spinner="monkey"):
            tree = get_tree_with_permissions(
                gitlab=ctx.obj, start=quote(start, safe="")
            )
        with console.pager():
            console.print(render_tree(tree))
        raise typer.Exit(0)
    except RequestException as exc:
        error_console.print(error(str(exc), "API Error"))
        raise typer.Exit(10)


@app.command()
def pipeline(
    ctx: typer.Context, start: str = typer.Argument(..., help="Group to start the tree")
) -> None:
    """
    Show the status of the last pipeline run for each project

    Starting at a group level and traveling down to the repositories
    """
    try:
        with console.status("Loading...", spinner="monkey"):
            tree = get_tree_with_pipeline(gitlab=ctx.obj, start=quote(start, safe=""))
        with console.pager():
            console.print(render_tree(tree))
        raise typer.Exit(0)
    except RequestException as exc:
        error_console.print(error(str(exc), "API Error"))
        raise typer.Exit(10)


@app.command()
def visibility(
    ctx: typer.Context, start: str = typer.Argument(..., help="Group to start the tree")
) -> None:
    """
    Show the visibility of each project and group

    Starting at a group level traveling down to the repositories and
    showing the visibility (public, intern, private)
    """
    try:
        with console.status("Loading...", spinner="monkey"):
            tree = get_tree_with_visibility(gitlab=ctx.obj, start=quote(start, safe=""))
        with console.pager():
            console.print(render_tree(tree))
        raise typer.Exit(0)
    except RequestException as exc:
        error_console.print(error(str(exc), "API Error"))
        raise typer.Exit(10)


@app.command()
def runners(
    ctx: typer.Context, start: str = typer.Argument(..., help="Group to start the tree")
) -> None:
    """
    Show the available runner

    Starting at a group level and traveling down to the repositories
    """
    try:
        with console.status("Loading...", spinner="monkey"):
            tree = get_tree_with_runner(gitlab=ctx.obj, start=quote(start, safe=""))
        with console.pager():
            console.print(render_tree(tree))
        raise typer.Exit(0)
    except RequestException as exc:
        error_console.print(error(str(exc), "API Error"))
        raise typer.Exit(10)
