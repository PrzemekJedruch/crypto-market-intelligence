# Crypto Market Intelligence — Data Model

## 1. Purpose

This document defines the normalized market data models used by the Crypto Market Intelligence project.

The goal is to provide one consistent internal representation of market data regardless of which exchange provides it.

Exchange-specific API responses must be converted into these common models before the rest of the application uses them.

Current model hierarchy:

```text
BaseMarketData
├── Candle
├── Trade
├── OpenInterest
└── FundingRate
```

Supporting enums:

- `Exchange`
- `MarketType`
- `TradeSide`

---

## 2. General Data Model Rules

All market data models should follow these principles:

- Use consistent field names across exchanges.
- Store timestamps in UTC.
- Keep raw market values separate from derived analytical features.
- Do not place API communication logic inside data models.
- Do not place database logic inside data models.
- Do not calculate indicators inside the base models.
- Preserve enough source information to identify where each record came from.
- Put only genuinely shared attributes in `BaseMarketData`.

Derived values such as:

- CVD
- Open Interest Change
- Relative Volume
- Funding Pressure
- Volatility
- Market Score

will be created later by the feature layer.

---

## 3. Supporting Enums

### 3.1 Exchange

Represents the source exchange.

Initial values:

```text
BINANCE
BYBIT
OKX
COINBASE
KRAKEN
```

### 3.2 MarketType

Represents the type of market.

Values:

```text
SPOT
PERPETUAL
FUTURES
```

Definitions:

- `SPOT` — direct asset market.
- `PERPETUAL` — derivative contract without an expiration date.
- `FUTURES` — derivative contract with an expiration date.

### 3.3 TradeSide

Represents the aggressor side of an executed trade.

Values:

```text
BUY
SELL
```

Definitions:

- `BUY` — the aggressive buyer removed liquidity from the ask side.
- `SELL` — the aggressive seller removed liquidity from the bid side.

---

## 4. BaseMarketData Model

### Purpose

`BaseMarketData` is the shared parent model for all normalized market data records.

It contains the fields that are common to candles, trades, Open Interest, and funding rate observations.

### Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| `exchange` | `Exchange` | Yes | Source exchange |
| `market_type` | `MarketType` | Yes | Spot, perpetual, or futures |
| `symbol` | `str` | Yes | Trading symbol, e.g. `BTCUSDT` |
| `timestamp` | `datetime` | Yes | Market data timestamp in UTC |

### Inheritance Structure

```text
BaseMarketData
├── Candle
├── Trade
├── OpenInterest
└── FundingRate
```

### Design Rule

`BaseMarketData` contains only fields that are genuinely shared by all child models.

It should not contain:

```text
interval
price
volume
trade_id
open_interest
funding_rate
```

Those fields remain in their specialized child models.

---

## 5. Candle Model

### Purpose

Represents one OHLCV candle.

`Candle` inherits:

```text
exchange
market_type
symbol
timestamp
```

from `BaseMarketData`.

### Candle-Specific Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| `interval` | `str` | Yes | Candle timeframe, e.g. `1m`, `5m`, `1h` |
| `open` | `float` | Yes | Opening price |
| `high` | `float` | Yes | Highest price |
| `low` | `float` | Yes | Lowest price |
| `close` | `float` | Yes | Closing price |
| `volume` | `float` | Yes | Trading volume during the candle |

### Logical Identity

```text
exchange
market_type
symbol
interval
timestamp
```

---

## 6. Trade Model

### Purpose

Represents one executed market trade.

`Trade` inherits:

```text
exchange
market_type
symbol
timestamp
```

from `BaseMarketData`.

### Trade-Specific Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| `trade_id` | `int` or `str` | Yes | Exchange-provided trade identifier |
| `price` | `float` | Yes | Execution price |
| `quantity` | `float` | Yes | Base asset quantity |
| `quote_value` | `float` | Yes | Trade value in quote currency |
| `side` | `TradeSide` | Yes | Aggressor side |

### Logical Identity

```text
exchange
market_type
symbol
trade_id
```

---

## 7. OpenInterest Model

### Purpose

Represents one Open Interest measurement for a derivatives market.

`OpenInterest` inherits:

```text
exchange
market_type
symbol
timestamp
```

from `BaseMarketData`.

### Open-Interest-Specific Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| `open_interest` | `float` | Yes | Open Interest in the exchange-provided unit |
| `open_interest_usd` | `float` | Yes | Open Interest normalized to USD/USDT |

### Logical Identity

```text
exchange
market_type
symbol
timestamp
```

### Important Note

Open Interest units may differ between exchanges.

Therefore:

- preserve the original exchange value,
- keep a normalized USD/USDT value when possible,
- perform conversion in the normalization layer.

---

## 8. FundingRate Model

### Purpose

Represents one funding rate observation for a perpetual market.

`FundingRate` inherits:

```text
exchange
market_type
symbol
timestamp
```

from `BaseMarketData`.

### Funding-Specific Fields

| Field | Type | Required | Description |
|---|---|---:|---|
| `funding_rate` | `float` | Yes | Funding rate value |
| `next_funding_time` | `datetime | None` | No | Next scheduled funding timestamp |

### Logical Identity

```text
exchange
market_type
symbol
timestamp
```

---

## 9. Relationships Between Models

```text
BaseMarketData
├── Candle
├── Trade
├── OpenInterest
└── FundingRate
       │
       ↓
Normalized Market Data
       │
       ↓
Database
       │
       ↓
Feature Engineering
```

Different models operate at different frequencies:

```text
Candles         interval-based
Trades          event-based
Open Interest   snapshot / interval-based
Funding Rate    funding-cycle-based
```

Timestamp alignment should happen later in the analytical pipeline.

---

## 10. Raw Data vs Derived Data

### Raw / Normalized Models

```text
Candle
Trade
OpenInterest
FundingRate
```

### Derived Features

```text
CVD
Volume Delta
Open Interest Change
Funding Pressure
Relative Volume
Volatility
Spot/Futures Divergence
Cross-Exchange Spread
Market Score
```

---

## 11. Database Mapping Direction

Suggested tables:

```text
candles
trades
open_interest
funding_rates
sync_state
```

Possible unique constraints:

### candles

```text
exchange + market_type + symbol + interval + timestamp
```

### trades

```text
exchange + market_type + symbol + trade_id
```

### open_interest

```text
exchange + market_type + symbol + timestamp
```

### funding_rates

```text
exchange + market_type + symbol + timestamp
```

The Python inheritance hierarchy does not require the database to use table inheritance.

---

## 12. Timestamp Standard

All timestamps inside the application should use UTC.

```text
API timestamp
    ↓
Normalizer
    ↓
UTC-aware datetime
    ↓
BaseMarketData child model
```

---

## 13. Symbol Standardization

Different exchanges may use different symbols.

Examples:

```text
Binance:  BTCUSDT
Coinbase: BTC-USD
OKX:      BTC-USDT-SWAP
```

A future `Instrument` model may contain:

```text
base_asset
quote_asset
market_type
exchange_symbol
```

This is intentionally outside the current scope.

---

## 14. Validation Direction

Basic validation may later include:

### Candle

```text
high >= open
high >= close
high >= low
low <= open
low <= close
volume >= 0
```

### Trade

```text
price > 0
quantity > 0
quote_value >= 0
```

### OpenInterest

```text
open_interest >= 0
open_interest_usd >= 0
```

### FundingRate

Funding rates may be positive, zero, or negative.

---

## 15. Future Models

Potential future models:

```text
Instrument
Ticker
OrderBookSnapshot
OrderBookLevel
Liquidation
MarketState
FeatureSnapshot
MarketSignal
Prediction
```

---

## 16. Current Scope

The current model scope is:

```text
BaseMarketData
├── Candle
├── Trade
├── OpenInterest
└── FundingRate
```

Initial market scope:

```text
Exchange: Binance
Market Type: Perpetual
Symbol: BTCUSDT
```

The next objective is:

```text
Exchange API
→ normalization
→ model
→ database
→ synchronization
```


---

## 17. Naming Conventions

The model layer follows consistent Python naming conventions.

### Files

Model files use `snake_case`:

```text
base_market_data.py
candle.py
trade.py
open_interest.py
funding_rate.py
```

### Classes

Model classes use `PascalCase`:

```text
BaseMarketData
Candle
Trade
OpenInterest
FundingRate
```

### Fields

Model fields use `snake_case`:

```text
market_type
trade_id
quote_value
open_interest
open_interest_usd
funding_rate
next_funding_time
```

The current names should remain short and domain-specific. `OpenInterest` is preferred over `OpenInterestData` because the surrounding model layer already makes the data-record meaning clear.

---

## 18. Model Testing

Basic tests should verify that each model can be constructed correctly and that inheritance from `BaseMarketData` works as expected.

Initial test file:

```text
tests/test_models.py
```

Initial test scope:

```text
BaseMarketData
Candle
Trade
OpenInterest
FundingRate
```

Tests should verify:

- inherited fields such as `exchange`, `market_type`, `symbol`, and `timestamp`,
- model-specific fields,
- enum values,
- optional fields such as `next_funding_time`,
- correct inheritance from `BaseMarketData`.

The initial tests should remain simple. Validation of market rules and exchange-specific normalization will be added later.

### Code Documentation Standard

Comments in Python code should be written in English.

Functions and methods should include concise docstrings describing their purpose.

Example:

```python
def test_base_market_data_creation():
    """Test that BaseMarketData stores all common market data fields correctly."""
```
