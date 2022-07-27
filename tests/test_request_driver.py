from typing import Any, List, Dict
from pytest import MonkeyPatch
from itertools import cycle
import pytest
from requests.sessions import Session
from gitlabtree.gitlab_helper import RequestDriver


class MockResponse:
    def __init__(self, data: Any, links: bool = False) -> None:
        self.data = data
        self.links = {"next": {"url": "http://next"}} if links else {}

    def json(self) -> Any:
        return self.data

    @staticmethod
    def raise_for_status() -> None:
        return


def mock_get_object(*args: List[Any], **kwargs: Dict[str, Any]) -> MockResponse:
    return MockResponse({"User": {"id": 1, "admin": True}})


def test_reqeust_driver_headers() -> None:
    rd = RequestDriver("myToken")
    assert rd.session.headers["Authorization"] == "Bearer myToken"
    assert rd.session.verify is True


def test_reqeust_driver_headers_no_verify() -> None:
    rd = RequestDriver("asdf1234", verify=False)
    assert rd.session.headers["Authorization"] == "Bearer asdf1234"
    assert rd.session.verify is False


def test_request_driver_get(monkeypatch: MonkeyPatch) -> None:
    rd = RequestDriver("asdf1234", verify=False)
    # Disable all requests just in case
    monkeypatch.delattr("requests.sessions.Session.request")
    monkeypatch.setattr(Session, "get", mock_get_object)

    result = rd.get("http://localhost")
    assert result == {"User": {"id": 1, "admin": True}}


def test_request_driver_get_paging(monkeypatch: MonkeyPatch) -> None:
    CYCLE = cycle(
        [MockResponse([{"User": "A"}], links=True), MockResponse([{"User": "B"}])]
    )

    def mock_get_list(*args: List[Any], **kwargs: Dict[str, Any]) -> MockResponse:
        return next(CYCLE)

    rd = RequestDriver("asdf1234", verify=False)
    # Disable all requests just in case
    monkeypatch.delattr("requests.sessions.Session.request")
    monkeypatch.setattr(Session, "get", mock_get_list)

    result = rd.get("http://localhost")
    assert result == [{"User": "A"}, {"User": "B"}]


def test_request_driver_wrong_paging_types(monkeypatch: MonkeyPatch) -> None:
    CYCLE = cycle(
        [MockResponse({"User": "A"}, links=True), MockResponse([{"User": "B"}])]
    )

    def mock_get_list(*args: List[Any], **kwargs: Dict[str, Any]) -> MockResponse:
        return next(CYCLE)

    rd = RequestDriver("asdf1234", verify=False)
    # Disable all requests just in case
    monkeypatch.delattr("requests.sessions.Session.request")
    monkeypatch.setattr(Session, "get", mock_get_list)

    with pytest.raises(Exception):
        result = rd.get("http://localhost")
