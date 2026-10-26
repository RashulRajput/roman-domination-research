# Research audit and handoff

## Update: connected path extremality is disproved

The later focused search disproves the proposed bound (m(G)\le m(P_n)) for connected chordal graphs: the 11-vertex tree (T_5), with five arms of length two, has (m(T_5)=274), while (m(P_{11})=273). The exact family formula and two independent count implementations are recorded in `results/path_extremal/RESULT.md` and its verifier. This does not settle the separate pointwise chordal bound (M(n)\le3^{n/2}) discussed below.

As of 2026-10-26. This note resets the project around the actual open target and records which earlier claims are published, which are computational claims awaiting reproduction, and what an independent mathematical check should cover.

## Target

For a finite simple graph $G$, let $m(G)$ be the number of pointwise-minimal Roman dominating functions $f:V(G)\to\{0,1,2\}$. Define

\[
M(n)=\max\{m(G):G\text{ chordal},\ |V(G)|=n\}.
\]

The working conjecture is $M(n)\le 3^{n/2}$ for every $n\ge1$. The matching lower-bound family gives $M(2t)\ge3^t$, so the conjecture would determine the exact exponential growth rate for chordal graphs.

## A useful exact encoding

For $S\subseteq V(G)$, define $f_S(v)=2$ when $v\in S$, $f_S(v)=0$ when $v\notin S$ and $N(v)\cap S\ne\varnothing$, and $f_S(v)=1$ otherwise. The function is a minimal RDF exactly when

\[
\forall s\in S\ \exists u\in N(s)\setminus S\quad N(u)\cap S=\{s\}.
\]

The condition says each vertex assigned 2 has a private zero-neighbor. The assignment outside $S$ is forced by minimality and Roman domination, so this is a bijective encoding, including $S=\varnothing$ (the all-ones function). This formulation reduces counting to counting subsets $S$ with the displayed witness property.

Disjoint union gives a second useful fact. Minimal RDFs on $G\dot\cup H$ are exactly independent choices of one minimal RDF on each component, hence

\[
m(G\dot\cup H)=m(G)m(H),\qquad M(n+k)\ge M(n)M(k).
\]

By Fekete's lemma, $\lambda=\lim_{n\to\infty}M(n)^{1/n}=\sup_n M(n)^{1/n}$ exists. A matching of $t$ disjoint edges has $3^t$ minimal RDFs, so $\lambda\ge\sqrt3$. The conjectured pointwise inequality is equivalent to $\lambda=\sqrt3$: any finite counterexample can be repeated as a disjoint union to force a strictly larger asymptotic rate. The published chordal enumeration algorithm gives the current upper bound $\lambda\le1.8940$.

## Literature status

Abu-Khzam, Fernau, and Mann's [MFCS 2023 paper](https://doi.org/10.4230/LIPIcs.MFCS.2023.6) proves an $O^*(1.8940^n)$ enumeration bound for chordal graphs and explicitly leaves its optimality open. It also records the matching lower bound $\Omega((\sqrt3)^n)$ for chordal graphs. The [JCSS version](https://doi.org/10.1016/j.jcss.2026.103834) retains the chordal tightness question.

The path result in the project is not a new discovery. Section 4 of the MFCS paper derives an order-5 recurrence for the number $b_n$ of path RDFs whose first vertex is not assigned 2, and relates the total $a_n=m(P_n)$ by $a_n=b_n+b_{n-2}$. The recurrence is

\[
b_n=b_{n-1}+b_{n-3}+b_{n-4}+b_{n-5}
\]

after the initial cases; it yields the already-published path growth bound $1.6852^n$. The sequence in the local scripts is consistent with this result. Do not present the path recurrence or its growth constant as the paper's novelty.

The 2024 [Algorithmica paper](https://doi.org/10.1007/s00453-024-01211-w) identifies the sets $S=V_2(f)$ as strongly irredundant sets: every selected vertex has a private neighbor outside the set. This gives a useful terminology and literature route. Bounds for maximal irredundant sets do not automatically apply, because the objects here are all strongly irredundant sets, not only inclusion-maximal ones. The published $1.5048^n$ bound for minimal dominating sets in chordal graphs ([TCS 2019](https://doi.org/10.1016/j.tcs.2019.03.017)) controls at most the no-value-1 subfamily of minimal RDFs; it says nothing by itself about functions that use value 1. More precisely, no-value-1 minimal RDFs require a dominating set whose selected vertices also have external private neighbors.

One sentence in the path discussion of the Roman Census paper says every minimal dominating set maps directly to a minimal RDF with values only 0 and 2. The formal privacy criterion above appears to exclude examples such as the two leaves of $P_3$, which form a minimal dominating set but give the nonminimal RDF $(2,0,2)$. Check the paper's context and any correction before relying on that sentence or its comparison of growth rates.

The 2025 preprint [Enumeration With Nice Roman Domination Properties](https://arxiv.org/abs/2511.20367) concerns perfect and connected variants; it is related background, but not the same minimal-RDF extremal question. Include it in a final novelty review to prevent terminology from conflating these variants.

## Audit of inherited computational claims

No project scripts were run during this audit. The following are source-level findings, not reproduced computational results.

- `search_counterexample.py` calls `nx.to_graph6_bytes` and labels the result a canonical form. Graph6 serialization preserves the current vertex labels; it is not an isomorphism-canonical labeling. Thus the reported 1,402,792 objects cannot be described as non-isomorphic on the basis of this code. The recursive generator does build graphs by adding each new vertex with a clique as its earlier neighborhood. If that recursion completed, it would include a PEO-ordered representative of every chordal isomorphism class, so a maximum-count search could still be exhaustive despite duplicate isomorphism classes. The run log and a reproducible extremal-data file are absent from the dossier.
- The same script's `generate_chordal_graphs_by_peo` function is a stub (`pass`); the actual exhaustive search is the separate nested recursion in `exhaustive_chordal_8`.
- `transfer_matrix.py` contains exploratory comments and states sampled from brute-force outputs, but does not construct a justified transition system or prove the recurrence. Treat it as a scratch file, not a proof.
- `recurrence_analysis.py` checks finitely many computed values and numerically estimates roots. Finite checking is not a proof, and the underlying path recurrence is already in the cited paper.
- The claims for the graph atlas, random families, and the $n=8$ search need saved inputs, exact outputs, and a reproducible run before they can be used as evidence in a manuscript.

The connected path-extremality target above has now been resolved negatively by (T_5); do not keep presenting it as open. The separate global chordal growth bound remains a different problem. For any renewed work on that bound, use exact witnesses, canonical graph encodings, and independent count output; the old reported (n=8) search still requires the audit described below.

Additional literature check for the verifier: the Roman Census paper's path discussion says every minimal dominating set directly gives a minimal RDF with labels only 0 and 2. Test this against \(P_3\) with the two endpoints as the dominating set and against the paper's privacy characterization. Determine whether there is a missing hypothesis, a different convention, or an error before relying on that comparison.

## Independent GPT-6 verification brief

Use the block below when asking an independent GPT-6 session to verify the mathematics. It is intentionally a verification request, not a request to accept the dossier's conclusions.

> Independently audit the mathematical claims in `RESEARCH_AUDIT.md` and the project files in `C:\Users\DELL\roman_domination_research`. Do not trust previous summaries or computed outputs. (1) Prove or correct the subset encoding of minimal Roman dominating functions via private zero-neighbors, including the empty set. (2) Prove the disjoint-union product rule, existence of the extremal exponential growth limit, and equivalence between (M(n)\le3^{n/2}) for every (n) and exact rate \(\sqrt3\). (3) Check the published path recurrence against the MFCS 2023 source and derive carefully what recurrence it implies for the total path count, including all base indices. (4) Audit `search_counterexample.py`: establish precisely what its recursive generator covers, whether it visits every chordal isomorphism class, what graph6 deduplication does, and whether the reported (n=8) claim is reproducible from the source. (5) Inspect the two counting implementations for logical errors without treating agreement on a small sample as proof. For every issue, give a concrete counterexample or a complete argument; label claims that remain unverified. Do not claim that the chordal extremal conjecture is proved unless a complete proof is supplied.
