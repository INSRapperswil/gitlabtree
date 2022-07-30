"""
Visibility Helper to get visibility information from GitLabAPI for projects and groups
"""
from typing import Any, List, Dict

from .gitlab_helper import GitLabHelper
from .tree_helper import TreeHelper
from .models import Group, Info
from .rich_helper import info_panel


def create_visibility_info(data: Dict[str, Any], gitlab: GitLabHelper) -> List[Info]:
    """Function to pass onto the Tree helper to create the VisibilityInfo for each project

    Args:
        data (Dict[str, Any]): Project data from the API
        gitlab (GitLabHelper): GitLab Helper (no API call needed)

    Returns:
        List[Info]: List of Visibility objects
    """
    info: List[Info] = [
        Info(text=f"{data['visibility']}", renderable=info_panel(data["visibility"]))
    ]
    return info


def get_tree_with_visibility(gitlab: GitLabHelper, start: str) -> Group:
    """Function to get the complete tree with the visibility status

    Args:
        gitlab (GitLabHelper): GitLab Helper for API calls
        start (str): Name of the group to start building the tree

    Returns:
        Group: Group object with all subgroups and repositories linked
    """
    tree_helper = TreeHelper(
        gitlab,
        group_processing=create_visibility_info,
        project_processing=create_visibility_info,
    )
    return tree_helper.get_tree(start)
