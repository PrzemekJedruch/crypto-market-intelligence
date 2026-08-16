# Crypto Market Intelligence — Roadmap

## Project Status

| Phase | Status | Progress |
|---|---|---:|
| 1. Core Data Models | ✅ DONE | 100% |
| 2. Exchange Interface | ✅ DONE | 100% |
| 3. Binance Integration | ✅ DONE | 100% |
| 4. Database Layer | 🟡 IN PROGRESS | 15% |
| 5. Historical Synchronization | ⬜ TODO | 0% |
| 6. Data Quality | ⬜ TODO | 0% |
| 7. Bybit Integration | ⬜ TODO | 0% |
| 8. OKX Integration | ⬜ TODO | 0% |
| 9. Multi-Symbol Support | ⬜ TODO | 0% |
| 10. Live Market Data | ⬜ TODO | 0% |
| 11. Feature Engineering | ⬜ TODO | 0% |
| 12. Cross-Exchange Aggregation | ⬜ TODO | 0% |
| 13. Market Scanner | ⬜ TODO | 0% |
| 14. Market Scoring | ⬜ TODO | 0% |
| 15. Backtesting | ⬜ TODO | 0% |
| 16. Machine Learning | ⬜ TODO | 0% |
| 17. Signal Engine | ⬜ TODO | 0% |
| 18. Product Layer | ⬜ TODO | 0% |

## Current Focus

**Completed:** Phase 3 — Binance Integration  
**Next Phase:** Phase 4 — Database Layer  
**Next Milestone:** Store normalized Binance market data in PostgreSQL and prepare the foundation for incremental synchronization.

### Completed Recently

- [x] Complete Binance candle downloads and normalization
- [x] Complete Binance aggregate trade downloads and normalization
- [x] Complete historical Open Interest downloads and normalization
- [x] Complete historical funding-rate downloads and normalization
- [x] Add shared Binance API error handling
- [x] Add candle request limits and pagination
- [x] Add two-level aggregate trade pagination
- [x] Add Open Interest pagination
- [x] Add funding-rate pagination
- [x] Cover the Binance exchange layer with automated tests
- [x] Document Binance API-specific behavior

### Next Tasks

- [ ] Configure PostgreSQL
- [ ] Create the database connection layer
- [ ] Define the initial market-data tables
- [ ] Add unique constraints
- [ ] Create repositories
- [ ] Prepare synchronization-state storage

## Status Legend

- ✅ **DONE** — all tasks in the phase are completed
- 🟡 **IN PROGRESS** — work is currently active
- ⬜ **TODO** — work has not started yet
- 🔴 **BLOCKED** — progress is currently blocked

---

## Project Direction

The project is developed in small stages.

The priority is to build a reliable market-data pipeline first. Advanced analytics, market scanning, backtesting, and machine learning are added only after the core data layer is stable.

---

## Phase 1 — Core Data Models

**Status:** ✅ DONE

### Goal

Define clean, reusable, and exchange-independent data structures.

### Completed

- [x] Create project structure
- [x] Create enums
- [x] Create `BaseMarketData`
- [x] Create `Candle`
- [x] Create `Trade`
- [x] Create `OpenInterest`
- [x] Create `FundingRate`
- [x] Use a shallow shared model hierarchy
- [x] Export models and enums through package `__init__.py` files
- [x] Define naming conventions
- [x] Define comment and docstring conventions
- [x] Add basic model tests

### Model Hierarchy

```text
BaseMarketData
├── Candle
├── Trade
├── OpenInterest
└── FundingRate
```

### Result

The project has a common internal representation for market data that is independent of any specific exchange.

---

## Phase 2 — Exchange Interface

**Status:** ✅ DONE

### Goal

Create a common contract for exchange integrations.

### Completed

- [x] Create `BaseExchange`
- [x] Define `get_candles()`
- [x] Define `get_trades()`
- [x] Define `get_open_interest()`
- [x] Define `get_funding_rate()`
- [x] Define `get_supported_symbols()`
- [x] Standardize UTC timestamp handling
- [x] Standardize symbol handling
- [x] Standardize returned internal models
- [x] Add tests for timestamp and symbol normalization

### Result

Exchange clients can implement the same application-facing interface while keeping exchange-specific logic inside their own classes.

---

## Phase 3 — Binance Integration

**Status:** ✅ DONE

### Goal

Implement the first complete market-data source.

### Initial Market

```text
Exchange: Binance
Market: USD-M Perpetual Futures
Symbol: BTCUSDT
```

### Completed

- [x] Connect to Binance public API
- [x] Download candles
- [x] Download aggregate trades
- [x] Download historical Open Interest
- [x] Download historical funding rates
- [x] Convert Binance candle responses into `Candle`
- [x] Convert Binance trade responses into `Trade`
- [x] Convert Binance Open Interest responses into `OpenInterest`
- [x] Convert Binance funding-rate responses into `FundingRate`
- [x] Normalize timestamps to UTC
- [x] Normalize symbols
- [x] Add `BinanceAPIError`
- [x] Centralize GET requests through `_get_json()`
- [x] Add request limits
- [x] Add candle pagination
- [x] Add aggregate-trade time-window pagination
- [x] Add aggregate-trade continuation with `fromId`
- [x] Add Open Interest pagination
- [x] Add funding-rate pagination
- [x] Add automated tests for the current Binance exchange layer
- [x] Document Binance-specific API behavior

### Result

Python can retrieve complete requested ranges of normalized BTCUSDT market data from Binance through the common exchange interface.

---

## Phase 4 — Database Layer

**Status:** 🟡 IN PROGRESS

### Goal

Store normalized market data persistently.

### Planned Tasks

- [x] Configure PostgreSQL
- [x] Create database connection layer
- [ ] Create candle table
- [ ] Create trade table
- [ ] Create Open Interest table
- [ ] Create funding-rate table
- [ ] Create synchronization-state table
- [ ] Create repositories
- [ ] Add unique constraints
- [ ] Prevent duplicate records
- [ ] Add repository tests

### Initial Uniqueness Rules

```text
Candles:
exchange + market_type + symbol + interval + timestamp

Trades:
exchange + market_type + symbol + trade_id

Open Interest:
exchange + market_type + symbol + timestamp

Funding Rates:
exchange + market_type + symbol + timestamp
```

### Result

Downloaded market data can be stored and retrieved reliably.

---

## Phase 5 — Historical Synchronization

**Status:** ⬜ TODO

### Goal

Download only missing data instead of downloading the full history every time.

### Planned Tasks

- [ ] Store last synchronized timestamp
- [ ] Detect missing time ranges
- [ ] Fetch missing data only
- [ ] Update synchronization state
- [ ] Handle interrupted synchronization
- [ ] Validate continuity
- [ ] Detect duplicates
- [ ] Detect missing records

### Target Flow

```text
Database contains data until timestamp T
        ↓
Application starts later
        ↓
Detect latest stored timestamp
        ↓
Download only T → now
        ↓
Store new records
        ↓
Update synchronization state
```

### Result

The application can resume data collection from the last successfully stored point.

---

## Phase 6 — Data Quality

**Status:** ⬜ TODO

### Goal

Verify that stored data is trustworthy.

### Planned Tasks

- [ ] Check missing timestamps
- [ ] Check duplicate records
- [ ] Check invalid prices
- [ ] Check invalid volumes
- [ ] Compare stored data with exchange responses
- [ ] Validate UTC timestamps
- [ ] Add logging
- [ ] Add data-quality tests

### Result

A stable and auditable historical dataset.

---

## Phase 7 — Bybit Integration

**Status:** ⬜ TODO

### Goal

Add the second exchange without changing the core architecture.

### Planned Tasks

- [ ] Implement `BybitExchange`
- [ ] Map Bybit symbols
- [ ] Normalize Bybit candles
- [ ] Normalize Bybit trades
- [ ] Normalize Bybit Open Interest
- [ ] Normalize Bybit funding rates
- [ ] Reuse existing repositories
- [ ] Reuse synchronization logic

### Result

The same application workflow works for Binance and Bybit.

---

## Phase 8 — OKX Integration

**Status:** ⬜ TODO

### Goal

Add a third major derivatives exchange.

### Planned Tasks

- [ ] Implement `OKXExchange`
- [ ] Normalize market data
- [ ] Reuse the common data models
- [ ] Reuse synchronization logic
- [ ] Compare values across exchanges

### Result

BTC market data is available from multiple major derivatives exchanges.

---

## Phase 9 — Multi-Symbol Support

**Status:** ⬜ TODO

### Goal

Move from BTCUSDT to multiple cryptocurrency markets.

### Initial Candidates

```text
BTCUSDT
ETHUSDT
SOLUSDT
XRPUSDT
```

### Planned Tasks

- [ ] Add symbol configuration
- [ ] Add exchange-specific symbol mapping
- [ ] Synchronize multiple symbols
- [ ] Track sync state per symbol
- [ ] Handle unavailable instruments

### Result

The system can collect data for many markets automatically.

---

## Phase 10 — Live Market Data

**Status:** ⬜ TODO

### Goal

Add real-time market-data collection.

### Planned Tasks

- [ ] Add WebSocket connections
- [ ] Stream trades
- [ ] Stream order-book updates
- [ ] Handle reconnects
- [ ] Handle heartbeats
- [ ] Handle temporary disconnects
- [ ] Store live data
- [ ] Merge live and historical datasets

### Result

The database is continuously updated with new market data.

---

## Phase 11 — Feature Engineering

**Status:** ⬜ TODO

### Goal

Convert normalized market data into analytical features.

### Initial Features

```text
Price Change
Return
Relative Volume
Buy Volume
Sell Volume
Volume Delta
CVD
Open Interest Change
Funding Change
Volatility
```

### Future Features

```text
Order Book Imbalance
Spot / Futures Divergence
Cross-Exchange Price Spread
Global Open Interest
Global CVD
OI-weighted Funding
Liquidation Imbalance
```

### Result

A feature dataset ready for quantitative analysis and modeling.

---

## Phase 12 — Cross-Exchange Aggregation

**Status:** ⬜ TODO

### Goal

Create market-wide metrics from multiple exchanges.

### Planned Tasks

- [ ] Normalize measurement units
- [ ] Align timestamps
- [ ] Apply exchange weights where appropriate
- [ ] Aggregate market data
- [ ] Compare exchange behavior
- [ ] Detect cross-exchange divergences

### Result

The platform provides a broader market view instead of relying on a single exchange.

---

## Phase 13 — Market Scanner

**Status:** ⬜ TODO

### Goal

Automatically search for unusual market conditions.

### Initial Conditions

- abnormal volume
- Open Interest spike
- price breakout
- CVD divergence
- funding extremes
- spot/futures divergence
- cross-exchange divergence

### Result

The system ranks instruments based on current market conditions.

---

## Phase 14 — Market Scoring

**Status:** ⬜ TODO

### Goal

Create an interpretable market-opportunity score.

### Initial Components

```text
Trend
Volume
Open Interest
CVD
Funding
Volatility
Market Structure
Cross-Exchange Confirmation
```

### Result

Each instrument receives a structured score that summarizes current market conditions.

---

## Phase 15 — Backtesting

**Status:** ⬜ TODO

### Goal

Measure whether scanner conditions and signals have historical value.

### Planned Tasks

- [ ] Define entry conditions
- [ ] Define exit conditions
- [ ] Include trading fees
- [ ] Include slippage
- [ ] Calculate returns
- [ ] Calculate win rate
- [ ] Calculate expectancy
- [ ] Calculate drawdown
- [ ] Calculate profit factor
- [ ] Perform walk-forward testing

### Result

The project can distinguish useful historical relationships from visually interesting but unreliable patterns.

---

## Phase 16 — Machine Learning

**Status:** ⬜ TODO

### Goal

Use historical features to estimate future market outcomes.

### Initial Model Candidates

- Logistic Regression
- Random Forest
- Gradient Boosting
- XGBoost / LightGBM

### Possible Targets

```text
Probability of breakout
Probability of large move
Probability of upward move
Probability of downward move
Probability of squeeze
```

### Validation Requirements

- time-based train/test split
- walk-forward validation
- no future-data leakage
- transaction costs included
- feature-importance analysis

### Result

Machine learning becomes an additional analytical layer rather than the foundation of the platform.

---

## Phase 17 — Signal Engine

**Status:** ⬜ TODO

### Goal

Convert scanner and model outputs into structured market signals.

### Possible Signal Fields

```text
symbol
direction
score
probability
timestamp
reasons
market conditions
```

### Result

Signals contain transparent context explaining why a market condition was detected.

---

## Phase 18 — Product Layer

**Status:** ⬜ TODO

### Goal

Turn the analytical engine into a usable application.

### Potential Modules

- web dashboard
- market scanner
- instrument detail view
- alerts
- historical signal explorer
- backtesting interface
- REST API
- user accounts
- subscription plans

### Result

Crypto Market Intelligence becomes a usable analytical product rather than only a research codebase.

---

## Long-Term Architecture

```text
Exchange APIs
    ↓
Exchange Clients
    ↓
Collectors
    ↓
Normalized Market Models
    ↓
Repositories / Database
    ↓
Synchronization
    ↓
Feature Engineering
    ↓
Cross-Exchange Aggregation
    ↓
Scanner
    ↓
Scoring
    ↓
Backtesting
    ↓
Machine Learning
    ↓
Signals
    ↓
API / Dashboard / Alerts
```

---

## Development Rule

Do not move to a major analytical layer until the underlying data layer is reliable.

```text
Reliable Data
    before
Features
    before
Scanner
    before
Backtesting
    before
Machine Learning
    before
Signals
    before
Product
```

A reliable dataset is more valuable than an advanced model built on incomplete or inconsistent market data.
