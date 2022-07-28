"""
Visibility Helper to get visibility information from GitLabAPI for projects and groups
"""
from typing import Any, List, Dict

from .gitlab_helper import GitLabHelper
from .models import Group, Repository, VisibilityInfo


class VisibilityHelper:
    """
    Visibility helper to get visibility for projects and groups
    """

    def __init__(self, gitlab: GitLabHelper) -> None:
        self.gitlab = gitlab
        self.projects: List[Any] = []

    def get_projects(self, group: str) -> None:
        """
        get all projects for group
        """
        self.projects = self.gitlab.get(
            f"groups/{group}/projects?include_subgroups=true"
        )

    def get_groups(self, search_group: str) -> Group:
        """
        get all groups
        """
        groups: Dict[str, Any] = self.gitlab.get(f"groups/{search_group}")
        subgroups: List[Dict[str, Any]] = self.gitlab.get(
            f"groups/{search_group}/descendant_groups"
        )

        top = Group(name=groups["name"])
        _id_groups = {groups["id"]: top}
        for group in sorted(subgroups, key=_get_full_path):
            group_obj = Group(
                name=group["name"], info=[VisibilityInfo(text=group["visibility"])]
            )
            _id_groups[group["parent_id"]].groups.append(group_obj)
            _id_groups[group["id"]] = group_obj

        for project in self.projects:
            project_obj = Repository(
                name=project["name"], info=[VisibilityInfo(text=project["visibility"])]
            )
            parent = project["namespace"]["id"]
            _id_groups[parent].repositories.append(project_obj)

        return top


def _get_full_path(i: Dict[str, Any]) -> str:
    return str(i["full_path"])
