"""
Greedy Group Recursion (GGR) Algorithm

Implementation based on Algorithm 1 from:
"Optimizing LLM Queries in Relational Data Analytics Workloads"

The algorithm reorders rows and fields of an input table to maximize
prefix hit count (PHC) for KV cache reuse in LLM inference.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def hitcount(
    value: str,
    col_idx: int,
    table: NDArray,
    functional_deps: dict[int, list[int]],
) -> tuple[float, list[int]]:
    """
    Calculate the hit count for a specific value in a column.

    Args:
        value: The value to calculate hit count for
        col_idx: The column index where the value is located
        table: The input table as a 2D numpy array of strings
        functional_deps: Dictionary mapping column index to list of
                        functionally dependent column indices

    Returns:
        Tuple of (hit_count, list of column indices including inferred columns)
    """
    # Line 4: Rv ← {i | T[i, c] = v}
    # Find all row indices where the column value equals the given value
    row_mask = table[:, col_idx] == value
    matching_rows = np.where(row_mask)[0]
    num_matching = len(matching_rows)

    if num_matching <= 1:
        # No hits possible with 0 or 1 matching rows
        return 0.0, [col_idx]

    # Line 5: inferred_cols ← {c' | (c, c') ∈ FD}
    inferred_cols = functional_deps.get(col_idx, [])

    # Line 6: tot_len = len(v)² + Σ_{c'∈inferred_cols} (Σ_{r∈Rv} len(T[r,c'])) / |Rv|
    tot_len = len(value) ** 2

    for inferred_col in inferred_cols:
        # Calculate average length of values in inferred column for matching rows
        lengths_sum = sum(len(table[r, inferred_col]) for r in matching_rows)
        avg_len = lengths_sum / num_matching
        tot_len += avg_len

    # Line 7: return tot_len × (|Rv| − 1), [c] + inferred_cols
    hit_count = tot_len * (num_matching - 1)
    cols = [col_idx] + inferred_cols

    return hit_count, cols


def ggr(
    table: NDArray,
    functional_deps: dict[int, list[int]],
    col_indices: list[int] | None = None,
) -> tuple[float, list[list[str]]]:
    """
    Greedy Group Recursion algorithm for maximizing prefix hit count.

    Args:
        table: Input table as a 2D numpy array of strings
        functional_deps: Dictionary mapping column index to list of
                        functionally dependent column indices
        col_indices: Current column indices being considered (used in recursion)

    Returns:
        Tuple of (prefix_hit_count, reordered_list_of_tuples)
    """
    n_rows, n_cols = table.shape

    # Initialize column indices if not provided
    if col_indices is None:
        col_indices = list(range(n_cols))

    # Line 10-12: Base case - single row
    if n_rows == 1:
        return 0.0, [list(table[0, col_indices])]

    # Line 13-16: Base case - single column
    if len(col_indices) == 1:
        col = col_indices[0]
        distinct_values = np.unique(table[:, col])

        total_score = 0.0
        for v in distinct_values:
            hc, _ = hitcount(v, col, table, functional_deps)
            total_score += hc

        # Sort rows by the single column value
        sorted_indices = np.argsort(table[:, col])
        sorted_rows = [[table[i, col]] for i in sorted_indices]

        return total_score, sorted_rows

    # Line 17: Initialize best values
    max_hc = -1.0
    best_value = None
    best_col = None
    best_cols: list[int] = []

    # Line 18-23: Find the value with maximum hit count
    for col in col_indices:
        distinct_values = np.unique(table[:, col])
        for v in distinct_values:
            hc, cols = hitcount(v, col, table, functional_deps)
            if hc > max_hc:
                max_hc = hc
                best_value = v
                best_col = col
                best_cols = cols

    # If no good grouping found, return rows as-is
    if best_value is None or best_col is None:
        return 0.0, [list(table[i, col_indices]) for i in range(n_rows)]

    # Line 24: R_v ← {i | T[i, b_c] = b_v}
    matching_mask = table[:, best_col] == best_value
    matching_row_indices = np.where(matching_mask)[0]
    non_matching_row_indices = np.where(~matching_mask)[0]

    # Line 25: A_HC, L_A ← GGR(T[rows \ R_v, cols], FD)
    # Recurse on rows NOT containing the best value
    if len(non_matching_row_indices) > 0:
        subtable_a = table[non_matching_row_indices]
        a_hc, l_a = ggr(subtable_a, functional_deps, col_indices)
    else:
        a_hc = 0.0
        l_a = []

    # Line 26: B_HC, L_B ← GGR(T[R_v, cols \ b_cols], FD)
    # Recurse on matching rows, excluding the best columns
    remaining_cols = [c for c in col_indices if c not in best_cols]

    if len(matching_row_indices) > 0 and len(remaining_cols) > 0:
        subtable_b = table[matching_row_indices]
        b_hc, l_b = ggr(subtable_b, functional_deps, remaining_cols)
    else:
        b_hc = 0.0
        l_b = [[] for _ in matching_row_indices]

    # Line 27: C_HC, _ ← HITCOUNT(b_v, b_c, T, FD)
    c_hc, _ = hitcount(best_value, best_col, table, functional_deps)

    # Line 28: S ← A_HC + B_HC + C_HC
    total_score = a_hc + b_hc + c_hc

    # Line 29: L ← [[b_v] + L_A[i] | i ∈ 1...|R_v|] + L_B
    # Build the prefix values for matching rows
    prefix_values = [table[matching_row_indices[0], c] for c in best_cols]

    # Combine prefix with remaining values for matching rows
    reordered_matching = []
    for i, row_result in enumerate(l_b):
        reordered_row = prefix_values + row_result
        reordered_matching.append(reordered_row)

    # Combine: matching rows (with prefix) + non-matching rows
    result_list = reordered_matching + l_a

    return total_score, result_list


def compute_phc(reordered_list: list[list[str]]) -> float:
    """
    Compute the actual Prefix Hit Count for a reordered list of tuples.

    PHC is the sum of squared lengths of consecutive matching field values
    starting from the first field.

    Args:
        reordered_list: List of tuples (rows) after reordering

    Returns:
        The prefix hit count
    """
    if len(reordered_list) <= 1:
        return 0.0

    total_phc = 0.0

    for r in range(1, len(reordered_list)):
        current_row = reordered_list[r]
        prev_row = reordered_list[r - 1]

        # Count consecutive matching fields from the start
        hit_length = 0.0
        for f in range(min(len(current_row), len(prev_row))):
            if current_row[f] == prev_row[f]:
                hit_length += len(current_row[f]) ** 2
            else:
                break

        total_phc += hit_length

    return total_phc
