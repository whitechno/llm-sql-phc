Optimizing LLM Queries: Comments and Suggestions
================================================
February 2, 2026

Main publication:  
[[LLM-SQL](https://arxiv.org/pdf/2403.05821)] "Optimizing LLM Queries in
Relational Data Analytics Workloads", 9 Apr 2025.

Followup publication with AI-driven algorithm improvement:  
[[AI-Sys](https://arxiv.org/pdf/2512.14806)] "Let the Barbarians In: How AI Can
Accelerate Systems Performance Research", Section 4.4, 22 Dec 2025.

[LLM-SQL] presents a "Greedy Group Recursion" (GGR) algorithm for optimizing LLM
queries by finding (a `n x m`) table re-arrangement that maximizes the LLM's KV
cache prefix hit count (PHC). Compared to the brute-force algorithm that
requires `n!*(m!)^n` potential orderings, GGR significantly reduces the search
space by selecting the highest-hit value and then reducing the dimensions of the
table at each recursive step with the maximum depth of recursion `O(min(n,m))`.
GGR achieves close-to-perfect PHC output with fast practical execution time.

Here we propose several adjustments to the GGR algorithm that improve the
output (moving it closer to the optimal solution) and also further improve the
execution time.

Algorithm improvements
----------------------

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

### Recursion early termination when only distinct values are present

If table scan tells that all values in the table are distinct (each appearing in
exactly one row), the algorithm terminates early and returns the `PHC=0` of the
table together with unmodified table:
```text
return 0, T
```
In other words, if the table cannot be optimized for hit count, the recursion
stops and the original table is returned. The situation of a table with all
distinct values can occur at the later stages of the recursion when only
singleton values from the long tail are left. In this situation the recursion
ends in one step.

Like the other three termination conditions (case of a single row, case of a
single column, and case of a full functional dependency of all columns), this
one also outputs the optimal solution (with a zero PHC).

We can say that this termination condition is a degenerate case of a full
functional dependency of all columns.

Also note that this termination condition does not improve the output but speeds
up the recursion, significantly in some cases.

[AI-Sys] paper also mentions this termination condition on line 11 of "(b)
Evolved prefix-aware policy" in Figure 4, page 9. However, it is an important
type of table condition that is worth mentioning separately.

### Multiple ties with max hit count: select the most informative column

When scanning the table for distinct values and selecting the highest-hit
value (lines 17–23), GGR algorithm selects the first value/column `b_v, b_c`
that gets the `max_HC`. But what if there are multiple values ("ties") with the
same `max_HC`?

[LLM-SQL] paper mentions this case on page 6: "when fields tie in HITCOUNT, GGR
may be suboptimal, as it lacks the exhaustive search used by OPHR to resolve
such ties".

Here we propose several ways to treat tied max hit counts with improvement in
output optimality and execution time.

First, we consider the case when some columns have multiple ties and propose two
adjustments to the algorithm:
1. Among the columns with multiple ties, we select the column with the highest
   number of distinct values with the max hit count. (We can call it the
   "most informative" column.) E.g., if column `A` has 3 distinct values with
   max hit count and column `B` has 2 distinct values with max hit count, we
   select column `A`.
2. Instead of splitting the table into two sub-tables and recursing on them, we
   split the table into multiple sub-tables, one for each distinct value plus
   the remaining rows.

The first adjustment improves the output optimality, and the second adjustment
improves the execution time.

**Example 1**
It is better illustrated by a simple example of a table with 4 rows and 2
columns `A` and `B`. The table has 3 distinct values with the same max hit
count: `a1` in column `A`, and `b1` and `b2` in column `B`. Also for simplicity,
we assume that `max_HC = 1`. (With `len(a1) = len(b1) = len(b2) = 1` and `|R_a1| =
|R_b1| = |R_b2| = 2`.)
```text
A    B
a1   b1
a1   b2
a2   b1
a3   b2
```

The original GGR algorithm selects `a1, A` to split the table into two
sub-tables and outputs the original table:
```text
A    B
a1   b1
a1   b2
a2   b1
a3   b2
```
with `PHC = 1` (and `PHR = 1/8`).

The adjusted algorithm selects `[b1, b2], B` to split the table into two
sub-tables and outputs the optimal solution:
```text
B    A 
b1   a1
b1   a2
b2   a1
b2   a3
```
with `PHC = 2` (and `PHR = 1/4`).

**Example 2**
We can extend previous example to a table with 8 rows, 2 columns, and 6 distinct
values with the same `max_HC = 1`: `a1, a2` in `A`, and `b1, b2, b3, b4` in `B`.
```text
A    B
a1   b1
a1   b2
a2   b3
a2   b4
a3   b1
a4   b2
a5   b3
a6   b4
```

The original GGR algorithm takes two iterations, selecting `a1, A` to split the
table in first iteration, and `a2, A` to split the table in second iteration. It
again outputs the original table:
```text
A    B
a1   b1
a1   b2
a2   b3
a2   b4
a3   b1
a4   b2
a5   b3
a6   b4
```
with `PHC = 2` (and `PHR = 2/16 = 1/8`).

The adjusted algorithm takes only one iteration selecting `[b1, b2, b3, b4], B`
to split the table into four sub-tables and outputs the optimal solution:
```text
B    A 
b1   a1
b1   a3
b2   a1
b2   a4
b3   a2
b3   a5
b4   a2
b4   a6
```
with `PHC = 4` (and `PHR = 4/16 = 1/4`).

As a generalization of the previous examples, we can consider a table with `4*N`
rows and two columns `A` and `B` with column `A` having `N` "doubles"
(`a1,a2,...,aN`) and column `B` having `2*N` "doubles" (`b1,b2,...,b2N`). Then
the original GGR algorithm takes `N` iterations and outputs the solution with
`PHC = N` (`PHR = N/8N = 1/8 = 12.5%`). The adjusted algorithm takes only one
iteration and outputs the optimal solution with `PHC = 2N`
(`PHR = 2N/8N = 1/4 = 25%`). This is a remarkable improvement in the output
optimality (`Diff = 12.5%`) with a significant reduction of iterations, even
though it is achieved for a specially crafted table.

**Example 3**
Consider a table with 10 rows, 2 columns `A` and `B`, and 3 tied distinct values
with the same `max_HC = 4`: `a1` in `A`, and `b1, b2` in `B`.
```text
A    B
a1   b1
a1   b1
a1   b1
a1   b2
a1   b2
a2   b1
a3   b1
a4   b2
a5   b2
a6   b2
```

The original GGR algorithm takes 6 iterations and outputs the solution
```text
A    B
a1   b1
a1   b1
a1   b1
a1   b2
a1   b2

B    A   
b2   a4   
b2   a5   
b2   a6 
b1   a2   
b1   a3  
```
with `PHC = 7+3 = 10` (`PHR = 10/20 = 50%`).

The adjusted algorithm takes 3 iterations and outputs the optimal solution
```text
B    A
b1   a1
b1   a1
b1   a1
b1   a2
b1   a3
b2   a1
b2   a1
b2   a4
b2   a5
b2   a6
```
with `PHC = 6+5 = 11` (`PHR = 11/20 = 55%`). Again this is a remarkable
improvement in both the output optimality (`Diff = 5%`) and execution time
(twice fewer iterations) for a specially crafted table.

### Multiple ties with max hit count: multiple most informative columns

What if there are two or more columns with the same top count of distinct values
with the max hit count?

In this case, we might be good with arbitrary choice among those columns.
However, there is a general preference for this kind of algorithms to be
deterministic as much as possible (reduce the randomness of the output).
Specifically, for GGR algorithm it means that the output (even if suboptimal)
should be the same regardless of the order of rows and columns in the input
table. This (increased) determinism might not necessarily improve the optimality
of the output, but it can make the algorithm more robust and more predictable.

Here we propose a tiebreaking strategy that not only increases the determinism
but also has the potential to improve the output optimality.

The tiebreaking strategy is based on choosing the column with the highest
average hit count. The average hit count of a column is computed as the sum of
hit counts of all distinct values divided by the total number of distinct
values. The rationale for this choice is that the column with the highest
average hit count is likely to be the most informative column and should be made
the first choice in the recursion to prevent the fragmentation of its distinct
values.

It is quite easy to craft a simple example of a table where this strategy leads
to a more optimal solution:
```text
A    B
a1   b1
a1   b1
a1   b2
a2   b1
a3   b2
```
Both columns `A` and `B` have one distinct value - `a1` in `A` and `b1` in `B` -
with the `max_HC = 2`. However, their average hit counts are different. Column
`A` has 3 distinct values `a1, a2, a3` and its `Avg_HC = (2 + 0 + 0) / 3 = 2/3`.
Column `B` has 2 distinct values `b1, b2` and its `Avg_HC = (2 + 1) / 2 = 3/2`.

Selecting `a1, A` in the first iteration produces output
```text
A    B
a1   b1
a1   b1
a1   b2
a2   b1
a3   b2
```
with `PHC = 3` (and `PHR = 3/10 = 30%`).

Selecting `b1, B` in the first iteration produces the optimal solution
```text
B    A
b1   a1
b1   a1
b1   a2
b2   a1
b2   a3
```
with `PHC = 4` (and `PHR = 4/10 = 40%`). It achieves higher PHC because it
preserves the "double" `b2, B` in the output.

### Column with K top hit counts

There could be a case when some column `A` has a distinct value `a1` with max
hit count higher than for any other column. This makes `a1, A` a proper choice
for the GGR iteration. However, it could be that column `A`'s second-highest hit
count value `a2` is also the second-highest hit count value in the entire table.
It could be going like this to up to `K` distinct values in column `A` that are
top highest hit count values in the entire table.

This is actually a widespread case in practice when the low-cardinality metadata
columns contain all top hit count distinct values.

We can exploit cases like this by splitting the table into `K+1` sub-tables in
one iteration rather than going through `K` separate iterations. In addition to
fewer iterations, this approach also speeds up the sub-tables size reduction,
especially during the first several iterations.

Note that this adjustment does not improve the output optimality but has the
potential to speed up the execution time.

### Ad-hoc heuristics for correlated distinct values

GGR algorithm takes full advantage of the table's Functional Dependency (FD)
rules to reduce the search space. It has a double benefit of improving the
output optimality and reducing the number of iterations. However, its usefulness
is limited to only a table-wide set of constraints. But what if two distinct
values in two columns happen to share the same rows?

In other words, we can have a case where two distinct values `a, A` and `b, B`
span the same rows in the table `R_a = R_b = R_ab`. In this case, we can apply
the same technique as for FD rules and combine two groups `a, A` and `b, B` into
a single two-column block `[(a,A),(b,B)]` spanning rows `R_ab` with a combined
hit count of `(len(a)^2 + len(b)^2)*(|R_ab| - 1)`. It can be extended to any
number of distinct values and columns as long as they all share the same rows.

We can find all tuples of distinct values that share the same rows in the table
by creating a hash table where the key is a hash of row indices and the value is
a list of distinct values that share the rows. Only distinct values with more
than one row should be added to the hash table. Hash table creation is done as
part of a Table Statistics calculation that runs every iteration step.

Similarly to FD rules, this technique improves the output optimality and reduces
the number of iterations.

Here is an example of a table where this technique can be applied:
```text
| A | B | C |
|---|---|---|
| a |   |   |
| a |   |   |
| a | b | c |
| a | b | c |
|   | b | c |
```
with `HC(a,A) = 3`, `HC(b,B) = HC(c,C) = 2`, `R_b = R_c = R_bc`, and
`HC(b,B) + HC(c,C) > HC(a,A)`.

GGR algorithm selects `a, A` to split the table and outputs
```text
| A |  | B | C |
|---|  |---|---|
| a |  |   |   |
| a |  |   |   |
| a |  | b | c |
| a |  | b | c |

| A | B | C |
|---|---|---|
|   | b | c |
```
with `PHC = 3 + 2 + 0 = 5` (`PHR = 5/15 = 33%`).

Adjusted GGR algorithm selects `[(b,B),(c,C)]` block to split the table and
outputs the optimal solution:
```text
| B | C |  | A |
|---|---|  |---|
| b | c |  | a |
| b | c |  | a |
| b | c |  |   |

| A | B | C |
|---|---|---|
| a |   |   |
| a |   |   |
```
with `PHC = 4 + 1 + 1 = 6` (`PHR = 6/15 = 40%`).

In case of a tie, i.e., when `HC(b,B) + HC(c,C) = HC(a,A)`, we select the
multi-column block.

How really beneficial is this data-heuristics-driven algorithm adjustment in
practice? Especially weighted by the complexity of implementation and additional
computational cost of the hash table creation? The answer depends on the
structure of the table. There are cases of the data sets with strong correlation
between some distinct values. Also, as recursion iterations start processing
distinct values with fewer rows, the probability of them sharing the same rows
increases. As a general recommendation, it is worth considering this heuristic
adjustment only if the table has a high correlation between distinct values.

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
