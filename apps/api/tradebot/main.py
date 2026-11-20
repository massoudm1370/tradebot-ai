"""Read-only research API. No real-money order endpoints."""
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from .quant import demo_candles, sma, ema, rsi, atr, research_signal

app = FastAPI(title="TradeBot AI - Signal Research", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_methods=["GET"], allow_headers=["*"])


@app.get("/health")
def health():
    return {"status": "ok", "mode": "SIGNAL_ONLY", "feed": "SYNTHETIC_DATA"}


@app.get("/api/demo")
def demo(count: int = Query(240, ge=35, le=2000)):
    candles = demo_candles(count)
    close = [c["close"] for c in candles]
    return {
        "source": "SYNTHETIC_DATA", "is_live": False,
        "symbol": "SYNTHETIC/USDT", "timeframe": "1h",
        "candles": candles,
        "indicators": {
            "sma20": sma(close, 20),
            "ema12": ema(close, 12),
            "ema26": ema(close, 26),
            "rsi14": rsi(close, 14),
            "atr14": atr(candles, 14),
        },
        "signal": research_signal(candles)
    }


@app.get("/api/capabilities")
def capabilities():
    return {
        "live_data": False,
        "ten_year_history": False,
        "trained_ml": False,
        "live_execution": False,
        "paper_wallet": False,
        "supported": ["synthetic_feed", "sma", "ema", "rsi", "atr", "illustrative_signal"]
    }
