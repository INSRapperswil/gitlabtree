from hashlib import new
from typing import Type, Any, Union, List, Dict
import requests


class RequestDriver:
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
        response = self.session.get(url)
        response.raise_for_status()
        data = response.json()

        # Pagination support
        while next := response.links.get("next", None):
            response = self.session.get(next["url"])
            response.raise_for_status()
            if not isinstance(data, list):
                raise Exception("Pagination is only support on lists")
            data.extend(response.json())
        return data
