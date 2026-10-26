# Path extremality disproved; exact counterexample and family

## Exact theorem proved

Let (T_k) be the tree formed from one center (c) by attaching (k) paths of length two, with vertices (c-x_i-y_i) for (1\le i\le k). Then

\[
m(T_k)=3^k+2^k-1.
\]

Here (m(G)) is the number of minimal Roman dominating functions on (G). The theorem is proved below. Each (T_k) is a tree, hence chordal, and has (2k+1) vertices.

The exponential growth rate of this family is exactly

\[
\lim_{k\to\infty}m(T_k)^{1/(2k+1)}=\sqrt3.
\]

The formula is strictly below ((\sqrt3)^{2k+1}) for every (k\ge1). Its growth rate also exceeds the known path growth rate, leading to counterexamples to path extremality.

Combining this family with the published forest upper bound shows that the maximum count among connected trees has exponential limsup exactly (\sqrt3). The upper bound is the forest theorem; the lower bound follows along odd orders (2k+1) from (T_k). This connected-tree refinement is a potential contribution; its novelty still needs a broader literature check.

### Proof

For any graph (G), a minimal Roman dominating function is determined by its set (S) of vertices labeled 2. Given (S), every vertex outside (S) adjacent to (S) must be labeled 0, and every other vertex must be labeled 1. Such a labeling is minimal exactly when every (s\in S) has a private zero neighbor: a vertex (u\notin S) adjacent to (s) and to no other vertex of (S). Indeed, such a neighbor is exactly what prevents lowering (s) from 2 to 1 while preserving domination.

Count the qualifying sets (S\subseteq V(T_k)) in two cases.

1. **The center is not in (S).** On each arm, the allowed choices are: select neither (x_i,y_i); select (x_i); or select (y_i). Selecting both is impossible because (y_i)'s only neighbor (x_i) would itself be labeled 2, leaving (y_i) without a private zero neighbor. Each of the three allowed choices has a private zero witness: (y_i) witnesses (x_i), and (x_i) witnesses (y_i). Choices on distinct arms do not interfere. This case contributes (3^k).
2. **The center is in (S).** No (y_i) can be selected: its only possible private zero neighbor (x_i) is adjacent to both (y_i) and the selected center. Each (x_i) may be selected or not. If selected, (y_i) is its private zero neighbor. If not selected, (x_i) is a private zero neighbor of (c). Thus the center has a private zero neighbor exactly when at least one (x_i) is not selected. Of the (2^k) choices for the (x_i), exclude the all-selected choice. This case contributes (2^k-1).

The cases are disjoint and exhaustive, giving (m(T_k)=3^k+2^k-1). For the limit, write

\[
m(T_k)=3^k\left(1+(2/3)^k-3^{-k}\right).
\]

Taking the ((2k+1))-st root gives the limit \(\sqrt3\), since the parenthetical factor has root tending to 1. Also, for (k\ge1), (1+(2/3)^k-3^{-k}\le4/3<\sqrt3), proving the strict finite bound.

## Explicit counterexample to path extremality

Let (T_5) have center 0 and five arms (0-x_i-y_i). It is a connected chordal graph (indeed, a tree) on 11 vertices. The exact formula gives

\[
m(T_5)=3^5+2^5-1=274.
\]

Direct label enumeration and the private-witness subset counter independently give (m(P_{11})=273). Thus

\[
m(T_5)=274>273=m(P_{11}),
\]

which disproves the conjecture that every connected chordal graph (G) of order (n) satisfies (m(G)\le m(P_n)). A canonical edge list is

\[
\{(0,1),(1,2),(0,3),(3,4),(0,5),(5,6),(0,7),(7,8),(0,9),(9,10)\}.
\]

Among all unlabeled trees through order 12, the exact census finds no tree counterexample below order 11; (T_5) is the only violating tree class at order 11. This does not establish that it is the smallest counterexample among all chordal graphs.

The 2023 paper *Roman Census* gives (m(P_n)=O^*(1.6852^n)), while the proved formula gives (m(T_k)^{1/(2k+1)}\to\sqrt3>1.6852). Consequently, (T_k) beats (P_{2k+1}) for all sufficiently large (k), so this is an infinite family of counterexamples. The paper already contains the expression (3^t+2^t-1) for a different split/cobipartite family and proves the (\sqrt3^n) upper bound for forests; neither the expression nor the general forest growth bound is claimed as new here. It studies path counts and chordal enumeration, and leaves the tight chordal counting bound open; its stated results do not present this connected path-extremality conjecture. This is a targeted literature check, not an exhaustive novelty review. See [the MFCS 2023 paper](https://doi.org/10.4230/LIPIcs.MFCS.2023.6), Theorem 3.4, Proposition 4.1, Theorem 7.1, and Section 8.

## Rejected induction lemmas

The first attempted lemma was: for every connected chordal (G) of order (n\ge2), **every** simplicial vertex (v) satisfies (m(G)-m(G-v)\le m(P_n)-m(P_{n-1})). It fails first at order 5. The graph with edges \(\{04,12,13,23,34\}\) is chordal; vertex 0 is simplicial and its deletion increment is 6, while the path increment is (12-7=5).

The existential repair, replacing “every” by “some simplicial vertex,” survives through order 6 but fails at order 7 on (T_3). Every simplicial vertex of (T_3) is a leaf; deleting any leaf lowers the count from 34 to 17, whereas (m(P_7)-m(P_6)=34-20=14).

A two-vertex repair also fails on (T_3): deleting any two of its three nonadjacent leaves leaves a connected graph with count 9. The decrement is (34-9=25), larger than (m(P_7)-m(P_5)=34-12=22). This rejects that specific replacement lemma.

## Exact simplicial-deletion identity obtained during the proof attempt

Although the proposed increment inequalities fail, the correct deletion accounting gives an exact identity. Let (v) be simplicial in (G), let (H=G-v), and let (Q=N_G(v)). For (S\subseteq V(H)), say (S) is **valid in (H)** when every (s\in S) has a private zero witness in (H), using the labeling determined by (S).

Define (D_v) as the number of sets (S) valid in (H) such that:

- (S\cap Q=\varnothing);
- every (s\in S) has a private zero witness in (H\setminus Q); and
- some (u\in Q) has no neighbor in (S) inside (H).

Define (R_v) as the number of sets (S\subseteq V(H)) such that:

- (S\cap Q=\{s\}) for one vertex (s);
- every (t\in S\setminus\{s\}) has a private zero witness in (H); and
- (s) has no private zero witness in (H).

Then

\[
m(G)=m(H)+D_v+R_v.
\]

To prove it, classify minimal RDFs by the label at (v). If (v=1), then (S\cap Q=\varnothing), and the restriction is a valid set in (H). If (v=0), then (S\cap Q\ne\varnothing). Every valid set in (H) with a selected neighbor of (v) gives one such extension; the only extra extensions are the (R_v) sets, where the zero at (v) supplies the missing private witness for the unique selected neighbor in (Q). If (v=2), its private zero witness must be some (u\in Q). Since (Q) is a clique, no vertex of (S\cap Q) can coexist with that witness, so (S\cap Q=\varnothing). The new selected vertex (v) destroys precisely the old private witnesses lying in (Q), which explains the requirement that every witness for (S) lie in (H\setminus Q). The zero witness for (v) is exactly a neighbor (u\in Q) with no neighbor in (S) in (H). These extensions are counted by (D_v). Every valid set in (H) contributes exactly one baseline extension, at (v=1) or (v=0), according as (S\cap Q) is empty or nonempty. Adding the two exceptional classes proves the identity.

The code checks this identity for every simplicial vertex of every connected chordal graph in the atlas through order 7, with zero mismatches. This is a verified identity with a proof above; no claim of novelty is made here.

## Reproducible evidence and limits

- `path_extremal_search.py` counts minimal RDFs in two ways: direct label enumeration and the private-zero-witness subset characterization. It also independently checks chordality, compares against the inherited counters through order 5, tests the path conjecture, and checks the deletion identity and attempted induction lemmas.
- `verify_subdivided_star.py` checks the formula by the subset counter for (k=1,\ldots,8), cross-checks both (T_k) and (P_{2k+1}) with direct label enumeration through (k=5), and exhausts all unlabeled trees through order 12.
- `path_extremal_results.json` contains the complete atlas census, per-graph witnesses and violations, and environment versions.
- `subdivided_star_results.json` contains the formula check table.

Re-run from the project directory:

```powershell
python results/path_extremal/path_extremal_search.py
python results/path_extremal/verify_subdivided_star.py
```

The atlas is exhaustive only through seven vertices. The tree census through 12 is exhaustive for trees, not for all chordal graphs. The exact formula and the order-11 counterexample are proved and independently counted; the exact formula's novelty remains unverified. The cited path-growth estimate is used only to infer that infinitely many members of this tree family beat paths.
