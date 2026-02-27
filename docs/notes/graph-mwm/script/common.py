"""Shared helpers for max_weight_matching benchmarks."""

import random
import time

import mwmatching
import networkx as nx
import rustworkx as rx


# ── graph builders ────────────────────────────────────────────────────────────

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


def edge_weight_map(edges: list[tuple]) -> dict:
    """Build {(u,v): w} lookup (both orderings) for scoring mwmatching results."""
    return {(u, v): w for u, v, w in edges} | {(v, u): w for u, v, w in edges}


# ── timed solvers ─────────────────────────────────────────────────────────────

def time_nx(g: nx.Graph) -> tuple[float, set]:
    t0 = time.perf_counter()
    result = nx.max_weight_matching(g, maxcardinality=False)
    return time.perf_counter() - t0, result


def time_rx(g: rx.PyGraph) -> tuple[float, set]:
    t0 = time.perf_counter()
    # weight_fn required; without it rustworkx uses default_weight=1 for all edges
    result = rx.max_weight_matching(g, max_cardinality=False, weight_fn=lambda x: x)
    return time.perf_counter() - t0, result


def time_mw(edges: list[tuple]) -> tuple[float, list]:
    t0 = time.perf_counter()
    result = mwmatching.maximum_weight_matching(edges)
    return time.perf_counter() - t0, result


# ── matching weight ───────────────────────────────────────────────────────────

def weight_nx(g: nx.Graph, matching: set) -> int:
    return sum(g[u][v]["weight"] for u, v in matching)


def weight_rx(g: rx.PyGraph, matching: set) -> int:
    return sum(g.get_edge_data(u, v) for u, v in matching)


def weight_mw(wmap: dict, matching: list) -> int:
    return sum(wmap[u, v] for u, v in matching)


# ── random graph generator ────────────────────────────────────────────────────

def random_sparse_edges(n: int, avg_degree: int = 4, seed: int = 0) -> list[tuple]:
    """Return (u, v, weight) list for a random sparse graph with ~avg_degree*n/2 edges."""
    rng = random.Random(seed)
    edge_set = set()
    for u in range(n):
        for _ in range(avg_degree):
            v = rng.randint(0, n - 1)
            if v != u:
                edge_set.add((min(u, v), max(u, v)))
    return [(u, v, rng.randint(1, 100)) for u, v in edge_set]
