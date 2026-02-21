Optimizing LLM Queries 1: Reference and Typos
=============================================
February 2, 2026

Main publication:  
[[LLM-SQL](https://arxiv.org/abs/2403.05821)] "Optimizing LLM Queries in
Relational Data Analytics Workloads", 9 Apr 2025.

Followup publication with AI-Driven Research for Systems (ADRS) algorithm
improvement:  
[[AI-Sys](https://arxiv.org/abs/2512.14806)] "Let the Barbarians In: How AI Can
Accelerate Systems Performance Research", Section 4.4, 22 Dec 2025.

GGR algorithm description
-------------------------

[LLM-SQL] presents a "Greedy Group Recursion" (GGR) algorithm for optimizing LLM
queries by finding (a `n x m`) table re-arrangement that maximizes the LLM's KV
cache prefix hit count (PHC). Compared to the brute-force algorithm that
requires `n!*(m!)^n` potential orderings, GGR significantly reduces the search
space by selecting the highest-hit value and then reducing the dimensions of the
table at each recursive step with the maximum depth of recursion `O(min(n,m))`.
GGR achieves close-to-perfect PHC output with fast practical execution time.

See code specification of Greedy Group Recursion (GGR) algorithm on page 5 of
the [LLM-SQL] paper.

At each recursive step, the GGR algorithm scans the table (lines 17–23) to find
all distinct values with corresponding hit counts (lines 3–8). It then selects
the highest-hit value `b_v` (with corresponding column `b_c`) and splits the
table into two sub-tables - one with all the rows `R_v` containing `b_v` value
in `b_c` column excluding the field where the value is located in, and another
sub-table with the remaining rows. It then recurses on the two sub-tables (lines
24–26) and calculates the total PHC as the sum of PHC of the sub-tables and
contributions of `b_v` (line 28).

The figure below shows the GGR algorithm recursion tree for a table with 3 top
hit count distinct values `v, b, a`:
![GGR algorithm](/docs/arXiv-mlsys/tex-source/figures/claude-figures/max_hit_recursion.svg)

The figure below shows the GGR algorithm recursion tree for a table similar to
the one above, but with additional column `c'` that is in FD rule with column
`c`:
![GGR algorithm with FD](/docs/arXiv-mlsys/tex-source/figures/claude-figures/max_hit_recursion_vprime.svg)

There are three cases when GGR algorithm can be _proven_ to achieve the optimal
PHC output:
1. Table contains only a single row. Then PHC is zero and the table is not
   rearranged. (Lines 10–12.)
2. Table contains only a single column. Then the table with sorted column values
   is returned and PHC is trivially computed. (Lines 13–16.)
3. Table contains one field `A` that functionally determines all other fields of
   a table. Then GGR algorithm prioritizes groups of values in `A` due to the
   accumulated hit count score (lines 3–8), capturing key correlations early and
   producing the optimal reordering. You can think of this as an extension of
   #2 - a table with a single column.

All three cases also serve as recursion termination conditions.

GGR Optimality
--------------

There are cases when GGR clearly produces suboptimal solutions.

One case is when distinct values tie in max hit count. In other words, it is the
case when several distinct values have the same hit count, and it is a maximum
hit count in the table. These ``tied'' distinct values can be in the same column
or across different columns. GGR algorithm doesn't provide any mechanism to
select a particular distinct value and just picks the first one it encounters
during a table scan. See an example of this case with GGR producing suboptimal
reordering in the figure below.
![GGR algorithm](/docs/arXiv-mlsys/tex-source/figures/claude-figures/subopt-example-1-ties.svg)
Example of a table with max hit count ties and suboptimal GGR output:
$HitCount(a) = HitCount(b1) = HitCount(b2)$

Another case is when a distinct value in one column correlates with a distinct
value in another column. This is not the case of FD-bound columns (even though
it might sound similar), but, rather, the case of data heuristics when two
distinct values in two columns happen to share the same rows. See an example of
this case with GGR producing suboptimal reordering in the figure below.
![GGR algorithm](/docs/arXiv-mlsys/tex-source/figures/claude-figures/subopt-example-2-corrs.svg)
Example of a table with correlated distinct values $b$ and $c$, and suboptimal
GGR output: $HitCount(a) = HitCount(b) + HitCount(c)$ and $R_b = R_c$


Minor typos in equations
------------------------

### Typo 1

On page 3, the equation (2) should have `1 <= c <= m` rather than `0 <= c < m`,
as it appears that everywhere else in the paper both rows and columns are
counted from `1` (to `n` and `m` respectively).

### Typo 2

On page 5, in the "Algorithm 1 Greedy Group Recursion" code specification, line
6: the contribution of each inferred column `c'` should have its value length to
be squared too `len(v')^2`, where `v'` is the inferred column `c'` value derived
from value `v` of parent column `c` based on the table's Functional Dependency
(FD) rules. Line 6 should read:
```text
tot_len = len(v)^2 + SUM_c'[len(v')^2]
```
There is also no need to average `len(T[r,c'])` over rows in `R_v` because all
values `v' = T[r,c']` are the same for all `r` in `R_v`.

### Typo 3

On page 5, in the "Algorithm 1 Greedy Group Recursion" code specification, line
29: when prepending max group value `b_v` to `L_B[i]`, it should also include
all values `b_vals` inferred from `b_c` by applying Functional Dependency (FD)
rules. Line 29 should be changed to:
```text
L <- [[b_v] + b_vals + L_B[i] | for i in R_v] + L_A
```
(Also note that line 29 mixed up `L_B` and `L_A` variables.)

`b_vals` should be computed in `HitCount` function with modified line 7:
```text
return tot_len * (|R_v| - 1), [c] + inferred_cols, inferred_vals
```

Then line 27 should be changed to
```text
C_HC, _, b_vals <- HitCount(b_v, b_c, T, FD)
```

Figures
-------
