from typing import List
from pydantic import BaseModel


class Repository(BaseModel):
    name: str

    def __rich__(self) -> str:
        return f":book: {self.name}"


class Group(BaseModel):
    name: str
    groups: List["Group"] = []
    repositories: List[Repository] = []

    def __rich__(self) -> str:
        return f":open_file_folder: {self.name}"
