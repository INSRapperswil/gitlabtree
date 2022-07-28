from typing import Any, Dict, List, Tuple, Callable, Optional

from gitlabtree.models import Group, Repository, Info
from .gitlab_helper import GitLabHelper


class TreeHelper:
    def __init__(
        self,
        gitlab: GitLabHelper,
        group_processing: Optional[
            Callable[[Dict[str, Any], GitLabHelper], List[Info]]
        ] = None,
        project_processing: Optional[
            Callable[[Dict[str, Any], GitLabHelper], List[Info]]
        ] = None,
    ) -> None:
        self.gitlab = gitlab
        self.group_processing = group_processing
        self.project_processing = project_processing

    def get_data(
        self, start: str
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]], List[Dict[str, Any]]]:
        top = self.gitlab.get(f"groups/{start}")
        groups = self.gitlab.get(f"groups/{start}/descendant_groups")
        projects = self.gitlab.get(f"groups/{start}/projects?include_subgroups=true")
        return (top, groups, projects)

    def create_tree(
        self,
        root_group: Dict[str, Any],
        descendat_groups: List[Dict[str, Any]],
        projects: List[Dict[str, Any]],
    ) -> Group:

        # Temporary dict to map group ID to group object
        _tmp_groups: Dict[int, Group] = {}

        top = Group(name=root_group["name"])
        _tmp_groups[root_group["id"]] = top

        for group_data in sorted(descendat_groups, key=lambda i: str(i["full_path"])):
            group = Group(name=group_data["name"])
            if self.group_processing:
                group_info = self.group_processing(group_data, self.gitlab)
                group.info.extend(group_info)
            _tmp_groups[group_data["parent_id"]].groups.append(group)
            _tmp_groups[group_data["id"]] = group

        for project_data in projects:
            repository = Repository(name=project_data["name"])
            if self.project_processing:
                repository_info = self.project_processing(project_data, self.gitlab)
                repository.info.extend(repository_info)
            parent = project_data["namespace"]["id"]
            _tmp_groups[parent].repositories.append(repository)

        return top

    def get_tree(
        self,
        start: str,
    ) -> Group:
        top, groups, projects = self.get_data(start)
        return self.create_tree(top, groups, projects)
