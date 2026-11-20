"""Deterministic synthetic price series and indicator research; not live market data."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from math import sin, cos, isfinite


def demo_candles(n: int = 240) -> list[dict]:
    if not 35 <= n <= 2000:
        raise ValueError("n must be between 35 and 2000")
    start = datetime(2025, 1, 1, tzinfo=timezone.utc)
    result = []
    prev = 100.0
    for i in range(n):
        close = round(100 + i * 0.035 + 3 * sin(i / 12) + cos(i / 5), 4)
        result.append({
            "time": int((start + timedelta(hours=i)).timestamp()),
            "open": prev,
            "high": round(max(prev, close) + 0.8, 4),
            "low": round(min(prev, close) - 0.8, 4),
            "close": close,
            "volume": round(1000 + abs(200 * sin(i / 7)), 2)
        })
        prev = close
    return result


def sma(values: list[float], period: int) -> list[float | None]:
    _validate(values, period)
    result = [None] * len(values)
    for i in range(period - 1, len(values)):
        result[i] = sum(values[i - period + 1:i + 1]) / period
    return result


def ema(values: list[float], period: int) -> list[float | None]:
    _validate(values, period)
    result = [None] * len(values)
    if len(values) < period:
        return result
    previous = sum(values[:period]) / period
    result[period - 1] = previous
    alpha = 2 / (period + 1)
    for i in range(period, len(values)):
        previous = alpha * values[i] + (1 - alpha) * previous
        result[i] = previous
    return result


def rsi(values: list[float], period: int = 14) -> list[float | None]:
    _validate(values, period)
    result = [None] * len(values)
    if len(values) <= period:
        return result
    delta = [values[i] - values[i - 1] for i in range(1, len(values))]
    gain = sum(max(x, 0) for x in delta[:period]) / period
    loss = sum(max(-x, 0) for x in delta[:period]) / period
    def calc(g: float, l: float) -> float:
        if g == 0 and l == 0:
            return 50
        if l == 0:
            return 100
        return 100 - 100 / (1 + g / l)
    result[period] = calc(gain, loss)
    for i in range(period + 1, len(values)):
        change = delta[i - 1]
        gain = (gain * (period - 1) + max(change, 0)) / period
        loss = (loss * (period - 1) + max(-change, 0)) / period
        result[i] = calc(gain, loss)
    return result


def atr(candles: list[dict], period: int = 14) -> list[float | None]:
    if period < 1:
        raise ValueError("period must be positive")
    ranges = []
    for i, candle in enumerate(candles):
        high, low = candle["high"], candle["low"]
        if high < low:
            raise ValueError("invalid candle")
        if i == 0:
            ranges.append(high - low)
        else:
            previous = candles[i - 1]["close"]
            ranges.append(max(high - low, abs(high - previous), abs(low - previous)))
    result = [None] * len(candles)
    if len(candles) < period:
        return result
    previous_atr = sum(ranges[:period]) / period
    result[period - 1] = previous_atr
    for i in range(period, len(candles)):
        previous_atr = (previous_atr * (period - 1) + ranges[i]) / period
        result[i] = previous_atr
    return result


def _validate(values: list[float], period: int) -> None:
    if period < 1:
        raise ValueError("period must be positive")
    if any(not isfinite(value) for value in values):
        raise ValueError("values must be finite")


def research_signal(candles: list[dict]) -> dict:
    close = [c["close"] for c in candles]
    f, s = ema(close, 12)[-1], ema(close, 26)[-1]
    momentum, volatility = rsi(close)[-1], atr(candles)[-1]
    decision = "NO_TRADE"
    if f is not None and s is not None and momentum is not None and volatility is not None:
        if f > s and 50 < momentum < 70:
            decision = "BUY"
        elif f < s and 30 < momentum < 50:
            decision = "SELL"
    answer = {
        "decision": decision, "symbol": "SYNTHETIC/USDT", "venue": "DEMO",
        "timeframe": "1h", "source": "SYNTHETIC_DATA", "simulated_only": True,
        "entry": None, "stop_loss": None, "take_profit": [],
        "reason": "Illustrative EMA(12/26) + RSI(14) + ATR(14) rule; unvalidated"
    }
    if decision != "NO_TRADE":
        from decimal import Decimal, ROUND_HALF_UP
        entry, sign = close[-1], 1 if decision == "BUY" else -1
        def tick(x: float) -> str:
            return str(Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
        answer["entry"] = tick(entry)
        answer["stop_loss"] = tick(entry - sign * 1.5 * volatility)
        answer["take_profit"] = [tick(entry + sign * k * 1.5 * volatility) for k in (1, 2, 3)]
    return answer
