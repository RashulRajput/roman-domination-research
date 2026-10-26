#!/usr/bin/env python3
"""Test whether balancing two spider legs can decrease the exact count."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

from test_spider_arm_split import edge_list, g6, partitions, spider
from tree_dp_recurrence import count_tree_dp


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, default=19)
    parser.add_argument("--output", type=Path, default=Path("spider_leg_balance_results.json"))
    args = parser.parse_args()
    smallest = None
    by_order = []
    start = time.perf_counter()
    for n in range(4, args.max_order + 1):
        moves = decreases = equal = increases = 0
        order_start = time.perf_counter()
        for lengths in partitions(n - 1):
            before = count_tree_dp(spider(lengths))
            for i, long_leg in enumerate(lengths):
                for j, short_leg in enumerate(lengths):
                    if i == j or long_leg < short_leg + 2:
                        continue
                    after_lengths = list(lengths)
                    after_lengths[i] -= 1
                    after_lengths[j] += 1
                    after_lengths.sort()
                    after_graph = spider(tuple(after_lengths))
                    after = count_tree_dp(after_graph)
                    moves += 1
                    if after < before:
                        decreases += 1
                        if smallest is None:
                            before_graph = spider(lengths)
                            smallest = {
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
        "operation": "transfer one edge from a leg a to a leg b when a>=b+2",
        "hypothesis_tested": "balancing two legs of a spider never decreases m",
        "exhaustive_orders": f"4..{args.max_order} over all integer partitions of n-1",
        "per_order": by_order,
        "smallest_counterexample": smallest,
        "total_seconds": time.perf_counter() - start,
    }
    args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    args.output.with_suffix(".log").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {args.output}", flush=True)


if __name__ == "__main__":
    main()
