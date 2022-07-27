from pytest import MonkeyPatch
import pytest


@pytest.fixture(autouse=True)
def env_gitlab_token(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("GITLAB_TOKEN", "MyTestingToken")
