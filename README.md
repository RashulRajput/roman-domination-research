# Extremal Minimal Roman Dominating Functions on Chordal Graphs & Trees

[![GitHub license](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)

An exact computational and combinatorial research project investigating the extremal growth rate of **pointwise-minimal Roman dominating functions (RDFs)** on chordal graphs and trees.

This project addresses and extends the open problem posed by **Abu-Khzam, Fernau, and Mann** in *Roman Census: Enumerating and Counting Roman Dominating Functions on Graph Classes* ([MFCS 2023](https://doi.org/10.4230/LIPIcs.MFCS.2023.6) / [JCSS 2026](https://doi.org/10.1016/j.jcss.2026.103834), [arXiv:2208.05261](https://arxiv.org/abs/2208.05261)).

---

## 💡 What Is This Project About? (A Quick Hint)

A **Roman dominating function** on a graph $G$ assigns labels $\{0, 1, 2\}$ to vertices such that every vertex labeled $0$ has a neighbor labeled $2$. The function is **minimal** if lowering any positive label by 1 destroys Roman domination.

Let $m(G)$ denote the number of minimal Roman dominating functions on $G$.

* **The Published Gap:** For chordal graphs, the best-known enumeration algorithm upper bound is $O^*(1.8940^n)$, while the established lower bound is $(\sqrt{3})^n \approx 1.7321^n$ (achieved by disconnected matchings $t \cdot K_2$). Whether any chordal graph family achieves an asymptotic growth rate higher than $\sqrt{3}$ was left explicitly open.
* **The Connected Graph Problem:** Disjoint edges are disconnected. Can **connected** graphs achieve the $\sqrt{3}^n$ growth rate?
* **Surprise Discovery:** While initial intuition favored paths $P_n$, paths grow at only $\lambda \approx 1.6851^n$. We discovered and proved that the **subdivided star family** $T_k$ (a center with $k$ arms of length 2, order $n = 2k+1$) surpasses paths at $n \ge 11$, with an exact closed-form count:
  $$m(T_k) = 3^k + 2^k - 1$$
  This establishes that connected trees achieve the limsup growth rate:
  $$\limsup_{n \to \infty} \Big(\max_{|V(T)|=n} m(T)\Big)^{1/n} = \sqrt{3}$$

---

## 🚀 Key Theorems & Contributions

1. **All-Order Connected-Tree Growth Theorem:**
   $$\boxed{\limsup_{n \to \infty} C(n)^{1/n} = \sqrt{3}}$$
   where $C(n) = \max \{m(T) : T \text{ is a tree of order } n\}$.
   - **Upper Bound:** Controlled by Abu-Khzam et al.'s forest-wide bound $m(F) \le (\sqrt{3})^{|V(F)|}$.
   - **Lower Bound Witness:** Established via the connected subdivided star family $T_k$ of order $2k+1$.
   *(Full proof in [`STRONGEST_NEW_RESULT.md`](STRONGEST_NEW_RESULT.md) and [`STRONGEST_THEOREM.md`](STRONGEST_THEOREM.md))*

2. **Refutation of Path-Extremality:**
   - At $n=11$, $m(T_5) = 274 > m(P_{11}) = 273$.
   - For all sufficiently large odd orders, $T_k$ strictly dominates the path $P_{2k+1}$.

3. **Complete Finite Extremal Sequence ($n=1$ to $20$):**
   Using custom dynamic programming solvers, we resolved the exact sequence $C(n)$ for all trees up to order 20:
   $$(C(1), \dots, C(20)) = (1, 3, 4, 7, 12, 20, 34, 57, 96, 162, 274, 460, 792, 1306, 2314, 3709, 6816, 10532, 20194, 29908)$$
   *(All extremal graphs and graph6 codes documented in [`COUNTEREXAMPLE_SEARCH.md`](COUNTEREXAMPLE_SEARCH.md) and [`results/path_extremal/extremal_summary_through_20.json`](results/path_extremal/extremal_summary_through_20.json))*

4. **Massive Chordal Censuses (0 Counterexamples to $M(n) \le 3^{n/2}$):**
   - Verified across all non-isomorphic chordal graphs in NetworkX Atlas ($n \le 7$).
   - Exhaustively verified all 1.4 million chordal graphs on $n=8$ generated via perfect elimination orderings (PEO). No graph exceeds $3^{n/2} = 81$.

---

## 📂 Repository Structure

```
├── STRONGEST_NEW_RESULT.md        # Primary theorem: limsup C(n)^(1/n) = sqrt(3) & proofs
├── STRONGEST_THEOREM.md           # Formal statement and proof of the subdivided star formula
├── NOVELTY_MATRIX.md              # Research novelty audit against MFCS 2023 / JCSS 2026
├── RESEARCH_AUDIT.md              # Audit of computational claims and formal handoffs
├── EXTREMAL_TREES.md              # Detailed structural analysis of extremal trees
├── EXTREMAL_CONJECTURE_AUDIT.md   # Audit of the working conjecture M(n) <= 3^(n/2)
├── COUNTEREXAMPLE_SEARCH.md       # Graph6 codes and isomorphism lists for small orders
├── PAPER_OUTLINE.md               # Target paper draft structure
│
├── count_minimal_rdf.py           # Dual independent engines: Brute force (3^n) & Subset (2^n)
├── chordal_census.py              # Atlas & structured family census runner
├── deep_analysis.py               # Structural analysis: building blocks, clique trees, simplicial vertices
├── recurrence_analysis.py         # Path order-5 recurrence and root verification
├── transfer_matrix.py             # Transfer-matrix state derivation for paths
│
└── results/path_extremal/         # Tree dynamic programming census & verification suite
    ├── fast_tree_dp.py            # Optimized DP solver for trees
    ├── full_tree_census.py        # Streamed full tree enumeration runner
    ├── extremal_summary_through_20.json  # Complete summary of extremal trees up to n=20
    ├── verify_subdivided_star.py  # Independent verification of m(T_k) = 3^k + 2^k - 1
    └── verify_fast_tree_dp.py     # Test suite cross-checking fast DP with brute force
```

---

## 🛠️ Verification & Reproduction

All computations are reproducible using Python 3.10+ with `networkx` and `numpy`:

```bash
# 1. Verify counting engines (cross-validates 3^n brute force against 2^n subset tests)
python count_minimal_rdf.py

# 2. Verify the subdivided star formula m(T_k) = 3^k + 2^k - 1
python results/path_extremal/verify_subdivided_star.py

# 3. Verify fast tree dynamic programming against direct enumeration
python results/path_extremal/verify_fast_tree_dp.py

# 4. Run the recurrence analysis and verify path polynomial roots
python recurrence_analysis.py
```

---

## 📚 References

- **F. N. Abu-Khzam, H. Fernau, K. Mann.** *Roman Census: Enumerating and Counting Roman Dominating Functions on Graph Classes.* MFCS 2023 (LIPIcs vol. 272, pp. 6:1–6:15). Journal version in *Journal of Computer and System Sciences* (JCSS), 2026.
- **F. N. Abu-Khzam, H. Fernau, K. Mann.** *Minimal Roman Dominating Functions: Extensions and Enumeration.* Algorithmica 86(6): 1862–1887 (2024).
