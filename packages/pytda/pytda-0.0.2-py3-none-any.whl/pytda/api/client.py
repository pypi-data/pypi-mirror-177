"""Client to make requests to the TD Ameritrade non-streaming API."""

__all__ = [
    "Candle",
    "CandleList",
    "GetOptionChain",
    "GetPriceHistory",
    "GetQuote",
    "GetQuotes",
    "GetUserPrincipals",
    "OptionChain",
    "Quote",
    "UserPrincipals",
]

from ..auth import Auth
from .method.get_option_chain import GetOptionChain, OptionChain
from .method.get_price_history import GetPriceHistory, CandleList, Candle
from .method.get_quote import GetQuote, Quote
from .method.get_quotes import GetQuotes
from .method.get_user_principals import GetUserPrincipals, UserPrincipals


class Client:  # pylint: disable=too-few-public-methods
    """Make API requests."""

    def __init__(self, auth: Auth) -> None:
        self.auth = auth
        self.get_option_chain = GetOptionChain(auth).get
        self.get_price_history = GetPriceHistory(auth).get
        self.get_quote = GetQuote(auth).get
        self.get_quotes = GetQuotes(auth).get
        self.get_user_principals = GetUserPrincipals(auth).get
