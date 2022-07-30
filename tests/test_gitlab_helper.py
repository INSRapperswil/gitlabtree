import pytest
from gitlabtree.gitlab_helper import GitLabHelper
from .fake_driver import FakeDriver, RequestDriver


def test_gitlab_helper() -> None:
    glh = GitLabHelper("https://test", "myToken")
    assert isinstance(glh.gitlab, RequestDriver)


def test_gitlab_helper_driver() -> None:
    glh = GitLabHelper("https://test", "myToken", request_cls=FakeDriver)
    assert isinstance(glh.gitlab, FakeDriver)


@pytest.mark.parametrize(
    "url, expected",
    [
        ("https://test", "https://test"),
        ("https://test/", "https://test"),
        ("test", "test"),
    ],
)
def test_gitlab_helper_api_url(url: str, expected: str) -> None:
    glh = GitLabHelper(url, "myToken")
    assert glh.api_url == expected


@pytest.mark.parametrize(
    "endpoint, expected",
    [
        ("/members", "https://test/members"),
        ("members", "https://test/members"),
        ("/projects/123", "https://test/projects/123"),
        ("projects/123", "https://test/projects/123"),
        ("/projects/123?test=123", "https://test/projects/123?test=123"),
        ("projects/123?test=123", "https://test/projects/123?test=123"),
    ],
)
def test_gitlab_helper_get_endpoint(endpoint: str, expected: str) -> None:
    glh = GitLabHelper("https://test", "myToken")
    assert glh._get_url(endpoint) == expected


def test_gitlab_helper_get() -> None:
    glh = GitLabHelper("https://test", "myToken", request_cls=FakeDriver)
    glh.gitlab.moked_data = {"https://test/users": [{"name": "a"}, {"name": "b"}]}  # type: ignore
    data = glh.get("users")
    assert [{"name": "a"}, {"name": "b"}] == data
