from typing import Optional, cast

import requests

from .types import Impact

TIMEOUT = 3
API_BASE_URI = "https://public.ecologi.com"


class EcologiException(RuntimeError):
    """Unknown error"""


class NotFoundException(EcologiException):
    """Not Found"""


class Ecologi:
    def __init__(self, base_uri: str = API_BASE_URI) -> None:
        self.base_uri: str = base_uri
        self.headers: dict = {}

    def user_exists(self, username: str) -> bool:
        try:
            return self.impact(username).get("trees") is not None
        except NotFoundException:
            return False

    def impact(self, username: str) -> Impact:
        return cast(Impact, self.get(f"/users/{username}/impact"))

    def get(self, url: str):
        return self.__request("GET", url)

    def __request(self, method: str, url: str, params: Optional[dict] = None):
        if params is None:
            params = {}

        if method == "GET":
            response = requests.get(
                self.base_uri + url, params=params, headers=self.headers
            )
        else:
            raise RuntimeError("Invalid request method provided")

        if response.status_code == 404:
            raise NotFoundException(response.json().get("responseCode"))
        if response.status_code >= 400:
            raise EcologiException(
                response.json().get("responseCode") or "Unknown error"
            )
        return response.json()
