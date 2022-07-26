from typing import List, Optional
from pydantic import BaseModel


class Repository(BaseModel):
    name: str


class Group(BaseModel):
    name: str
    groups: Optional[List["Group"]]
    repositories: Optional[List[Repository]]
