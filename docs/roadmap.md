# Crypto Market Intelligence — Roadmap

## Project Status

| Phase | Status | Progress |
|---|---|---:|
| 1. Core Data Models | ✅ DONE | 100% |
| 2. Exchange Interface | ✅ DONE | 100% |
| 3. Binance Integration | 🟡 **IN PROGRESS** | 12% |
| 4. Database Layer | ⬜ TODO | 0% |
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

**Current Phase:** Phase 3 — Binance Integration

**Status:** 🟡 **IN PROGRESS**  
**Next Milestone:**  Implement the first real market data source.
### Completed Recently

- [x] Complete Phase 1 — Core Data Models
- [x] Complete Phase 2 — Exchange Interface
- [x] Connect to Binance public API

### Next Tasks

- [ ] Download candles
- [ ] Download trades
- [ ] Download Open Interest
- [ ] Download funding rates
- [ ] Convert Binance responses into internal models
- [ ] Add basic error handling
- [ ] Add request limits and pagination handling


## Status Legend

- ✅ **DONE** — all tasks in the phase are completed
- 🟡 **IN PROGRESS** — work is currently active
- ⬜ **TODO** — work has not started yet
- 🔴 **BLOCKED** — progress is currently blocked

## Project Direction

The project will be developed in small stages.

The priority is to build a reliable market data pipeline first.
Advanced analytics, market scanning, backtesting, and machine learning will be added only after the core data layer is stable.

---

## Phase 1 — Core Data Models
**Status:** ✅ **DONE**

### Goal

Define clean, reusable, and exchange-independent data structures.

### Tasks

- [x] Create project structure
- [x] Create enums
- [x] Create `BaseMarketData`
- [x] Create `Candle`
- [x] Create `Trade`
- [x] Create `OpenInterest`
- [x] Create `FundingRate`
- [x] Refactor market models to inherit from `BaseMarketData`
- [x] Update `models/__init__.py`
- [x] Create `README.md`
- [x] Create `architecture.md`
- [x] Create `roadmap.md`
- [x] Create `data_model.md`
- [x] Update architecture documentation after the base-model refactor
- [x] Review naming conventions
- [x] Define comment and docstring conventions
- [x] Add basic tests for all models

### Current Model Hierarchy

```text
BaseMarketData
├── Candle
├── Trade
├── OpenInterest
└── FundingRate
```

### Expected Result

A clean and exchange-independent model layer with shared market identity fields and minimal duplication.
---

## Phase 2 — Exchange Interface

**Status:** ✅ **DONE**

### Goal

Create a common contract for exchange integrations.

### Tasks

- [x] Create `BaseExchange`
- [x] Define `get_candles()`
- [x] Define `get_trades()`
- [x] Define `get_open_interest()`
- [x] Define `get_funding_rate()`
- [x] Define `get_supported_symbols()`
- [x] Standardize timestamps
- [x] Standardize symbol handling
- [x] Standardize returned models

### Expected Result

Every supported exchange can be used through the same interface.

---

## Phase 3 — Binance Integration

**Status:** 🟡 **IN PROGRESS**

### Goal

Implement the first real market data source.

### Initial Market

```text
Exchange: Binance
Market: Perpetual
Symbol: BTCUSDT
```

### Tasks

- [x] Connect to Binance public API
- [ ] Download candles
- [ ] Download trades
- [ ] Download Open Interest
- [ ] Download funding rates
- [ ] Convert Binance responses into internal models
- [ ] Add basic error handling
- [ ] Add request limits and pagination handling

### Expected Result

Python can retrieve normalized BTCUSDT market data from Binance.

---

## Phase 4 — Database Layer

**Status:** ⬜ TODO

### Goal

Store market data persistently.

### Tasks

- [ ] Configure PostgreSQL
- [ ] Create database connection layer
- [ ] Create candle table
- [ ] Create trade table
- [ ] Create Open Interest table
- [ ] Create funding rate table
- [ ] Create synchronization state table
- [ ] Create repositories
- [ ] Add unique constraints
- [ ] Prevent duplicate records

### Expected Result

Downloaded market data can be stored and retrieved reliably.

---

## Phase 5 — Historical Synchronization

**Status:** ⬜ TODO

### Goal

Download only missing data instead of downloading the full history every time.

### Tasks

- [ ] Store last synchronized timestamp
- [ ] Detect missing time ranges
- [ ] Fetch missing data only
- [ ] Update synchronization state
- [ ] Handle interrupted synchronization
- [ ] Validate continuity
- [ ] Detect duplicates
- [ ] Detect missing records

### Expected Result

The application can resume data collection from the last successfully stored point.

Example:

```text
Database contains BTCUSDT candles until 10:00
        ↓
Application starts at 11:00
        ↓
Download only 10:00 → 11:00
        ↓
Store new candles
        ↓
Update sync state
```

---

## Phase 6 — Data Quality

**Status:** ⬜ TODO

### Goal

Verify that stored data is trustworthy.

### Tasks

- [ ] Check missing timestamps
- [ ] Check duplicate records
- [ ] Check invalid prices
- [ ] Check invalid volumes
- [ ] Compare stored data with exchange responses
- [ ] Validate UTC timestamps
- [ ] Add logging
- [ ] Add basic tests

### Expected Result

A stable and auditable historical dataset.

---

## Phase 7 — Bybit Integration

**Status:** ⬜ TODO

### Goal

Add the second exchange without changing the core architecture.

### Tasks

- [ ] Implement `BybitExchange`
- [ ] Map Bybit symbols
- [ ] Normalize Bybit candles
- [ ] Normalize Bybit trades
- [ ] Normalize Bybit Open Interest
- [ ] Normalize Bybit funding rates
- [ ] Reuse existing repositories
- [ ] Reuse synchronization logic

### Expected Result

The same application workflow works for Binance and Bybit.

---

## Phase 8 — OKX Integration

**Status:** ⬜ TODO

### Goal

Add a third major derivatives exchange.

### Tasks

- [ ] Implement `OKXExchange`
- [ ] Normalize market data
- [ ] Reuse the common data models
- [ ] Reuse synchronization logic
- [ ] Compare values across exchanges

### Expected Result

BTC market data is available from:

```text
Binance
Bybit
OKX
```

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

Later:

```text
Top 20
Top 50
Top 100
```

### Tasks

- [ ] Add symbol configuration
- [ ] Add exchange-specific symbol mapping
- [ ] Synchronize multiple symbols
- [ ] Track sync state per symbol
- [ ] Handle unavailable instruments

### Expected Result

The system can collect data for many markets automatically.

---

## Phase 10 — Live Market Data

**Status:** ⬜ TODO

### Goal

Add real-time data collection.

### Tasks

- [ ] Add WebSocket connections
- [ ] Stream trades
- [ ] Stream order book updates
- [ ] Handle reconnects
- [ ] Handle heartbeat messages
- [ ] Handle temporary disconnects
- [ ] Store live data
- [ ] Merge live and historical datasets

### Expected Result

The database is continuously updated with new market data.

---

## Phase 11 — Feature Engineering

**Status:** ⬜ TODO

### Goal

Convert raw market data into analytical features.

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

### Expected Result

A feature dataset ready for analysis and modeling.

---

## Phase 12 — Cross-Exchange Aggregation

**Status:** ⬜ TODO

### Goal

Create global market metrics from multiple exchanges.

### Examples

```text
Binance OI
+
Bybit OI
+
OKX OI
=
Global Open Interest
```

and:

```text
Binance CVD
+
Bybit CVD
+
OKX CVD
=
Global Futures CVD
```

### Tasks

- [ ] Normalize measurement units
- [ ] Apply exchange weights where appropriate
- [ ] Align timestamps
- [ ] Aggregate data
- [ ] Compare exchange behavior
- [ ] Detect divergences

### Expected Result

The platform provides a market-wide view instead of a single-exchange view.

---

## Phase 13 — Market Scanner

**Status:** ⬜ TODO

### Goal

Automatically search for unusual market conditions.

### Initial Scanner Conditions

- abnormal volume
- Open Interest spike
- price breakout
- CVD divergence
- funding extremes
- spot/futures divergence
- cross-exchange divergence

### Expected Result

The system ranks instruments based on current market conditions.

Example:

```text
SOLUSDT    91
BTCUSDT    82
ETHUSDT    67
XRPUSDT    45
```

---

## Phase 14 — Market Scoring

**Status:** ⬜ TODO

### Goal

Create an interpretable market opportunity score.

### Initial Approach

Start with rule-based scoring.

Possible components:

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

### Expected Result

Each instrument receives a score from 0 to 100.

Machine learning should not be introduced until the rule-based system and dataset are validated.

---

## Phase 15 — Backtesting

**Status:** ⬜ TODO

### Goal

Measure whether scanner conditions and signals have historical value.

### Tasks

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

### Expected Result

The project can distinguish useful signals from visually interesting but unprofitable patterns.

---

## Phase 16 — Machine Learning

**Status:** ⬜ TODO

### Goal

Use historical features to estimate future market outcomes.

### Initial Models

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
- no future data leakage
- transaction costs included
- feature importance analysis

### Expected Result

ML becomes an additional analytical layer, not the foundation of the platform.

---

## Phase 17 — Signal Engine

**Status:** ⬜ TODO

### Goal

Convert scanner and model outputs into structured market signals.

Possible signal information:

```text
symbol
direction
score
probability
timestamp
reasons
market conditions
```

Example:

```text
SOLUSDT

Direction: LONG
Score: 89
Probability: 0.74

Reasons:
- Open Interest increasing
- Positive Spot CVD
- Relative volume above normal
- Neutral funding
- Breakout confirmed
```

---

## Phase 18 — Product Layer

**Status:** ⬜ TODO

### Goal

Turn the analytical engine into a usable application.

Potential modules:

- web dashboard
- market scanner
- instrument detail view
- alerts
- historical signal explorer
- backtesting interface
- REST API
- user accounts
- subscription plans

### Expected Result

Crypto Market Intelligence becomes a usable analytical product rather than only a research project.

---

## Long-Term Architecture

```text
Exchange APIs
    ↓
Exchange Clients
    ↓
Collectors
    ↓
BaseMarketData Child Models
    ↓
Database
    ↓
Synchronization
    ↓
Feature Engineering
    ↓
Cross-Exchange Aggregation
    ↓
Market State
    ↓
Scanner
    ↓
Scoring
    ↓
Machine Learning
    ↓
Signals
    ↓
Backtesting
    ↓
API / Dashboard / Alerts
```

---

## Development Rule

Do not move to the next major layer until the previous layer is reliable.

The development order should remain:

```text
Data quality
    before
Features
    before
Scanner
    before
Machine Learning
    before
Signals
    before
Product monetization
```

A reliable dataset is more important than an advanced model built on incomplete or inconsistent market data.