"""TD Ameritrade API endpoint base."""

from abc import ABCMeta, abstractmethod
from collections.abc import Iterable, Mapping
from datetime import datetime
from urllib.parse import urlencode
import requests

from pytda.auth import Auth

Params = Mapping[str, str | Iterable[str]]


class Request(metaclass=ABCMeta):
    """Abstract base class to make requests to an endpoint."""

    def __init__(self, auth: Auth) -> None:
        self.auth = auth

    # It would be nice to make this a static property
    @staticmethod
    def base_url() -> str:
        """Base URL of all endpoints."""
        return "https://api.tdameritrade.com/"

    # It would be nice to make this a static abstract property
    @staticmethod
    @abstractmethod
    def path() -> str:
        """Path relative to the base URL of the endpoint."""

    @property
    def _auth_header(self) -> Mapping[str, str]:
        """The authorization header."""
        return {"Authorization": f"Bearer {self.auth.access_token}"}

    @staticmethod
    def _append_params(url: str, params: Params) -> str:
        """
        Return a URL joined with the encoded params. Any Iterable value is
        joined by commas into a str, then encoded.
        """
        final_params = {
            k: ",".join(v) if isinstance(v, Iterable) and not isinstance(v, str) else v
            for k, v in params.items()
        }
        return f"{url}?{urlencode(final_params, safe='')}"

    @staticmethod
    def _dt_to_ms(d_t: datetime) -> int:
        """Convert a timestamp to milliseconds."""
        return int(round(d_t.timestamp() * 1000))

    def _endpoint(self, **kwargs: str | Params) -> str:
        """Return an endpoint for a name and any identifiers and params encoded."""
        if "params" in kwargs and isinstance(kwargs["params"], Mapping):
            ids = {k: v for k, v in kwargs.items() if k != "params"}
            return Request._append_params(
                f"{Request.base_url()}{self.path()}".format(**ids), kwargs["params"]
            )
        return f"{Request.base_url()}{self.path()}".format(**kwargs)

    def _get(self, url: str) -> requests.Response:
        """Add the auth header and return the results of a get request."""
        res = requests.get(url, headers=self._auth_header, timeout=5)
        if res.status_code == 200:
            return res
        if res.status_code == 401:
            self.auth.request_access_tokens(refresh=True)
            res = requests.get(url, headers=self._auth_header, timeout=5)
            if res.status_code == 200:
                return res
        res.raise_for_status()
        return res
