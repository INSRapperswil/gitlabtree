"""
GitLabTree CLI tool
"""

import typer

from urllib.parse import quote
from rich.console import Console

from .rich_helper import error, render_tree
from .gitlab_helper import GitLabHelper
from .visibility_helper import VisibilityHelper
from .runner_helper import get_tree_with_runner

console = Console()
error_console = Console()

app = typer.Typer()


@app.callback()
def callback(
    ctx: typer.Context,
    api_url: str = typer.Option(
        "https://gitlab.ost.ch/api/v4", help="GitLab API URL", envvar="GITLAB_API"
    ),
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
    ctx: typer.Context,
) -> None:
    """
    Show granted permissions

    Starting at a group level and traveling down to the repositories
    """
    type(ctx.obj)
    error_console.print(error("Not implemented yet. But coming soon :soon: :smirk:"))
    raise typer.Exit(1)


@app.command()
def pipeline(
    ctx: typer.Context,
) -> None:
    """
    Show the status of the last pipeline run for each project

    Starting at a group level and traveling down to the repositories
    """
    type(ctx.obj)
    error_console.print(error("Not implemented yet. But coming soon :soon: :smirk:"))
    raise typer.Exit(1)


@app.command()
def visibility(
    ctx: typer.Context,
) -> None:
    """
    Show the visibility of each project and group

    Starting at a group level traveling down to the repositories and
    showing the visibility (public, intern, private)
    """
    visibilityhelper = VisibilityHelper(gitlab=ctx.obj)
    visibilityhelper.get_projects("ins-stud")
    groups = visibilityhelper.get_groups("ins-stud")
    console.print(render_tree(groups))

    raise typer.Exit(0)


@app.command()
def runners(
    ctx: typer.Context, start: str = typer.Argument(..., help="Group to start the tree")
) -> None:
    """
    Show the available runner

    Starting at a group level and traveling down to the repositories
    """
    tree = get_tree_with_runner(gitlab=ctx.obj, start=quote(start, safe=""))
    console.print(render_tree(tree))
    raise typer.Exit(0)
