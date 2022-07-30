from rich.table import Table

from gitlabtree.models import Info
from gitlabtree.gitlab_helper import GitLabHelper
from gitlabtree.permissions import create_permission_info, get_tree_with_permissions

from .fixture_helper import *


def test_create_permissions_info(
    moked_data_permissions: Dict[str, Any], gitlab_helper: GitLabHelper
) -> None:
    data = moked_data_permissions[
        "https://a/groups/start/projects?include_subgroups=true"
    ][0]
    gitlab_helper.gitlab.moked_data = moked_data_permissions  # type: ignore
    info = create_permission_info(data, gitlab_helper)

    assert len(info) == 0

    data2 = moked_data_permissions["https://a/groups/start"]
    info2 = create_permission_info(data2, gitlab_helper)

    assert len(info2) == 1
    permissions2 = info2[0]
    assert permissions2.text == "admin"
    assert isinstance(permissions2.renderable, Table)
    assert permissions2.renderable.row_count == 1
    assert (
        list(permissions2.renderable.columns[0].cells)[0]
        == "[link=http://a/asdf]admin[/link]"
    )
    assert list(permissions2.renderable.columns[1].cells)[0] == "Ms. Admin"
    assert list(permissions2.renderable.columns[2].cells)[0] == "active"
    assert list(permissions2.renderable.columns[3].cells)[0] == "50"
    assert list(permissions2.renderable.columns[4].cells)[0] == ""

    data3 = moked_data_permissions[
        "https://a/groups/start/projects?include_subgroups=true"
    ][2]
    info3 = create_permission_info(data3, gitlab_helper)

    assert len(info3) == 1
    permissions3 = info3[0]
    assert permissions3.text == "user1 user2"
    assert isinstance(permissions3.renderable, Table)
    assert permissions3.renderable.row_count == 2
    assert (
        list(permissions3.renderable.columns[0].cells)[1]
        == "[link=http://a/asdf]user2[/link]"
    )
    assert list(permissions3.renderable.columns[1].cells)[1] == "User Zwei"
    assert list(permissions3.renderable.columns[2].cells)[1] == "active"
    assert list(permissions3.renderable.columns[3].cells)[1] == "40"
    assert list(permissions3.renderable.columns[4].cells)[1] == "2022-07-30"


def test_get_tree_with_permissions(
    gitlab_helper: GitLabHelper, moked_data_permissions: Dict[str, Any]
) -> None:
    gitlab_helper.gitlab.moked_data = moked_data_permissions  # type: ignore

    tree = get_tree_with_permissions(gitlab_helper, "start")

    assert tree.dict() == {
        "groups": [
            {
                "groups": [
                    {
                        "groups": [],
                        "info": [{"text": "user1"}],
                        "name": "cat",
                        "repositories": [
                            {
                                "info": [],
                                "name": "devon",
                            }
                        ],
                    },
                    {
                        "groups": [],
                        "info": [],
                        "name": "dog",
                        "repositories": [
                            {
                                "info": [
                                    {"text": "user1 user2"},
                                ],
                                "name": "leo",
                            }
                        ],
                    },
                ],
                "info": [],
                "name": "animal",
                "repositories": [],
            }
        ],
        "info": [{"text": "admin"}],
        "name": "start",
        "repositories": [
            {
                "info": [],
                "name": "banana",
            }
        ],
    }
