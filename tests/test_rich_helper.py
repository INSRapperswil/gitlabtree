from gitlabtree.rich_helper import error


def test_error_msg() -> None:
    result = error("demo error")
    assert result.renderable == "demo error"
    assert result.title == "ERROR"


def test_error_title() -> None:
    result = error("demo error", "My Error")
    assert result.renderable == "demo error"
    assert result.title == "My Error"
