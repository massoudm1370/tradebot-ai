# TradeBot AI — Signal-Only Research Terminal

A first working codebase for a professional AI-ready charting and signal research platform. **No live trading, order execution, wallet custody or private keys.**

## Current features
- FastAPI backend with **deterministic SYNTHETIC candles**, and SMA, EMA, RSI, ATR.
- Illustrative (unvalidated) EMA + RSI signal with optional Entry/SL/TP levels using synthetic prices.
- Next.js frontend using TradingView Lightweight Charts, candlesticks, EMA overlays and synthetic price lines.
- Python unit/API tests and GitHub Actions workflow.

**Not yet implemented:** real-time feeds, historical decade ingestion, trainable ML/DL, backtesting engine, simulated wallet, timeframe optimisation, or trading platform plugins. These belong to future milestones.

## Run backend
```bash
cd apps/api
python -m venv .venv
# Activate the virtualenv for your shell, then:
python -m pip install -e ".[test]"
uvicorn tradebot.main:app --reload --port 8000
python -m pytest -q
```

## Run frontend
```bash
cd apps/web
npm install
npm run dev
```
Open http://localhost:3000. Optional: set `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000` in your local shell.

## Important
Do not use these synthetic price levels to place actual trades. The API has no order-placement capability. See [the roadmap](docs/ROADMAP.md) and [coding rules](AGENTS.md).
