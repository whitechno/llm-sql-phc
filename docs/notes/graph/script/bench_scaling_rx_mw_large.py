"""
Large-scale benchmark for rustworkx vs mwmatching (van Rantwijk v3).
Random sparse graphs (avg degree ≈ 4), n = 10,000 to 50,000.
NetworkX excluded — O(n³) pure Python is impractical at this scale.
"""

from common import (
    edge_weight_map, rx_graph,
    random_sparse_edges,
    time_rx, time_mw,
    weight_rx, weight_mw,
)

SIZES = [10_000, 20_000, 50_000]
AVG_DEGREE = 4
REPEATS = 3


def main() -> None:
    print("=" * 72)
    print("  Large-scale: rustworkx vs mwmatching (n up to 50,000)")
    print("=" * 72)
    print()

    w = 12
    print(f"  {'n':>7}  {'m':>8}  {'rx (ms)':>{w}}  {'mw (ms)':>{w}}"
          f"  {'rx/mw':>6}  weights")
    print(f"  {'-'*7}  {'-'*8}  {'-'*w}  {'-'*w}  {'-'*6}  {'-'*7}")

    for n in SIZES:
        edges = random_sparse_edges(n, avg_degree=AVG_DEGREE)
        g_rx = rx_graph(edges)
        wmap = edge_weight_map(edges)

        # warm up
        time_rx(g_rx)
        time_mw(edges)

        t_rx_total = t_mw_total = 0.0
        for _ in range(REPEATS):
            t, m_rx = time_rx(g_rx)
            t_rx_total += t
            t, m_mw = time_mw(edges)
            t_mw_total += t

        t_rx = t_rx_total / REPEATS
        t_mw = t_mw_total / REPEATS

        w_rx = weight_rx(g_rx, m_rx)
        w_mw = weight_mw(wmap, m_mw)
        ok = "OK" if w_rx == w_mw else f"rx={w_rx} mw={w_mw}"

        print(f"  {n:>7,}  {len(edges):>8,}"
              f"  {t_rx*1e3:>{w}.2f}  {t_mw*1e3:>{w}.2f}"
              f"  {t_rx/t_mw:>5.1f}x  {ok}")

    print()


if __name__ == "__main__":
    main()
