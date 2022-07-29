"""
Pydantic models with __rich__ for easy printing with rich
"""
from typing import List
from pydantic import BaseModel
from rich.panel import Panel
from rich.console import RenderableType


class Info(BaseModel):
    """
    Object to link to repositories or groups
    """

    text: str

    def __rich__(self) -> RenderableType:
        return Panel(self.text, style="blue", width=30)


class Repository(BaseModel):
    """
    Object representing a repository
    """

    name: str
    info: List[Info] = []

    def __rich__(self) -> str:
        return f":book: {self.name}"


class Group(BaseModel):
    """
    Object representing a group
    """

    name: str
    groups: List["Group"] = []
    repositories: List[Repository] = []
    info: List[Info] = []

    def __rich__(self) -> str:
        return f":open_file_folder: {self.name}"


class PermissionInfo(Info):
    """
    Derived info object with specific rich rendering
    """

    text: str

    def __rich__(self) -> RenderableType:
        return f"{self.text}"  # ToDo: Implement


class PipelineInfo(Info):
    """
    Derived info object with specific rich rendering
    """

    text: str

    def __rich__(self) -> RenderableType:
        return f"{self.text}"  # ToDo: Implement


class VisibilityInfo(Info):
    """
    Derived info object with specific rich rendering
    """

    text: str

    def __rich__(self) -> RenderableType:
        return f"{self.text}"  # ToDo: Implement


class RunnerInfo(Info):
    """
    Derived info object with specific rich rendering
    """

    text: str
    active: bool
    is_shared: bool

    def __rich__(self) -> RenderableType:
        style = "red" if self.is_shared else "yellow"
        title = "active" if self.active else "passive"
        return Panel(
            f"{self.text}", width=40, style=style, title=title, title_align="left"
        )
