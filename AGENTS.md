# TradeBot AI rules
- SIGNAL ONLY: no broker/exchange order routes, exchange trading keys, custody, blockchain signing or real-money execution.
- Clearly label synthetic feeds and signals as DEMO / NOT LIVE.
- Unknown, stale or missing data means NO_TRADE.
- Never claim 90% win rate, trained ML models or 10-year coverage without real evidence.
- Avoid future-data leakage; all indicators compute from past bars only.
- Implement small PRs with tests and document unimplemented features.
