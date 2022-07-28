"""
Visibility Helper to get visibility information from GitLabAPI for projects and groups
"""

from gitlabtree.gitlab_helper import GitLabHelper


class VisibilityHelper:
    """
    Visibility helper to get visibility for projects and groups
    """

    def __init__(self, gitlab) -> None:
        self.gitlab = gitlab

    def get_projects(self) -> None:
        data = self.gitlab.get("projects")
        for project in data:
            id = project['id']
            name = project['name']
            namespace = project['namespace']['name']
            visibility = project['visibility']
            print(namespace + "/" + name)
            print(visibility)
        print(data)
