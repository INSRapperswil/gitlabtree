import pytest
from typing import Dict, Any
from gitlabtree.gitlab_helper import GitLabHelper
from gitlabtree.tree_helper import TreeHelper

from .fake_driver import FakeDriver


@pytest.fixture
def gitlab_helper() -> GitLabHelper:
    return GitLabHelper("https://a", "token", FakeDriver)


@pytest.fixture
def tree_helper(gitlab_helper: GitLabHelper) -> TreeHelper:
    return TreeHelper(gitlab_helper)


@pytest.fixture
def moked_data() -> Dict[str, Any]:
    return {
        "https://a/groups/start": {"name": "start", "id": 123, "full_path": "start"},
        "https://a/groups/start/descendant_groups": [
            {"name": "cat", "id": 54, "full_path": "start/animal/cat", "parent_id": 40},
            {"name": "dog", "id": 30, "full_path": "start/animal/dog", "parent_id": 40},
            {"name": "animal", "id": 40, "full_path": "start/animal", "parent_id": 123},
        ],
        "https://a/groups/start/projects?include_subgroups=true": [
            {
                "name": "devon",
                "id": 60,
                "full_path": "start/animal/cat/devon",
                "namespace": {"id": 54},
            },
            {
                "name": "banana",
                "id": 100,
                "full_path": "start/banana",
                "namespace": {"id": 123},
            },
            {
                "name": "leo",
                "id": 10,
                "full_path": "start/animal/dog/leo",
                "namespace": {"id": 30},
            },
        ],
    }


@pytest.fixture
def moked_data_runners(moked_data: Dict[str, Any]) -> Dict[str, Any]:
    moked_data.update(
        {
            "https://a/projects/60/runners": [
                {"description": "runner1", "active": True, "is_shared": True}
            ],
            "https://a/projects/100/runners": [
                {"description": "runner1", "active": True, "is_shared": True}
            ],
            "https://a/projects/10/runners": [
                {"description": "runner1", "active": True, "is_shared": True},
                {"description": "runner2", "active": False, "is_shared": False},
            ],
        }
    )
    return moked_data
