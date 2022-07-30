"""
GitLab Helper and RequestDriver to interact with the GitLab API
"""
from typing import Type, Any
import requests


class RequestDriver:
    """
    Driver to use requests Session
    """

    def __init__(self, token: str, verify: bool = True) -> None:
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Cache-Control": "no-cache",
        }
        session = requests.Session()
        session.headers.update(headers)
        session.verify = verify
        self.session = session

    def get(self, url: str) -> Any:
        """Get JSON data from the API. Pagination support

        Args:
            url (str): API URL

        Raises:
            Exception: Pagination is not possible if API does not return a list

        Returns:
            Any: Data from the API
        """
        response = self.session.get(url)
        response.raise_for_status()
        data = response.json()

        # Pagination support
        while next_page := response.links.get("next", None):
            response = self.session.get(next_page["url"])
            response.raise_for_status()
            if not isinstance(data, list):
                raise Exception("Pagination is only supported on lists")
            data.extend(response.json())
        return data


class GitLabHelper:
    """
    GitLabHelper to interact with GitLab and make writing tests easy 🍻
    """

    def __init__(
        self, api_url: str, token: str, request_cls: Type[RequestDriver] = RequestDriver
    ) -> None:
        self.api_url = api_url[:-1] if api_url[-1] == "/" else api_url
        self.gitlab = request_cls(token)

    def _get_url(self, endpoint: str) -> str:
        endpoint = endpoint[1:] if endpoint[0] == "/" else endpoint
        return f"{self.api_url}/{endpoint}"

    def get(self, endpoint: str) -> Any:
        """Retrieving API data

        Args:
            endpoint (str): Requested API endpoint. Example 'groups/1234'

        Returns:
            Any: Data from the API
        """
        return self.gitlab.get(self._get_url(endpoint))
