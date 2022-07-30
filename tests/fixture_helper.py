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
        "https://a/groups/start": {
            "name": "start",
            "id": 123,
            "full_path": "start",
            "parent_id": None,
            "visibility": "public",
        },
        "https://a/groups/start/descendant_groups": [
            {
                "name": "cat",
                "id": 54,
                "full_path": "start/animal/cat",
                "parent_id": 40,
                "visibility": "public",
            },
            {
                "name": "dog",
                "id": 30,
                "full_path": "start/animal/dog",
                "parent_id": 40,
                "visibility": "private",
            },
            {
                "name": "animal",
                "id": 40,
                "full_path": "start/animal",
                "parent_id": 123,
                "visibility": "public",
            },
        ],
        "https://a/groups/start/projects?include_subgroups=true": [
            {
                "name": "devon",
                "id": 60,
                "full_path": "start/animal/cat/devon",
                "namespace": {"id": 54},
                "visibility": "public",
                "default_branch": "develop",
            },
            {
                "name": "banana",
                "id": 100,
                "full_path": "start/banana",
                "namespace": {"id": 123},
                "visibility": "internal",
                "default_branch": "develop",
            },
            {
                "name": "leo",
                "id": 10,
                "full_path": "start/animal/dog/leo",
                "namespace": {"id": 30},
                "visibility": "private",
                "default_branch": "main",
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


@pytest.fixture
def moked_data_pipelines(moked_data: Dict[str, Any]) -> Dict[str, Any]:
    moked_data.update(
        {
            "https://a/projects/60/pipelines?ref=develop&order_by=updated_at&per_page=1": [
                {
                    "ref": "develop",
                    "status": "success",
                    "updated_at": "2022-07-30T19:02:06.900+02:00",
                    "web_url": "http://a/asdf",
                }
            ],
            "https://a/projects/100/pipelines?ref=develop&order_by=updated_at&per_page=1": [],
            "https://a/projects/10/pipelines?ref=main&order_by=updated_at&per_page=1": [
                {
                    "ref": "main",
                    "status": "failed",
                    "updated_at": "2022-07-30T19:02:06.900+02:00",
                    "web_url": "http://a/asdf",
                },
                {
                    "ref": "main",
                    "status": "success",
                    "updated_at": "2022-07-29T19:02:06.900+02:00",
                    "web_url": "http://a/asdf",
                },
            ],
        }
    )
    return moked_data


@pytest.fixture
def moked_data_permissions(moked_data: Dict[str, Any]) -> Dict[str, Any]:
    moked_data.update(
        {
            "https://a/projects/60/members": [],
            "https://a/projects/100/members": [],
            "https://a/projects/10/members": [
                {
                    "name": "User Uno",
                    "username": "user1",
                    "state": "active",
                    "access_level": 40,
                    "expires_at": None,
                    "web_url": "http://a/asdf",
                },
                {
                    "name": "User Zwei",
                    "username": "user2",
                    "state": "active",
                    "access_level": 40,
                    "expires_at": "2022-07-30",
                    "web_url": "http://a/asdf",
                },
            ],
            "https://a/groups/123/members": [
                {
                    "name": "Ms. Admin",
                    "username": "admin",
                    "state": "active",
                    "access_level": 50,
                    "expires_at": None,
                    "web_url": "http://a/asdf",
                },
            ],
            "https://a/groups/30/members": [],
            "https://a/groups/40/members": [],
            "https://a/groups/54/members": [
                {
                    "name": "User Uno",
                    "username": "user1",
                    "state": "active",
                    "access_level": 40,
                    "expires_at": None,
                    "web_url": "http://a/asdf",
                }
            ],
        }
    )
    return moked_data
