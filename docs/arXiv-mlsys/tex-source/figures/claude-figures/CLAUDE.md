# Figure Descriptions

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