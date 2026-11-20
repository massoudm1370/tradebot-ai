# TradeBot AI

AI-assisted, **signal-only** quantitative research and visual trading terminal.

> **Safety:** TradeBot AI is for research, charting, historical evaluation and simulated trading. It must not submit live exchange/broker orders, hold user funds or sign blockchain transactions.

## Status

Initial repository bootstrap. A working vertical slice will be introduced through a pull request.

## Intended architecture

- **Web:** Next.js / TypeScript / TradingView Lightweight Charts.
- **API:** Python / FastAPI with deterministic demo market data.
- **Research:** Indicators, strategy registry, walk-forward validation, later ML/DL.
- **Integrations:** Read-only market data and supported chart companion plugins.
- **Execution:** Paper/simulated only.

All example prices and signals must be clearly labelled as synthetic, never real-time market recommendations.

See the forthcoming `docs/` and `AGENTS.md` for development instructions.
