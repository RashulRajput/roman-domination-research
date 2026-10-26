#!/usr/bin/env python3
"""Independently verify the minimal local-transformation counterexamples."""

from __future__ import annotations

import json
from pathlib import Path

import networkx as nx

from verify_extended_extremizers import direct_subset_count


ROOT = Path(__file__).resolve().parent


def direct_histogram(tree: nx.Graph) -> list[int]:
    vertices = list(tree.nodes())
    index = {v: i for i, v in enumerate(vertices)}
    n = len(vertices)
    neighbors = [0] * n
    for v in vertices:
        for w in tree.neighbors(v):
            neighbors[index[v]] |= 1 << index[w]
    universe = (1 << n) - 1
    histogram = [0] * (n + 1)
    for selected in range(1 << n):
        remaining = selected
        valid = True
        while remaining:
            bit = remaining & -remaining
            remaining ^= bit
            i = bit.bit_length() - 1
            candidates = neighbors[i] & (universe ^ selected)
            witness = False
            while candidates:
                u_bit = candidates & -candidates
                candidates ^= u_bit
                u = u_bit.bit_length() - 1
                if neighbors[u] & selected == bit:
                    witness = True
                    break
            if not witness:
                valid = False
                break
        if valid:
            histogram[selected.bit_count()] += 1
    return histogram


def verify(result_file: str, key: str, before_key: str, after_key: str) -> dict:
    data = json.loads((ROOT / result_file).read_text(encoding="utf-8"))
    item = data[key]
    before = nx.from_graph6_bytes(item[before_key].encode("ascii"))
    after = nx.from_graph6_bytes(item[after_key].encode("ascii"))
    before_count = direct_subset_count(before)
    after_count = direct_subset_count(after)
    before_hist = direct_histogram(before)
    after_hist = direct_histogram(after)
    if before_count != item.get("source_count", item.get("before_count")):
        raise AssertionError((result_file, "source mismatch", before_count, item))
    if after_count != item.get("moved_count", item.get("after_count")):
        raise AssertionError((result_file, "target mismatch", after_count, item))
    return {
        "source_graph6": item[before_key],
        "source_edges": item.get("source_edges", item.get("before_edges")),
        "source_count_direct": before_count,
        "source_by_subset_size": before_hist,
        "target_graph6": item[after_key],
        "target_edges": item.get("moved_edges", item.get("after_edges")),
        "target_count_direct": after_count,
        "target_by_subset_size": after_hist,
        "order": item["n"],
    }


def main() -> None:
    results = {
        "leaf_to_leaf_transfer": verify(
            "leaf_transfer_order_8.json",
            "smallest_counterexample",
            "source_graph6",
            "moved_graph6",
        ),
        "split_arm_r_to_2_plus_r_minus_2": verify(
            "spider_arm_split_results.json",
            "smallest_counterexample",
            "before_graph6",
            "after_graph6",
        ),
        "balance_two_spider_legs": verify(
            "spider_leg_balance_results.json",
            "smallest_counterexample",
            "before_graph6",
            "after_graph6",
        ),
    }
    out = ROOT / "transformation_counterexamples_direct_check.json"
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    (ROOT / "transformation_counterexamples_direct_check.log").write_text(
        json.dumps(results, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
