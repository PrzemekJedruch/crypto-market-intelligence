# Crypto Market Intelligence — Architecture

## 1. Project Goal

The goal of this project is to build a modular market data platform for cryptocurrency analysis.

The first stage focuses on:

- collecting market data from multiple exchanges,
- normalizing the data into common Python models,
- storing the data in a database,
- synchronizing only missing historical data,
- preparing a clean foundation for later feature engineering, scanning, backtesting, and machine learning.

The initial data types are:

- Candles
- Trades
- Open Interest
- Funding Rate

---

## 2. Initial Project Structure

```text
crypto-market-intelligence/
│
├── README.md
├── main.py
├── config.py
│
├── models/
│   ├── __init__.py
│   ├── base_market_data.py
│   ├── candle.py
│   ├── trade.py
│   ├── open_interest.py
│   └── funding_rate.py
│
├── enums/
│   ├── __init__.py
│   ├── exchange.py
│   ├── market_type.py
│   └── trade_side.py
│
├── exchanges/
│   ├── __init__.py
│   ├── base_exchange.py
│   ├── binance.py
│   ├── bybit.py
│   └── okx.py
│
├── collectors/
│   ├── __init__.py
│   └── market_collector.py
│
├── storage/
│   ├── __init__.py
│   ├── database.py
│   ├── candle_repository.py
│   ├── trade_repository.py
│   ├── open_interest_repository.py
│   ├── funding_repository.py
│   └── sync_repository.py
│
├── services/
│   ├── __init__.py
│   └── market_data_service.py
│
└── docs/
    ├── architecture.md
    ├── data_model.md
    └── roadmap.md
```

---

## 3. Main Responsibility Rule

Each layer has one clear responsibility.

```text
Exchange API
    ↓
Exchange Client
    ↓
Collector
    ↓
Python Data Models
    ↓
Repository
    ↓
Database
```

The project should follow these rules:

- Exchange classes do not know anything about the database.
- Repository classes do not know anything about exchange APIs.
- Data models do not contain API logic.
- Services coordinate the workflow between components.
- Feature engineering will be added later and will not be mixed with raw data collection.

---

## 4. Data Models

Data models represent normalized market data.

They should contain data only and remain independent from external APIs and database implementations.

The current model hierarchy uses a small shared base class to avoid repeating common market-data fields.

```text
BaseMarketData
├── Candle
├── Trade
├── OpenInterest
└── FundingRate
```

### BaseMarketData

`BaseMarketData` contains attributes shared by all current market data models.

Fields:

```text
exchange
market_type
symbol
timestamp
```

Responsibilities:

- provide a consistent source identity for market records,
- standardize exchange, market type, symbol, and timestamp,
- reduce duplication between specialized models.

`BaseMarketData` should contain only fields that are genuinely common to all child models.

It should not contain exchange API logic, database logic, indicators, or model-specific fields.

### Candle

Represents one OHLCV candle.

Inherits from `BaseMarketData`.

Candle-specific fields:

```text
interval
open
high
low
close
volume
```

### Trade

Represents one executed market trade.

Inherits from `BaseMarketData`.

Trade-specific fields:

```text
trade_id
price
quantity
quote_value
side
```

`side` represents the aggressor side of the transaction.

### OpenInterest

Represents one Open Interest measurement.

Inherits from `BaseMarketData`.

Open-Interest-specific fields:

```text
open_interest
open_interest_usd
```

### FundingRate

Represents one funding rate measurement.

Inherits from `BaseMarketData`.

Funding-specific fields:

```text
funding_rate
next_funding_time
```

### Model Design Rule

The inheritance hierarchy is intentionally shallow.

```text
BaseMarketData
    ↓
Specialized Market Data Model
```

The project should avoid deep inheritance trees. New models should inherit from `BaseMarketData` only when they genuinely share its common market identity fields.
---

## 5. Enum Layer

Enums provide standardized values across the entire application.

### Exchange

Possible values:

```text
BINANCE
BYBIT
OKX
COINBASE
KRAKEN
```

### MarketType

Possible values:

```text
SPOT
PERPETUAL
FUTURES
```

### TradeSide

Possible values:

```text
BUY
SELL
```

---

## 6. Exchange Layer

The exchange layer is responsible only for communication with external exchange APIs.

Every exchange implementation should expose the same public interface.

Examples:

```text
BinanceExchange
BybitExchange
OKXExchange
```

Each implementation converts exchange-specific API responses into the common project data models derived from `BaseMarketData`.

---

## 7. BaseExchange Contract

`BaseExchange` defines the methods that every supported exchange should implement.

It is the common contract for all exchange clients.

### Required methods

#### get_candles

Purpose:

Fetch historical OHLCV candles.

Inputs:

```text
symbol
interval
start_time
end_time
limit
```

Returns:

```text
list[Candle]
```

---

#### get_trades

Purpose:

Fetch executed trades for a symbol.

Inputs:

```text
symbol
start_time
end_time
limit
```

Returns:

```text
list[Trade]
```

---

#### get_open_interest

Purpose:

Fetch Open Interest data.

Inputs:

```text
symbol
start_time
end_time
interval
```

Returns:

```text
list[OpenInterest]
```

or, for a current snapshot:

```text
OpenInterest
```

The exact behavior should be standardized before implementation.

---

#### get_funding_rate

Purpose:

Fetch funding rate history.

Inputs:

```text
symbol
start_time
end_time
limit
```

Returns:

```text
list[FundingRate]
```

---

#### get_supported_symbols

Purpose:

Return symbols available on the selected exchange and market type.

Inputs:

```text
market_type
```

Returns:

```text
list[str]
```

Example:

```text
BTCUSDT
ETHUSDT
SOLUSDT
```

---

## 8. Exchange Implementations

### BinanceExchange

Responsibilities:

- communicate with Binance APIs,
- handle Binance-specific parameters,
- parse Binance responses,
- convert responses into project models.

It should not:

- save anything to the database,
- calculate CVD,
- calculate indicators,
- manage synchronization state.

### BybitExchange

Same responsibilities as `BinanceExchange`, but for Bybit.

### OKXExchange

Same responsibilities as `BinanceExchange`, but for OKX.

---

## 9. Collector Layer

The collector coordinates data requests.

### MarketCollector

Responsibilities:

- select an exchange client,
- request specific market data,
- request data for a defined time range,
- return normalized `BaseMarketData` child models.

Conceptual operations:

```text
collect_candles()
collect_trades()
collect_open_interest()
collect_funding_rates()
```

The collector should not directly write SQL queries.

---

## 10. Storage Layer

The storage layer is responsible for persistent data.

### Database

Responsibilities:

- manage the database connection,
- manage sessions or connection pools,
- provide infrastructure for repositories.

---

## 11. Repository Layer

Repositories are responsible for reading and writing specific data models.

### CandleRepository

Expected operations:

```text
save()
save_many()
get_last_timestamp()
get_by_range()
```

### TradeRepository

Expected operations:

```text
save()
save_many()
get_last_trade_id()
get_last_timestamp()
get_by_range()
```

### OpenInterestRepository

Expected operations:

```text
save()
save_many()
get_last_timestamp()
get_by_range()
```

### FundingRepository

Expected operations:

```text
save()
save_many()
get_last_timestamp()
get_by_range()
```

---

## 12. Synchronization Repository

### SyncRepository

This repository stores synchronization state.

The system must know how far data has already been downloaded.

Example synchronization key:

```text
exchange
market_type
symbol
data_type
interval
```

Example state:

```text
exchange: Binance
market_type: Perpetual
symbol: BTCUSDT
data_type: candles
interval: 1m
last_timestamp: 2026-08-08 10:00:00
```

Expected operations:

```text
get_last_sync()
update_last_sync()
```

This allows the application to download only missing data.

---

## 13. Service Layer

### MarketDataService

This is the main orchestration layer.

Responsibilities:

1. Ask the repository for the latest stored timestamp.
2. Determine the missing time range.
3. Ask the collector to download missing data.
4. Receive normalized `BaseMarketData` child models.
5. Save the new records using repositories.
6. Update the synchronization state.

Conceptual flow:

```text
MarketDataService
        ↓
SyncRepository
        ↓
Find last stored timestamp
        ↓
MarketCollector
        ↓
Exchange Client
        ↓
Exchange API
        ↓
BaseMarketData Child Models
        ↓
Repository
        ↓
Database
        ↓
Update Sync State
```

---

## 14. Application Entry Point

### main.py

`main.py` should remain small.

Its responsibility is to initialize application components and start the selected workflow.

Later examples may include:

```text
sync BTCUSDT candles
sync BTCUSDT trades
sync BTCUSDT open interest
sync BTCUSDT funding
```

Business logic should not be placed directly in `main.py`.

---

## 15. Configuration

### config.py

This module will later contain application configuration such as:

```text
database configuration
enabled exchanges
default symbols
default market type
request limits
timeouts
logging configuration
```

Secrets such as API keys should not be committed to GitHub.

They should be loaded from environment variables or a local `.env` file.

---

## 16. First Data Flow

The first working version should support:

```text
BTCUSDT
    ↓
Binance Perpetual
    ↓
Candles
Trades
Open Interest
Funding Rate
    ↓
BaseMarketData Child Models
    ↓
Database
```

---

## 17. Historical Synchronization Flow

On the first run:

```text
Database is empty
    ↓
Download historical data
    ↓
Store data
    ↓
Save synchronization timestamp
```

On the next run:

```text
Read last synchronization timestamp
    ↓
Download only missing data
    ↓
Store new records
    ↓
Update synchronization timestamp
```

This prevents downloading the same historical data repeatedly.

---

## 18. Future Layers

These layers should be added only after the data pipeline is stable.

```text
features/
scanner/
backtest/
ml/
signals/
risk/
api/
dashboard/
```

Future flow:

```text
Raw Market Data
        ↓
Normalized Data
        ↓
Feature Engineering
        ↓
Cross-Exchange Aggregation
        ↓
Market Scanner
        ↓
Scoring
        ↓
Machine Learning
        ↓
Signals
        ↓
Backtesting / Paper Trading
```

---

## 19. Architecture Principle

The most important design principle is separation of responsibilities.

```text
Exchange
    = fetches external data

Collector
    = coordinates data collection

BaseMarketData
    = provides shared market identity fields

Model
    = represents specialized normalized market data

Repository
    = reads and writes database records

Service
    = coordinates application logic

Feature Engine
    = calculates analytical features later
```

This structure keeps the project modular and makes it possible to add more exchanges, data types, databases, and analytical modules without rewriting the entire application.
