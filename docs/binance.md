# Binance Integration

This document describes Binance-specific implementation details used by the Crypto Market Intelligence project.

The purpose of this file is to document exchange-specific behavior that should remain isolated inside `BinanceExchange`.

## Market

The initial Binance integration uses:

```text
Binance USD-M Futures
```

The first supported market type is:

```text
PERPETUAL
```

Initial development symbol:

```text
BTCUSDT
```

## Base URL

```text
https://fapi.binance.com
```

This base URL is used for Binance USD-M Futures public market data endpoints.

## Connectivity

The API connection can be checked with:

```text
GET /fapi/v1/ping
```

The project exposes this check through:

```python
BinanceExchange.ping()
```

A successful request returns `True`.

Unit tests mock the HTTP request so that the test suite does not depend on an active internet connection or Binance availability.

Live connectivity has also been verified manually against the Binance public API.

## Internal Symbol Format

The project uses normalized symbols in uppercase alphanumeric format without separators.

Examples:

```text
"btcusdt"    -> "BTCUSDT"
" BTCUSDT "  -> "BTCUSDT"
"BTC-USDT"   -> ValueError
"BTC/USDT"   -> ValueError
```

Exchange-specific symbol conversion should remain inside the relevant exchange client.

For Binance USD-M Futures, the internal format already matches symbols such as:

```text
BTCUSDT
ETHUSDT
```

## Timestamp Standard

All timestamps inside the application must be timezone-aware and normalized to UTC.

Binance market-data timestamps are returned as Unix timestamps in milliseconds.

Example:

```text
1786637160000
```

Before creating internal models, these timestamps must be converted into timezone-aware UTC `datetime` objects.

General conversion concept:

```text
Binance milliseconds
        ↓
Unix timestamp in seconds
        ↓
UTC datetime
```

Naive Python `datetime` values without timezone information are rejected by `BaseExchange`.

---

## Candles

### Endpoint

Raw candle data is downloaded from:

```text
GET /fapi/v1/klines
```

Current project method:

```python
BinanceExchange._get_candles_raw()
```

The leading underscore indicates that this is an internal helper method. It returns the raw Binance response and is not intended to be used directly by the rest of the application.

The future public method:

```python
BinanceExchange.get_candles()
```

will return normalized internal `Candle` models.

### Request Parameters

Currently used parameters:

```text
symbol
interval
limit
```

Example:

```text
symbol   = BTCUSDT
interval = 1m
limit    = 5
```

### Raw Binance Kline Structure

A Binance kline is returned as a positional list.

Example:

```text
[
    1786637160000,
    "63465.00",
    "63484.10",
    "63431.00",
    "63431.10",
    "149.946",
    1786637219999,
    "9515860.53600",
    2530,
    "106.039",
    "6729645.42100",
    "0"
]
```

Field positions:

```text
[0]  Open time
[1]  Open price
[2]  High price
[3]  Low price
[4]  Close price
[5]  Volume
[6]  Close time
[7]  Quote asset volume
[8]  Number of trades
[9]  Taker buy base asset volume
[10] Taker buy quote asset volume
[11] Ignore
```

Important implementation details:

- timestamps are numeric Unix milliseconds,
- OHLC prices are returned as strings,
- volume values are returned as strings,
- number of trades is numeric,
- the final field is currently not used by the project.

### Candle Mapping

The initial internal `Candle` model uses only part of the Binance response.

```text
Binance response        Internal Candle
------------------------------------------------
[0]  Open time       -> timestamp
[1]  Open price      -> open
[2]  High price      -> high
[3]  Low price       -> low
[4]  Close price     -> close
[5]  Volume          -> volume

Exchange.BINANCE     -> exchange
MarketType.PERPETUAL -> market_type
requested symbol     -> symbol
requested interval   -> interval
```

Before creating `Candle`, Binance values must be normalized:

```text
timestamp -> timezone-aware UTC datetime
open      -> float
high      -> float
low       -> float
close     -> float
volume    -> float
```

Fields such as quote volume, trade count, and taker-buy volume are not currently stored in the base `Candle` model.

They may become useful later for feature engineering and can be added deliberately if the data model requires them.

---

## Trades

### Endpoint

Raw aggregate trade data is downloaded from:

```text
GET /fapi/v1/aggTrades
```

Current project method:

```python
BinanceExchange._get_trades_raw()
```

This method returns the raw Binance aggregate-trade response.

The future public method:

```python
BinanceExchange.get_trades()
```

will convert the raw response into normalized internal `Trade` models.

### Request Parameters

Currently used parameters:

```text
symbol
limit
```

Example:

```text
symbol = BTCUSDT
limit  = 5
```

### Raw Binance Aggregate Trade Structure

Example response record observed during live testing:

```text
{
    "a": 3407848248,
    "p": "62912.60",
    "q": "0.113",
    "nq": "0.113",
    "f": 7970054172,
    "l": 7970054174,
    "T": 1786639477827,
    "m": false
}
```

Relevant fields:

```text
a  -> aggregate trade ID
p  -> execution price
q  -> quantity
f  -> first underlying trade ID
l  -> last underlying trade ID
T  -> trade time in Unix milliseconds
m  -> whether the buyer was the maker
```

An additional field was observed in the live response:

```text
nq
```

The project does not currently depend on `nq`. It should remain ignored unless its purpose is explicitly required by the internal data model.

### Aggressor Side Mapping

The internal `Trade.side` represents the aggressor/taker side.

The Binance `m` field is interpreted as:

```text
m = False
buyer is not the maker
buyer is the taker/aggressor
-> TradeSide.BUY

m = True
buyer is the maker
seller is the taker/aggressor
-> TradeSide.SELL
```

### Trade Mapping

Planned mapping:

```text
Binance                 Internal Trade
------------------------------------------------
a                    -> trade_id
p                    -> price
q                    -> quantity
p * q                -> quote_value
T                    -> timestamp
m=False              -> TradeSide.BUY
m=True               -> TradeSide.SELL

Exchange.BINANCE     -> exchange
MarketType.PERPETUAL -> market_type
requested symbol     -> symbol
```

Before creating `Trade`, values must be normalized:

```text
trade_id    -> int
price       -> float
quantity    -> float
quote_value -> float
timestamp   -> timezone-aware UTC datetime
side        -> TradeSide
```

---

## Open Interest

### Endpoint

Historical Open Interest data is downloaded from:

```text
GET /futures/data/openInterestHist
```

Current project method:

```python
BinanceExchange._get_open_interest_raw()
```

This method returns the raw Binance response.

The future public method:

```python
BinanceExchange.get_open_interest()
```

will convert the response into normalized internal `OpenInterest` models.

### Request Parameters

Currently used parameters:

```text
symbol
period
limit
```

Example:

```text
symbol = BTCUSDT
period = 5m
limit  = 5
```

### Raw Binance Open Interest Structure

Example response record observed during live testing:

```text
{
    "symbol": "BTCUSDT",
    "sumOpenInterest": "109816.19100000",
    "sumOpenInterestValue": "6921956114.35020000",
    "CMCCirculatingSupply": "20069371.00000000",
    "timestamp": 1786640100000
}
```

Fields used by the project:

```text
symbol                 -> market symbol
sumOpenInterest        -> total Open Interest
sumOpenInterestValue   -> Open Interest value
timestamp              -> Unix timestamp in milliseconds
```

Additional field returned by the endpoint:

```text
CMCCirculatingSupply
```

This field is not currently stored in the internal `OpenInterest` model.

For:

```text
period = 5m
```

consecutive timestamps are separated by:

```text
300000 ms = 5 minutes
```

### Open Interest Mapping

Planned mapping:

```text
Binance                     Internal OpenInterest
------------------------------------------------------
symbol                   -> symbol
sumOpenInterest          -> open_interest
sumOpenInterestValue     -> open_interest_usd
timestamp                -> timestamp

Exchange.BINANCE         -> exchange
MarketType.PERPETUAL     -> market_type
```

Before creating `OpenInterest`, values must be normalized:

```text
sumOpenInterest      -> float
sumOpenInterestValue -> float
timestamp            -> timezone-aware UTC datetime
```

---

## Raw Data vs Internal Models

The exchange layer is responsible for converting Binance-specific responses into project models.

### Candle Flow

```text
Binance API
    ↓
_get_candles_raw()
    ↓
raw Binance kline response
    ↓
get_candles()
    ↓
normalization and conversion
    ↓
list[Candle]
    ↓
rest of the application
```

### Trade Flow

```text
Binance API
    ↓
_get_trades_raw()
    ↓
raw Binance aggregate trade response
    ↓
get_trades()
    ↓
normalization and aggressor-side mapping
    ↓
list[Trade]
    ↓
rest of the application
```

### Open Interest Flow

```text
Binance API
    ↓
_get_open_interest_raw()
    ↓
raw Binance Open Interest response
    ↓
get_open_interest()
    ↓
normalization and conversion
    ↓
list[OpenInterest]
    ↓
rest of the application
```

The rest of the application should not depend on Binance positional arrays, short Binance response keys, or other Binance-specific response formats.

This keeps collectors, repositories, services, analytics, and machine-learning code exchange-independent.

---

## HTTP Request Rules

Current Binance requests use:

```text
timeout = 10 seconds
```

Responses must be validated with:

```python
response.raise_for_status()
```

This ensures HTTP errors are raised instead of being silently treated as valid market data.

More complete error handling will be added later in Phase 3.

---

## Testing Strategy

HTTP unit tests use `unittest.mock.patch`.

Example:

```text
@patch("exchanges.binance.requests.get")
```

This replaces `requests.get()` used inside `exchanges/binance.py` with a mock for the duration of the test.

The unit tests therefore verify project behavior without requiring:

- internet access,
- Binance availability,
- live API responses.

Current mocked tests cover:

- API `ping`,
- raw candle requests,
- raw aggregate trade requests,
- raw Open Interest requests.

Live API checks are performed separately when validating the integration.

Live requests have been used to verify:

- API connectivity,
- five `BTCUSDT` one-minute candles,
- five `BTCUSDT` aggregate trades,
- five `BTCUSDT` Open Interest records with a `5m` period.

---

## Phase 3 Progress

Current Binance integration progress:

```text
[x] Connect to Binance public API
[x] Download candles
[x] Download trades
[x] Download Open Interest
[ ] Download funding rates
[ ] Convert Binance responses into internal models
[ ] Add basic error handling
[ ] Add request limits and pagination handling
```

---

## Future Documentation Updates

This file should be expanded as Binance integration grows.

Add documentation for:

- funding-rate endpoint and response mapping,
- request weights and rate limits,
- pagination behavior,
- supported intervals,
- API error responses,
- retry strategy,
- missing-data handling,
- symbol discovery,
- historical synchronization behavior,
- WebSocket market data,
- any Binance-specific edge cases discovered during development.

---

## Design Rule

Binance-specific details belong inside the Binance exchange layer.

The rest of the project should work with normalized internal models rather than raw Binance API structures.
