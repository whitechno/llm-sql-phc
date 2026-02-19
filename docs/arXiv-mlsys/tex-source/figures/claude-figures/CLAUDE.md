# Figure Descriptions

Note: use this command to convert SVG to PDF:
```text
rsvg-convert -f pdf -o max_hit_recursion.pdf max_hit_recursion.svg
```

## max_hit_recursion.svg

The figure illustrates a key step of the Greedy Group Recursion algorithm
(prefix hit maximization). All gaps between adjacent areas are 10px, except the
gap between Top and Bottom groups in the Right section, which is 40px.

```
  1. Legend (two entries, left to right):
     - Gray block arrow with "GGR Recursion Step" label
     - Solid-border yellow square with "Max Hit Count Distinct Value Group" label

  2. Left table — single black-bordered grid (6 rows, 3 columns):
     - Rows 0-2: "b" in column 2, "v" in column 3
     - Row 3: "v" in column 3 only
     - Rows 4-5: "a" in column 1

  3. Arrow 1 — gray block arrow pointing right

  4. Middle section — split into two groups (10px gap between them):
     - Top group:
       - Yellow solid-border column (v,v,v,v) — 4 rows
       - Blue solid-border area (2 columns × 4 rows, internal dashed grid) —
         "b,b,b" in column 2 (right), row 3 empty
     - Bottom group:
       - Green solid-border area (3 columns × 2 rows, internal dashed grid) —
         "a,a" in column 1 (left)

  5. Arrows 2 — two gray block arrows pointing right (one per group)

  6. Right section — shows the max group value promotion:
     - Top group (3 areas, 10px gaps):
       1) Yellow solid-border column (b,b,b) — 3 rows (max group value)
       2) Blue solid-border area (1 column × 3 rows, internal dashed h-lines) — to the right
       3) Green solid-border area (2 columns × 1 row, internal dashed v-line) — below both
     - Bottom group (40px gap from top group):
       - Yellow solid-border column (a,a) — 2 rows
       - Blue solid-border area (2 columns × 2 rows, internal dashed grid) — to the right
```

## max_hit_recursion_vprime.svg

The figure extends max_hit_recursion.svg by adding a second distinct value
column `v'` (grouped with `v` in the yellow area). All gaps between adjacent
areas are 10px, except the gap between Top and Bottom groups in the Right
section, which is 40px.

```
  1. Legend (two entries, left to right):
     - Gray block arrow with "GGR Recursion Step" label
     - Solid-border yellow square with "Max Hit Count Distinct Value Group" label

  2. Left table — single black-bordered grid (6 rows, 4 columns):
     - Rows 0-2: "b" in column 2, "v" in column 3, "v'" in column 4
     - Row 3: "v" in column 3, "v'" in column 4 only
     - Rows 4-5: "a" in column 1

  3. Arrow 1 — gray block arrow pointing right

  4. Middle section — split into two groups (10px gap between them):
     - Top group:
       - Yellow solid-border area (2 columns × 4 rows, internal dashed v-line) —
         "v,v,v,v" in column 1 (left), "v',v',v',v'" in column 2 (right)
       - Blue solid-border area (2 columns × 4 rows, internal dashed grid) —
         "b,b,b" in column 2 (right), row 3 empty
     - Bottom group:
       - Green solid-border area (4 columns × 2 rows, internal dashed grid) —
         "a,a" in column 1 (left)

  5. Arrows 2 — two gray block arrows pointing right (one per group)

  6. Right section — shows the max group value promotion:
     - Top group (3 areas, 10px gaps):
       1) Yellow solid-border column (b,b,b) — 3 rows (max group value)
       2) Blue solid-border area (1 column × 3 rows, internal dashed h-lines) — to the right
       3) Green solid-border area (2 columns × 1 row, internal dashed v-line) — below both
     - Bottom group (40px gap from top group):
       - Yellow solid-border column (a,a) — 2 rows
       - Blue solid-border area (3 columns × 2 rows, internal dashed grid) — to the right
```

## subopt-example-1-ties.svg

```
  1. Legend: "GGR suboptimal example 1" label
  
  2. Left table — single black-bordered grid (4 rows, 2 columns):
     - Row 0: "b1" in column 2
     - Row 1: "a" in column 1, "b1" in column 2
     - Row 2: "a" in column 1, "b2" in column 2
     - Row 3: "b2" in column 2

  3. Arrow 1 — gray block arrow pointing right

  4. Middle section — split into two groups (10px gap between them):
     - Top group:
       - Yellow solid-border column (a,a) — 2 rows
       - Blue solid-border area (1 column × 2 rows, internal dashed grid) —
         "b1,b2" in column 1
     - Bottom group:
       - Green solid-border area (2 columns × 2 rows, internal dashed grid) —
         "b1,b2" in column 2
```

```bash
rsvg-convert -f pdf -o subopt-example-1-ties.pdf subopt-example-1-ties.svg
```

## subopt-example-2-corrs.svg

```
  1. Legend: "GGR suboptimal example 2" label
  
  2. Left table — single black-bordered grid (4 rows, 3 columns):
     - Row 0: "a" in column 1
     - Row 1: "a" in column 1
     - Row 2: "a" in column 1, "b" in column 2, "c" in column 3
     - Row 3: "b" in column 2, "c" in column 3

  3. Arrow 1 — gray block arrow pointing right

  4. Middle section — split into two groups (10px gap between them):
     - Top group:
       - Yellow solid-border column (a,a,a) — 3 rows
       - Blue solid-border area (2 columns × 3 rows, internal dashed grid) —
         "b,c" in row 2 (third row)
     - Bottom group:
       - Green solid-border area (3 columns × 1 row, internal dashed grid) —
         "b" in column 2, "c" in column 3
```

```bash
rsvg-convert -f pdf -o subopt-example-2-corrs.pdf subopt-example-2-corrs.svg
```

## 2-01-aggr-k-top.svg

The figure illustrates a recursion step of the Adjusted Greedy Group Recursion
algorithm for the case when column `V` has 3 top hit count distinct values.

```
  1. Legend (two entries, left to right):
     - Gray block arrow with "AGGR Recursion Step" label
     - Solid-border yellow square with "Top Hit Count Value Groups" label

  2. Left table — single black-bordered grid (7 rows, 2 columns):
     - Rows 0-1: "v1" in column 2
     - Rows 2-3: "v2" in column 2
     - Rows 4-5: "v3" in column 2
     - Row 6: empty

  3. Arrow 1 — gray block arrow pointing right

  4. Middle section — split into 4 vertically positioned groups (10px gap between them):
     - Top group:
       - Yellow solid-border column (v1,v1) — 2 rows
       - Blue solid-border area (1 columns × 2 rows, internal dashed grid) — empty
     - Second group:
       - Yellow solid-border column (v2,v2) — 2 rows
       - Blue solid-border area (1 columns × 2 rows, internal dashed grid) — empty
     - Third group:
       - Yellow solid-border column (v3,v3) — 2 rows
       - Blue solid-border area (1 columns × 2 rows, internal dashed grid) — empty
     - Bottom group:
       - Green solid-border area (2 columns × 1 row, internal dashed grid) — empty
```

```bash
rsvg-convert -f pdf -o 2-01-aggr-k-top.pdf 2-01-aggr-k-top.svg
```
