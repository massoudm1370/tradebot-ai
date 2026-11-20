"use client";

import { useEffect, useRef, useState } from "react";
import { createChart, CandlestickSeries, LineSeries, type IChartApi, type UTCTimestamp } from "lightweight-charts";

type Candle = { time: number; open: number; high: number; low: number; close: number; volume: number };
type Signal = { decision: string; entry: string | null; stop_loss: string | null; take_profit: string[]; timeframe: string; reason: string; simulated_only: boolean };
type Data = { candles: Candle[]; indicators: { ema12: (number | null)[]; ema26: (number | null)[]; rsi14: (number | null)[] }; signal: Signal; source: string; symbol: string; timeframe: string; is_live: boolean };

function Chart({ data }: { data: Data }) {
  const div = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!div.current) return;
    const node = div.current;
    const chart: IChartApi = createChart(node, {
      width: node.clientWidth, height: node.clientHeight,
      layout: { background: { color: "#131a26" }, textColor: "#98a4b8" },
      grid: { vertLines: { color: "#222d3f" }, horzLines: { color: "#222d3f" } },
      rightPriceScale: { borderColor: "#29364a" },
      timeScale: { borderColor: "#29364a", timeVisible: true },
    });
    const bars = chart.addSeries(CandlestickSeries, { upColor: "#24c59e", downColor: "#ff657b", wickUpColor: "#24c59e", wickDownColor: "#ff657b", borderVisible: false });
    bars.setData(data.candles.map(c => ({ ...c, time: c.time as UTCTimestamp })));
    const addLine = (values: (number | null)[], color: string) => {
      const series = chart.addSeries(LineSeries, { color, lineWidth: 2, priceLineVisible: false, lastValueVisible: false });
      series.setData(values.flatMap((value, i) => value === null ? [] : [{ time: data.candles[i].time as UTCTimestamp, value }]));
    };
    addLine(data.indicators.ema12, "#e9b44c");
    addLine(data.indicators.ema26, "#599cff");
    if (data.signal.entry) {
      bars.createPriceLine({ price: Number(data.signal.entry), color: "#f5bd55", lineWidth: 2, axisLabelVisible: true, title: "DEMO ENTRY" });
      bars.createPriceLine({ price: Number(data.signal.stop_loss), color: "#ff657b", lineWidth: 2, axisLabelVisible: true, title: "DEMO SL" });
      for (const [i, tp] of data.signal.take_profit.entries()) {
        bars.createPriceLine({ price: Number(tp), color: "#24c59e", lineWidth: 1, axisLabelVisible: true, title: "DEMO TP" + (i + 1) });
      }
    }
    chart.timeScale().fitContent();
    const observer = new ResizeObserver(() => chart.applyOptions({ width: node.clientWidth, height: node.clientHeight }));
    observer.observe(node);
    return () => { observer.disconnect(); chart.remove(); };
  }, [data]);
  return <div ref={div} className="chart" aria-label="Synthetic candlestick research chart" />;
}

export default function Home() {
  const [data, setData] = useState<Data | null>(null);
  const [error, setError] = useState<string | null>(null);
  useEffect(() => {
    const controller = new AbortController();
    fetch((process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000") + "/api/demo", { signal: controller.signal })
      .then(r => { if (!r.ok) throw new Error("API returned " + r.status); return r.json(); })
      .then((result: Data) => setData(result))
      .catch(e => { if (!controller.signal.aborted) setError(String(e)); });
    return () => controller.abort();
  }, []);
  return <>
    <header><div className="logo">TRADEBOT <span>AI</span></div><div className="tag">DEMO · NO LIVE TRADING</div></header>
    <main>
      <div className="headline"><h1>Quant Research Terminal</h1><div className="muted">AI-ready visual research workspace · Signal-only · No broker execution</div></div>
      <div className="notice">All prices, candles and signals below are SYNTHETIC. This is not a live market feed or investment recommendation.</div>
      {error && <div className="panel" role="alert">API unavailable: {error}. Start the FastAPI server on port 8000.</div>}
      {!data && !error && <div className="panel">Loading synthetic demo data…</div>}
      {data && <div className="grid">
        <section className="panel">
          <h2>{data.symbol} <span className="muted small">/ {data.timeframe} · Synthetic candles</span></h2>
          <Chart data={data} />
          <div className="metric"><span className="muted">Chart indicators</span><span>EMA 12 / EMA 26</span></div>
        </section>
        <aside className="stacked">
          <div className="panel"><h2>Illustrative signal</h2>
            <div className="status">{data.signal.decision}</div>
            <div className="metric"><span className="muted">Timeframe</span><span className="value">{data.signal.timeframe}</span></div>
            <div className="metric"><span className="muted">Entry</span><span className="value">{data.signal.entry ?? "—"}</span></div>
            <div className="metric"><span className="muted">Stop loss</span><span className="value negative">{data.signal.stop_loss ?? "—"}</span></div>
            {data.signal.take_profit.map((tp, i) => <div key={i} className="metric"><span className="muted">Take profit {i + 1}</span><span className="value positive">{tp}</span></div>)}
            <p className="muted small">{data.signal.reason}</p>
          </div>
          <div className="panel"><h2>Project status</h2>
            <div className="metric"><span className="muted">Live prices</span><span>Not connected</span></div>
            <div className="metric"><span className="muted">ML training</span><span>Not implemented</span></div>
            <div className="metric"><span className="muted">Execution</span><span>Disabled</span></div>
            <div className="metric"><span className="muted">Data source</span><span>SYNTHETIC</span></div>
          </div>
        </aside>
      </div>}
      <div className="footer">TradeBot AI Research Preview · Not financial advice · No live execution</div>
    </main>
  </>;
}
