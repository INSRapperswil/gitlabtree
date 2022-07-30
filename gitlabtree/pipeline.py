"""
Helper functions for the pipeline cli subcommand
"""
from typing import Dict, Any, List

from .gitlab_helper import GitLabHelper
from .models import Group, Info
from .tree_helper import TreeHelper


def create_pipeline_info(data: Dict[str, Any], gitlab: GitLabHelper) -> List[Info]:
    """Function to pass onto the Tree helper to create the PipelineInfo for each project

    Args:
        data (Dict[str, Any]): Project data from the API
        gitlab (GitLabHelper): GitLab Helper to make projects/<id>/pipeline get

    Returns:
        List[Info]: List of Pipeline objects
    """
    # https://gitlab.ost.ch/api/v4/projects/4662/pipelines?ref=develop&order_by=updated_at&per_page=1
    pipeline_data = gitlab.get(
        f"projects/{data['id']}/pipelines?ref={data['default_branch']}&order_by=updated_at&per_page=1"
    )
    info: List[Info] = []
    if pipeline_data:
        pipeline = pipeline_data[0]
        info.append(
            # PipelineInfo(
            #     text=f"{pipeline['ref']} {pipeline['status']} {pipeline['updated_at']}",
            #     status=pipeline["status"],
            #     url=pipeline["web_url"],
            # )
            Info(
                text=f"{pipeline['ref']} {pipeline['status']} {pipeline['updated_at']}"
            )
        )
    return info


def get_tree_with_pipeline(gitlab: GitLabHelper, start: str) -> Group:
    """Function to get the complete tree with the last pipeline status
       for the default branch

    Args:
        gitlab (GitLabHelper): GitLab Helper for API calls
        start (str): Name of the group to start building the tree

    Returns:
        Group: Group object with all subgroups and repositories linked
    """
    tree_helper = TreeHelper(
        gitlab,
        group_processing=None,
        project_processing=create_pipeline_info,
    )
    return tree_helper.get_tree(start)
