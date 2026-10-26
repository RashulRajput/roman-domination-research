#!/usr/bin/env python3
"""Exhaustively test a natural path-smoothing inequality on small trees.

Operation: choose a leaf ell adjacent to v and a distinct leaf x; replace
v-ell by x-ell. This preserves order and treehood and transfers one leaf to
another leaf. The script records every tested move, exact DP counts, and the
smallest counterexample to the conjecture that the move never decreases m.
"""

from __future__ import annotations

import json
import argparse
import time
from pathlib import Path

import networkx as nx

from tree_dp_recurrence import count_tree_dp


def g6(graph: nx.Graph) -> str:
    return nx.to_graph6_bytes(graph, header=False).decode("ascii").strip()


def edge_list(graph: nx.Graph) -> list[list[int]]:
    return [list(e) for e in sorted(tuple(sorted(e)) for e in graph.edges())]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, default=12)
    parser.add_argument("--output", type=Path, default=Path("leaf_transfer_results.json"))
    args = parser.parse_args()
    max_order = args.max_order
    records: list[dict] = []
    per_order: list[dict] = []
    smallest_failure = None
    start = time.perf_counter()
    for n in range(3, max_order + 1):
        trees = 0
        moves = decreases = equals = increases = 0
        order_start = time.perf_counter()
        for tree in nx.generators.nonisomorphic_trees(n):
            trees += 1
            before = count_tree_dp(tree)
            leaves = [v for v in tree if tree.degree(v) == 1]
            for ell in leaves:
                v = next(iter(tree.neighbors(ell)))
                for x in leaves:
                    if x == ell or x == v:
                        continue
                    moved = tree.copy()
                    moved.remove_edge(v, ell)
                    moved.add_edge(x, ell)
                    if not nx.is_tree(moved):
                        raise AssertionError("leaf transfer did not produce a tree")
                    after = count_tree_dp(moved)
                    moves += 1
                    if after < before:
                        decreases += 1
                        if smallest_failure is None:
                            smallest_failure = {
                                "n": n,
                                "source_graph6": g6(tree),
                                "source_edges": edge_list(tree),
                                "source_count": before,
                                "moved_graph6": g6(moved),
                                "moved_edges": edge_list(moved),
                                "moved_count": after,
                                "move": {"leaf": ell, "from_neighbor": v, "to_leaf": x},
                            }
                        if n <= 8:
                            records.append(
                                {
                                    "n": n,
                                    "source_graph6": g6(tree),
                                    "source_count": before,
                                    "moved_graph6": g6(moved),
                                    "moved_count": after,
                                    "move": {"leaf": ell, "from_neighbor": v, "to_leaf": x},
                                }
                            )
                    elif after == before:
                        equals += 1
                    else:
                        increases += 1
        per_order.append(
            {
                "n": n,
                "unlabeled_trees": trees,
                "moves": moves,
                "decreases": decreases,
                "equal": equals,
                "increases": increases,
                "seconds": time.perf_counter() - order_start,
            }
        )
        print(per_order[-1], flush=True)

    result = {
        "operation": "replace leaf edge v-ell by x-ell for a distinct existing leaf x",
        "hypothesis_tested": "every such leaf transfer satisfies m(after) >= m(before)",
        "exhaustive_orders": f"3..{max_order}",
        "per_order": per_order,
        "smallest_counterexample": smallest_failure,
        "all_counterexamples_through_order_8": records,
        "total_seconds": time.perf_counter() - start,
        "networkx": nx.__version__,
    }
    out = args.output
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    log = out.with_suffix(".log")
    log.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {out} and {log}", flush=True)


if __name__ == "__main__":
    main()
