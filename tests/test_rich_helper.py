from gitlabtree.rich_helper import error, render_tree
from gitlabtree.models import Group


def test_error_msg() -> None:
    result = error("demo error")
    assert result.renderable == "demo error"
    assert result.title == "ERROR"


def test_error_title() -> None:
    result = error("demo error", "My Error")
    assert result.renderable == "demo error"
    assert result.title == "My Error"


def test_render_tree_only_top() -> None:
    data = Group(name="aa")
    tree = render_tree(data)
    assert len(tree.children) == 0


def test_render_tree() -> None:
    data = Group(
        **{
            "name": "aa",
            "groups": [{"name": "bb"}, {"name": "cc"}],
            "repositories": [{"name": "11"}, {"name": "11"}],
        }
    )
    tree = render_tree(data)
    assert len(tree.children) == 4


def test_render_tree_with_info() -> None:
    data = Group(
        **{
            "name": "aa",
            "groups": [{"name": "bb"}, {"name": "cc"}],
            "repositories": [{"name": "11"}, {"name": "11"}],
            "info": [{"text": "test_123"}, {"text": "test_456"}],
        }
    )
    tree = render_tree(data)
    assert len(tree.children) == 5
