# Graph algorithm for max disjoint pairs

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

