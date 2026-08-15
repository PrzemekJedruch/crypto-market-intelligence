# Crypto Market Intelligence

A Python project for building a clearer view of the cryptocurrency market across multiple exchanges.

The goal is not to create another price chart. The goal is to combine market data such as price, trading activity, Open Interest, and funding rates into a single research platform that can later support market scanning, backtesting, quantitative analysis, and machine learning.

---

## Why This Project Exists

Crypto markets are fragmented.

The same asset can trade on several exchanges at the same time, while each venue provides different information about volume, derivatives activity, funding, liquidity, and positioning.

Looking at one exchange gives only part of the picture.

**Crypto Market Intelligence** is being built to answer questions such as:

- Is a price move supported by real spot demand?
- Is Open Interest rising together with price, or is leverage being reduced?
- Are futures traders becoming unusually aggressive?
- Is funding becoming crowded?
- Do several exchanges confirm the same market move?
- Are there unusual conditions that historically appeared before larger price movements?

The long-term objective is to transform fragmented exchange data into useful market intelligence.

---

## What the Platform Will Do

The platform is designed around a simple workflow:

```text
Market Data
    ↓
Normalized Data
    ↓
Historical Database
    ↓
Market Features
    ↓
Cross-Exchange Analysis
    ↓
Scanner & Scoring
    ↓
Backtesting
    ↓
Machine Learning
    ↓
Signals, API, Dashboard & Alerts
```

Instead of treating every exchange separately, the system will convert data into a common format so that markets can be compared and analyzed consistently.

---

## Market Data

The first version focuses on four core data types:

- **Candles** — price and volume over time
- **Trades** — executed market activity
- **Open Interest** — outstanding derivatives positions
- **Funding Rates** — positioning pressure in perpetual futures

These datasets will later be combined to create higher-level analytical features.

Examples include:

- price and Open Interest divergence,
- spot vs futures activity,
- buy/sell pressure,
- CVD,
- relative volume,
- funding pressure,
- cross-exchange confirmation,
- market participation changes,
- liquidity and order-book imbalance.

---

## Exchanges

The platform is intended to support several major cryptocurrency exchanges.

Planned coverage includes:

- Binance
- Bybit
- OKX
- Coinbase
- Kraken

The first completed exchange integration is **Binance USD-M Futures**.

The next development focus is persistent historical storage and incremental synchronization. Additional exchanges will be added after the first end-to-end data pipeline is stable.

---

## Current Status

### ✅ Core Market Models

The common internal representation for market data is complete.

The project currently supports normalized models for:

- candles,
- trades,
- Open Interest,
- funding rates.

### ✅ Exchange Interface

A common exchange interface has been created so future exchanges can expose market data in the same way.

### ✅ Binance Integration

Binance is the first completed exchange integration.

Implemented:

- public API connectivity,
- candle downloads,
- aggregate trade downloads,
- historical Open Interest downloads,
- historical funding-rate downloads,
- UTC timestamp normalization,
- symbol normalization,
- conversion of Binance responses into internal market-data models,
- basic API error handling,
- request limits and historical pagination,
- automated tests for the current exchange layer.

### ⏭️ Next: Historical Storage

The next milestone is to persist normalized market data in PostgreSQL and then synchronize only data that is missing from the local dataset.

---

## First Working Milestone

The first complete data pipeline is intentionally narrow:

```text
BTCUSDT
    ↓
Binance Perpetual Futures
    ↓
Candles + Trades + Open Interest + Funding
    ↓
Normalized Data
    ↓
Historical Storage
    ↓
Incremental Synchronization
```

Once this pipeline is reliable, the same architecture can be expanded to more symbols and exchanges.

---

## Long-Term Vision

The long-term goal is a multi-exchange market intelligence platform capable of identifying unusual market conditions rather than simply displaying raw data.

Potential analytical modules include:

- Global Open Interest
- Global Spot CVD
- Global Futures CVD
- OI-weighted Funding
- Spot/Futures Divergence
- Cross-Exchange Price Divergence
- Relative Volume
- Liquidation Imbalance
- Order Book Imbalance
- Market Regime Detection

These features can later feed a market scanner and scoring engine.

A simplified example:

```text
BTCUSDT

Market Score: 82 / 100

Spot demand        ↑ strong
Futures activity   ↑ rising
Open Interest      ↑ expanding
Funding            neutral
Cross-exchange     confirmed

Possible interpretation:
strong participation with broad market confirmation
```

The score itself is not intended to be a trading recommendation. It would be a structured way to summarize multiple market conditions.

---

## Research Direction

One of the main research goals is to investigate whether combinations of market variables contain useful information about future price behavior.

Examples:

```text
Spot Volume
+ Futures Volume
+ Open Interest
+ CVD
+ Funding
+ Market Structure
```

The project will eventually allow these relationships to be tested systematically through historical analysis and backtesting.

Machine learning will be introduced only after the underlying data pipeline and feature engineering are reliable.

---

## Possible Future Products

If the research and data pipeline prove useful, the project could evolve beyond a personal research tool.

Possible directions include:

- market scanner,
- analytics dashboard,
- trading alerts,
- research API,
- historical market datasets,
- quantitative research tools,
- subscription-based analytics,
- B2B market intelligence services.

The project is currently focused on engineering and research rather than commercialization.

---

## Technology

The project is written primarily in **Python**.

The broader technology direction includes:

- Python
- pytest
- PostgreSQL
- Pandas / Polars
- REST and WebSocket APIs
- Parquet
- asynchronous data collection

Technology is added only when it solves a real project requirement. The priority is a reliable and understandable system rather than unnecessary infrastructure.

---

## Project Roadmap

Development is planned in stages:

```text
1. Core market models                 ✅
2. Common exchange interface          ✅
3. Binance integration                ✅
4. Historical storage                 ⏭️
5. Incremental synchronization
6. Data-quality validation
7. Additional exchanges
8. Multi-symbol support
9. Live market data
10. Feature engineering
11. Cross-exchange aggregation
12. Market scanner and scoring
13. Backtesting
14. Machine learning
15. API, dashboard and alerts
```

Detailed technical notes are kept in the [`docs/`](docs/) directory so the main README can remain focused on the purpose and direction of the project.

---

## Project Philosophy

A few principles guide the development of this project:

- **Data quality before machine learning**
- **Simple architecture before unnecessary complexity**
- **Reusable market data instead of exchange-specific logic**
- **Historical validation before live signals**
- **Incremental development instead of building everything at once**
- **Research first, conclusions second**

The most important asset of the project is not a prediction model.

It is a reliable market-data foundation that makes serious research possible.

---

## Author

**Przemyslaw Jedruch**

Independent educational and research project focused on cryptocurrency market data engineering, quantitative analysis, and market intelligence.

---

## Data Sources

Market data is collected from public APIs provided by cryptocurrency exchanges.

Planned and current data providers include:

- Binance
- Bybit
- OKX
- Coinbase
- Kraken

All market data remains subject to the terms, licensing conditions, rate limits, and usage policies of the respective exchanges and data providers.

This project is independent and is not affiliated with, sponsored by, endorsed by, or officially connected with any exchange or financial institution.

---

## License

A software license has not yet been selected for this repository.

A dedicated `LICENSE` file should be added before defining reuse, redistribution, or commercial-use terms.

---

## Disclaimer

This project is provided for educational, research, data-analysis, and software-development purposes only.

Nothing in this repository — including source code, market data, indicators, analytical features, scores, signals, forecasts, backtests, machine-learning outputs, documentation, or examples — constitutes financial, investment, trading, legal, tax, or other professional advice.

The project does not provide a recommendation or solicitation to buy, sell, hold, or trade cryptocurrencies, derivatives, securities, or other financial instruments.

Cryptocurrency and derivatives markets involve substantial risk, including the possible loss of some or all invested capital. Historical results, simulations, statistical relationships, backtests, model predictions, and market signals do not guarantee future performance.

Market data and analytical outputs may contain errors, delays, missing observations, exchange-specific inconsistencies, API failures, or other inaccuracies. External exchanges, APIs, libraries, and data providers may change or become unavailable without notice.

All software, data, calculations, and outputs are provided on an **"as is"** and **"as available"** basis without warranties of accuracy, completeness, reliability, timeliness, availability, fitness for a particular purpose, or future performance.

Any use of this project for live trading, automated trading, investment decisions, risk management, or other financial activity is performed entirely at the user's own risk and responsibility.

Users are responsible for independently verifying all data, assumptions, calculations, signals, and results and for complying with all laws, regulations, tax obligations, exchange rules, and other requirements applicable in their jurisdiction.

The author assumes no responsibility or liability for financial losses, trading losses, lost profits, missed opportunities, data loss, system failures, or other consequences resulting directly or indirectly from the use of this project.
