# Greedy Group Recursion (GGR) algorithm for optimizing LLM queries

### Functional Dependency (FD) definition

Two columns `A` and `B` are in FD rule `A <-> B` if, for any two rows `r1` and
`r2`, whenever `r1[A] = r2[A]` then `r1[B] = r2[B]`, and vice versa.

In other words, for any distinct value `a` in column `A`, all rows `R_a` with
`r[A] = a` must have the same value `b` in column `B` (and vice versa). This can
be expressed as `R_a = R_b`.

If columns `A` and `B` are functionally dependent, there is a one-to-one
correspondence between their distinct values.

FD rules can be specified as a list of disjoint sets containing either column
names or column indices. For example, for the table with columns
`A, B, C, D, E, F` where `A <-> B` and `C <-> D <-> E`, the FD rules can be
specified as `[[A, B], [C, D, E]]` or as `[[0, 1], [2, 3, 4]]`.

**Example 1** Table with 4 fields: product_id, category, category_code,
description
```text
[
    ["P001", "Electronics", "EL", "Smartphone with 128GB storage"],
    ["P002", "Electronics", "EL", "Laptop with 16GB RAM"],
    ["P003", "Clothing", "CL", "Cotton T-shirt, size M"],
    ["P004", "Electronics", "EL", "Wireless headphones"],
    ["P005", "Clothing", "CL", "Denim jeans, size 32"],
    ["P006", "Clothing", "CL", "Winter jacket, size L"],
]
```
In this example, `product_id <-> description` and `category <-> category_code`
are functional dependencies that are expressed as `[[0, 3], [1, 2]]`.

**Example 2** Table with FD rule `Category <-> Code` expressed as `[[0, 3]]`:
```text
---------------------------------------------
Row   Category     Brand      Product    Code
---------------------------------------------
0     Electronics  Apple      iPhone     E    
1     Clothing     Nike       Shoes      C    
2     Electronics  Samsung    TV         E    
3     Clothing     Adidas     Jacket     C    
4     Electronics  Apple      MacBook    E    
5     Clothing     Nike       T-Shirt    C
```
