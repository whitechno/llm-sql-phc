"""
Demo of the Greedy Group Recursion (GGR) algorithm.
"""

import numpy as np

from ggr import compute_phc, ggr


def main():
    # Example table with 4 fields: category, brand, product, category_code
    # From README.md example demonstrating functional dependencies
    # category (col 0) <-> category_code (col 3) are mutually dependent
    # brand (col 1) <-> product (col 2) are mutually dependent
    table = np.array(
        [
            ["Electronics", "Apple", "iPhone", "E"],
            ["Clothing", "Nike", "Shoes", "C"],
            ["Electronics", "Samsung", "TV", "E"],
            ["Clothing", "Adidas", "Shoes", "C"],  # try changing "Shoes" to "Jacket"
            ["Electronics", "Apple", "MacBook", "E"],
            ["Clothing", "Nike", "T-Shirt", "C"],
        ],
        dtype=object,
    )

    print("Original Table:")
    print("-" * 70)
    print(f"{'Row':<5} {'0 Category':<14} {'1 Brand':<10} {'2 Product':<12} {'3 Code':<7}")
    print("-" * 70)
    for i, row in enumerate(table):
        print(f"{i:<5} {row[0]:<14} {row[1]:<10} {row[2]:<12} {row[3]:<7}")

    # Define functional dependencies as disjoint sets of mutually dependent columns
    # FD group [0, 3]: category <-> category_code (bidirectional)
    functional_deps: list[list[int]] = [[0, 3]]

    print("\n" + "=" * 70)
    print("Running GGR Algorithm...")
    print("=" * 70)

    # Run GGR algorithm
    phc_score, reordered, col_orders, orig_rows, recursion_count = ggr(
        table, functional_deps
    )

    print(f"\nComputed PHC Score: {phc_score:.2f}")
    print(f"Recursion iterations: {recursion_count}")
    print("\nReordered Table (rows and fields reordered for max prefix sharing):")
    print("-" * 70)
    for i, (row, cols, orig) in enumerate(zip(reordered, col_orders, orig_rows)):
        print(f"{i}: ({orig}, {cols}) {row}")

    # Verify with actual PHC computation
    actual_phc = compute_phc(reordered)
    print(f"\nVerified PHC: {actual_phc:.2f}")

    # Compare with original order
    original_list = [list(row) for row in table]
    original_phc = compute_phc(original_list)
    print(f"Original Order PHC: {original_phc:.2f}")

    if actual_phc > original_phc:
        improvement = ((actual_phc - original_phc) / max(original_phc, 1)) * 100
        print(f"\nImprovement: {improvement:.1f}% better PHC with reordering")


if __name__ == "__main__":
    main()
