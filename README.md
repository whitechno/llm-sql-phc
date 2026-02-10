# Greedy Group Recursion (GGR) algorithm for optimizing LLM queries

### Functional Dependency (FD) definition

Two columns `A` and `B` are in FD rule `A <-> B` if, for any two rows `r1` and
`r2`, whenever `r1[A] = r2[A]` then `r1[B] = r2[B]`, and vice versa.

In other words, for any distinct value `a` in column `A`, all rows `R_a` with
`r[A] = a` must have the same value `b` in column `B` (and vice versa). This can
be expressed as `R_a = R_b`.

If columns `A` and `B` are functionally dependent, there is a one-to-one
correspondence between their distinct values.

FD rules can be specified as a list of disjoined sets of column names (or column
indices). For example, for the table with columns `A, B, C, D, E, F` where
`A <-> B` and
`C <-> D <-> E`, the FD rules can be specified as
```text
[
    [A, B],
    [C, D, E]
]
```

Example table with 4 fields: product_id, category, category_code, description
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
are functional dependencies that can be expressed as:
```text
[
    [0, 3],
    [1, 2],
]
```
