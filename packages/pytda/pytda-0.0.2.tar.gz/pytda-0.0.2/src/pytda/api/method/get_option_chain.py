"""
TD Ameritrade API get option chain endpoint.

https://developer.tdameritrade.com/option-chains/apis/get/marketdata/chains
"""

from collections.abc import Mapping, MutableMapping
from typing import Literal, Optional, TypedDict, TypeGuard

from pytyu.json import is_json_schema

from .base import Request

ContractType = Literal["CALL", "PUT", "ALL"]
"""Option chain contract type."""

Strategy = Literal[
    "SINGLE",
    "ANALYTICAL",
    "COVERED",
    "VERTICAL",
    "CALENDAR",
    "STRANGLE",
    "STRADDLE",
    "BUTTERFLY",
    "CONDOR",
    "DIAGONAL",
    "COLLAR",
    "ROLL",
]
"""Option chain strategy."""

Range = Literal["ITM", "NTM", "OTM", "SAK", "SBK", "SNK", "ALL"]
"""Option chain strike price range."""

Month = Literal[
    "JAN",
    "FEB",
    "MAR",
    "APR",
    "MAY",
    "JUN",
    "JUL",
    "AUG",
    "SEP",
    "OCT",
    "NOV",
    "DEC",
    "ALL",
]
"""Option chain month."""

OptionType = Literal["S", "NS", "ALL"]
"""Option chain type."""

Number = int | float


class OptionChain(TypedDict):
    "Option chain data type." ""

    symbol: str
    status: str
    underlying: Optional[str]
    strategy: str
    interval: Number
    isDelayed: bool
    isIndex: bool
    interestRate: float
    underlyingPrice: float
    volatility: Number
    daysToExpiration: Number
    numberOfContracts: Number
    callExpDateMap: Mapping[str, object]
    putExpDateMap: Mapping[str, object]


class GetOptionChain(Request):
    """Make requests to the get opton chain endpoint."""

    @staticmethod
    def path() -> str:
        """Path relative to the base URL of the endpoint."""
        return "v1/marketdata/chains"

    @staticmethod
    def is_option_chain(val: object) -> TypeGuard[OptionChain]:
        """Narrow `val` to `OptionChain` type."""
        return is_json_schema(val, OptionChain)

    def get(
        self,
        symbol: str,
        contract_type: Optional[ContractType] = None,
        strike_count: Optional[int] = None,
        include_quotes: Optional[bool] = None,
        strategy: Optional[Strategy] = None,
        interval: Optional[int] = None,
        strike: Optional[float] = None,
        rng: Optional[Range] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        volatility: Optional[float] = None,
        underlying_price: Optional[float] = None,
        interest_rate: Optional[float] = None,
        dte: Optional[int] = None,
        exp_month: Optional[Month] = None,
        option_type: Optional[OptionType] = None,
    ) -> OptionChain:
        """Make a request to the get option chain endpoint."""
        params: MutableMapping[str, str] = {"symbol": symbol}

        if contract_type is not None:
            params["contractType"] = contract_type
        if strike_count is not None:
            params["strikeCount"] = str(strike_count)
        if include_quotes is not None:
            params["includeQuotes"] = str(include_quotes).upper()
        if strategy is not None:
            params["strategy"] = strategy
        if interval is not None:
            params["interval"] = str(interval)
        if strike is not None:
            params["strike"] = str(strike)
        if rng is not None:
            params["range"] = rng
        if from_date is not None:
            params["fromDate"] = from_date
        if to_date is not None:
            params["toDate"] = to_date
        if volatility is not None:
            params["volatility"] = str(volatility)
        if underlying_price is not None:
            params["underlyingPrice"] = str(underlying_price)
        if interest_rate is not None:
            params["interestRate"] = str(interest_rate)
        if dte is not None:
            params["daysToExpiration"] = str(dte)
        if exp_month is not None:
            params["expMonth"] = str(exp_month)
        if option_type is not None:
            params["optionType"] = str(option_type)

        res = self._get(self._endpoint(params=params))
        option_chain = res.json()
        assert GetOptionChain.is_option_chain(option_chain)
        return option_chain
