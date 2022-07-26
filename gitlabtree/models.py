from typing import List
from pydantic import BaseModel
from rich.panel import Panel
from rich.console import RenderableType


class Info(BaseModel):
    text: str

    def __rich__(self) -> RenderableType:
        return Panel(self.text, style="blue", width=30)


class Repository(BaseModel):
    name: str
    info: List[Info] = []

    def __rich__(self) -> str:
        return f":book: {self.name}"


class Group(BaseModel):
    name: str
    groups: List["Group"] = []
    repositories: List[Repository] = []
    info: List[Info] = []

    def __rich__(self) -> str:
        return f":open_file_folder: {self.name}"


class PermissionInfo(Info):
    text: str

    def __rich__(self) -> RenderableType:
        return f"{self.text}"  # ToDo: Implement


class PipelineInfo(Info):
    text: str

    def __rich__(self) -> RenderableType:
        return f"{self.text}"  # ToDo: Implement


class VisibilityInfo(Info):
    text: str

    def __rich__(self) -> RenderableType:
        return f"{self.text}"  # ToDo: Implement
