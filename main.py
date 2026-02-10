"""
Demo of the Greedy Group Recursion (GGR) algorithm.
"""

import numpy as np

from ggr import compute_phc, ggr


def main():
    # Example table with 3 fields: product_id, category, description
    # Rows represent different records that would be sent to an LLM
    table = np.array(
        [
            ["P001", "Electronics", "Smartphone with 128GB storage"],
            ["P002", "Electronics", "Laptop with 16GB RAM"],
            ["P003", "Clothing", "Cotton T-shirt, size M"],
            ["P004", "Electronics", "Wireless headphones"],
            ["P005", "Clothing", "Denim jeans, size 32"],
            ["P006", "Clothing", "Winter jacket, size L"],
        ],
        dtype=object,
    )

    print("Original Table:")
    print("-" * 60)
    for i, row in enumerate(table):
        print(f"Row {i}: {list(row)}")

    # Define functional dependencies
    # In this example: product_id -> category (column 0 determines column 1)
    # This means if we know the product_id, we know the category
    functional_deps: dict[int, list[int]] = {
        # No functional dependencies in this simple example
    }

    print("\n" + "=" * 60)
    print("Running GGR Algorithm...")
    print("=" * 60)

    # Run GGR algorithm
    phc_score, reordered = ggr(table, functional_deps)

    print(f"\nComputed PHC Score: {phc_score:.2f}")
    print("\nReordered Table:")
    print("-" * 60)
    for i, row in enumerate(reordered):
        print(f"Row {i}: {row}")

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
