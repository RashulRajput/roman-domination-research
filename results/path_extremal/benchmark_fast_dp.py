#!/usr/bin/env python3
"""Benchmark audited and array DPs on an identical canonical prefix."""

import argparse
import json
import time
from pathlib import Path

import networkx as nx

from fast_tree_dp import count_tree_dp_fast
from memo_tree_dp import MemoizedTreeCounter
from bounded_memo_tree_dp import BoundedMemoizedTreeCounter
from tree_dp_recurrence import count_tree_dp


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--order", type=int, default=17)
    parser.add_argument("--limit", type=int, default=500)
    args = parser.parse_args()
    trees = []
    for i, tree in enumerate(nx.generators.nonisomorphic_trees(args.order)):
        if i >= args.limit:
            break
        trees.append(tree)
    start = time.perf_counter()
    old = [count_tree_dp(t) for t in trees]
    old_seconds = time.perf_counter() - start
    start = time.perf_counter()
    fast = [count_tree_dp_fast(t) for t in trees]
    fast_seconds = time.perf_counter() - start
    memo = MemoizedTreeCounter()
    start = time.perf_counter()
    memoized = [memo.count(t) for t in trees]
    memo_seconds = time.perf_counter() - start
    bounded = BoundedMemoizedTreeCounter(cache_limit=10)
    start = time.perf_counter()
    bounded_values = [bounded.count(t) for t in trees]
    bounded_seconds = time.perf_counter() - start
    if old != fast or old != memoized or old != bounded_values:
        raise AssertionError("benchmark counters disagree")
    result = {"order": args.order, "canonical_prefix_trees": len(trees), "audited_dp_seconds": old_seconds, "array_dp_seconds": fast_seconds, "unbounded_memo_dp_seconds": memo_seconds, "bounded_memo_dp_seconds": bounded_seconds, "bounded_shapes_cached": len(bounded.messages), "bounded_speedup": old_seconds / bounded_seconds}
    out = Path(__file__).resolve().parent / f"dp_benchmark_n{args.order}_prefix{len(trees)}.json"
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    out.with_suffix(".log").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(result)


if __name__ == "__main__":
    main()
