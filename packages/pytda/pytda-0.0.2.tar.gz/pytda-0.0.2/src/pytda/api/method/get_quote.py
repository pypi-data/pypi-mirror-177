"""
TD Ameritrade API get quote endpoint.

https://developer.tdameritrade.com/quotes/apis/get/marketdata/{symbol}/quotes
"""

from collections.abc import Mapping
from typing import TypedDict, TypeGuard

from pytyu.json import is_json, is_json_schema

from .base import Request

Number = int | float


# We have to use the alternative syntax because some keys are not valid identifiers.
# https://peps.python.org/pep-0589/#alternative-syntax
EquityQuoteData = TypedDict(
    "EquityQuoteData",
    {
        "assetType": str,
        "assetMainType": str,
        "cusip": str,
        "assetSubType": str,
        "symbol": str,
        "description": str,
        "bidPrice": Number,
        "bidSize": Number,
        "bidId": str,
        "askPrice": Number,
        "askSize": Number,
        "askId": str,
        "lastPrice": Number,
        "lastSize": Number,
        "lastId": str,
        "openPrice": Number,
        "highPrice": Number,
        "lowPrice": Number,
        "bidTick": str,
        "closePrice": Number,
        "netChange": Number,
        "totalVolume": Number,
        "quoteTimeInLong": Number,
        "tradeTimeInLong": Number,
        "mark": Number,
        "exchange": str,
        "exchangeName": str,
        "marginable": bool,
        "shortable": bool,
        "volatility": Number,
        "digits": Number,
        "52WkHigh": Number,
        "52WkLow": Number,
        "nAV": Number,
        "peRatio": Number,
        "divAmount": Number,
        "divYield": Number,
        "divDate": str,
        "securityStatus": str,
        "regularMarketLastPrice": Number,
        "regularMarketLastSize": Number,
        "regularMarketNetChange": Number,
        "regularMarketTradeTimeInLong": Number,
        "netPercentChangeInDouble": Number,
        "markChangeInDouble": Number,
        "markPercentChangeInDouble": Number,
        "regularMarketPercentChangeInDouble": Number,
        "delayed": bool,
        "realtimeEntitled": bool,
    },
)
"""Equity quote data type."""


# We have to use the alternative syntax because some keys are not valid identifiers.
IndexQuoteData = TypedDict(
    "IndexQuoteData",
    {
        "assetType": str,
        "assetMainType": str,
        "cusip": str,
        "assetSubType": str,
        "symbol": str,
        "description": str,
        "lastPrice": Number,
        "openPrice": Number,
        "highPrice": Number,
        "lowPrice": Number,
        "closePrice": Number,
        "netChange": Number,
        "totalVolume": Number,
        "tradeTimeInLong": Number,
        "exchange": str,
        "exchangeName": str,
        "digits": Number,
        "52WkHigh": Number,
        "52WkLow": Number,
        "securityStatus": str,
        "netPercentChangeInDouble": Number,
        "delayed": bool,
        "realtimeEntitled": bool,
    },
)
"""Index quote data type."""


Quote = Mapping[str, EquityQuoteData | IndexQuoteData]
"""Quote data type."""


class GetQuote(Request):
    """Make requests to the get quote endpoint."""

    @staticmethod
    def path() -> str:
        """Path relative to the base URL of the endpoint."""
        return "v1/marketdata/{symbol}/quotes"

    @staticmethod
    def is_equity_quote_data(val: object) -> TypeGuard[EquityQuoteData]:
        """Narrow `val` to `EquityQuoteData` type."""
        return is_json_schema(val, EquityQuoteData)

    @staticmethod
    def is_index_quote_data(val: object) -> TypeGuard[IndexQuoteData]:
        """Narrow `val` to `IndexQuoteData` type."""
        return is_json_schema(val, IndexQuoteData)

    @staticmethod
    def is_quote_data(val: object) -> TypeGuard[EquityQuoteData | IndexQuoteData]:
        """Narrow `val` to a quote data type."""
        return GetQuote.is_equity_quote_data(val) or GetQuote.is_index_quote_data(val)

    @staticmethod
    def is_quote(val: object) -> TypeGuard[Quote]:
        """Narrow `val` to `Quote` type."""
        return is_json(val) and all(
            GetQuote.is_quote_data(data) for data in val.values()
        )

    def get(self, symbol: str) -> Quote:
        """Make a request to the get quote endpoint."""
        res = self._get(self._endpoint(symbol=symbol))
        quote = res.json()
        assert GetQuote.is_quote(quote)
        return quote
