#!/usr/bin/env python3
"""Test a branch-splitting move on spiders with exact rooted-DP counts.

The move replaces one leg of length r >= 3 by two legs of lengths 2 and
r-2. The total number of vertices is unchanged. We test the proposed
inequality m(after) >= m(before), minimizing any counterexample by order.
"""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import networkx as nx

from tree_dp_recurrence import count_tree_dp


def partitions(total: int, minimum: int = 1):
    if total == 0:
        yield ()
        return
    for first in range(minimum, total + 1):
        for tail in partitions(total - first, first):
            yield (first,) + tail


def spider(lengths: tuple[int, ...]) -> nx.Graph:
    graph = nx.Graph()
    graph.add_node(0)
    next_vertex = 1
    for length in lengths:
        previous = 0
        for _ in range(length):
            graph.add_edge(previous, next_vertex)
            previous = next_vertex
            next_vertex += 1
    return graph


def g6(graph: nx.Graph) -> str:
    return nx.to_graph6_bytes(graph, header=False).decode("ascii").strip()


def edge_list(graph: nx.Graph) -> list[list[int]]:
    return [list(e) for e in sorted(tuple(sorted(e)) for e in graph.edges())]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, default=19)
    parser.add_argument("--output", type=Path, default=Path("spider_arm_split_results.json"))
    args = parser.parse_args()
    records: list[dict] = []
    by_order: list[dict] = []
    smallest = None
    start = time.perf_counter()
    for n in range(4, args.max_order + 1):
        moves = decreases = equal = increases = 0
        order_start = time.perf_counter()
        for lengths in partitions(n - 1):
            before_graph = spider(lengths)
            before = count_tree_dp(before_graph)
            for i, r in enumerate(lengths):
                if r < 3:
                    continue
                after_lengths = list(lengths)
                after_lengths.pop(i)
                after_lengths.extend((2, r - 2))
                after_lengths.sort()
                after_graph = spider(tuple(after_lengths))
                after = count_tree_dp(after_graph)
                moves += 1
                item = {
                    "n": n,
                    "before_legs": list(lengths),
                    "after_legs": after_lengths,
                    "before_graph6": g6(before_graph),
                    "before_edges": edge_list(before_graph),
                    "before_count": before,
                    "after_graph6": g6(after_graph),
                    "after_edges": edge_list(after_graph),
                    "after_count": after,
                }
                if after < before:
                    decreases += 1
                    if smallest is None:
                        smallest = item
                    if n <= 12:
                        records.append(item)
                elif after == before:
                    equal += 1
                else:
                    increases += 1
        by_order.append(
            {
                "n": n,
                "spider_leg_partitions": sum(1 for _ in partitions(n - 1)),
                "moves": moves,
                "decreases": decreases,
                "equal": equal,
                "increases": increases,
                "seconds": time.perf_counter() - order_start,
            }
        )
        print(by_order[-1], flush=True)
    result = {
        "operation": "replace one leg r>=3 by legs 2 and r-2",
        "hypothesis_tested": "splitting a long spider arm never decreases m",
        "exhaustive_orders": f"4..{args.max_order} over all integer partitions of n-1",
        "per_order": by_order,
        "smallest_counterexample": smallest,
        "counterexamples_through_order_12": records,
        "total_seconds": time.perf_counter() - start,
        "networkx": nx.__version__,
    }
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    args.output.with_suffix(".log").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {args.output}", flush=True)


if __name__ == "__main__":
    main()
