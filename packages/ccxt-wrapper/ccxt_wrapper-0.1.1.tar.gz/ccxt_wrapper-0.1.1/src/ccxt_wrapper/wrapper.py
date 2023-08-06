from __future__ import annotations

import warnings
from copy import deepcopy
from typing import Any, Generic, TypeVar

from ccxt.async_support import Exchange

from .core import cast
from .dtypes import (
    Balance,
    Balances,
    Currency,
    CurrencyLimits,
    Deposit,
    Fee,
    Literal,
    Market,
    MarketLimits,
    MinMax,
    Ohlcv,
    Order,
    OrderBook,
    Precision,
    PrivateTrade,
    PublicTrade,
    Status,
    Ticker,
)

_Exchange = TypeVar("_Exchange", bound=Exchange)


def cast_market(market: dict[str, Any]) -> Market:
    market = deepcopy(market)
    for key_limits, limits in market["limits"].items():
        market["limits"][key_limits] = cast(MinMax, limits)
    if market.get("precision") is not None:
        market["precision"] = cast(Precision, market["precision"])
    if market.get("limits") is not None:
        market["limits"] = cast(MarketLimits, market["limits"])
    return cast(Market, market)


def cast_currency(currency: dict[str, Any]) -> Currency:
    currency = deepcopy(currency)
    if currency.get("limits") is not None:
        currency["limits"] = cast(CurrencyLimits, currency["limits"])
    return cast(Currency, currency)


def cast_order(order: dict[str, Any]) -> Order:
    order = deepcopy(order)
    if order.get("fee") is not None:
        order["fee"] = cast(Fee, order["fee"])
    if order.get("trades") is not None:
        order["trades"] = [cast(PrivateTrade, trade) for trade in order["trades"]]
    return cast(Order, order)


def cast_private_trade(trade: dict[str, Any]) -> PrivateTrade:
    trade = deepcopy(trade)
    if trade.get("fee") is not None:
        trade["fee"] = cast(Fee, trade["fee"])
    return cast(PrivateTrade, trade)


class CCXTWrapper(Generic[_Exchange]):

    _ex: _Exchange

    @staticmethod
    async def new(
        exchange_type: type[_Exchange],
        api_key: str | None = None,
        secret: str | None = None,
        enableRateLimit: bool = True,
        sandbox: bool = False,
        default_type: str | None = None,
        **kwargs: Any,
    ) -> "CCXTWrapper[_Exchange]":
        d: dict[str, Any] = {
            "apiKey": api_key,
            "secret": secret,
            "enableRateLimit": enableRateLimit,
        }
        if default_type is not None:
            d["options"] = {"defaultType": default_type}
        ex = exchange_type(d, **kwargs)
        ex.set_sandbox_mode(sandbox)
        await ex.load_markets()
        ex.set_sandbox_mode(sandbox)
        return CCXTWrapper(ex)

    async def __aenter__(
        self,
        exchange_type: type[_Exchange],
        api_key: str,
        secret: str,
        enableRateLimit: bool = True,
        **kwargs: Any,
    ) -> "CCXTWrapper[_Exchange]":
        return await self.new(exchange_type, api_key, secret, enableRateLimit, **kwargs)

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self._ex.close()

    def __init__(self, exchange: _Exchange):
        self._ex = exchange

    @property
    def exchange(self) -> _Exchange:
        return self._ex

    async def load_markets(
        self, reload: bool = False, params: dict[str, Any] = {}
    ) -> dict[str, Market]:
        markets = await self._ex.load_markets(reload, params)
        if isinstance(markets, list):
            return {market["symbol"]: cast_market(market) for market in markets}
        return {symbol: cast_market(market) for symbol, market in markets.items()}

    async def fetch_markets(self, params: dict[str, Any] = {}) -> dict[str, Market]:
        markets = await self._ex.fetch_markets(params)
        if isinstance(markets, list):
            return {market["symbol"]: cast_market(market) for market in markets}
        return {symbol: cast_market(market) for symbol, market in markets.items()}

    async def fetch_currencies(
        self, params: dict[str, Any] = {}
    ) -> dict[str, Currency] | None:
        currencies = await self._ex.fetch_currencies(params)
        if currencies is None:
            return None
        return {code: cast_currency(currency) for code, currency in currencies.items()}

    async def fetch_ticker(self, symbol: str, params: dict[str, Any] = {}) -> Ticker:
        ticker = await self._ex.fetch_ticker(symbol, params)
        return cast(Ticker, ticker)

    async def fetch_tickers(
        self, symbols: list[str], params: dict[str, Any] = {}
    ) -> dict[str, Ticker] | None:
        tickers = await self._ex.fetch_tickers(symbols, params)
        if isinstance(tickers, list):
            return {ticker["symbol"]: cast(Ticker, ticker) for ticker in tickers}
        if isinstance(tickers, dict):
            return {symbol: cast(Ticker, ticker) for symbol, ticker in tickers.items()}
        return None

    async def fetch_trades(
        self,
        symbol: str,
        since: int | None = None,
        limit: int | None = None,
        params: dict[str, Any] = {},
    ) -> list[PublicTrade]:
        trades = await self._ex.fetch_trades(symbol, since, limit, params)
        return [cast(PublicTrade, trade) for trade in trades]

    async def fetch_order_book(
        self, symbol: str, limit: int | None = None, params: dict[str, Any] = {}
    ) -> OrderBook:
        order_book = await self._ex.fetch_order_book(symbol, limit, params)
        return cast(OrderBook, order_book)

    async def fetch_ohlcv(
        self,
        symbol: str,
        timeframe: str = "1m",
        since: int | None = None,
        limit: int | None = None,
        params: dict[str, Any] = {},
    ) -> Ohlcv:
        ohlcvs = await self._ex.fetch_ohlcv(symbol, timeframe, since, limit, params)
        return [tuple(ohlcv) for ohlcv in ohlcvs]  # type: ignore

    async def fetch_status(self, params: dict[str, Any] = {}) -> Status:
        status = await self._ex.fetch_status(params)
        return cast(Status, status)

    async def fetch_balance(self, params: dict[str, Any] = {}) -> Balances:
        balance = await self._ex.fetch_balance(params)
        res = cast(Balances, balance)
        for key, value in balance.items():
            if key in ["info", "free", "used", "total"]:
                continue
            if not isinstance(value, dict):
                warnings.warn(RuntimeWarning(f"Unexpected type for key {key}"))
                continue
            res[key] = cast(Balance, value)
        return res

    async def create_order(
        self,
        symbol: str,
        type: Literal["market", "limit"],
        side: Literal["buy", "sell"],
        amount: float,
        price: float | None = None,
        params: dict[str, Any] = {},
    ) -> Order:
        order = await self._ex.create_order(symbol, type, side, amount, price, params)
        return cast_order(order)

    async def cancel_order(
        self, id: str, symbol: str | None = None, params: dict[str, Any] = {}
    ) -> Order:
        order = await self._ex.cancel_order(id, symbol, params)
        return cast_order(order)

    async def fetch_order(
        self, id: str, symbol: str | None = None, params: dict[str, Any] = {}
    ) -> Order:
        order = await self._ex.fetch_order(id, symbol, params)
        return cast_order(order)

    async def fetch_orders(
        self,
        symbol: str | None = None,
        since: int | None = None,
        limit: int | None = None,
        params: dict[str, Any] = {},
    ) -> list[Order]:
        orders = await self._ex.fetch_orders(symbol, since, limit, params)
        return [cast_order(order) for order in orders]

    async def fetch_open_orders(
        self,
        symbol: str | None = None,
        since: int | None = None,
        limit: int | None = None,
        params: dict[str, Any] = {},
    ) -> list[Order]:
        orders = await self._ex.fetch_open_orders(symbol, since, limit, params)
        return [cast_order(order) for order in orders]

    async def fetch_closed_orders(
        self,
        symbol: str | None = None,
        since: int | None = None,
        limit: int | None = None,
        params: dict[str, Any] = {},
    ) -> list[Order]:
        orders = await self._ex.fetch_closed_orders(symbol, since, limit, params)
        return [cast_order(order) for order in orders]

    async def fetch_my_trades(
        self,
        symbol: str | None = None,
        since: int | None = None,
        limit: int | None = None,
        params: dict[str, Any] = {},
    ) -> list[PrivateTrade]:
        trades = await self._ex.fetch_my_trades(symbol, since, limit, params)
        return [cast_private_trade(trade) for trade in trades]

    async def deposit(
        self,
        code: str,
        amount: float,
        address: str,
        tag: str | None = None,
        params: dict[str, Any] = {},
    ) -> Deposit:
        deposit = self._ex.deposit(code, amount, address, tag, params)
        return cast(Deposit, deposit)

    async def withdraw(
        self,
        code: str,
        amount: float,
        address: str,
        tag: str | None = None,
        params: dict[str, Any] = {},
    ) -> Any:
        withdraw = await self._ex.withdraw(code, amount, address, tag, params)
        return withdraw

    """{
    'id':   'exchange'                   // lowercase string exchange id
    'name': 'Exchange'                   // human-readable string
    'countries': [ 'US', 'CN', 'EU' ],   // array of ISO country codes
    'urls': {
        'api': 'https://api.example.com/data',  // string or dictionary of base API URLs
        'www': 'https://www.example.com'        // string website URL
        'doc': 'https://docs.example.com/api',  // string URL or array of URLs
    },
    'version':         'v1',             // string ending with digits
    'api':             { ... },          // dictionary of api endpoints
    'has': {                             // exchange capabilities
        'CORS': false,
        'publicAPI': true,
        'privateAPI': true,
        'cancelOrder': true,
        'createDepositAddress': false,
        'createOrder': true,
        'fetchBalance': true,
        'fetchCanceledOrders': false,
        'fetchClosedOrder': false,
        'fetchClosedOrders': false,
        'fetchCurrencies': false,
        'fetchDepositAddress': false,
        'fetchMarkets': true,
        'fetchMyTrades': false,
        'fetchOHLCV': false,
        'fetchOpenOrder': false,
        'fetchOpenOrders': false,
        'fetchOrder': false,
        'fetchOrderBook': true,
        'fetchOrders': false,
        'fetchStatus': 'emulated',
        'fetchTicker': true,
        'fetchTickers': false,
        'fetchBidsAsks': false,
        'fetchTrades': true,
        'withdraw': false,
    },
    'timeframes': {
    // empty if the exchange.has['fetchOHLCV'] !== true
        '1m': '1minute',
        '1h': '1hour',
        '1d': '1day',
        '1M': '1month',
        '1y': '1year',
    },
    'timeout':           10000,          // number in milliseconds
    'rateLimit':         2000,           // number in milliseconds
    'userAgent':        'ccxt/1.1.1 ...' // string, HTTP User-Agent header
    'verbose':           false,          // boolean, output error details
    'markets':          { ... }          // dictionary of markets/pairs by symbol
    'symbols':          [ ... ]          // sorted list of string symbols (traded pairs)
    'currencies':       { ... }          // dictionary of currencies by currency code
    'markets_by_id':    { ... },         // dictionary of dictionaries (markets) by id
    'currencies_by_id': { ... },         // dictionary of dictionaries (markets) by id
    'apiKey':   '92560ffae9b8a0421...',  // string public apiKey (ASCII, hex, Base64
    , ...)
    'secret':   '9aHjPmW+EtRRKN/Oi...'   // string private secret key
    'password': '6kszf4aci8r',           // string password
    'uid':      '123456',                // string user id
    'options':          { ... },         // exchange-specific options
    // ... other properties here ...
}"""

    @property
    def id(self) -> str:
        """Lowercase string exchange id."""
        return self._ex.id

    @property
    def name(self) -> str:
        """Human-readable string."""
        return self._ex.name

    @property
    def countries(self) -> list[str]:
        """Array of ISO country codes."""
        return self._ex.countries

    @property
    def urls(self) -> dict[str, str]:
        """Dictionary of base API URLs."""
        return self._ex.urls

    @property
    def version(self) -> str:
        """String ending with digits."""
        return self._ex.version

    @property
    def api(self) -> dict[str, dict[str, str]]:
        """Dictionary of api endpoints."""
        return self._ex.api

    @property
    def has(self) -> dict[str, bool]:
        """Exchange capabilities."""
        return self._ex.has

    @property
    def timeframes(self) -> dict[str, str]:
        """Empty if the exchange.has['fetchOHLCV'] !== true."""
        return self._ex.timeframes

    @property
    def timeout(self) -> int:
        """Number in milliseconds."""
        return self._ex.timeout

    @property
    def rateLimit(self) -> int:
        """Number in milliseconds."""
        return self._ex.rateLimit

    @property
    def userAgent(self) -> str:
        """HTTP User-Agent header."""
        return self._ex.userAgent

    @property
    def verbose(self) -> bool:
        """Output error details."""
        return self._ex.verbose

    @property
    def markets(self) -> dict[str, Market]:
        """Dictionary of markets/pairs by symbol."""
        return {
            symbol: cast_market(market) for symbol, market in self._ex.markets.items()
        }

    @property
    def symbols(self) -> list[str]:
        """Sorted list of string symbols (traded pairs)."""
        return self._ex.symbols

    @property
    def currencies(self) -> dict[str, Currency]:
        """Dictionary of currencies by currency code."""
        return {
            code: cast_currency(currency)
            for code, currency in self._ex.currencies.items()
        }

    @property
    def markets_by_id(self) -> dict[str, Market]:
        """Dictionary of dictionaries (markets) by id."""
        return {
            id: cast_market(market) for id, market in self._ex.markets_by_id.items()
        }

    @property
    def currencies_by_id(self) -> dict[str, Currency]:
        """Dictionary of dictionaries (markets) by id."""
        return {
            id: cast_currency(currency)
            for id, currency in self._ex.currencies_by_id.items()
        }

    @property
    def apiKey(self) -> str:
        """Public apiKey (ASCII, hex, Base64, ...)."""
        return self._ex.apiKey

    @property
    def secret(self) -> str:
        """Private secret key."""
        return self._ex.secret

    @property
    def password(self) -> str:
        """Password."""
        return self._ex.password

    @property
    def uid(self) -> str:
        """User id."""
        return self._ex.uid

    @property
    def options(self) -> dict[str, Any]:
        """Exchange-specific options."""
        return self._ex.options
