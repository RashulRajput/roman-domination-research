# Exact extremal formula: conjecture and literature audit

**Search date:** 2026-10-26.

## The conjectures under review

Let \(m(T)\) be the number of pointwise-minimal Roman dominating functions
(minimal RDFs) on a tree \(T\), and define
\[
C(n)=\max\{m(T): |V(T)|=n,\ T\text{ a tree}\}.
\]
The proposed formulas are
\[
C(2k)=m(P_{2k}),\qquad
C(2k+1)=3^k+2^k-1=m(T_k),
\]
where \(T_k\) is the tree with a center and \(k\) arms of length two.
These remain **conjectures**. The exhaustive census now confirms them through
order 20; this finite range is not a proof for all \(n\).

## Literature findings and exact overlap

### Roman Census

Abu-Khzam, Fernau, and Mann, [*Roman Census: Enumerating and Counting Roman
Dominating Functions on Graph Classes*](https://doi.org/10.4230/LIPIcs.MFCS.2023.6),
appeared at MFCS 2023; a later journal version is listed in the *Journal of
Computer and System Sciences* (2026),
[DOI 10.1016/j.jcss.2026.103834](https://doi.org/10.1016/j.jcss.2026.103834).
The full [MFCS paper PDF](https://drops.dagstuhl.de/opus/volltexte/2023/18540/pdf/LIPIcs-MFCS-2023-6.pdf)
and [full arXiv version](https://arxiv.org/abs/2208.05261) were reviewed.

Relevant exact overlap:

- Their Theorem 3.4 contains the expression \(3^t+2^t-1\) in a lower-bound
  construction on split/cobipartite graphs with \(3t\) vertices. The graph
  family is different from the \(2k+1\)-vertex subdivided star \(T_k\).
  Thus the expression itself is prior; a formula specifically for \(T_k\)
  was not located.
- Their forest theorem gives \(m(F)\le(\sqrt3)^{|V(F)|}\), with equality
  attained by disjoint unions of \(P_2\). This proves the same exponential
  upper bound for trees, but its sharp construction is disconnected.
- Their path section gives exact recurrences and an
  \(O^*(1.6852^n)\) path upper bound. It does not state that paths maximize
  \(m(T)\) over trees of fixed order.
- Their results for forests and chordal graphs concern enumeration-time
  bounds and an exponential lower bound, not an exact pointwise formula for
  \(C(n)\).

The proposed pointwise formulas would be substantially stronger than the
forest-wide exponential bound: they would specify \(C(n)\) and its
extremizers separately at every order. They have not been proved here.

### Minimal RDFs and open irredundance

Abu-Khzam, Fernau, and Mann, [*Minimal Roman Dominating Functions:
Extensions and Enumeration*](https://doi.org/10.1007/s00453-024-01211-w),
prove the minimality characterization through the \(V_2\) set and use the
term “strong irredundance.” The underlying set condition is the established
notion of **open irredundance**: each selected vertex has an external private
neighbor outside the selected set. The equivalence of the set property is
prior terminology, not a new contribution.

Earlier tree work includes Farley and Proskurowski,
[*Computing the Maximum Order of an Open Irredundant Set in a Tree*]
(https://www.cs.uoregon.edu/Reports/TR-1983-005.pdf), later published in
the 1984 West Coast conference proceedings. This develops a tree algorithm
for the *maximum cardinality of one open-irredundant set*. Cockayne, Favaron,
Finbow, and Mynhardt,
[*Open Irredundance and Maximum Degree in Graphs*]
(https://doi.org/10.1016/j.disc.2007.10.002), study open-irredundance
parameters such as the minimum/maximum size among maximal sets and
degree-dependent bounds. These are cardinality questions. The present
problem counts **all** open-irredundant subsets (including the empty set)
and then maximizes that count over trees. No exact tree extremal-count
formula of this type was found in the sources reviewed.

### Related extremal counting on trees

These papers are close in method or motivation but count different objects:

- Rote, [*The Maximum Number of Minimal Dominating Sets in a Tree*]
(https://doi.org/10.1137/1.9781611975482.73), gives a sharp exponential
growth result and extremal constructions for minimal dominating sets.
- Tu, Zhang, and Shi, [*The Maximum Number of Maximum Dissociation Sets in
Trees*](https://doi.org/10.1002/jgt.22627), determine a pointwise extremal
formula and characterize equality trees for maximum dissociation sets.
- Earlier work on maximal independent sets and irredundance in trees likewise
concerns distinct set families. These provide analogies, not the claimed
minimal-RDF extremal theorem.

The cited tree/path papers in the *Roman Census* bibliography most relevant
to this objective, together with its later related works, were checked.
Related successors reviewed include [*Hitting the Romans*]
(https://arxiv.org/abs/2302.11417), [*Perfect Roman Domination and Unique
Response Roman Domination*](https://arxiv.org/abs/2309.07018), and
[*Enumeration With Nice Roman Domination Properties*]
(https://arxiv.org/abs/2511.20367). They address extension algorithms,
other Roman variants, or other set-counting problems; none of the reviewed
sources states the proposed \(C(n)\) formulas. This targeted citation audit
does not claim exhaustive coverage of every unrelated reference or every
later citing paper.

## Search record

The following exact and topic searches were run on 2026-10-26:

- "maximum number of minimal Roman dominating functions" trees
- "minimal Roman dominating functions" tree extremal
- "m(T)" "minimal Roman dominating" tree extremal
- "C(n)" minimal Roman dominating functions trees
- "path extremality" minimal Roman dominating functions
- "3^k+2^k-1" "Roman" tree
- "subdivided star" minimal Roman dominating functions
- "number of open irredundant sets" tree
- "open irredundant" tree maximum number of sets
- "maximum order of an open irredundant set in a tree"
- "maximum number of open irredundant sets" trees
- "Roman Census" tree Theorem 7.1 path

No exact match for either proposed pointwise formula was located in this
targeted search. That is evidence about the reviewed record, **not proof of
novelty or priority**.

## Assessment

| Proposed result | Nearest prior result | Difference | Novelty confidence |
|---|---|---|---|
| \(m(T_k)=3^k+2^k-1\) | Same expression in Roman Census for a different split/cobipartite construction | Exact count for this particular subdivided-star tree | Low to moderate; priority unresolved |
| \(C(2k)=m(P_{2k})\) | Exact path recurrences and forest upper bound in Roman Census | Pointwise extremality among all trees | Unresolved; no proof or direct prior statement located |
| \(C(2k+1)=m(T_k)\) | Forest-wide \((\sqrt3)^n\) bound and disconnected sharpness example | Connected, order-by-order extremal structure | Unresolved; no proof or direct prior statement located |
| \(\limsup C(n)^{1/n}=\sqrt3\) | Roman Census forest upper bound, sharp for disconnected forests | Connected tree lower-bound family \(T_k\) | Plausible connected-class refinement; priority unresolved |
| Rooted DP and finite census | Prior open-irredundance tree optimization algorithms | Counts every admissible set rather than maximizing its size | Correct computational contribution; algorithmic novelty not claimed |

The pointwise conjectures should not be presented as theorems. The strongest
current finite evidence is a complete canonical census through order 20;
details and verification artifacts are in
[COUNTEREXAMPLE_SEARCH.md](COUNTEREXAMPLE_SEARCH.md).
