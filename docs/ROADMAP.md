# TradeBot AI build plan
1. Foundation: FastAPI demo research data, Next.js chart, CI tests.
2. Read-only market-data connectors: historical OHLCV, licensed sources, up to 10 years where available; websocket and data quality monitoring.
3. Indicator/strategy registry, event-driven replay and paper-trading simulator.
4. ML/DL: chronological evaluation, walk-forward tests, baselines, probability calibration; avoid guaranteed outcomes.
5. Signal engine: automatic timeframe proposals, entry/SL/TP, liquidity filters, expiry, model provenance.
6. Visual terminal and supported TradingView/MT5/cTrader visual-only plugins. TradingView Pine cannot call arbitrary external HTTP endpoints.
No live order execution at any phase.
