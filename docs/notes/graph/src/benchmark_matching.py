"""
Benchmark max_weight_matching: NetworkX vs rustworkx.

Sample graphs:
  - small path / cycle graphs for correctness spot-check
  - random sparse graphs of increasing size (m ~ 4n) for timing
"""

import random
import time

import networkx as nx
import rustworkx as rx


# ── helpers ──────────────────────────────────────────────────────────────────

def random_sparse_edges(n: int, avg_degree: int = 4, seed: int = 0) -> list[tuple]:
    """Return a list of (u, v, weight) for a random sparse graph with ~avg_degree*n/2 edges."""
    rng = random.Random(seed)
    edge_set = set()
    for u in range(n):
        for _ in range(avg_degree):
            v = rng.randint(0, n - 1)
            if v != u:
                edge_set.add((min(u, v), max(u, v)))
    return [(u, v, rng.randint(1, 100)) for u, v in edge_set]


def nx_graph(edges: list[tuple]) -> nx.Graph:
    g = nx.Graph()
    for u, v, w in edges:
        g.add_edge(u, v, weight=w)
    return g


def rx_graph(edges: list[tuple]) -> rx.PyGraph:
    n = max(max(u, v) for u, v, _ in edges) + 1
    g = rx.PyGraph()
    g.add_nodes_from(range(n))
    for u, v, w in edges:
        g.add_edge(u, v, w)
    return g


def time_nx(g: nx.Graph) -> tuple[float, set]:
    t0 = time.perf_counter()
    result = nx.max_weight_matching(g, maxcardinality=False)
    elapsed = time.perf_counter() - t0
    return elapsed, result


def time_rx(g: rx.PyGraph) -> tuple[float, set]:
    t0 = time.perf_counter()
    # weight_fn is required; without it rustworkx uses default_weight=1 for all edges
    result = rx.max_weight_matching(g, max_cardinality=False, weight_fn=lambda x: x)
    elapsed = time.perf_counter() - t0
    return elapsed, result


def matching_weight_nx(g: nx.Graph, matching: set) -> int:
    return sum(g[u][v]["weight"] for u, v in matching)


def matching_weight_rx(g: rx.PyGraph, matching: set) -> int:
    return sum(g.get_edge_data(u, v) for u, v in matching)


# ── named sample graphs ───────────────────────────────────────────────────────

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


# ── main ─────────────────────────────────────────────────────────────────────

def run_sample(name: str, edges: list[tuple]) -> None:
    g_nx = nx_graph(edges)
    g_rx = rx_graph(edges)

    t_nx, m_nx = time_nx(g_nx)
    t_rx, m_rx = time_rx(g_rx)

    w_nx = matching_weight_nx(g_nx, m_nx)
    w_rx = matching_weight_rx(g_rx, m_rx)

    match_ok = "OK" if w_nx == w_rx else f"MISMATCH (nx={w_nx} rx={w_rx})"

    n = g_nx.number_of_nodes()
    m = g_nx.number_of_edges()
    print(f"  {name}")
    print(f"    n={n}, m={m}  |  weight: nx={w_nx} rx={w_rx}  [{match_ok}]")
    print(f"    time:  nx={t_nx*1e6:.1f} µs   rx={t_rx*1e6:.1f} µs   "
          f"speedup={t_nx/t_rx:.1f}x" if t_rx > 0 else "")
    print()


def run_scaling(sizes: list[int], avg_degree: int = 4, repeats: int = 5) -> None:
    print(f"  {'n':>7}  {'m':>7}  {'nx (ms)':>10}  {'rx (ms)':>10}  {'speedup':>8}  weight-match")
    print(f"  {'-'*7}  {'-'*7}  {'-'*10}  {'-'*10}  {'-'*8}  {'-'*12}")
    for n in sizes:
        edges = random_sparse_edges(n, avg_degree=avg_degree)
        g_nx = nx_graph(edges)
        g_rx = rx_graph(edges)

        # warm up
        nx.max_weight_matching(g_nx, maxcardinality=False)
        rx.max_weight_matching(g_rx, max_cardinality=False)

        t_nx_total = 0.0
        t_rx_total = 0.0
        for _ in range(repeats):
            t, m_nx = time_nx(g_nx)
            t_nx_total += t
            t, m_rx = time_rx(g_rx)
            t_rx_total += t

        t_nx = t_nx_total / repeats
        t_rx = t_rx_total / repeats

        w_nx = matching_weight_nx(g_nx, m_nx)
        w_rx = matching_weight_rx(g_rx, m_rx)
        match_ok = "OK" if w_nx == w_rx else f"MISMATCH"
        speedup = t_nx / t_rx if t_rx > 0 else float("inf")

        print(f"  {n:>7,}  {g_nx.number_of_edges():>7,}  "
              f"{t_nx*1e3:>10.2f}  {t_rx*1e3:>10.2f}  {speedup:>7.1f}x  {match_ok}")


def main() -> None:
    print("=" * 64)
    print("  max_weight_matching benchmark: NetworkX vs rustworkx")
    print("=" * 64)
    print()

    print("── Named sample graphs ──────────────────────────────────────")
    print()
    for s in SAMPLES:
        run_sample(s["name"], s["edges"])

    print("── Scaling: random sparse graphs (avg degree ≈ 4) ───────────")
    print()
    # NetworkX is pure Python O(n³) so large n is very slow; cap at 2000
    sizes = [100, 300, 500, 750, 1_000, 1_500, 2_000]
    run_scaling(sizes, avg_degree=4, repeats=3)
    print()


if __name__ == "__main__":
    main()
