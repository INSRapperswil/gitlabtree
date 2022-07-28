from typing import Dict, Any, List

from .gitlab_helper import GitLabHelper
from .models import Group, Info, RunnerInfo
from .tree_helper import TreeHelper


def create_runner_info(data: Dict[str, Any], gitlab: GitLabHelper) -> List[Info]:
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
    tree_helper = TreeHelper(
        gitlab,
        group_processing=None,
        project_processing=create_runner_info,
    )
    return tree_helper.get_tree(start)
