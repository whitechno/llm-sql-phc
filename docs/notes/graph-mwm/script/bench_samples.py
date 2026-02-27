"""
Named sample graphs — correctness check and timing for all three libraries:
NetworkX, rustworkx, mwmatching (van Rantwijk v3).
"""

from common import (
    edge_weight_map, nx_graph, rx_graph,
    time_nx, time_rx, time_mw,
    weight_nx, weight_rx, weight_mw,
)

SAMPLES = [
    {
        "name": "tiny (4 nodes, from graph-CLAUDE.md)",
        "edges": [(1, 2, 1), (2, 3, 3), (3, 4, 1), (1, 3, 1)],
    },
    {
        "name": "path P6",
        "edges": [(i, i + 1, i + 1) for i in range(5)],
    },
    {
        "name": "complete K6 (all weights=1)",
        "edges": [(u, v, 1) for u in range(6) for v in range(u + 1, 6)],
    },
    {
        "name": "complete K6 (random weights)",
        "edges": [(u, v, (u * 7 + v * 3) % 10 + 1) for u in range(6) for v in range(u + 1, 6)],
    },
]


def run_sample(name: str, edges: list[tuple]) -> None:
    g_nx = nx_graph(edges)
    g_rx = rx_graph(edges)
    wmap = edge_weight_map(edges)

    t_nx, m_nx = time_nx(g_nx)
    t_rx, m_rx = time_rx(g_rx)
    t_mw, m_mw = time_mw(edges)

    w_nx = weight_nx(g_nx, m_nx)
    w_rx = weight_rx(g_rx, m_rx)
    w_mw = weight_mw(wmap, m_mw)

    weights = f"nx={w_nx} rx={w_rx} mw={w_mw}"
    ok = "OK" if w_nx == w_rx == w_mw else f"MISMATCH ({weights})"

    n = g_nx.number_of_nodes()
    m = g_nx.number_of_edges()
    print(f"  {name}")
    print(f"    n={n}, m={m}  |  weight: {weights}  [{ok}]")
    print(f"    time:  nx={t_nx*1e6:.1f} µs"
          f"   rx={t_rx*1e6:.1f} µs  (speedup {t_nx/t_rx:.1f}x)"
          f"   mw={t_mw*1e6:.1f} µs  (speedup {t_nx/t_mw:.1f}x)")
    print()


def main() -> None:
    print("=" * 72)
    print("  Named sample graphs: NetworkX vs rustworkx vs mwmatching")
    print("=" * 72)
    print()
    for s in SAMPLES:
        run_sample(s["name"], s["edges"])


if __name__ == "__main__":
    main()
