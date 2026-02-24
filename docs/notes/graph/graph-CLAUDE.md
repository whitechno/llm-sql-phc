# Graph algorithm for max disjoint pairs

## Problem Statement

We have a regular graph with edges of positive weights. We can assume that
weights are integers.

If that can influence the solution, we can also assume that number of edges `M`
is `M ~ C*N`, where `N` is the number of nodes and `C` is some constant.

The goal is to break the graph into disjoint pairs or singles of nodes such that
the sum of the weights of the links connecting the pairs is maximized. The
output graph should not contain incident edges, and it should have the maximum
sum of edge weights.

For example, for a graph with nodes `1,2,3,4` and edges:
```text
A: 2,3
B: 3,4
C: 1,2
D: 1,3
```

<img src="graph-example.svg" width="150" alt="graph-example">

If `wA = 3` and `wB = wC = wD = 1`, then the max-weight output is `A:2,3; 1; 4`
with total weight `wA = 3`.

If `wA = 3` and `wB = wC = wD = 2`, then the max-weight output is
`B:3,4; C:1,2` with total weight `wB + wC = 4`.

**Is there an efficient algorithm for this problem?**
Yes — This Is Maximum Weight Matching

Yes, there is an efficient algorithm for this problem. This is the Maximum
Weight Matching problem, specifically for finding a maximum weight matching in a
general graph. It can be solved efficiently using Edmond's Blossom Algorithm
(also known as the Edmonds-Gallai decomposition), which runs in polynomial time
`O(n³)` or `O(n²m)` depending on the implementation, where `n` is the number of
nodes and `m` is the number of edges.

The problem described is the classical Maximum Weight Matching problem on a
general (non-bipartite) graph. The goal is to select a set of edges with no two
sharing a node (a "matching") such that the total edge weight is maximized.

Efficient Algorithm: Edmond's Blossom Algorithm (Jack Edmonds, 1965, also known
as the Edmonds-Gallai decomposition) solves this in polynomial time. The
weighted generalization runs in:
- `O(n³)` for general graphs
- `O(nm log n)` for sparse graphs (which applies here since `m ~ C·n`)

How It Works (High Level):
1. Start with an empty matching.
2. Repeatedly find augmenting paths — paths that alternate between non-matching
   and matching edges, starting and ending at unmatched nodes.
3. The key complication for general (non-bipartite) graphs is handling
   odd-length cycles ("blossoms"), which the algorithm contracts and then
   expands.
4. Weights are handled via dual variables (from LP duality), ensuring
   optimality.

For the above example with `wA=3, wB=wC=wD=1`:
- Matching `{A}` gives weight 3; matching `{B,C}` gives weight 2. → Algorithm
  picks `{A}`.

For `wA=3, wB=wC=wD=2`:
- Matching `{A}` gives weight 3; matching `{B,C}` gives weight 4. → Algorithm
  picks `{B,C}`.

## Complexity Landscape

```text
┌─────────────┬───────────────────────────────────────┐
│ Complexity  │             Applicable to             │
├─────────────┼───────────────────────────────────────┤
│ O(n³)       │ Dense and sparse graphs (classic)     │ Edmonds' blossom + primal-dual
├─────────────┼───────────────────────────────────────┤
│ O(nm log n) │ Sparse graphs (theoretically optimal) │ Galil, Micali & Gabow
└─────────────┴───────────────────────────────────────┘
```
For `M ~ C·N` (sparse), `O(nm log n) = O(n² log n)`, which is much better than
`O(n³)`.

## Libraries

### O(n³) — Easy to install, actively maintained

**[NetworkX](https://networkx.org/)** `networkx.max_weight_matching()`
([docs](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.matching.max_weight_matching.html))
- Pure Python, Edmonds' blossom + primal-dual
- Uses exact integer arithmetic when all weights are integers
- Slow for large graphs due to Python overhead
- `pip install networkx`

**[rustworkx](https://www.rustworkx.org/)** `rustworkx.max_weight_matching()`
([docs](https://www.rustworkx.org/apiref/rustworkx.max_weight_matching.html),
[GitHub](https://github.com/Qiskit/rustworkx))
- Rust port of van Rantwijk's Python code (same O(n³) algorithm)
- ~10–50x faster than NetworkX in practice due to Rust backend
- IBM/Qiskit project
- `pip install rustworkx`

### O(nm log n) — Theoretically optimal for sparse graphs

[Van Rantwijk v3](https://git.jorisvr.nl/joris/maximum-weight-matching/src/tag/v3)
([article](https://jorisvr.nl/article/maximum-matching))
- The only accessible Python implementation of the true O(nm log n) algorithm
- Self-contained Python package (no external dependencies), also ships C++
  header
- Not on PyPI — must install manually from his personal Gitea:
  ```bash
  git clone https://git.jorisvr.nl/joris/maximum-weight-matching
  cd maximum-weight-matching/python && pip install .
  ```

**[LEMON](https://lemon.cs.elte.hu/trac/lemon)** (C++ only, no usable Python
bindings)
([matching API](http://lemon.cs.elte.hu/pub/doc/latest-svn/a00852.html))
- Production-quality O(nm log n) `MaxWeightedMatching` for general graphs
- Reference C++ implementation, part of COIN-OR project
- [pylemon](https://pylemon.readthedocs.io/en/latest/)
  (v0.0.3, stale since 2022) and [cylemon](https://github.com/cstraehl/cylemon)
  ("very partial" Cython) exist but neither exposes general graph max weight
  matching usably

### Specialized / Not applicable

Both Blossom V and PyMatching solve **minimum-cost perfect matching** (every
node must be paired, no singles). This differs from our problem in two ways: we
want maximum weight (not minimum cost), and we allow singles (non-perfect).
Despite this, Blossom V *can* solve our problem via a standard reduction: add
dummy nodes with zero-weight edges to absorb unmatched nodes and negate weights
to convert max → min.

**[Blossom V](https://pub.ista.ac.at/~vnk/papers/blossom5.pdf)**
(Kolmogorov, C++)
- Solves min-weight perfect matching on **general graphs**
- Applicable via reduction (see above), but no official Python package
- License prohibits embedding in other libraries

**[PyMatching](https://pymatching.readthedocs.io/en/latest/)**
([GitHub](https://github.com/oscarhiggott/PyMatching), [PyPI](https://pypi.org/project/PyMatching/))
- Solves min-weight perfect matching on **restricted graph topologies** only
  (designed for quantum error correction surface codes)
- Cannot be repurposed for general graphs — not applicable

### Summary table

| Library                                                                            | Complexity      | General graph | Max weight              | Python  | pip install | Status   |
|------------------------------------------------------------------------------------|-----------------|---------------|-------------------------|---------|-------------|----------|
| [Van Rantwijk v3](https://git.jorisvr.nl/joris/maximum-weight-matching/src/tag/v3) | O(nm log n)     | yes           | yes                     | yes     | manual      | active   |
| [LEMON](https://lemon.cs.elte.hu/trac/lemon) + pylemon                             | O(nm log n)     | yes           | yes                     | partial | yes         | stale    |
| [rustworkx](https://www.rustworkx.org/)                                            | O(n³)           | yes           | yes                     | yes     | yes         | active   |
| [NetworkX](https://networkx.org/)                                                  | O(n³)           | yes           | yes                     | yes     | yes         | active   |
| [Blossom V](https://pub.ista.ac.at/~vnk/papers/blossom5.pdf)                       | O(n(m+n log n)) | yes           | min-weight perfect only | no      | no          | C++ only |
| [PyMatching](https://pymatching.readthedocs.io/en/latest/)                         | near-linear     | special       | min-weight perfect only | yes     | yes         | active   |



