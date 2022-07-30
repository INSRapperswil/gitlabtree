from rich.panel import Panel

from gitlabtree.models import Info
from gitlabtree.gitlab_helper import GitLabHelper
from gitlabtree.pipeline import create_pipeline_info, get_tree_with_pipeline

from .fixture_helper import *


def test_create_pipeline_info(
    moked_data_pipelines: Dict[str, Any], gitlab_helper: GitLabHelper
) -> None:
    data = moked_data_pipelines[
        "https://a/groups/start/projects?include_subgroups=true"
    ][0]
    gitlab_helper.gitlab.moked_data = moked_data_pipelines  # type: ignore
    info = create_pipeline_info(data, gitlab_helper)

    assert len(info) == 1
    pipeline1 = info[0]
    assert pipeline1.text == "develop success 2022-07-30T19:02:06.900+02:00"
    assert isinstance(pipeline1.renderable, Panel)
    assert (
        pipeline1.renderable.renderable
        == "[link=http://a/asdf]develop success 2022-07-30T19:02:06.900+02:00[/link]"
    )
    assert pipeline1.renderable.style == "green"
    assert pipeline1.renderable.title == "develop"

    data2 = moked_data_pipelines[
        "https://a/groups/start/projects?include_subgroups=true"
    ][2]
    info2 = create_pipeline_info(data2, gitlab_helper)

    assert len(info2) == 1
    pipeline2 = info2[0]
    assert pipeline2.text == "main failed 2022-07-30T19:02:06.900+02:00"
    assert isinstance(pipeline2.renderable, Panel)
    assert (
        pipeline2.renderable.renderable
        == "[link=http://a/asdf]main failed 2022-07-30T19:02:06.900+02:00[/link]"
    )
    assert pipeline2.renderable.style == "red"
    assert pipeline2.renderable.title == "main"


def test_get_tree_with_pipeline(
    gitlab_helper: GitLabHelper, moked_data_pipelines: Dict[str, Any]
) -> None:
    gitlab_helper.gitlab.moked_data = moked_data_pipelines  # type: ignore

    tree = get_tree_with_pipeline(gitlab_helper, "start")

    assert len(tree.repositories[0].info) == 0
    assert len(tree.groups[0].groups[1].repositories[0].info) == 1
    info = tree.groups[0].groups[1].repositories[0].info[0]
    assert info.text == "main failed 2022-07-30T19:02:06.900+02:00"
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
                                "info": [
                                    {
                                        "text": "develop success 2022-07-30T19:02:06.900+02:00"
                                    }
                                ],
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
                                    {
                                        "text": "main failed 2022-07-30T19:02:06.900+02:00"
                                    },
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
                "info": [],
                "name": "banana",
            }
        ],
    }
