import pytest
from typing import Dict, Any, Type
from .fake_driver import FakeDriver, FakeRaiseDriver


def test_error_msg() -> None:
    moked_data: Dict[str, Any] = {
        "http://test1": {"test1": [0, 1, 3]},
        "http://test2": [{"a": 1}, {"b": 2}],
    }
    fd = FakeDriver(moked_data=moked_data)
    for url, data in moked_data.items():
        assert data == fd.get(url)


def test_fake_raise_driver() -> None:
    moked_data: Dict[str, Type[BaseException]] = {
        "http://test1": FileNotFoundError,
        "http://test2": ConnectionError,
    }
    frd = FakeRaiseDriver(moked_data=moked_data)
    for url, exc in moked_data.items():
        with pytest.raises(exc):
            frd.get(url)
