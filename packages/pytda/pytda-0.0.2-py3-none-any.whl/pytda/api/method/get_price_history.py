"""
TD Ameritrade API get price history endpoint.

https://developer.tdameritrade.com/price-history/apis/get/marketdata/{symbol}/pricehistory
"""

from collections.abc import MutableMapping, Sequence
from typing import Literal, Optional, TypedDict, TypeGuard

from dateutil import parser
from pytyu.json import is_json_schema

from .base import Request


Period = Literal["day", "month", "year", "ytd"]
"""Price history period type."""

Frequency = Literal["minute", "daily", "weekly", "monthly"]
"""Price history frequency type."""


# We have to use the alternative syntax because some keys are not valid identifiers.
# https://peps.python.org/pep-0589/#alternative-syntax
Candle = TypedDict(
    "Candle",
    {
        "datetime": int,
        "open": float,
        "high": float,
        "low": float,
        "close": float,
        "volume": int,
    },
)
"""Price history candle type."""


class CandleList(TypedDict):
    """Price history candle list type."""

    symbol: str
    empty: bool
    candles: Sequence[Candle]


class GetPriceHistory(Request):
    """Make requests to the get price history endpoint."""

    @staticmethod
    def path() -> str:
        """Path relative to the base URL of the endpoint."""
        return "v1/marketdata/{symbol}/pricehistory"

    @staticmethod
    def is_candle_list(val: object) -> TypeGuard[CandleList]:
        """Narrow `val` to `CandleList` type."""
        return is_json_schema(val, CandleList)

    def get(
        self,
        symbol: str,
        period_type: Period = "day",
        period: Optional[int] = None,
        freq_type: Optional[Frequency] = None,
        freq: Optional[int] = None,
        end_date: Optional[str] = None,
        start_date: Optional[str] = None,
        need_ext_hours: Optional[bool] = None,
    ) -> CandleList:
        """Make a request to the get price history endpoint."""
        params: MutableMapping[str, str] = {"periodType": period_type}

        if period is not None:
            params["period"] = str(period)
        if freq_type is not None:
            params["frequencyType"] = freq_type
        if freq is not None:
            params["frequency"] = str(freq)
        if end_date is not None:
            params["endDate"] = str(Request._dt_to_ms(parser.parse(end_date)))
        if start_date is not None:
            params["starDate"] = str(Request._dt_to_ms(parser.parse(start_date)))
        if need_ext_hours is not None:
            params["needExtendedHours"] = str(need_ext_hours).lower()

        res = self._get(self._endpoint(symbol=symbol, params=params))
        candle_list = res.json()
        assert GetPriceHistory.is_candle_list(candle_list)
        return candle_list
