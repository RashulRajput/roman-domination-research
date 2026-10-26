#!/usr/bin/env python3
"""Independent subset/private-zero counter for extended census extremizers."""

from __future__ import annotations

import json
import time
from pathlib import Path

import networkx as nx


ROOT = Path(__file__).resolve().parent


def direct_subset_count(tree: nx.Graph) -> int:
    """Count S with every selected vertex having an external private neighbor."""
    n = tree.number_of_nodes()
    vertices = list(tree.nodes())
    index = {v: i for i, v in enumerate(vertices)}
    neighbors = [0] * n
    for v in vertices:
        i = index[v]
        for w in tree.neighbors(v):
            neighbors[i] |= 1 << index[w]
    universe = (1 << n) - 1
    total = 0
    for selected in range(1 << n):
        remaining = selected
        valid = True
        while remaining:
            bit = remaining & -remaining
            i = bit.bit_length() - 1
            remaining ^= bit
            witness = False
            # A private *zero* must be outside S. In open-neighborhood
            # notation, N(u) intersect S={s} alone would also allow u in S.
            candidates = neighbors[i] & (universe ^ selected)
            while candidates:
                u_bit = candidates & -candidates
                u = u_bit.bit_length() - 1
                candidates ^= u_bit
                if neighbors[u] & selected == bit:
                    witness = True
                    break
            if not witness:
                valid = False
                break
        total += valid
    return total


def load_legacy_summary(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    marker = '  "trees": ['
    prefix = text[: text.index(marker)].rstrip()
    if prefix.endswith(","):
        prefix = prefix[:-1]
    return json.loads(prefix + "\n}")["summaries"]


def main() -> None:
    max_n = 20
    summaries = []
    start = time.perf_counter()
    old_summaries = {}
    for file_name in (
        "tree_census_extension_through_16.json",
        "tree_census_extension_through_18.json",
    ):
        for item in load_legacy_summary(ROOT / file_name):
            old_summaries[item["n"]] = item
    for n in range(13, max_n + 1):
        if n <= 18:
            summary = old_summaries[n]
            maximum = summary["C_n"]
            extremizer_codes = summary["extremizer_graph6"]
        else:
            summary = json.loads((ROOT / f"tree_census_n{n}_summary.json").read_text(encoding="utf-8"))
            maximum = summary["C_n"]
            extremizer_codes = summary["extremizers_graph6"]
        for code in extremizer_codes:
            graph = nx.from_graph6_bytes(code.encode("ascii"))
            direct = direct_subset_count(graph)
            if direct != maximum:
                raise AssertionError({"n": n, "graph6": code, "DP maximum": maximum, "direct": direct})
        path_tree = nx.path_graph(n)
        path_direct = direct_subset_count(path_tree)
        if n % 2:
            k = (n - 1) // 2
            tk = nx.Graph()
            tk.add_node(0)
            for i in range(k):
                tk.add_edges_from(((0, 2 * i + 1), (2 * i + 1, 2 * i + 2)))
            tk_direct = direct_subset_count(tk)
        else:
            tk_direct = None
        summaries.append(
            {
                "n": n,
                "C_n_by_DP": maximum,
                "extremizer_count": len(extremizer_codes),
                "extremizer_counts_by_independent_subset_counter": [maximum for _ in extremizer_codes],
                "path_count_by_independent_subset_counter": path_direct,
                "T_k_count_by_independent_subset_counter": tk_direct,
                "all_extremizers_agree": True,
            }
        )
        print(summaries[-1], flush=True)
    result = {
        "method": "independent exhaustive subset/private-zero counter",
        "orders": "13..20",
        "summaries": summaries,
        "seconds": time.perf_counter() - start,
    }
    (ROOT / "extended_extremizer_independent_check.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8"
    )
    (ROOT / "extended_extremizer_independent_check.log").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
