# Strongest result established

## Theorem

Let (T_k) be the tree with a center (c) and (k) arms (c-x_i-y_i), (1\le i\le k). Let (m(G)) denote the number of pointwise-minimal Roman dominating functions of (G). Then

\[
m(T_k)=3^k+2^k-1.
\]

Consequently, if (C(n)=\max\{m(T):T\text{ is a tree of order }n\}), then

\[
\limsup_{n\to\infty} C(n)^{1/n}=\sqrt3.
\]

Moreover, (m(T_k)>m(P_{2k+1})) for all sufficiently large (k); in particular, (m(T_5)=274>273=m(P_{11})).

The formula and proof below are self-contained. The asymptotic upper bounds used afterward are published results of Abu-Khzam, Fernau, and Mann in [Roman Census](https://doi.org/10.4230/LIPIcs.MFCS.2023.6).

## Proof

In the private-neighbor criterion below, the witness \(u\) is required to
lie outside \(S\), so that it has RDF value 0. Thus the exact condition is
\(u\in N(s)\setminus S\) and \(N(u)\cap S=\{s\}\).

For a graph (G), write (S=V_2(f)). Any minimal RDF has no vertex of value 1 adjacent to a vertex of value 2: changing that 1 to 0 would still satisfy Roman domination. Every vertex outside (S) adjacent to (S) must therefore have value 0, and every vertex outside the closed neighborhood (N[S]) must have value 1. Thus (S) uniquely determines the only possible minimal RDF labeling:

\[
f_S(v)=
\begin{cases}
2,&v\in S,\\
0,&v\in N(S),\\
1,&v\notin N[S].
\end{cases}
\]

This labeling is minimal exactly when every (s\in S) has an external private neighbor, namely a vertex (u\in N(s)\) with (N(u)\cap S=\{s\}\). If such a neighbor exists, lowering (f_S(s)=2) to 1 leaves that zero vertex undominated. If none exists, every zero neighbor of (s) has another neighbor in (S), so lowering (f_S(s)) to 1 preserves Roman domination. A possible pointwise decrease involving multiple coordinates also implies a valid single-coordinate decrease: choose a coordinate changed by the smaller RDF; any zero that remains zero in the smaller RDF must already have a supporting 2 there. Hence this external-private-neighbor condition is necessary and sufficient.

Now count the qualifying sets (S\subseteq V(T_k)).

1. **The center is not in (S).** On each arm the allowed choices are: no selected vertex, (x_i\in S), or (y_i\in S). The choice (x_i,y_i\in S) is impossible because (y_i) would have no zero neighbor. The choices on different arms do not interfere: a selected (x_i) has private zero neighbor (y_i), and a selected (y_i) has private zero neighbor (x_i). This gives (3^k) sets.
2. **The center is in (S).** No leaf (y_i) can be selected: if (x_i\in S), it has no zero neighbor; if (x_i\notin S), its only possible private zero neighbor (x_i) is adjacent to the selected center as well. Each (x_i) may independently be selected or omitted. The center needs at least one omitted (x_i) as a private zero neighbor, so the all-selected choice is excluded. This gives (2^k-1) sets.

Adding the cases proves (m(T_k)=3^k+2^k-1).

For the growth statement, Roman Census proves (m(F)\le(\sqrt3)^{|V(F)|}) for every forest (F), so (C(n)^{1/n}\le\sqrt3) for every (n). On the subsequence (n=2k+1),

\[
C(2k+1)^{1/(2k+1)}\ge (3^k+2^k-1)^{1/(2k+1)}\longrightarrow\sqrt3.
\]

These two inequalities give the asserted limsup. They do not prove that (C(n)^{1/n}\) converges along all orders.

Roman Census also proves (m(P_n)=O^*(1.6852^n)). Since (\sqrt3>1.6852), this path upper bound and the formula imply (m(T_k)>m(P_{2k+1})) for all sufficiently large (k). The exact order-11 comparison was checked by three independent counters; see [the full census data](results/path_extremal/tree_census_through_12.json).

## Proof status and limits

- **Proved here:** the exact (T_k) formula; the connected-tree limsup; and an eventual infinite sequence of strict path counterexamples, conditional only on the published path upper bound.
- **Exact finite verification:** (m(T_5)=274) and (m(P_{11})=273), and all tree counts/maximizers through order 12.
- **Not proved:** that (T_k) is extremal for every odd order; that paths maximize at every even order; or that (C(n)^{1/n}\) has a limit.
- The expression (3^k+2^k-1) also appears for a different split/cobipartite graph family in Roman Census. The current theorem is stated only for this particular tree family; novelty is assessed cautiously in [NOVELTY_MATRIX.md](NOVELTY_MATRIX.md).
