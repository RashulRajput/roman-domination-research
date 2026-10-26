# Extremal minimal-RDF counts for trees: exact census through order 12

This file records the original completed census through order 12. The
canonical enumeration has since been extended through order 20; see
[COUNTEREXAMPLE_SEARCH.md](COUNTEREXAMPLE_SEARCH.md) and
[STRONGEST_NEW_RESULT.md](STRONGEST_NEW_RESULT.md) for the updated finite
results and all added encodings.

Let (m(G)) be the number of pointwise-minimal Roman dominating functions on (G), and let

\[
C(n)=\max\{m(T):T\text{ is an unlabeled tree on }n\text{ vertices}\}.
\]

## Verified census

All **987** unlabeled tree classes on 1 through 12 vertices were enumerated. Every count was checked three ways: (A) subsets of (V_2) tested by the private-zero characterization; (B) exhaustive enumeration of all (3^n) labelings and coordinate-decrease minimality checks; and (C) the rooted-tree dynamic program proved below. Every path count was also checked by all three. The exhaustive generator and machine-readable class data are linked under Reproducibility.

| (n) | Tree classes | (C(n)) | (m(P_n)) | Extremal classes | Every extremal class (graph6 encoding) | (T_{(n-1)/2}) extremal? |
|---:|---:|---:|---:|---|---|:---:|
| 1 | 1 | 1 | 1 | 1 | (P_1): `@` | n/a |
| 2 | 1 | 3 | 3 | 1 | (P_2): `A_` | n/a |
| 3 | 1 | 4 | 4 | 1 | (P_3=T_1): `Bg` | yes |
| 4 | 2 | 7 | 7 | 1 | (P_4): `Cq` | n/a |
| 5 | 3 | 12 | 12 | 1 | (P_5=T_2): `DqC` | yes |
| 6 | 6 | 20 | 20 | 1 | (P_6): `EpOG` | n/a |
| 7 | 11 | 34 | 34 | 2 | (P_7): `FpOGG`; (T_3): `FqD?G` | yes (ties (P_7)) |
| 8 | 23 | 57 | 57 | 1 | (P_8): `GpD?GC` | n/a |
| 9 | 47 | 96 | 96 | 2 | (P_9): `HpD?GC@`; (T_4): `HqD?I?@` | yes (ties (P_9)) |
| 10 | 106 | 162 | 162 | 1 | (P_{10}): `IpCI?C@?G` | n/a |
| 11 | 235 | 274 | 273 | 1 | (T_5): `JqD?I?@O??_` | yes (unique maximum) |
| 12 | 551 | 460 | 460 | 1 | (P_{12}): `KpCGI?@?G?_@` | n/a |

The graph6 strings encode one representative of each extremal isomorphism class. The JSON also records the representative edge list and Prüfer sequence for every tree class, not just maximizers.

### What the completed census establishes

- (C(n)=m(P_n)) for (n\le10) and (n=12); at each of those orders the path is the unique extremizer.
- At orders 7 and 9 there is one additional extremizer, respectively (T_3) and (T_4), tied with the path.
- At order 11, (T_5) is the unique extremizer and (m(T_5)=274>273=m(P_{11})).
- Among tested odd orders (3,5,7,9,11), (T_k) is extremal at every order. This is only a finite observation through order 11; no extremality conclusion is made beyond the census.
- The census does not establish that paths maximize at all even orders, or that the T_k family maximizes at all odd orders.

## Provisional conjectures (unproved)

The finite data suggests two simple statements worth testing, but neither is asserted as a theorem:

1. For every even n >= 2, P_n is the unique tree maximizing m(T).
2. For every k >= 1, T_k maximizes m(T) among trees of order 2k+1.

Their only current support is the completed census: the first was checked through n=12, and the second through k=5. No census claim or extremality claim is made beyond those orders.

## A structural rooted-tree recurrence

**Private-neighbor convention.** Every displayed condition of the form
\(N(u)\cap S=\{s\}\) in this report also requires \(u\notin S\).
The private witness must be a zero vertex; the neighborhood equality alone
would wrongly admit a selected vertex \(u\).

The recurrence below is exact for every tree and is the basis of counter C. It gives a rigorous boundary-state alternative to an unsupported scalar recurrence involving only (m(T)).

For any (S\subseteq V(G)), define it to be admissible when every (s\in S) has a neighbor (u\) with (N(u)\cap S=\{s\}\). The minimal-RDF characterization gives a bijection between admissible (S) and minimal RDFs, with (S=V_2). Root a tree at (r). For a vertex (v), let (T_v) be its rooted subtree and define (D_v^p(s,c,q)) as follows:

- (p\in\{0,1\}) records whether the parent of (v) is selected in (S) (for the root, (p=0));
- (s\in\{0,1\}) records whether (v\in S);
- (c=\min(2,\#\text{ selected children of }v));
- (q=1) exactly when (s=1) and no zero child of (v) is a private witness for (v). Thus (v) still needs its parent to witness it. The witness requirements of all other selected vertices in (T_v) have already been resolved.

For a fixed (p,s), combine one state ((s_w,c_w,q_w)) from each child (w)'s table (D_w^s). Set

\[
c=\min\left(2,\sum_w s_w\right).
\]

Discard this child-state combination if any (q_w=1), unless

\[
s=0,\qquad p=0,\qquad c=1.
\]

Indeed, an unresolved selected child can use (v) as its private zero only if (v\) is unselected, has exactly one selected neighbor in total, and that neighbor is this unique selected child. For a surviving combination, set

\[
q=1\quad\Longleftrightarrow\quad s=1\text{ and there is no child }w\text{ with }s_w=0,\ c_w=0.
\]

Such a zero child has exactly one selected neighbor, namely (v), and hence witnesses (v). Add the product of the child-state counts to (D_v^p(s,c,q)). At the root there is no parent to resolve a remaining witness request, so

\[
m(T)=\sum_{s,c}D_r^0(s,c,0).
\]

Induction from the leaves proves the recurrence: the only boundary effect of a subtree on its parent is whether its root is selected and, if selected, whether it still needs the parent as a private zero witness; the capped child count records whether the root can itself be a private zero for the parent. The recurrence agrees with both independent counters on all 987 census trees.

## Failed scalar induction attempt

A tempting path-based leaf induction would assert

\[
m(T)\le m(T-v)+m(P_n)-m(P_{n-1})
\]

for some leaf (v) of every (n)-vertex tree (T). It already fails on (T_3): (m(T_3)=34), every leaf deletion leaves a 6-vertex tree with count 17, while (m(P_7)-m(P_6)=34-20=14). The proposed right side is 31, below 34.

The corresponding scalar induction for (C(n)),

\[
C(n)\le C(n-1)+m(P_n)-m(P_{n-1}),
\]

also fails at (n=11): (274>162+(273-162)=273). Thus path increments do not control one-vertex growth of the tree maximum. The rooted-state recurrence remains exact, but this census and recurrence do **not** yield a general closed form for (C(n)) or a characterization of its maximizers.

## Reproducibility and exact encodings

- Re-run the exhaustive census: `lean-ctx -c "python results/path_extremal/full_tree_census.py"`.
- Re-run the separate rooted-DP audit: `lean-ctx -c "python results/path_extremal/tree_dp_recurrence.py"`.
- [Census generator and three exact counters](results/path_extremal/full_tree_census.py)
- [Rooted-tree recurrence implementation and verification](results/path_extremal/tree_dp_recurrence.py)
- [Original family/path verifier](results/path_extremal/verify_subdivided_star.py)
- [Machine-readable records for all 987 trees, including graph6, edges, Prüfer sequences, and all three counts](results/path_extremal/tree_census_through_12.json)
- [Census run log](results/path_extremal/tree_census_through_12.log)
- [Rooted-DP cross-check log](results/path_extremal/tree_dp_verification.log)
- [Subdivided-star formula and path-counterexample checks](results/path_extremal/subdivided_star_results.json)

Every numerical census claim in this report is finite and exhaustively verified through order 12. No claim about (C(n)) beyond that range is inferred from the table.
