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

The leading underscore indicates that this is an internal helper method. It returns the raw Binance response and is not intended to be used by the rest of the application.

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

Important implementation detail:

- timestamps are numeric Unix milliseconds,
- OHLC prices are returned as strings,
- volume values are returned as strings,
- number of trades is numeric,
- the last field is currently not used by the project.

## Candle Mapping

The first internal `Candle` model uses only part of the Binance response.

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

## Raw Data vs Internal Models

The exchange layer is responsible for converting Binance-specific responses into project models.

Expected candle flow:

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

Expected trade flow:

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

The rest of the application should not depend on Binance positional arrays or Binance-specific response formats.

This keeps collectors, repositories, services, analytics, and machine-learning code exchange-independent.

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

## Testing Strategy

HTTP unit tests use `unittest.mock.patch`.

Example concept:

```text
@patch("exchanges.binance.requests.get")
```

This replaces `requests.get()` used inside `exchanges/binance.py` with a mock for the duration of the test.

The unit tests therefore verify project behavior without requiring:

- internet access,
- Binance availability,
- live API responses.

Live API checks are performed separately when validating the integration.

## Phase 3 Progress

Current Binance integration progress:

```text
[x] Connect to Binance public API
[x] Download candles
[x] Download trades
[ ] Download Open Interest
[ ] Download funding rates
[ ] Convert Binance responses into internal models
[ ] Add basic error handling
[ ] Add request limits and pagination handling
```

## Future Documentation Updates

This file should be expanded as Binance integration grows.

Add documentation for:

- Open Interest endpoint and response mapping,
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

## Design Rule

Binance-specific details belong inside the Binance exchange layer.

The rest of the project should work with normalized internal models rather than raw Binance API structures.
