"""
TD Ameritrade API get user principals endpoint.

https://developer.tdameritrade.com/user-principal/apis/get/userprincipals-0
"""

from collections.abc import Iterable, Sequence
from typing import Optional, TypedDict, TypeGuard

from pytyu.json import is_json_schema

from .base import Request


class UserPrincipalsStreamerInfoData(TypedDict):
    """User principals streamer info data type."""

    streamerBinaryUrl: str
    streamerSocketUrl: str
    token: str
    tokenTimestamp: str
    userGroup: str
    accessLevel: str
    acl: str
    appId: str


class UserPrincipalsQuotesData(TypedDict):
    """User principals quotes data type."""

    isNyseDelayed: bool
    isNasdaqDelayed: bool
    isOpraDelayed: bool
    isAmexDelayed: bool
    isCmeDelayed: bool
    isIceDelayed: bool
    isForexDelayed: bool


class UserPrincipalsStreamerSubKeysData(TypedDict):
    """User principals streamer subscription keys data type."""

    key: str


class UserPrincipalsStreamerSubData(TypedDict):
    """User principals streamer subscriptions data type."""

    keys: Sequence[UserPrincipalsStreamerSubKeysData]


class UserPrincipalsExchAgmntsData(TypedDict):
    """User principals exchange agreements data type."""

    NASDAQ_EXCHANGE_AGREEMENT: str
    OPRA_EXCHANGE_AGREEMENT: str
    NYSE_EXCHANGE_AGREEMENT: str


class UserPrincipalsAuthData(TypedDict):
    """User principals authorizations data type."""

    apex: bool
    levelTwoQuotes: bool
    stockTrading: bool
    marginTrading: bool
    streamingNews: bool
    optionTradingLevel: str
    streamerAccess: bool
    advancedMargin: bool
    scottradeAccount: bool
    autoPositionEffect: bool


class UserPrincipalsAcctData(TypedDict):
    """User principals account data type."""

    accountId: str
    displayName: str
    accountCdDomainId: str
    company: str
    segment: str
    acl: str
    authorizations: UserPrincipalsAuthData


class UserPrincipals(TypedDict):
    """User principals response type."""

    userId: str
    userCdDomainId: str
    primaryAccountId: str
    lastLoginTime: str
    tokenExpirationTime: str
    loginTime: str
    accessLevel: str
    stalePassword: bool
    professionalStatus: str
    streamerInfo: Optional[UserPrincipalsStreamerInfoData]
    quotes: UserPrincipalsQuotesData
    streamerSubscriptionKeys: Optional[UserPrincipalsStreamerSubData]
    exchangeAgreements: UserPrincipalsExchAgmntsData
    accounts: Sequence[UserPrincipalsAcctData]


class GetUserPrincipals(Request):
    """Make requests to the get quote endpoint."""

    @staticmethod
    def path() -> str:
        """Path relative to the base URL of the endpoint."""
        return "v1/userprincipals"

    @staticmethod
    def is_user_principals(val: object) -> TypeGuard[UserPrincipals]:
        """Narrow `val` to `UserPrincipals` type."""
        return is_json_schema(val, UserPrincipals)

    def get(self, fields: Optional[Iterable[str]] = None) -> UserPrincipals:
        """Make a request to the get user principals endpoint."""
        params = {}
        if fields:
            params["fields"] = fields
        res = self._get(self._endpoint(params=params))
        user_principals = res.json()
        assert GetUserPrincipals.is_user_principals(user_principals)
        return user_principals
