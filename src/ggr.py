"""
Greedy Group Recursion (GGR) Algorithm

Implementation based on Algorithm 1 from:
"Optimizing LLM Queries in Relational Data Analytics Workloads"
(after several typos fixed)

The algorithm reorders rows and fields of an input table to maximize
prefix hit count (PHC) for KV cache reuse in LLM inference.
"""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def get_inferred_cols(col_idx: int, fd_groups: list[list[int]]) -> list[int]:
    """
    Find all columns that are functionally dependent on the given column.

    FD groups are disjoint sets of mutually dependent column indices.
    If col_idx is in a group, all other columns in that group are inferred.

    Args:
        col_idx: The column index to find dependencies for
        fd_groups: List of disjoint sets of mutually dependent column indices

    Returns:
        List of column indices that are inferred from col_idx (excluding col_idx itself)
    """
    for group in fd_groups:
        if col_idx in group:
            return [c for c in group if c != col_idx]
    return []


def hitcount(
    value: str,
    col_idx: int,
    table: NDArray,
    functional_deps: list[list[int]],
) -> tuple[float, list[int]]:
    """
    Calculate the hit count for a specific value in a column.

    Args:
        value: The value to calculate hit count for
        col_idx: The column index where the value is located
        table: The input table as a 2D numpy array of strings
        functional_deps: List of disjoint sets of mutually dependent column indices

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
    inferred_cols = get_inferred_cols(col_idx, functional_deps)

    # Line 6: tot_len = len(v)² + Σ_{c'∈inferred_cols} (Σ_{r∈Rv} len(T[r,c'])) / |Rv|
    tot_len = len(value) ** 2

    for inferred_col in inferred_cols:
        # Calculate average length of values in inferred column for matching rows
        lengths_sum = sum(len(table[r, inferred_col]) for r in matching_rows)
        avg_len = lengths_sum / num_matching
        tot_len += avg_len ** 2

    # Line 7: return tot_len × (|Rv| − 1), [c] + inferred_cols
    hit_count = tot_len * (num_matching - 1)
    cols = [col_idx] + inferred_cols

    return hit_count, cols


def ggr(
    table: NDArray,
    functional_deps: list[list[int]],
    col_indices: list[int] | None = None,
    row_indices: list[int] | None = None,
) -> tuple[float, list[list[str]], list[list[int]], list[int], int]:
    """
    Greedy Group Recursion algorithm for maximizing prefix hit count.

    Args:
        table: Input table as a 2D numpy array of strings
        functional_deps: List of disjoint sets of mutually dependent column indices
        col_indices: Current column indices being considered (used in recursion)
        row_indices: Original row indices being considered (used in recursion)

    Returns:
        Tuple of (prefix_hit_count, reordered_values, reordered_col_indices,
                  original_row_indices, recursion_count)
        where reordered_col_indices[i] is the column order for row i,
        original_row_indices[i] is the original row number for row i,
        and recursion_count is the total number of ggr() calls
    """
    n_rows, n_cols = table.shape

    # Initialize column indices if not provided
    if col_indices is None:
        col_indices = list(range(n_cols))

    # Initialize row indices if not provided
    if row_indices is None:
        row_indices = list(range(n_rows))

    # Line 10-12: Base case - single row
    if n_rows == 1:
        return 0.0, [list(table[0, col_indices])], [col_indices], [row_indices[0]], 1

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
        col_orders = [[col] for _ in sorted_indices]
        orig_rows = [row_indices[i] for i in sorted_indices]

        return total_score, sorted_rows, col_orders, orig_rows, 1

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
        return (
            0.0,
            [list(table[i, col_indices]) for i in range(n_rows)],
            [col_indices for _ in range(n_rows)],
            row_indices,
            1,
        )

    # Line 24: R_v ← {i | T[i, b_c] = b_v}
    matching_mask = table[:, best_col] == best_value
    matching_row_indices = np.where(matching_mask)[0]
    non_matching_row_indices = np.where(~matching_mask)[0]

    # Line 25: A_HC, L_A ← GGR(T[rows \ R_v, cols], FD)
    # Recurse on rows NOT containing the best value
    if len(non_matching_row_indices) > 0:
        subtable_a = table[non_matching_row_indices]
        rows_a = [row_indices[i] for i in non_matching_row_indices]
        a_hc, l_a, cols_a, orig_a, count_a = ggr(
            subtable_a, functional_deps, col_indices, rows_a
        )
    else:
        a_hc = 0.0
        l_a = []
        cols_a = []
        orig_a = []
        count_a = 0

    # Line 26: B_HC, L_B ← GGR(T[R_v, cols \ b_cols], FD)
    # Recurse on matching rows, excluding the best columns
    remaining_cols = [c for c in col_indices if c not in best_cols]

    if len(matching_row_indices) > 0 and len(remaining_cols) > 0:
        subtable_b = table[matching_row_indices]
        rows_b = [row_indices[i] for i in matching_row_indices]
        b_hc, l_b, cols_b, orig_b, count_b = ggr(
            subtable_b, functional_deps, remaining_cols, rows_b
        )
    else:
        b_hc = 0.0
        l_b = [[] for _ in matching_row_indices]
        cols_b = [[] for _ in matching_row_indices]
        orig_b = [row_indices[i] for i in matching_row_indices]
        count_b = 0

    # Line 27: C_HC, _ ← HITCOUNT(b_v, b_c, T, FD)
    c_hc, _ = hitcount(best_value, best_col, table, functional_deps)

    # Line 28: S ← A_HC + B_HC + C_HC
    total_score = a_hc + b_hc + c_hc

    # Line 29: L ← [[b_v] + L_A[i] | i ∈ 1...|R_v|] + L_B
    # Build the prefix values for matching rows
    prefix_values = [table[matching_row_indices[0], c] for c in best_cols]

    # Combine prefix with remaining values for matching rows
    reordered_matching = []
    cols_matching = []
    for i, row_result in enumerate(l_b):
        reordered_row = prefix_values + row_result
        reordered_matching.append(reordered_row)
        cols_matching.append(best_cols + cols_b[i])

    # Combine: matching rows (with prefix) + non-matching rows
    result_list = reordered_matching + l_a
    result_cols = cols_matching + cols_a
    result_orig = orig_b + orig_a
    total_count = 1 + count_a + count_b

    return total_score, result_list, result_cols, result_orig, total_count


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
