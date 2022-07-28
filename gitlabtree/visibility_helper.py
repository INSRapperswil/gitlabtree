"""
Visibility Helper to get visibility information from GitLabAPI for projects and groups
"""
from typing import Any, List

from gitlabtree.models import Group, Repository, VisibilityInfo


class VisibilityHelper:
    """
    Visibility helper to get visibility for projects and groups
    """

    def __init__(self, gitlab) -> None:
        self.gitlab = gitlab
        self.projects: List = []
        self.groups: List = []
        self.subgroups: List = []

    def get_projects(self, group) -> Any:
        """
        get all projects for group
        """
        self.projects = self.gitlab.get(
            f"groups/{group}/projects?include_subgroups=true"
        )
        return self.projects

    def get_groups(self, group) -> Any:
        """
        get all groups
        """
        self.groups = self.gitlab.get(f"groups/{group}")
        self.subgroups = self.gitlab.get(f"groups/{group}/descendant_groups")

        top = Group(name=self.groups["name"])
        _id_groups = {self.groups["id"]: top}
        for group in sorted(self.subgroups, key=lambda i: i["full_path"]):
            g = Group(
                name=group["name"], info=[VisibilityInfo(text=group["visibility"])]
            )
            _id_groups[group["parent_id"]].groups.append(g)
            _id_groups[group["id"]] = g

        for project in self.projects:
            p = Repository(
                name=project["name"], info=[VisibilityInfo(text=project["visibility"])]
            )
            parent = project["namespace"]["id"]
            _id_groups[parent].repositories.append(p)

        return top
