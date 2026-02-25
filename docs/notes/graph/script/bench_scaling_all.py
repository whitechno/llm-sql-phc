"""
Scaling benchmark for all three libraries: NetworkX, rustworkx, mwmatching.
Random sparse graphs (avg degree ≈ 4), n up to 2,000.
NetworkX is pure Python O(n³) and becomes impractical beyond this range.
"""

from common import (
    edge_weight_map, nx_graph, rx_graph,
    random_sparse_edges,
    time_nx, time_rx, time_mw,
    weight_nx, weight_rx, weight_mw,
)

SIZES = [100, 300, 500, 750, 1_000, 1_500, 2_000]
AVG_DEGREE = 4
REPEATS = 3


def main() -> None:
    print("=" * 72)
    print("  Scaling: NetworkX vs rustworkx vs mwmatching (n up to 2,000)")
    print("=" * 72)
    print()

    w = 10
    print(f"  {'n':>7}  {'m':>7}  {'nx (ms)':>{w}}  {'rx (ms)':>{w}}  {'mw (ms)':>{w}}"
          f"  {'nx/rx':>6}  {'nx/mw':>6}  {'rx/mw':>6}  weights")
    print(f"  {'-'*7}  {'-'*7}  {'-'*w}  {'-'*w}  {'-'*w}"
          f"  {'-'*6}  {'-'*6}  {'-'*6}  {'-'*7}")

    for n in SIZES:
        edges = random_sparse_edges(n, avg_degree=AVG_DEGREE)
        g_nx = nx_graph(edges)
        g_rx = rx_graph(edges)
        wmap = edge_weight_map(edges)

        # warm up
        time_nx(g_nx)
        time_rx(g_rx)
        time_mw(edges)

        t_nx_total = t_rx_total = t_mw_total = 0.0
        for _ in range(REPEATS):
            t, m_nx = time_nx(g_nx)
            t_nx_total += t
            t, m_rx = time_rx(g_rx)
            t_rx_total += t
            t, m_mw = time_mw(edges)
            t_mw_total += t

        t_nx = t_nx_total / REPEATS
        t_rx = t_rx_total / REPEATS
        t_mw = t_mw_total / REPEATS

        w_nx = weight_nx(g_nx, m_nx)
        w_rx = weight_rx(g_rx, m_rx)
        w_mw = weight_mw(wmap, m_mw)
        ok = "OK" if w_nx == w_rx == w_mw else f"nx={w_nx} rx={w_rx} mw={w_mw}"

        print(f"  {n:>7,}  {len(edges):>7,}"
              f"  {t_nx*1e3:>{w}.2f}  {t_rx*1e3:>{w}.2f}  {t_mw*1e3:>{w}.2f}"
              f"  {t_nx/t_rx:>5.1f}x  {t_nx/t_mw:>5.1f}x  {t_rx/t_mw:>5.1f}x  {ok}")

    print()


if __name__ == "__main__":
    main()
