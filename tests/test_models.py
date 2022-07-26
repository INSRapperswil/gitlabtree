from rich.panel import Panel
from gitlabtree.models import (
    Repository,
    Group,
    Info,
    PermissionInfo,
    PipelineInfo,
    VisibilityInfo,
)


def test_recursive_models() -> None:
    top = Group(
        name="Top",
        repositories=[Repository(name="first level")],
        groups=[
            Group(
                name="second level",
                groups=[
                    Group(
                        name="third level",
                        repositories=[
                            Repository(name="third level 1"),
                            Repository(name="third level 2"),
                            Repository(name="third level 3"),
                        ],
                    ),
                ],
            ),
            Group(name="second second"),
        ],
    )
    assert top.name == "Top"
    assert top.repositories[0].name == "first level"
    assert top.groups[0].name == "second level"
    assert top.groups[1].name == "second second"
    assert top.groups[0].groups[0].name == "third level"
    assert len(top.groups[0].groups[0].repositories) == 3
    assert top.groups[0].groups[0].repositories[2].name == "third level 3"


def test_recursive_models_from_dict() -> None:
    top = Group(
        **{
            "name": "Top",
            "groups": [
                {
                    "name": "second level",
                    "groups": [
                        {
                            "name": "third level",
                            "groups": [],
                            "repositories": [
                                {"name": "third level 1"},
                                {"name": "third level 2"},
                                {"name": "third level 3"},
                            ],
                        }
                    ],
                    "repositories": [],
                },
                {"name": "second second", "groups": [], "repositories": []},
            ],
            "repositories": [{"name": "first level"}],
        }
    )
    assert top.name == "Top"
    assert top.repositories[0].name == "first level"
    assert top.groups[0].name == "second level"
    assert top.groups[1].name == "second second"
    assert top.groups[0].groups[0].name == "third level"
    assert len(top.groups[0].groups[0].repositories) == 3
    assert top.groups[0].groups[0].repositories[2].name == "third level 3"


def test_group_rich_protocol() -> None:
    group = Group(name="Test 123", groups=[Group(name="second")])
    assert group.__rich__() == ":open_file_folder: Test 123"


def test_repository_rich_protocol() -> None:
    repo = Repository(name="Test 123")
    assert repo.__rich__() == ":book: Test 123"


def test_info_rich_protocol() -> None:
    repo = Info(text="Test 123")
    rich_rendered = repo.__rich__()
    assert isinstance(rich_rendered, Panel)
    assert rich_rendered.renderable == "Test 123"


def test_permission_rich_protocol() -> None:
    """
    ToDo: Update/change this test
    """
    repo = PermissionInfo(text="Test 123")
    assert repo.__rich__() == "Test 123"


def test_pipeline_rich_protocol() -> None:
    """
    ToDo: Update/change this test
    """
    repo = PipelineInfo(text="Test 123")
    assert repo.__rich__() == "Test 123"


def test_vivibility_rich_protocol() -> None:
    """
    ToDo: Update/change this test
    """
    repo = VisibilityInfo(text="Test 123")
    assert repo.__rich__() == "Test 123"
