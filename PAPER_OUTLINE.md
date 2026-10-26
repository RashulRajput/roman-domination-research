# Working paper outline

## Working title

**The extremal growth rate of minimal Roman dominating functions on chordal graphs**

## Status

This is a research outline, not a submission-ready manuscript. The chordal extremal theorem is open. The path recurrence and its growth constant are already in Abu-Khzam, Fernau, and Mann (MFCS 2023), so they are background rather than a novelty claim.

## Abstract

Write this after the main result exists. State the extremal question, the main theorem or counterexample family, the proof method, and its exact exponential consequence. Computational evidence cannot replace the theorem.

## 1. Introduction

- Define the extremal function $M(n)$ and exponential rate $\lambda$.
- Explain the known interval $\sqrt3\le\lambda\le1.8940$.
- State the open tightness question from the MFCS 2023 and JCSS papers.
- State the paper's contribution only after a proof or a reproducible counterexample family is complete.
- Distinguish the extremal count from the running time of a particular enumeration algorithm.

## 2. Definitions and an exact subset model

For each subset $S\subseteq V(G)$, define $f_S$ by:

- $f_S(v)=2$ if $v\in S$;
- $f_S(v)=0$ if $v\notin S$ and $N(v)\cap S\ne\varnothing$;
- $f_S(v)=1$ otherwise.

**Lemma 2.1 (private-zero characterization).** The function $f_S$ is a minimal RDF if and only if every $s\in S$ has a neighbor $u\notin S$ with $N(u)\cap S=\{s\}$.

**Proof plan.** Outside $S$, Roman domination forces a zero adjacent to $S$ and a one not adjacent to $S$; a one adjacent to $S$ could be lowered to zero. A selected vertex $s$ can be lowered from 2 to 1 precisely when every adjacent zero has another neighbor in $S$. Thus minimality is equivalent to a private zero-neighbor for each selected vertex. Include $S=\varnothing$, which yields the all-ones minimal RDF.

This lemma turns the count into a count of strongly irredundant sets, using the terminology of the 2024 Algorithmica paper.

## 3. The growth-rate formulation

**Lemma 3.1 (disjoint-union product).** For vertex-disjoint graphs $G,H$, $m(G\sqcup H)=m(G)m(H)$.

**Proposition 3.2 (existence of the rate).** The sequence $M(n)$ is supermultiplicative, and $\lambda=\lim_{n\to\infty}M(n)^{1/n}=\sup_{n\ge1}M(n)^{1/n}$ exists.

**Proof plan.** Disjoint unions of chordal graphs are chordal, and minimal RDF choices factor over components. Apply Fekete's lemma to $\log M(n)$; $1\le M(n)\le2^n$ supplies finiteness.

**Corollary 3.3 (finite-counterexample amplification).** The pointwise conjecture $M(n)\le3^{n/2}$ for all $n$ is equivalent to $\lambda=\sqrt3$. If a chordal graph $H$ of order $k$ has $m(H)>3^{k/2}$, then the disjoint union of $t$ copies has $m(H)^t$ minimal RDFs and forces $\lambda\ge m(H)^{1/k}>\sqrt3$.

The matching $tK_2$ supplies $m(tK_2)=3^t$, hence $\lambda\ge\sqrt3$. The published chordal enumeration algorithm gives $\lambda\le1.8940$.

## 4. Prior results and novelty boundary

- Cite the chordal enumeration bound and its open tightness question from [MFCS 2023](https://doi.org/10.4230/LIPIcs.MFCS.2023.6) and the [JCSS version](https://doi.org/10.1016/j.jcss.2026.103834).
- Record that forests and interval graphs already have matching $\sqrt3$ exponential bounds.
- Record the path recurrence as prior work; do not call it a new discovery.
- Use strong irredundance as a search term, while distinguishing all strongly irredundant sets from maximal irredundant sets.
- Explain that the chordal minimal-dominating-set bound applies only to a subfamily of minimal RDFs, not to functions using value 1.
- Review all later citations and related variants before making a novelty claim.

## 5. Main theorem (open slot)

**Conjecture 5.1.** For every chordal graph $G$ of order $n$, $m(G)\le3^{n/2}$.

If proved, conclude $M(n)\le3^{n/2}$ and, with the matching lower bound, obtain $\lambda=\sqrt3$. If disproved, state an explicit chordal graph $H$, its exact count $q$, and the repeated disjoint-union family, giving $\lambda\ge q^{1/|V(H)|}$.

The proof must use a structural chordal-graph argument. Candidate interfaces include a clique-tree dynamic program or a clique-separator recurrence whose states record which boundary vertices still need a private zero-neighbor. The earlier dossier reports one-vertex ratios above $\sqrt3$, but does not preserve an exact witness; establish that obstruction independently before using it. Do not assume a one-vertex recurrence without proof.

## 6. Computational evidence

Include only after reproduction:

- Identify the graph generator, whether objects are labeled or canonically unlabeled, and prove coverage.
- Save canonical graph encodings, exact counts, program versions, and complete logs.
- Validate the subset counter against direct $3^n$ assignment enumeration on a published set of small examples.
- Keep random-search results explicitly separate from exhaustive results.
- State clearly that a finite census cannot prove Conjecture 5.1.

## 7. Discussion

Explain whether the result closes the known chordal gap, improves a lower bound, or identifies a structural subclass with a new exact rate. List the next open questions without implying they are solved.

## Appendix checklist

- Complete proof of every lemma used in the main theorem.
- Independent verification report.
- Reproducibility instructions and archived input/output data.
- Literature search date, search terms, and all papers checked.
