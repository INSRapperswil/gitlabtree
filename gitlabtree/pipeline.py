"""
Helper functions for the pipeline cli subcommand
"""
from typing import Dict, Any, List

from .gitlab_helper import GitLabHelper
from .models import Group, Info
from .tree_helper import TreeHelper
from .rich_helper import info_panel


def create_pipeline_info(data: Dict[str, Any], gitlab: GitLabHelper) -> List[Info]:
    """Function to pass onto the Tree helper to create the PipelineInfo for each project

    Args:
        data (Dict[str, Any]): Project data from the API
        gitlab (GitLabHelper): GitLab Helper to make projects/<id>/pipeline get

    Returns:
        List[Info]: List of Pipeline objects
    """
    pipeline_data = gitlab.get(
        f"projects/{data['id']}/pipelines?ref={data['default_branch']}&order_by=updated_at&per_page=1"
    )
    info: List[Info] = []
    if pipeline_data:
        pipeline = pipeline_data[0]
        panel = info_panel(
            f"[link={pipeline['web_url']}]{pipeline['ref']} {pipeline['status']} {pipeline['updated_at']}[/link]",
            title=pipeline["ref"],
            style="green" if pipeline["status"] == "success" else "red",
            width=50,
        )
        info.append(
            Info(
                text=f"{pipeline['ref']} {pipeline['status']} {pipeline['updated_at']}",
                renderable=panel,
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
