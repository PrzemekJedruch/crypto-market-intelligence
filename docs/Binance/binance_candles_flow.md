# Binance Candles Data Flow

This document explains the complete candle-data path inside `BinanceExchange`, from a public `get_candles()` call, through pagination and HTTP communication, back to normalized internal `Candle` models.

The key idea is that the candle flow is split into several layers, and each layer has one clear responsibility.

---

## High-Level Flow

```text
get_candles()
    ↓
_get_all_candles_raw()
    ↓
_get_candles_raw()
    ↓
_get_json()
    ↓
Binance API
```

Then the data comes back:

```text
Binance API
    ↓
raw JSON
    ↓
_get_candles_raw()
    ↓
_get_all_candles_raw()
    ↓
get_candles()
    ↓
Candle(...)
    ↓
list[Candle]
```

---

## 1. `get_candles()` — Public Method

`get_candles()` is the method that the rest of the application should use.

Example:

```python
candles = exchange.get_candles(
    symbol="BTCUSDT",
    market_type=MarketType.PERPETUAL,
    interval="1m",
    start_time=start,
    end_time=end,
)
```

The rest of the application should not need to know:

- which Binance endpoint is used,
- how Binance JSON is structured,
- how pagination works,
- how timestamps are converted,
- how request errors are handled.

`get_candles()` simply means:

> Return normalized candle data for this symbol and time range.

Inside the method, the input is normalized first.

```python
normalized_start = self._normalize_timestamp(start_time)
normalized_end = self._normalize_timestamp(end_time)
normalized_symbol = self._normalize_symbol(symbol)
```

Symbol normalization:

```text
" btcusdt "
    ↓
"BTCUSDT"
```

Timestamp normalization:

```text
datetime in any supported timezone
    ↓
UTC datetime
```

Then the UTC `datetime` values are converted into Unix timestamps in milliseconds:

```python
int(normalized_start.timestamp() * 1000)
```

Example:

```text
2026-08-15 10:00:00 UTC
        ↓
1786788000000
```

Binance receives integer timestamps, not Python `datetime` objects.

After normalization, `get_candles()` calls:

```python
_get_all_candles_raw()
```

It does not call `_get_candles_raw()` directly because one Binance request may not be enough to download the whole requested range.

---

## 2. What Does `raw` Mean?

In this project, `raw` means:

> Data in the external exchange API format, before conversion into internal project models.

A raw Binance candle looks like a positional list:

```python
[
    1786637160000,
    "63465.00",
    "63484.10",
    "63431.00",
    "63431.10",
    "149.946",
    ...
]
```

This is still Binance-specific data.

It is not yet:

```python
Candle(
    exchange=Exchange.BINANCE,
    symbol="BTCUSDT",
    ...
)
```

So the distinction is:

```text
RAW
=
exchange-specific API format
```

and:

```text
NORMALIZED
=
common internal project format
```

Example:

```text
Binance raw:

[
    1786637160000,
    "63465.00",
    "63484.10",
    ...
]


Internal normalized model:

Candle(
    exchange=Exchange.BINANCE,
    market_type=MarketType.PERPETUAL,
    symbol="BTCUSDT",
    timestamp=...,
    open=63465.0,
    high=63484.1,
    ...
)
```

This separation is important because every exchange can return a different API structure, while the rest of the application should work with the same `Candle` model.

---

## 3. `_get_all_candles_raw()` — Download the Full Range

`_get_all_candles_raw()` is responsible for:

> Downloading all raw candles for the requested time range, even if multiple API requests are required.

For example, if the application needs:

```text
10,000 candles
```

and one request downloads at most:

```text
1,000 candles
```

then the client must perform multiple requests:

```text
request 1 → 1000
request 2 → 1000
request 3 → 1000
...
```

That logic belongs in:

```python
_get_all_candles_raw()
```

The method first converts the candle interval into milliseconds:

```python
interval_ms = self._interval_to_milliseconds(interval)
```

This is necessary because pagination must know where the next candle starts.

---

## 4. `_interval_to_milliseconds()` — Convert Candle Interval

This helper converts a Binance candle interval into milliseconds.

Example:

```python
"1m" → 60_000
"5m" → 300_000
"1h" → 3_600_000
"1d" → 86_400_000
```

Why is this needed?

Assume the final candle from the first page starts at:

```text
10:59
```

and the interval is:

```text
1m
```

Then the next candle starts at:

```text
11:00
```

In code:

```python
next_start_time = last_open_time + interval_ms
```

Visual example:

```text
10:57
10:58
10:59   ← last candle from page 1
  +
1 minute
  ↓
11:00   ← first candle requested on page 2
```

This prevents the last candle from one page from being requested again on the next page.

---

## 5. Pagination Loop in `_get_all_candles_raw()`

The main pagination loop is conceptually:

```python
while current_start_time <= end_time:
```

This means:

> Keep requesting data until the requested end of the range is reached.

Inside the loop:

```python
candles = self._get_candles_raw(...)
```

At this point the flow moves one level lower.

---

## 6. `_get_candles_raw()` — One Binance Candle Request

The important difference is:

```text
_get_all_candles_raw()
```

means:

```text
download ALL required candle pages
```

while:

```text
_get_candles_raw()
```

means:

```text
perform ONE candle request
```

So the relationship looks like:

```text
_get_all_candles_raw()
        │
        ├── _get_candles_raw() → request 1
        ├── _get_candles_raw() → request 2
        ├── _get_candles_raw() → request 3
        └── ...
```

`_get_candles_raw()` builds Binance-specific request parameters:

```python
params = {
    "symbol": normalized_symbol,
    "interval": interval,
    "limit": limit,
}
```

Then, if present:

```python
params["startTime"] = start_time
params["endTime"] = end_time
```

Example:

```python
{
    "symbol": "BTCUSDT",
    "interval": "1m",
    "limit": 1000,
    "startTime": 1786788000000,
    "endTime": 1786791600000,
}
```

This method does not convert raw Binance candles into `Candle` models.

Instead, it sends the request through:

```python
_get_json()
```

---

## 7. `_get_json()` — Shared HTTP Layer

`_get_json()` is the shared HTTP communication helper.

For candle data it receives, for example:

```python
endpoint="/fapi/v1/klines"
```

and:

```python
params={...}
```

It combines:

```text
BASE_URL
+
endpoint
```

Example:

```text
https://fapi.binance.com
+
/fapi/v1/klines
```

Result:

```text
https://fapi.binance.com/fapi/v1/klines
```

Then the actual HTTP request is sent:

```python
response = requests.get(...)
```

This is the point where communication with Binance happens.

```text
_get_json()
    ↓
requests.get()
    ↓
Internet
    ↓
Binance API
```

---

## 8. Binance Response and Error Handling

Binance returns JSON, for example:

```python
[
    [
        1786637160000,
        "63465.00",
        "63484.10",
        "63431.00",
        "63431.10",
        "149.946",
        ...
    ],
    [
        ...
    ]
]
```

Before returning JSON, `_get_json()` runs:

```python
response.raise_for_status()
```

This checks whether the HTTP request succeeded.

If the request fails, for example because of:

```text
400
404
429
500
network failure
timeout-related request failure
```

the low-level `requests` exception is converted into:

```python
BinanceAPIError
```

This means the rest of the project does not need to work directly with:

```python
requests.RequestException
```

It can work with the exchange-specific:

```python
BinanceAPIError
```

If the request succeeds:

```python
return response.json()
```

and the raw Binance response starts moving back up the call chain.

---

## 9. Return to `_get_candles_raw()`

`_get_json()` returns:

```python
[
    [...],
    [...],
    [...]
]
```

`_get_candles_raw()` returns this data unchanged to the pagination layer.

Its responsibility is therefore:

```text
Binance candle endpoint parameters
+
one request
```

It does not perform full-range pagination and does not create `Candle` objects.

---

## 10. Return to `_get_all_candles_raw()`

Assume the first request returns:

```text
1000 raw candles
```

The method appends them:

```python
all_candles.extend(candles)
```

Example:

```text
all_candles:

request 1
↓
1000 records

request 2
↓
+1000 records

request 3
↓
+350 records
```

Final result:

```text
2350 raw candles
```

After every page, the method reads the open time of the last candle:

```python
last_open_time = candles[-1][0]
```

The `[0]` is used because the Binance raw candle stores open time at index `0`.

Then:

```python
next_start_time = last_open_time + interval_ms
```

This becomes the starting point of the next request.

---

## 11. When Does Candle Pagination Stop?

There are several stop conditions.

### Binance returns no data

```python
if not candles:
    break
```

This means there is nothing more to download.

### Returned page is smaller than the request limit

```python
if len(candles) < self.CANDLE_REQUEST_LIMIT:
    break
```

Example:

```text
limit = 1000
returned = 237
```

This indicates that the current requested range has been exhausted.

### Next page does not move forward

```python
if next_start_time <= current_start_time:
    break
```

This is a defensive guard against an infinite loop if unexpected data causes the timestamp not to advance.

### Requested end time is reached

The outer loop stops when:

```python
current_start_time > end_time
```

---

## 12. `_get_all_candles_raw()` Still Returns Raw Data

After pagination:

```python
return all_candles
```

The result is still Binance-specific raw data:

```python
[
    [timestamp, "open", "high", ...],
    [timestamp, "open", "high", ...],
    ...
]
```

No `Candle` models have been created yet.

---

## 13. Back to `get_candles()` — Normalization

Now `get_candles()` receives all raw candles.

This is where raw Binance data is converted into internal project models.

Example:

```python
Candle(
    exchange=self.exchange,
    market_type=market_type,
    symbol=normalized_symbol,
    timestamp=datetime.fromtimestamp(
        candle[0] / 1000,
        tz=timezone.utc,
    ),
    interval=interval,
    open=float(candle[1]),
    high=float(candle[2]),
    low=float(candle[3]),
    close=float(candle[4]),
    volume=float(candle[5]),
)
```

Example raw Binance candle:

```python
[
    1786637160000,
    "63465.00",
    "63484.10",
    "63431.00",
    "63431.10",
    "149.946",
]
```

becomes:

```python
Candle(
    exchange=Exchange.BINANCE,
    market_type=MarketType.PERPETUAL,
    symbol="BTCUSDT",
    timestamp=datetime(...),
    interval="1m",
    open=63465.0,
    high=63484.1,
    low=63431.0,
    close=63431.1,
    volume=149.946,
)
```

This step is called normalization:

```text
Binance-specific raw format
        ↓
common internal project format
```

The final return type is:

```python
list[Candle]
```

---

## Complete Candle Flow

```text
USER / SERVICE
        │
        │ requests candles
        ↓
get_candles()
        │
        ├── normalize symbol
        ├── normalize timestamps
        ├── convert datetime → milliseconds
        ↓
_get_all_candles_raw()
        │
        ├── convert interval → milliseconds
        ├── control pagination
        ↓
_get_candles_raw()
        │
        ├── build Binance params
        ├── symbol
        ├── interval
        ├── limit
        ├── startTime
        └── endTime
        ↓
_get_json()
        │
        ├── requests.get()
        ├── timeout
        ├── raise_for_status()
        ├── BinanceAPIError
        └── response.json()
        ↓
BINANCE API
        │
        ↓
RAW JSON
        │
        ↓
_get_candles_raw()
        │
        ↓
_get_all_candles_raw()
        │
        ├── collect page
        ├── calculate next start
        ├── request next page
        └── repeat
        ↓
all RAW candles
        │
        ↓
get_candles()
        │
        ├── convert strings → floats
        ├── convert milliseconds → UTC datetime
        └── create Candle(...)
        ↓
list[Candle]
        │
        ↓
REST OF APPLICATION
```

---

## Responsibility Summary

```text
get_candles()
=
what the application wants to receive
```

```text
_get_all_candles_raw()
=
how many requests are needed to download the full range
```

```text
_get_candles_raw()
=
how one Binance candle request is built
```

```text
_get_json()
=
how HTTP communication with Binance is performed
```

```text
Candle(...)
=
how Binance raw data becomes the internal project format
```

---

## Why This Separation Matters

This design keeps responsibilities separate:

```text
pagination
≠
HTTP
≠
normalization
≠
application-facing API
```

As a result:

- pagination can change without changing model conversion,
- HTTP error handling can change in one place,
- Binance-specific JSON stays inside the exchange layer,
- the rest of the application works with `Candle`,
- future exchange integrations can return the same internal model even if their API response is completely different.
