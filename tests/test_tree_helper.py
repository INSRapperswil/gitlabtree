import pytest
from typing import Dict, Any, List
from gitlabtree.models import Info
from gitlabtree.gitlab_helper import GitLabHelper
from gitlabtree.tree_helper import TreeHelper

from .fake_driver import FakeDriver


def demo_processing(data: Dict[str, Any], gitlab: GitLabHelper) -> List[Info]:
    return [Info(text="demo")]


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


def test_tree_helper_init(gitlab_helper: GitLabHelper) -> None:
    th = TreeHelper(gitlab=gitlab_helper)
    assert isinstance(th.gitlab, GitLabHelper)
    assert th.group_processing is None
    assert th.project_processing is None


def test_tree_helper_init_processing(gitlab_helper: GitLabHelper) -> None:

    th = TreeHelper(
        gitlab=gitlab_helper,
        group_processing=demo_processing,
        project_processing=demo_processing,
    )
    assert isinstance(th.gitlab, GitLabHelper)
    assert th.group_processing is demo_processing
    assert th.project_processing is demo_processing


def test_tree_helper_get_data(
    tree_helper: TreeHelper, moked_data: Dict[str, Any]
) -> None:
    tree_helper.gitlab.gitlab.moked_data = moked_data  # type: ignore
    tree_helper.get_data("start")

    assert tree_helper._top == moked_data["https://a/groups/start"]
    assert tree_helper._groups == moked_data["https://a/groups/start/descendant_groups"]
    assert (
        tree_helper._projects
        == moked_data["https://a/groups/start/projects?include_subgroups=true"]
    )


def test_tree_helper_create_tree(
    tree_helper: TreeHelper, moked_data: Dict[str, Any]
) -> None:
    tree_helper._top = moked_data["https://a/groups/start"]
    tree_helper._groups = moked_data["https://a/groups/start/descendant_groups"]
    tree_helper._projects = moked_data[
        "https://a/groups/start/projects?include_subgroups=true"
    ]

    tree = tree_helper.create_tree()

    assert tree.name == "start"
    assert len(tree.groups) == 1
    assert len(tree.repositories) == 1
    assert tree.dict() == {
        "groups": [
            {
                "groups": [
                    {
                        "groups": [],
                        "info": [],
                        "name": "cat",
                        "repositories": [{"info": [], "name": "devon"}],
                    },
                    {
                        "groups": [],
                        "info": [],
                        "name": "dog",
                        "repositories": [{"info": [], "name": "leo"}],
                    },
                ],
                "info": [],
                "name": "animal",
                "repositories": [],
            }
        ],
        "info": [],
        "name": "start",
        "repositories": [{"info": [], "name": "banana"}],
    }


def test_tree_helper_create_tree_group_processing(
    tree_helper: TreeHelper, moked_data: Dict[str, Any]
) -> None:
    tree_helper._top = moked_data["https://a/groups/start"]
    tree_helper._groups = moked_data["https://a/groups/start/descendant_groups"]
    tree_helper._projects = moked_data[
        "https://a/groups/start/projects?include_subgroups=true"
    ]
    tree_helper.group_processing = demo_processing

    tree = tree_helper.create_tree()

    assert tree.info[0].text == "demo"
    assert len(tree.info) == 1
    assert tree.dict() == {
        "groups": [
            {
                "groups": [
                    {
                        "groups": [],
                        "info": [{"text": "demo"}],
                        "name": "cat",
                        "repositories": [{"info": [], "name": "devon"}],
                    },
                    {
                        "groups": [],
                        "info": [{"text": "demo"}],
                        "name": "dog",
                        "repositories": [{"info": [], "name": "leo"}],
                    },
                ],
                "info": [{"text": "demo"}],
                "name": "animal",
                "repositories": [],
            }
        ],
        "info": [{"text": "demo"}],
        "name": "start",
        "repositories": [{"info": [], "name": "banana"}],
    }


def test_tree_helper_create_tree_project_processing(
    tree_helper: TreeHelper, moked_data: Dict[str, Any]
) -> None:
    tree_helper._top = moked_data["https://a/groups/start"]
    tree_helper._groups = moked_data["https://a/groups/start/descendant_groups"]
    tree_helper._projects = moked_data[
        "https://a/groups/start/projects?include_subgroups=true"
    ]
    tree_helper.project_processing = demo_processing

    tree = tree_helper.create_tree()

    assert tree.repositories[0].info[0].text == "demo"
    assert len(tree.repositories[0].info) == 1
    assert tree.dict() == {
        "groups": [
            {
                "groups": [
                    {
                        "groups": [],
                        "info": [],
                        "name": "cat",
                        "repositories": [{"info": [{"text": "demo"}], "name": "devon"}],
                    },
                    {
                        "groups": [],
                        "info": [],
                        "name": "dog",
                        "repositories": [{"info": [{"text": "demo"}], "name": "leo"}],
                    },
                ],
                "info": [],
                "name": "animal",
                "repositories": [],
            }
        ],
        "info": [],
        "name": "start",
        "repositories": [{"info": [{"text": "demo"}], "name": "banana"}],
    }


def test_tree_helper_get_tree(
    tree_helper: TreeHelper, moked_data: Dict[str, Any]
) -> None:
    tree_helper.gitlab.gitlab.moked_data = moked_data  # type: ignore

    tree = tree_helper.get_tree("start")
    assert tree.name == "start"
    assert len(tree.groups) == 1
    assert len(tree.repositories) == 1
    assert tree.dict() == {
        "groups": [
            {
                "groups": [
                    {
                        "groups": [],
                        "info": [],
                        "name": "cat",
                        "repositories": [{"info": [], "name": "devon"}],
                    },
                    {
                        "groups": [],
                        "info": [],
                        "name": "dog",
                        "repositories": [{"info": [], "name": "leo"}],
                    },
                ],
                "info": [],
                "name": "animal",
                "repositories": [],
            }
        ],
        "info": [],
        "name": "start",
        "repositories": [{"info": [], "name": "banana"}],
    }
