# Crypto Market Intelligence

A modular multi-exchange cryptocurrency market data platform built in Python.

The project is designed to collect, normalize, store, and later analyze market data from major cryptocurrency exchanges. Its long-term goal is to create a reliable foundation for cross-exchange analytics, market scanning, feature engineering, backtesting, and machine learning.

## Project Goals

The first stages of the project focus on building a clean and reliable market data pipeline.

The system will:

- collect market data from multiple exchanges,
- normalize exchange-specific responses into common Python models,
- store historical and live data,
- synchronize only missing data,
- support multiple market types,
- prepare data for future quantitative analysis.

The initial supported market data types are:

- Candles
- Trades
- Open Interest
- Funding Rates

Planned exchanges include:

- Binance
- Bybit
- OKX
- Coinbase
- Kraken

## Current Status

### Phase 1 — Core Data Models

**Status: ✅ DONE**

The first development phase is complete.

Implemented:

- `BaseMarketData`
- `Candle`
- `Trade`
- `OpenInterest`
- `FundingRate`
- `Exchange`
- `MarketType`
- `TradeSide`
- model and enum exports through `__init__.py`
- naming conventions
- English code comments and function/method docstrings
- basic `pytest` coverage for all current market models

The model test suite verifies:

- object creation,
- inheritance from `BaseMarketData`,
- inherited common fields,
- model-specific fields,
- enum usage,
- optional funding data.

Tests are currently run with:

```bash
python -m pytest
```

### Phase 2 — Exchange Interface

**Status: 🟡 IN PROGRESS**

The next milestone is to define the common exchange contract through `BaseExchange`.

Planned methods:

```text
get_candles()
get_trades()
get_open_interest()
get_funding_rate()
get_supported_symbols()
```

## Architecture

The project follows a layered architecture with clear separation of responsibilities.

```text
Exchange API
    ↓
Exchange Client
    ↓
Collector
    ↓
BaseMarketData Child Models
    ↓
Repository
    ↓
Database
    ↓
Feature Engineering
    ↓
Cross-Exchange Analytics
    ↓
Market Scanner
    ↓
Machine Learning
```

Each layer has one responsibility:

- **Exchange clients** communicate with external exchange APIs.
- **Collectors** coordinate data collection.
- **Models** represent normalized market data.
- **Repositories** handle database reads and writes.
- **Services** coordinate application workflows.
- **Tests** verify model behavior, construction, and inheritance.
- **Feature modules** will later calculate analytical market features.

More details are available in [`docs/architecture.md`](docs/architecture.md).

## Project Structure

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
├── tests/
│   └── test_models.py
│
└── docs/
    ├── architecture.md
    ├── data_model.md
    └── roadmap.md
```

## Data Model

The current model layer uses a small shared base class.

```text
BaseMarketData
├── Candle
├── Trade
├── OpenInterest
└── FundingRate
```

### BaseMarketData

Contains the common market identity fields:

```text
exchange
market_type
symbol
timestamp
```

The inheritance hierarchy is intentionally shallow. Specialized models inherit only the fields that are genuinely shared.

### Candle

Represents one OHLCV candle.

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

Represents one executed trade.

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

Open-Interest-specific fields:

```text
open_interest
open_interest_usd
```

### FundingRate

Represents one funding rate measurement.

Funding-specific fields:

```text
funding_rate
next_funding_time
```

Detailed model documentation is available in [`docs/data_model.md`](docs/data_model.md).

## First Working Milestone

The first full data pipeline will focus on:

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
Normalized Python Models
    ↓
Database
```

The application should remember the latest synchronized timestamp so that subsequent runs download only missing data.

## Planned Development

The project roadmap is divided into development phases.

Completed:

```text
Phase 1 — Core Data Models
```

Current:

```text
Phase 2 — Exchange Interface
```

Later phases include:

- Binance integration,
- PostgreSQL storage,
- historical synchronization,
- data-quality checks,
- Bybit integration,
- OKX integration,
- multi-symbol support,
- live WebSocket data,
- feature engineering,
- cross-exchange aggregation,
- market scanning,
- market scoring,
- backtesting,
- machine learning,
- signal generation,
- API, dashboard, and alerts.

See [`docs/roadmap.md`](docs/roadmap.md) for the complete development plan.

## Long-Term Vision

The final platform should identify unusual market conditions across multiple exchanges rather than simply display price charts.

Examples of future analytics include:

```text
Global Open Interest
Global Spot CVD
Global Futures CVD
OI-weighted Funding
Spot/Futures Divergence
Cross-Exchange Price Divergence
Relative Volume
Liquidation Imbalance
Order Book Imbalance
```

These features can later be used by a scanner or machine learning model to detect potential market opportunities.

## Technology Direction

The initial stack is expected to include:

- Python
- pytest
- PostgreSQL
- Pandas / Polars
- Asyncio
- HTTP / WebSocket APIs
- Parquet for historical analytical datasets

Additional infrastructure should only be introduced when required by data volume or system complexity.

## Development Principles

The project should remain:

- modular,
- testable,
- exchange-independent,
- data-source-independent,
- easy to extend,
- suitable for quantitative research.

Additional code conventions:

- modules and files use `snake_case`,
- functions and methods use `snake_case`,
- classes use `PascalCase`,
- enum members use `UPPER_CASE`,
- code comments are written in English,
- functions and methods include concise docstrings,
- business logic is not placed directly inside API clients or data models.

## Licensing, Author, and Acknowledgements

- **Author:** Przemyslaw Jedruch
- **Project type:** Independent educational and research project focused on cryptocurrency market data engineering, quantitative analysis, and market intelligence.
- **Market data sources:** Market data will be collected from public APIs provided by cryptocurrency exchanges such as Binance, Bybit, OKX, Coinbase, and Kraken.
- **Data attribution:** All market data remains subject to the terms, licensing conditions, and usage policies of the respective exchanges and data providers.
- **Code license:** A software license has not yet been selected for this repository. A dedicated `LICENSE` file should be added before defining reuse or redistribution terms.
- **Acknowledgements:** This project relies on the open-source Python ecosystem and the public API documentation provided by cryptocurrency exchanges and data providers.

This is an independent project. Any analysis, indicators, models, signals, forecasts, or conclusions produced by this repository are the author's own and do not represent an endorsement by any exchange, data provider, or third-party organization.

## References

- [Binance Developers](https://developers.binance.com/)
- [Bybit API Documentation](https://bybit-exchange.github.io/docs/)
- [OKX API Documentation](https://www.okx.com/docs-v5/en/)
- [Coinbase Developer Documentation](https://docs.cdp.coinbase.com/)
- [Kraken API Documentation](https://docs.kraken.com/api/)
- [Python Documentation](https://docs.python.org/3/)
- [pytest Documentation](https://docs.pytest.org/)
- [pandas Documentation](https://pandas.pydata.org/docs/)
- [Polars Documentation](https://docs.pola.rs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## Disclaimer

This project is intended for research, data analysis, and software development purposes. It does not constitute financial or investment advice.
