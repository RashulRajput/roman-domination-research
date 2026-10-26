# Paper assessment

**Update (2026-10-26):** the complete canonical tree census is now through
order 20, and it still supports the two pointwise extremal conjectures in
that finite range. No all-order proof or sharper tree upper bound was
obtained. The detailed current audit is in
[COUNTEREXAMPLE_SEARCH.md](COUNTEREXAMPLE_SEARCH.md) and
[STRONGEST_NEW_RESULT.md](STRONGEST_NEW_RESULT.md).

## Current contribution

The work contains a clean exact theorem for the subdivided-star tree (T_k), a rigorously derived connected-tree growth-rate limsup, an eventual comparison showing paths are beaten by a connected tree family, and a complete canonical extremal-tree census through order 20. The original census through order 12 uses three exact counters. A separately implemented fixed-array DP rechecked all 1,345,037 individual counts at orders 13–20 with zero mismatches; an independent subset counter additionally checked the extrema and the path/T_k counts.

The main formula is (m(T_k)=3^k+2^k-1). Its proof is short and transparent. The numerical expression already occurs in Roman Census for a different split/cobipartite family, and the general ((\sqrt3)^n) forest upper bound is also published. The mathematical difference is the **connected tree** lower-bound family and its consequences. The census gives a concrete first path counterexample at order 11 and documents the small-order extremizers; it is not itself an all-orders theorem.

## Is this sufficient for a research note?

**Assessment: not yet, on the evidence currently available.** A short note could be defensible if a broader literature check confirms that the connected-tree $\sqrt3$-rate lower bound and the exact $T_k$ statement are absent. At present, the count expression has a close published analogue, the rate theorem is a short combination of the published forest upper bound and the $T_k$ formula, and the path counterexample’s numerical margin is one. The exact tree formula may be a useful lemma, but the standalone significance is modest.

This is an editorial judgment, not a claim that the results are unpublishable. The novelty review in [NOVELTY_MATRIX.md](NOVELTY_MATRIX.md) records the evidence and its limits.

## Mathematical gap that remains

The central unresolved question is the pointwise extremal function

\[
C(n)=\max\{m(T):T\text{ is an }n\text{-vertex tree}\}.
\]

The census establishes (C(n)) through n=20. It finds paths as unique maximizers at all tested even orders, including n=20; ties between paths and (T_k) at orders 7 and 9; and T_k as an extremizer at every tested odd order through 19. It does not prove any of these patterns for larger orders. The path-maximizes-for-every-connected-chordal-graph proposal is false, already on (T_5).

The exact rooted-tree DP in [EXTREMAL_TREES.md](EXTREMAL_TREES.md) is structurally sound and verified, but it has not yet been turned into a sharp optimization argument over tree shapes. A scalar leaf-deletion induction based on path increments fails at orders 7 and 11, so any proof needs boundary states that retain the private-witness information.

## What would materially strengthen the paper

The most valuable next result would be a theorem that determines (C(n)) for all (n), or a sharp recurrence/upper bound with an equality characterization of the extremal tree classes. A weaker but still substantive advance would be a structural theorem that isolates the possible extremizers (for example, a proved reduction to a specific class of rooted trees) and then solves the resulting optimization.

The rate question itself is settled at the limsup level by the proved (T_k) formula plus the published forest bound. A stronger rate paper would need genuinely sharper pointwise information, such as a best possible constant-factor bound for (C(n)/(\sqrt3)^n), together with matching constructions or stability information. No such bound is claimed here.

## Proven versus observed

- **Proven:** $m(T_k)=3^k+2^k-1$; $\limsup C(n)^{1/n}=\sqrt3$; and $T_k$ eventually exceeds $P_{2k+1}$, using the published path upper bound.
- **Exhaustively observed:** the exact (C(n)), every extremal isomorphism class, and the displayed path/T-family comparisons for orders 1 through 20; every individual extended-census count was also checked by a second DP implementation.
- **Not established:** path extremality at all even orders, (T_k)-extremality at all odd orders, a limit (rather than limsup) for (C(n)^{1/n}), or a formula for (C(n)).

See [STRONGEST_THEOREM.md](STRONGEST_THEOREM.md) for the complete proof and [EXTREMAL_TREES.md](EXTREMAL_TREES.md) for the census, recurrence, failed induction, scripts, logs, and encodings.
