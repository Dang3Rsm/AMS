# π-AMS: Python Trading & Execution Infrastructure

A lightweight Python trading backend and execution system simulating real-time exchange order routing, market data ingestion, and trigger-enforced ledger accounting.

---

## ⚡ Core Trading Systems & Features

* **Market Data Ingestion Engine**: Streams live quotes and 5-minute intraday OHLC candlestick charts via Yahoo Finance (`yfinance`) across 3,370+ NASDAQ tickers with automated offline session synthesis.
* **Order Execution Pipeline**: Simulates exchange fill latencies (`Pending` $\rightarrow$ `Completed` / `Cancelled`) via asynchronous worker threads with live order cancellation support.
* **Pre-Trade Risk & Sizing Controls**: Enforces pre-trade validation to block invalid quantities and prevent short-selling unheld inventory.
* **Automated VWAP & P&L Ledger**: Atomic database triggers recalculate volume-weighted average price (VWAP) and live realized/unrealized P&L immediately upon fill completion.
* **Audit Trail & Governance**: Immutable transactional audit logging (`user_audit`) tracking trade lifecycle events and user actions with multi-tier RBAC (`Trader`, `Admin`).

---

## 🛠️ Tech Stack

* **Backend & Concurrency**: Python 3.12, Flask, Threading, APScheduler
* **Market Data & Analytics**: `yfinance`, Pandas, NumPy, Plotly (Candlesticks)
* **Ledger & Persistence**: MySQL (ACID Transactions, SQL Triggers, Foreign Keys)
* **Auth & Security**: Bcrypt salted hashing, Session-based RBAC

---

## 🚀 Quickstart

```bash
# 1. Clone & setup virtualenv
git clone https://github.com/your-username/AMS.git
cd AMS
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Seed database (schemas, triggers, and 3,370+ NASDAQ stocks)
python setup_db.py

# 3. Launch server
python run.py
```
Open **`http://localhost:5000`** in your browser.

### Demo Logins
* **Trader**: `user@ams.com` | `password123`
* **Admin**: `admin@ams.com` | `password123`
