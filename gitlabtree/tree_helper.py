"""
Tree Helper object to download the data and create the free
The objects from gitlabtree.models will be used for the tree
"""
from typing import Any, Dict, List, Callable, Optional

from .models import Group, Repository, Info
from .gitlab_helper import GitLabHelper


class TreeHelper:
    """
    Tree helper object to download the data and build the tree
    """

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

        self._top: Dict[str, Any] = {}
        self._groups: List[Dict[str, Any]] = []
        self._projects: List[Dict[str, Any]] = []

    def get_data(self, start: str) -> None:
        """Download the base data. All groups and projects
        groups/{start}
        groups/{start}/descendant_group
        groups/{start}/projects?include_subgroups=true

        Args:
            start (str): Name or ID of the starting group
        """
        self._top = self.gitlab.get(f"groups/{start}")
        self._groups = self.gitlab.get(f"groups/{start}/descendant_groups")
        self._projects = self.gitlab.get(
            f"groups/{start}/projects?include_subgroups=true"
        )

    def create_tree(
        self,
    ) -> Group:
        """Actually building the tree
        1. Creating the top Group object
        2. Storing the top Group object in a dict so it can be found again by ID
        3. Sorting all descendant groups by full_path so the parent is processed first
        4. Looping over all descendant groups and creating the object,
           storing in the dict, looking for the parent Group object with
           the "parent_id" to link the created object to the parent Group.
        5. If group_processing function is provided, the Info objects can be created
           with the provided function and be added to the new object
        6. Looping over all projects and creating the object and looking for the parent
           object with the 'parent_id' to link the created object to the parent Group.
        7. If group_processing function is provided, the Info objects can be created
           with the provided function and be added to the new object

        Returns:
            Group: Group object with all subgroups and repositories linked
        """

        # Temporary dict to map group ID to group object
        _tmp_groups: Dict[int, Group] = {}

        top = Group(name=self._top["name"])
        if self.group_processing:
            group_info = self.group_processing(self._top, self.gitlab)
            top.info.extend(group_info)

        _tmp_groups[self._top["id"]] = top

        for group_data in sorted(self._groups, key=lambda i: str(i["full_path"])):
            group = Group(name=group_data["name"])
            if self.group_processing:
                group_info = self.group_processing(group_data, self.gitlab)
                group.info.extend(group_info)
            _tmp_groups[group_data["parent_id"]].groups.append(group)
            _tmp_groups[group_data["id"]] = group

        for project_data in self._projects:
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
        """Downloading the data and building the tree

        Args:
            start (str): Name or ID of the starting group

        Returns:
            Group: Group object with all subgroups and repositories linked
        """
        self.get_data(start)
        return self.create_tree()
