from gitlabtree.models import Info
from gitlabtree.gitlab_helper import GitLabHelper
from gitlabtree.runner import create_runner_info, get_tree_with_runner

from .fixture_helper import *


def test_create_runner_info(
    moked_data_runners: Dict[str, Any], gitlab_helper: GitLabHelper
) -> None:
    data = moked_data_runners["https://a/groups/start/projects?include_subgroups=true"][
        0
    ]
    gitlab_helper.gitlab.moked_data = moked_data_runners  # type: ignore
    info = create_runner_info(data, gitlab_helper)

    assert len(info) == 1
    runner1 = info[0]
    assert runner1.text == f"runner1 - True"

    data2 = moked_data_runners[
        "https://a/groups/start/projects?include_subgroups=true"
    ][2]
    info2 = create_runner_info(data2, gitlab_helper)

    assert len(info2) == 2
    runner2 = info2[1]
    assert runner2.text == "runner2 - False"


def test_get_tree_with_runner(
    gitlab_helper: GitLabHelper, moked_data_runners: Dict[str, Any]
) -> None:
    gitlab_helper.gitlab.moked_data = moked_data_runners  # type: ignore

    tree = get_tree_with_runner(gitlab_helper, "start")

    assert isinstance(tree.repositories[0].info[0], Info)
    info = tree.repositories[0].info[0]
    assert info.text == "runner1 - True"
    assert len(tree.groups[0].groups[1].repositories[0].info) == 2
    assert tree.dict() == {
        "groups": [
            {
                "groups": [
                    {
                        "groups": [],
                        "info": [],
                        "name": "cat",
                        "repositories": [
                            {
                                "info": [{"text": "runner1 - True"}],
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
                                    {"text": "runner1 - True"},
                                    {"text": "runner2 - False"},
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
        "info": [],
        "name": "start",
        "repositories": [
            {
                "info": [{"text": "runner1 - True"}],
                "name": "banana",
            }
        ],
    }
