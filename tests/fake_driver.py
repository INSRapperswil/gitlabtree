from typing import Any, Dict, List, Union, Type
from gitlabtree.gitlab_helper import RequestDriver


class FakeDriver(RequestDriver):
    """
    Fake driver returning the defined payload in moked_data for each URL
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.moked_data: Dict[str, Union[Dict[Any, Any], List[Any]]] = {}

    def get(self, url: str) -> Any:
        return self.moked_data.get(url)


class FakeRaiseDriver(RequestDriver):
    """
    Fake driver raising exception defined in moked_data for each URL
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.moked_data: Dict[str, Type[BaseException]] = {}

    def get(self, url: str) -> Any:
        raise self.moked_data.get(url, Exception)
