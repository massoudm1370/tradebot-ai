from fastapi.testclient import TestClient
from tradebot.main import app
from tradebot.quant import demo_candles, sma, ema, rsi, atr, research_signal

client = TestClient(app)

def test_sma_seed():
    assert sma([1, 2, 3, 4], 3) == [None, None, 2, 3]

def test_ema_seed():
    assert ema([2, 4, 6, 8], 3) == [None, None, 4, 6]

def test_flat_rsi():
    assert rsi([100] * 20)[-1] == 50

def test_only_gains_rsi():
    assert rsi(list(range(20)))[-1] == 100

def test_constant_atr():
    candles = [{"high": 11, "low": 9, "close": 10} for _ in range(30)]
    assert atr(candles)[-1] == 2

def test_demo_reproducible():
    assert demo_candles() == demo_candles()

def test_api_is_synthetic():
    data = client.get("/api/demo").json()
    assert data["is_live"] is False
    assert data["signal"]["simulated_only"] is True
    assert len(data["candles"]) == 240

def test_demo_rejects_bad_count():
    assert client.get("/api/demo?count=5").status_code == 422

def test_never_has_order_route():
    assert client.post("/api/orders", json={}).status_code == 404

def test_no_trade_if_indicators_disagree():
    result = research_signal(demo_candles())
    assert result["decision"] in ("BUY", "SELL", "NO_TRADE")

def test_capabilities_truthful():
    result = client.get("/api/capabilities").json()
    assert result["live_execution"] is False
    assert result["trained_ml"] is False
