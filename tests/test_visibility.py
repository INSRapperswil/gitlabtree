from rich.panel import Panel

from gitlabtree.models import Info
from gitlabtree.gitlab_helper import GitLabHelper
from gitlabtree.visibility import create_visibility_info, get_tree_with_visibility

from .fixture_helper import *


def test_create_visibility_info(
    moked_data: Dict[str, Any], gitlab_helper: GitLabHelper
) -> None:
    data = moked_data["https://a/groups/start/projects?include_subgroups=true"][0]
    gitlab_helper.gitlab.moked_data = moked_data  # type: ignore
    info = create_visibility_info(data, gitlab_helper)

    assert len(info) == 1
    visibility1 = info[0]
    assert visibility1.text == f"public"
    assert isinstance(visibility1.renderable, Panel)
    assert visibility1.renderable.renderable == f"public"

    data2 = moked_data["https://a/groups/start/projects?include_subgroups=true"][2]
    info2 = create_visibility_info(data2, gitlab_helper)

    assert len(info2) == 1
    visibility2 = info2[0]
    assert visibility2.text == "private"
    assert isinstance(visibility2.renderable, Panel)
    assert visibility2.renderable.renderable == f"private"


def test_get_tree_with_visibility(
    gitlab_helper: GitLabHelper, moked_data: Dict[str, Any]
) -> None:
    gitlab_helper.gitlab.moked_data = moked_data  # type: ignore

    tree = get_tree_with_visibility(gitlab_helper, "start")

    assert isinstance(tree.repositories[0].info[0], Info)
    info = tree.repositories[0].info[0]
    assert info.text == "internal"
    assert len(tree.groups[0].groups[1].repositories[0].info) == 1
    assert tree.model_dump() == {
        "groups": [
            {
                "groups": [
                    {
                        "groups": [],
                        "info": [{"text": "public"}],
                        "name": "cat",
                        "repositories": [
                            {
                                "info": [{"text": "public"}],
                                "name": "devon",
                            }
                        ],
                    },
                    {
                        "groups": [],
                        "info": [{"text": "private"}],
                        "name": "dog",
                        "repositories": [
                            {
                                "info": [
                                    {"text": "private"},
                                ],
                                "name": "leo",
                            }
                        ],
                    },
                ],
                "info": [{"text": "public"}],
                "name": "animal",
                "repositories": [],
            }
        ],
        "info": [{"text": "public"}],
        "name": "start",
        "repositories": [
            {
                "info": [{"text": "internal"}],
                "name": "banana",
            }
        ],
    }
