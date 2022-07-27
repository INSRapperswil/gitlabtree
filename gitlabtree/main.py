import typer

from rich.console import Console

from .rich_helper import error
from .gitlab_helper import GitLabHelper

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

    Starting at a group level treveling down to the repositories
    """
    error_console.print(error("Not implemented yet. But comming soon :soon: :smirk:"))
    raise typer.Exit(1)


@app.command()
def pipeline(
    ctx: typer.Context,
) -> None:
    """
    Show the status of the last pipeline run for each project

    Starting at a group level treveling down to the repositories
    """
    error_console.print(error("Not implemented yet. But comming soon :soon: :smirk:"))
    raise typer.Exit(1)


@app.command()
def visibility(
    ctx: typer.Context,
) -> None:
    """
    Show the visibility of for each project and group

    Starting at a group level treveling down to the repositories and showing the visibility (public, intern, private)
    """
    error_console.print(error("Not implemented yet. But comming soon :soon: :smirk:"))
    raise typer.Exit(1)
