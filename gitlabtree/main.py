import typer

from rich.console import Console

from .rich_helper import error

console = Console()
error_console = Console()

app = typer.Typer()


@app.callback()
def callback() -> None:
    """
    GitLab🌲 to get a quick GitLab 🌲-view in your console
    """


@app.command()
def permissions() -> None:
    """
    Show granted permissions

    Starting at a group level treveling down to the repositories
    """
    error_console.print(error("Not implemented yet. But comming soon :soon: :smirk:"))
    raise typer.Exit(1)


@app.command()
def pipeline() -> None:
    """
    Show the status of the last pipeline run for each project

    Starting at a group level treveling down to the repositories
    """
    error_console.print(error("Not implemented yet. But comming soon :soon: :smirk:"))
    raise typer.Exit(1)


@app.command()
def visibility() -> None:
    """
    Show the visibility of for each project and group

    Starting at a group level treveling down to the repositories and showing the visibility (public, intern, private)
    """
    error_console.print(error("Not implemented yet. But comming soon :soon: :smirk:"))
    raise typer.Exit(1)
