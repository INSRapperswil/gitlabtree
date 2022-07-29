"""
Helper functions for the runners cli subcommand
"""
from typing import Dict, Any, List

from .gitlab_helper import GitLabHelper
from .models import Group, Info, PermissionInfo
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

    for member in permission_data:
        info.append(
            PermissionInfo(
                text=member["name"],
                user=member["username"],
                url=member["web_url"],
            )
        )
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
