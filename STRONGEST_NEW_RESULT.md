# Strongest established result

## All-order theorem: connected trees have limsup growth \(\sqrt3\)

Let \(C(n)=\max\{m(T): T\text{ is a tree on }n\text{ vertices}\}\). Then
\[
\boxed{\displaystyle \limsup_{n\to\infty} C(n)^{1/n}=\sqrt3.}
\]
This is an established theorem of the current project. Its upper bound is the
published forest-wide theorem of Abu-Khzam, Fernau, and Mann; its connected
lower-bound witness is the subdivided-star family below. This deduction does
not establish novelty or the pointwise extremal formulas.

### Proof

For each \(k\ge1\), let \(T_k\) have a center \(v\) and \(k\) arms
\(v x_i y_i\), where each \(y_i\) is a leaf. The standard private-zero
characterization says a support \(S=V_2(f)\) determines a minimal RDF exactly
when every \(s\in S\) has a zero neighbor \(u\notin S\) with
\(N(u)\cap S=\{s\}\); vertices outside \(N[S]\) receive label 1 and all
other vertices outside \(S\) receive label 0.

Count such supports by whether \(v\in S\).

1. If \(v\notin S\), on each arm the permitted choices are
   \(\varnothing,\{x_i\},\{y_i\}\). Choosing both \(x_i,y_i\) is forbidden,
   because the selected leaf \(y_i\) has no zero neighbor. Each of the three
   remaining choices gives the selected vertex, if any, a private zero
   neighbor on that arm. Different arms do not interact. This gives \(3^k\)
   supports.
2. If \(v\in S\), no leaf \(y_i\) can be selected. If \(x_i\) is selected,
   the leaf has no zero neighbor; if \(x_i\) is omitted, then a selected
   \(y_i\) would have only the zero candidate \(x_i\), which is also adjacent
   to the selected center. Each \(x_i\) is therefore independently selected
   or omitted, but at least one must be omitted to give \(v\) a private zero
   neighbor. This gives \(2^k-1\) supports.

Hence \(m(T_k)=3^k+2^k-1\). Since \(|V(T_k)|=2k+1\),
\[
\lim_{k\to\infty}m(T_k)^{1/(2k+1)}=\sqrt3,
\qquad C(2k+1)\ge m(T_k),
\]
so \(\limsup C(n)^{1/n}\ge\sqrt3\). The published theorem
\(m(F)\le(\sqrt3)^{|V(F)|}\) for every forest \(F\) gives
\(C(n)^{1/n}\le\sqrt3\) for every \(n\), hence the reverse limsup bound.
Equality follows. This proves a limsup only; it does not show that
\(C(n)^{1/n}\) converges.

As a further corollary, \(T_k\) eventually has more minimal RDFs than the
odd path \(P_{2k+1}\). Roman Census gives the path bound
\(m(P_n)=O^*(1.6852^n)\), while
\(m(T_k)^{1/(2k+1)}\to\sqrt3>1.6852\). Choose any fixed base strictly
between these two numbers; the polynomial factor suppressed by \(O^*\) is
eventually dominated by the exponential gap. Thus
\(m(T_k)>m(P_{2k+1})\) for all sufficiently large \(k\). This refutes
path-extremality on all sufficiently large odd orders, but it does not
identify the maximizing tree at those orders.

The forest upper bound appears in Theorem 7.1 of Abu-Khzam, Fernau, and Mann,
[*Roman Census*](https://doi.org/10.4230/LIPIcs.MFCS.2023.6). The full
tree-specific formula proof is also preserved in
[STRONGEST_THEOREM.md](STRONGEST_THEOREM.md). The literature audit did not
locate a prior connected-tree statement of this limsup, but priority remains
unresolved.

## Finite extremal theorem

Let \(m(T)\) count the pointwise-minimal Roman dominating functions on a
tree \(T\), and \(C(n)=\max_{|V(T)|=n}m(T)\). A complete canonical
enumeration proves the following finite statement:

\[
\big(C(1),\ldots,C(20)\big)=
(1,3,4,7,12,20,34,57,96,162,274,460,792,1306,2314,3709,6816,10532,20194,29908).
\]

For every order \(1\le n\le20\), all extremal isomorphism classes are listed
with graph6 codes in
[COUNTEREXAMPLE_SEARCH.md](COUNTEREXAMPLE_SEARCH.md) and edge lists in
[extremal_summary_through_20.json](results/path_extremal/extremal_summary_through_20.json).
At each even order in this range, \(P_n\) is the unique extremizer. At odd
orders \(3\le n\le19\), \(T_k\) is extremal for \(n=2k+1\); the path ties
with \(T_3\) at order 7 and \(T_4\) at order 9. The single-vertex tree is
the unique order-1 tree. These statements are finite, exhaustive
results, not claims for larger orders.

## Proof of the finite statement

### Minimal RDFs as private-zero subsets

Let \(S=V_2(f)\) for a minimal RDF \(f\). A vertex labeled 1 cannot be
adjacent to a vertex of \(S\), since lowering 1 to 0 would leave it adjacent
to a 2 and preserve Roman domination. Every vertex in \(N(S)\setminus S\)
is therefore labeled 0, while every vertex outside \(N[S]\) must be 1. Thus \(S\)
uniquely determines the only possible minimal-RDF labeling:
\[
f_S(v)=
\begin{cases}
2,&v\in S,\\
0,&v\in N(S)\setminus S,\\
1,&v\notin N[S].
\end{cases}
\]

This labeling is minimal exactly when every \(s\in S\) has a private zero
\(u\notin S\) with \(u\in N(s)\) and \(N(u)\cap S=\{s\}\). Such a zero
prevents lowering \(f_S(s)\) from 2 to 1. Conversely, if \(s\) has no such
zero, every zero neighbor of \(s\) has another neighbor in \(S\), so
lowering \(f_S(s)\) to 1 preserves Roman domination. Testing one-coordinate
decreases suffices: if a pointwise smaller RDF existed, restoring all but
one changed coordinate to their original, larger values preserves every
zero-domination condition and yields a valid one-coordinate decrease.
Therefore \(m(T)\) equals the number of subsets \(S\) with this
external-private-zero property. The empty set qualifies and corresponds to
the all-ones RDF.

### Exact rooted recurrence

The canonical enumeration uses the recurrence proved in
[STRUCTURAL_PROOF_ATTEMPTS.md](STRUCTURAL_PROOF_ATTEMPTS.md). Root \(T\) at
\(r\). For each vertex \(v\), its table \(D_v^p(s,c,q)\) tracks whether its
parent and itself are selected, the number \(c\) of selected children
capped at 2, and whether \(v\) still needs a parent private-zero witness.
For a child state \((s_w,c_w,q_w)\), aggregate
\[
c=\min(2,\sum_w s_w),\quad
R=\bigvee_w q_w,\quad
H=\bigvee_w [s_w=0,\ c_w=0].
\]
Reject a combination with \(R=1\) unless \((s,p,c)=(0,0,1)\); otherwise
set \(q=[s=1\text{ and }H=0]\), multiplying and summing child
multiplicities. At the root,
\[
m(T)=\sum_{s\in\{0,1\}}\sum_{c=0}^2D_r^0(s,c,0).
\]

Induction on subtree height proves this recurrence: \(R\) records a selected
child whose only possible remaining witness is \(v\), and \(H\) records
exactly whether a zero child is adjacent to \(v\) and to no other selected
vertex. The full state definitions and proof are in the structural report.

### Exhaustive class coverage and independent checks

For each \(n\ge2\), the census used NetworkX's
[Wright–Richmond–Odlyzko–McKay generator for nonisomorphic trees](https://networkx.org/documentation/stable/reference/generators.html#networkx.generators.nonisomorphic_trees),
which enumerates one representative of every free-tree isomorphism class.
The singleton was handled explicitly. Generated class totals for every
order through 20 matched the known unlabeled-tree counts, including 823,065
classes at order 20. Each record stores the graph6 encoding, exact edge
list, and DP count.

The original census through order 12 uses three exact counters. For orders
13–20, a separately implemented fixed-array rooted DP recomputed every stored
tree count: 1,345,037 trees, zero mismatches, in 1,289.656 seconds. An
independent exhaustive subset/private-zero counter also rechecked every
reported extremizer and the path count (and \(T_k\) where applicable). The
array and bounded shape-memoized implementations agree with the audited
sparse-state DP on all 987 trees through order 12. The full cross-check data,
script, and log are linked in [COUNTEREXAMPLE_SEARCH.md](COUNTEREXAMPLE_SEARCH.md).

## Exact counterexamples to tempting proof lemmas

The universally monotone leaf-to-leaf path-smoothing claim fails first at
order 6. Moving the leaf edge \(1\!-\!2\) to \(4\!-\!2\) changes the tree
with edges \(\{01,03,05,12,34\}\) from 17 admissible subsets to the tree
with edges \(\{01,03,05,24,34\}\) with 15. The independent subset-size
histograms are \((1,6,8,2,0,0,0)\) and \((1,6,8,0,0,0,0)\), respectively.
This is the smallest such leaf-transfer counterexample: all moves through
order 5 were checked and none decreased the count.

Two spider transformations also fail: splitting a length-three arm of
\(P_5\) into arms of lengths 2 and 1 changes \(m\) from 12 to 9; balancing
legs \((1,1,2,4)\) to \((1,1,3,3)\) changes \(m\) from 57 to 56 at order 9.
Each exact graph encoding, edge set, and independent count histogram is
preserved in
[transformation_counterexamples_direct_check.json](results/path_extremal/transformation_counterexamples_direct_check.json).
These refute the specified lemmas; they do not rule out transformations
conditioned on the DP boundary states.

## Relation to prior work and limits

The forest bound \(m(F)\le(\sqrt3)^{|V(F)|}\) and its sharpness for
disconnected unions of \(P_2\) are prior results in
[*Roman Census*](https://doi.org/10.4230/LIPIcs.MFCS.2023.6). The same
expression \(3^t+2^t-1\) also appears there for a different split/cobipartite
family. The connected-tree limsup result from the earlier
[proved \(T_k\) formula](STRONGEST_THEOREM.md) is a short corollary of that
forest upper bound and the \(T_k\) lower-bound family. None of these prior
facts proves the pointwise formulas for \(C(n)\).

No counterexample to either proposed pointwise formula was found through
order 20. No all-order proof, structural reduction to paths/\(T_k\), or
tree-specific upper bound sharper than the forest bound was established.
The exact formulas remain conjectures.

## Reproduction

- Full canonical data through order 20:
  [tree_census_n20.jsonl.gz](results/path_extremal/tree_census_n20.jsonl.gz).
- Order 20 metadata and run log:
  [summary](results/path_extremal/tree_census_n20_summary.json),
  [log](results/path_extremal/tree_census_n20.log).
- Generator/streaming driver:
  [stream_tree_census.py](results/path_extremal/stream_tree_census.py).
- Bounded exact recurrence:
  [bounded_memo_tree_dp.py](results/path_extremal/bounded_memo_tree_dp.py).
- Full second-counter census check:
[verify_full_extended_census.py](results/path_extremal/verify_full_extended_census.py),
[summary](results/path_extremal/full_extended_census_independent_check.json),
and [log](results/path_extremal/full_extended_census_independent_check.log).
- Independent extremizer verification:
  [verify_extended_extremizers.py](results/path_extremal/verify_extended_extremizers.py)
  and [verification log](results/path_extremal/extended_extremizer_independent_check.log).
- Earlier three-counter census and its evidence:
  [full_tree_census.py](results/path_extremal/full_tree_census.py) and
  [the all-tree records through 12](results/path_extremal/tree_census_through_12.json).
