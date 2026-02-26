"""
Combined benchmark: collect timings for all three libraries across the full
size range, print a unified table, and save a log-log plot to bench_plot.svg.

Sizes with all three libs (nx, rx, mw): up to 2,000
Sizes with rx and mw only:              up to 50,000
Sizes with mw only:                     up to 100,000

Note on AVG_DEGREE: each node makes AVG_DEGREE=4 random neighbor attempts,
yielding m ≈ n × AVG_DEGREE = 4n edges (duplicate undirected edges are rare
for large sparse graphs). The actual average node degree is 2m/n ≈ 8, not 4.
AVG_DEGREE is therefore "edges per node" (m/n), not the graph-theoretic
average degree.

Results are cached in bench_plot.json. If the file exists, benchmarks are
skipped and the table + plot are regenerated from cached data.
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

from common import (
    edge_weight_map, nx_graph, rx_graph,
    random_sparse_edges,
    time_nx, time_rx, time_mw,
    weight_nx, weight_rx, weight_mw,
)

# ── benchmark sizes ───────────────────────────────────────────────────────────

SIZES_ALL   = [100, 300, 500, 750, 1_000, 1_500, 2_000]
SIZES_RX_MW = [3_000, 5_000, 7_000, 10_000, 20_000, 50_000]
SIZES_MW    = [100_000]
AVG_DEGREE  = 4 # graph simulation parameter: neighbor attempts per node;
                # m/n ≈ AVG_DEGREE; avg node degree ≈ 2×AVG_DEGREE
REPEATS     = 3

DATA_FILE = Path(__file__).parent / "bench_plot.json"
SVG_FILE  = Path(__file__).parent.parent / "bench_plot.svg"


# ── timing helper ─────────────────────────────────────────────────────────────

def measure(n: int, include_nx: bool = False, include_rx: bool = True) -> dict:
    edges = random_sparse_edges(n, avg_degree=AVG_DEGREE)
    wmap  = edge_weight_map(edges)
    row   = dict(n=n, m=len(edges))

    if include_rx:
        g_rx = rx_graph(edges)
        time_rx(g_rx)  # warm up
        t_rx_total = 0.0
        for _ in range(REPEATS):
            t, m_rx = time_rx(g_rx); t_rx_total += t
        row["rx"]   = t_rx_total / REPEATS * 1e3
        row["w_rx"] = weight_rx(g_rx, m_rx)

    time_mw(edges)  # warm up
    t_mw_total = 0.0
    for _ in range(REPEATS):
        t, m_mw = time_mw(edges); t_mw_total += t
    row["mw"]   = t_mw_total / REPEATS * 1e3
    row["w_mw"] = weight_mw(wmap, m_mw)

    if include_nx:
        g_nx = nx_graph(edges)
        time_nx(g_nx)  # warm up
        t_nx_total = 0.0
        for _ in range(REPEATS):
            t, m_nx = time_nx(g_nx); t_nx_total += t
        row["nx"]   = t_nx_total / REPEATS * 1e3
        row["w_nx"] = weight_nx(g_nx, m_nx)

    return row


# ── run / cache ───────────────────────────────────────────────────────────────

def run_benchmarks() -> list[dict]:
    rows  = []
    sizes = ([(n, True,  True)  for n in SIZES_ALL]   +
             [(n, False, True)  for n in SIZES_RX_MW] +
             [(n, False, False) for n in SIZES_MW])
    total = len(sizes)
    for i, (n, inc_nx, inc_rx) in enumerate(sizes, 1):
        label = "all three" if inc_nx else ("rx + mw" if inc_rx else "mw only")
        print(f"  [{i}/{total}] n={n:,} ({label}) …", flush=True)
        rows.append(measure(n, include_nx=inc_nx, include_rx=inc_rx))
    return rows


def load_or_run() -> list[dict]:
    if DATA_FILE.exists():
        print(f"  Loading cached data from {DATA_FILE.name}")
        return json.loads(DATA_FILE.read_text())
    print("  No cache found — running benchmarks …")
    rows = run_benchmarks()
    DATA_FILE.write_text(json.dumps(rows, indent=2))
    print(f"  Results saved to {DATA_FILE.name}")
    return rows


# ── table ─────────────────────────────────────────────────────────────────────

def print_table(rows: list[dict]) -> None:
    print()
    print(f"  {'n':>7}  {'m':>8}  {'nx (ms)':>12}  {'rx (ms)':>12}  {'mw (ms)':>12}  weights")
    print(f"  {'-'*7}  {'-'*8}  {'-'*12}  {'-'*12}  {'-'*12}  {'-'*7}")
    for r in rows:
        nx_s = f"{r['nx']:>12.2f}" if "nx" in r else f"{'—':>12}"
        rx_s = f"{r['rx']:>12.2f}" if "rx" in r else f"{'—':>12}"
        if "nx" in r and "rx" in r:
            ok = "OK" if r["w_nx"] == r["w_rx"] == r["w_mw"] else "MISMATCH"
        elif "rx" in r:
            ok = "OK" if r["w_rx"] == r["w_mw"] else "MISMATCH"
        else:
            ok = "—"
        print(f"  {r['n']:>7,}  {r['m']:>8,}  {nx_s}  {rx_s}  {r['mw']:>12.2f}  {ok}")
    print()


# ── plot ──────────────────────────────────────────────────────────────────────

def save_plot(rows: list[dict]) -> None:
    ns_nx = [r["n"] for r in rows if "nx" in r]
    ns_rx = [r["n"] for r in rows if "rx" in r]
    ns_mw = [r["n"] for r in rows]

    t_nx = [r["nx"] for r in rows if "nx" in r]
    t_rx = [r["rx"] for r in rows if "rx" in r]
    t_mw = [r["mw"] for r in rows]

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.loglog(ns_nx, t_nx, "o-", color="#e15759", lw=2, ms=5,
              label="NetworkX  O(n³) Python")
    ax.loglog(ns_rx, t_rx, "s-", color="#4e79a7", lw=2, ms=5,
              label="rustworkx  O(n³) Rust")
    ax.loglog(ns_mw, t_mw, "^-", color="#59a14f", lw=2, ms=5,
              label="mwmatching  O(nm log n) Python")

    ax.axvline(x=2_000, color="gray", lw=1, ls="--", alpha=0.6)
    ax.text(2_200, t_mw[0] * 0.6, "crossover\n≈ n=2,000",
            fontsize=8, color="gray", va="top")

    ax.set_xlabel("n  (number of nodes, log scale)", fontsize=11)
    ax.set_ylabel("time  (ms, log scale)", fontsize=11)
    ax.set_title(
        "Compare Max Weight Matching libs: NetworkX vs rustworkx vs mwmatching\n"
        "random sparse graphs,  m/n ≈ 4  (avg node degree ≈ 8)",
        fontsize=11)

    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: f"{y:g}"))
    ax.legend(fontsize=9)
    ax.grid(True, which="both", ls=":", alpha=0.5)

    fig.tight_layout()
    fig.savefig(SVG_FILE, format="svg")
    print(f"  Plot saved to {SVG_FILE.name}")


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    print("=" * 72)
    print("  Combined benchmark: NetworkX vs rustworkx vs mwmatching")
    print("=" * 72)
    print()

    rows = load_or_run()

    print("=" * 72)
    print("  Results")
    print("=" * 72)
    print_table(rows)

    save_plot(rows)


if __name__ == "__main__":
    main()
