#!/usr/bin/env python3
"""Cross-check the array DP against the previously audited DP."""

from __future__ import annotations

import time
from pathlib import Path

import networkx as nx

from fast_tree_dp import count_tree_dp_fast
from memo_tree_dp import MemoizedTreeCounter
from bounded_memo_tree_dp import BoundedMemoizedTreeCounter
from tree_dp_recurrence import count_tree_dp


def main() -> None:
    checked = 0
    start = time.perf_counter()
    memo = MemoizedTreeCounter()
    bounded = BoundedMemoizedTreeCounter(cache_limit=10)
    singleton = nx.empty_graph(1)
    if (count_tree_dp(singleton) != count_tree_dp_fast(singleton)
            or count_tree_dp(singleton) != memo.count(singleton)
            or count_tree_dp(singleton) != bounded.count(singleton)):
        raise AssertionError("singleton mismatch")
    checked += 1
    for n in range(2, 13):
        for tree in nx.generators.nonisomorphic_trees(n):
            old = count_tree_dp(tree)
            new = count_tree_dp_fast(tree)
            memoized = memo.count(tree)
            bounded_value = bounded.count(tree)
            if old != new or old != memoized or old != bounded_value:
                raise AssertionError({"n": n, "edges": list(tree.edges()), "old": old, "fast": new, "memoized": memoized, "bounded": bounded_value})
            checked += 1
    elapsed = time.perf_counter() - start
    lines = [
        f"Array, memoized, and bounded-memo DPs agree with audited DP on all {checked} canonical trees through n=12.",
        f"Bounded memo cache_limit=10, rooted shapes cached={len(bounded.messages)}",
        f"Seconds: {elapsed:.6f}",
    ]
    print("\n".join(lines))
    (Path(__file__).resolve().parent / "fast_dp_validation.log").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


if __name__ == "__main__":
    main()
