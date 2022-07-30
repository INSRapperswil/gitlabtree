"""
Helper functions for the runners cli subcommand
"""
from typing import Dict, Any, List

from rich.table import Table

from .gitlab_helper import GitLabHelper
from .models import Group, Info
from .tree_helper import TreeHelper


def create_permission_info(data: Dict[str, Any], gitlab: GitLabHelper) -> List[Info]:
    """Function to pass onto the Tree helper to create the RunnerInfo for each project

    Args:
        data (Dict[str, Any]): Project data from the API
        gitlab (GitLabHelper): GitLab Helper to make projects/<id>/members get

    Returns:
        List[Info]: List of RunnerInfo objects
    """
    info: List[Info] = []
    kind = "groups" if "parent_id" in data else "projects"
    permission_data = gitlab.get(f"{kind}/{data['id']}/members")

    users = []
    table = Table(title="Permissions")
    table.add_column("Username")
    table.add_column("Name")
    table.add_column("state")
    table.add_column("Access Level")
    table.add_column("Expires at")
    for member in permission_data:
        table.add_row(
            f"[link={member['web_url']}]{member['username']}[/link]",
            member["name"],
            member["state"],
            str(member["access_level"]),
            member["expires_at"],
        )
        users.append(member["username"])
    if users:
        info.append(Info(text=" ".join(users), renderable=table))
    return info


def get_tree_with_permissions(gitlab: GitLabHelper, start: str) -> Group:
    """Function to get the complete tree with the permissions information

    Args:
        gitlab (GitLabHelper): GitLab Helper for API calls
        start (str): Name of the group to start building the tree

    Returns:
        Group: Group object with all subgroups and repositories linked
    """
    tree_helper = TreeHelper(
        gitlab,
        group_processing=create_permission_info,
        project_processing=create_permission_info,
    )
    return tree_helper.get_tree(start)
