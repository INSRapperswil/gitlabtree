"""
Helper functions for the runners cli subcommand
"""
from typing import Dict, Any, List

from .gitlab_helper import GitLabHelper
from .models import Group, Info, RunnerInfo
from .tree_helper import TreeHelper


def create_runner_info(data: Dict[str, Any], gitlab: GitLabHelper) -> List[Info]:
    """Function to pass onto the Tree helper to create the RunnerInfo for each project

    Args:
        data (Dict[str, Any]): Project data from the API
        gitlab (GitLabHelper): GitLab Helper to make projects/<id>/runners get

    Returns:
        List[Info]: List of RunnerInfo objects
    """
    runner_data = gitlab.get(f"projects/{data['id']}/runners")
    info: List[Info] = []
    for runner in runner_data:
        info.append(
            RunnerInfo(
                text=runner["description"],
                active=runner["active"],
                is_shared=runner["is_shared"],
            )
        )
    return info


def get_tree_with_runner(gitlab: GitLabHelper, start: str) -> Group:
    """Function to get the complete tree with the runner information

    Args:
        gitlab (GitLabHelper): GitLab Helper for API calls
        start (str): Name of the group to start building the tree

    Returns:
        Group: Group object with all subgroups and repositories linked
    """
    tree_helper = TreeHelper(
        gitlab,
        group_processing=None,
        project_processing=create_runner_info,
    )
    return tree_helper.get_tree(start)
