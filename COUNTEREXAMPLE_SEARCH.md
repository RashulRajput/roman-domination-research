# Exact counterexample search and tree census

## Exhaustive results

The canonical enumeration is complete through order 20. For every generated
tree the bounded-memo rooted DP counted \(m(T)\); the canonical class totals
matched the unlabeled-tree sequence. A separately implemented fixed-array
rooted DP then recomputed every stored count for all 1,345,037 trees of orders
13–20, with zero mismatches. The extremizers and path/subdivided-star counts
were additionally checked with the independent exhaustive subset/private-zero
counter.

| \(n\) | Unlabeled trees | \(C(n)\) | \(m(P_n)\) | All extremal classes (graph6) |
|---:|---:|---:|---:|---|
| 1 | 1 | 1 | 1 | \(P_1\): **@** |
| 2 | 1 | 3 | 3 | \(P_2\): **A_** |
| 3 | 1 | 4 | 4 | \(P_3=T_1\): **Bg** |
| 4 | 2 | 7 | 7 | \(P_4\): **Cq** |
| 5 | 3 | 12 | 12 | \(P_5=T_2\): **DqC** |
| 6 | 6 | 20 | 20 | \(P_6\): **EpOG** |
| 7 | 11 | 34 | 34 | \(P_7\): **FpOGG**; \(T_3\): **FqD?G** |
| 8 | 23 | 57 | 57 | \(P_8\): **GpD?GC** |
| 9 | 47 | 96 | 96 | \(P_9\): **HpD?GC@**; \(T_4\): **HqD?I?@** |
| 10 | 106 | 162 | 162 | \(P_{10}\): **IpCI?C@?G** |
| 11 | 235 | 274 | 273 | \(T_5\): **JqD?I?@O??_** |
| 12 | 551 | 460 | 460 | \(P_{12}\): **KpCGI?@?G?_@** |
| 13 | 1,301 | 792 | 775 | \(T_6\): **LqD?I?@O??g??@** |
| 14 | 3,159 | 1,306 | 1,306 | \(P_{14}\): **MpCGGD??G?_@?@??_** |
| 15 | 7,741 | 2,314 | 2,201 | \(T_7\): **NqD?I?@O??g??@O???G** |
| 16 | 19,320 | 3,709 | 3,709 | \(P_{16}\): **OpCGGC@O??_@?@??_?G?@** |
| 17 | 48,629 | 6,816 | 6,250 | \(T_8\): **PqD?I?@O??g??@O???I????C** |
| 18 | 123,867 | 10,532 | 10,532 | \(P_{18}\): **QpCGGC@?I??@?@??_?G?@??C??G** |
| 19 | 317,955 | 20,194 | 17,748 | \(T_9\): **RqD?I?@O??g??@O???I????D?????G** |
| 20 | 823,065 | 29,908 | 29,908 | \(P_{20}\): **SpCGGC@?G?g??@??_?G?@??C??G??G??C** |

The table records **every** extremal isomorphism class in the complete
range. At orders 7 and 9, the path ties with \(T_3\) and \(T_4\); at every
other order through 20 the listed extremizer is unique. Thus the proposed
even/odd formulas survive this range, but the census is not an all-order
proof.

The machine-readable
[extremizer summary through 20](results/path_extremal/extremal_summary_through_20.json)
contains graph6 and edge-list encodings. The complete tree records are in
[the original census through 12](results/path_extremal/tree_census_through_12.json),
[orders 13–16](results/path_extremal/tree_census_extension_through_16.json),
[orders 17–18](results/path_extremal/tree_census_extension_through_18.json),
and the compressed
[order-19 JSONL census](results/path_extremal/tree_census_n19.jsonl.gz) and
[order-20 JSONL census](results/path_extremal/tree_census_n20.jsonl.gz).

## Counterexample search status

- **Even-order path conjecture:** no counterexample through order 20.
- **Odd-order \(T_k\) conjecture:** no counterexample through order 19.
- **Ties:** the additional extremizers at orders 7 and 9 are the only ties
  through order 20.
- **Path-extremality outside the even-order claim:** already false at order
  11, since \(m(T_5)=274>273=m(P_{11})\).

The path and \(T_k\) counts at every order 13–20, and every extremal tree
count, agree with the independent subset counter; see
[extended_extremizer_independent_check.json](results/path_extremal/extended_extremizer_independent_check.json).
Every individual census count at orders 13–20 also agrees between the bounded
memo DP and fixed-array DP; see the
[cross-check summary](results/path_extremal/full_extended_census_independent_check.json),
[run log](results/path_extremal/full_extended_census_independent_check.log),
and [reproduction script](results/path_extremal/verify_full_extended_census.py).
The original orders 1–12 have three exact counters, as documented in
[EXTREMAL_TREES.md](EXTREMAL_TREES.md).

## Order-20 attempt

An initial unbounded shape-cache run processed a canonical prefix of 519,739
of the 823,065 order-20 tree classes before it was stopped at approximately
1.1 GB of memory. Its prefix maximum was 29,908, equal to \(m(P_{20})\);
the candidate was checked by both the rooted DP and the independent subset
counter. This prefix was **not exhaustive** and is not used to state \(C(20)\).
The interrupted gzip stream and status record are retained as
[original partial stream](results/path_extremal/tree_census_n20_partial_oldmemo.jsonl.gz),
[recovered complete rows](results/path_extremal/tree_census_n20_partial_oldmemo_recovered.jsonl.gz),
and [partial-run summary](results/path_extremal/tree_census_n20_partial_oldmemo.jsonl.summary.json).

A second run used shape memoization only for rooted subtrees of order at most
10. It completed all 823,065 classes; the class-count check passed. It found
\(C(20)=m(P_{20})=29{,}908\) with a unique extremal class. The graph6 tree
and \(P_{20}\) were independently recounted by the subset counter. The run
took 490.88 seconds and cached 1,205 rooted shapes. The script and completed
artifacts are
[stream_tree_census.py](results/path_extremal/stream_tree_census.py),
[bounded_memo_tree_dp.py](results/path_extremal/bounded_memo_tree_dp.py),
the [order-20 data](results/path_extremal/tree_census_n20.jsonl.gz),
[summary](results/path_extremal/tree_census_n20_summary.json), and
[run log](results/path_extremal/tree_census_n20.log).

## Runtime and reproduction

The canonical DP run times were 1.14, 3.27, 8.35, and 20.24 seconds for
orders 13–16; 57.56 seconds for order 17; 144.14 seconds for order 18; and
226.76 seconds for order 19, and 490.88 seconds for order 20. The
corresponding logs are
[through 16](results/path_extremal/tree_census_extension_through_16.log),
[through 18](results/path_extremal/tree_census_extension_through_18.log),
[order 19](results/path_extremal/tree_census_n19.log), and
[order 20](results/path_extremal/tree_census_n20.log).

Run from the project root:

- Orders 1–12 with all three counters:
  lean-ctx -c "python results/path_extremal/full_tree_census.py"
- Orders 13–16:
  lean-ctx -c "python results/path_extremal/extend_tree_census.py --max-order 16"
- Orders 17–18:
  lean-ctx -c "python results/path_extremal/extend_tree_census.py --start-order 17 --max-order 18"
- One streamed order, including 19 or 20:
  lean-ctx -c "python results/path_extremal/stream_tree_census.py 20"

The stream command uses the bounded-memo exact recurrence. The all-order
conjectures remain unproved regardless of the finite census.
