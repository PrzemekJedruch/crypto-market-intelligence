# Crypto Market Intelligence

A modular multi-exchange cryptocurrency market data platform built in Python.

The project is designed to collect, normalize, store, and later analyze market data from major cryptocurrency exchanges. Its long-term goal is to create a reliable foundation for cross-exchange analytics, market scanning, feature engineering, backtesting, and machine learning.

## Project Goals

The first stage of the project focuses on building a clean and reliable market data pipeline.

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

## Architecture

The project follows a layered architecture with clear separation of responsibilities.

```text
Exchange API
    ↓
Exchange Client
    ↓
Collector
    ↓
Normalized Data Models
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
- **Feature modules** will later calculate analytical market features.

More details are available in [`docs/architecture.md`](docs/architecture.md).

## Initial Project Structure

```text
crypto-market-intelligence/
│
├── README.md
├── main.py
├── config.py
│
├── models/
│   ├── __init__.py
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

## Initial Data Models

### Candle

Represents one OHLCV candle.

Main fields:

```text
exchange
market_type
symbol
interval
timestamp
open
high
low
close
volume
```

### Trade

Represents one executed trade.

Main fields:

```text
exchange
market_type
symbol
trade_id
timestamp
price
quantity
quote_value
side
```

### Open Interest

Represents one Open Interest measurement.

Main fields:

```text
exchange
market_type
symbol
timestamp
open_interest
open_interest_usd
```

### Funding Rate

Represents one funding rate measurement.

Main fields:

```text
exchange
market_type
symbol
timestamp
funding_rate
next_funding_time
```

## First Milestone

The first working version will focus on:

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

The application should also remember the latest synchronized timestamp so that subsequent runs download only missing data.

## Planned Development

After the core data pipeline is stable, the project will be extended with:

- Bybit and OKX integrations,
- multi-symbol support,
- live WebSocket data,
- cross-exchange aggregation,
- CVD,
- Open Interest changes,
- funding pressure,
- spot vs futures divergence,
- order book imbalance,
- market scoring,
- market scanner,
- backtesting,
- machine learning models,
- alerts,
- API,
- dashboard.

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

Business logic should not be placed directly inside API clients or data models.

## Status

Early development — core architecture and market data models are being defined.


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
- [pandas Documentation](https://pandas.pydata.org/docs/)
- [Polars Documentation](https://docs.pola.rs/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## Disclaimer

This project is intended for research, data analysis, and software development purposes. It does not constitute financial or investment advice.
