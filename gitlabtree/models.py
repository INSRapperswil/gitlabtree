from typing import List
from pydantic import BaseModel


class Repository(BaseModel):
    name: str


class Group(BaseModel):
    name: str
    groups: List["Group"] = []
    repositories: List[Repository] = []
