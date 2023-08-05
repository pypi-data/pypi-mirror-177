"""
TD Ameritrade API get quote endpoint.

https://developer.tdameritrade.com/quotes/apis/get/marketdata/{symbol}/quotes
"""

from collections.abc import Iterable

from .get_quote import GetQuote, Quote


class GetQuotes(GetQuote):
    """Make requests to the get quotes endpoint."""

    @staticmethod
    def path() -> str:
        """Path relative to the base URL of the endpoint."""
        return "v1/marketdata/quotes"

    def get(self, symbol: Iterable[str]) -> Quote:
        """Make a request to the get quotes endpoint."""
        res = self._get(self._endpoint(params={"symbol": symbol}))
        quotes = res.json()
        assert GetQuotes.is_quote(quotes)
        return quotes
