"""
Pydantic models with __rich__ for easy printing with rich
"""
from typing import List, Optional
from pydantic import BaseModel, Field
from rich.panel import Panel
from rich.console import RenderableType


class Info(BaseModel):
    """
    Object to link to repositories or groups
    """

    text: str
    renderable: Optional[RenderableType] = Field(None, exclude=True)

    class Config:
        arbitrary_types_allowed = True

    def __rich__(self) -> RenderableType:
        if self.renderable:
            return self.renderable
        return Panel(self.text, style="blue", width=30)

    def __str__(self) -> str:
        return self.text


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
