#!/usr/bin/env python3
"""Canonical exact tree census using the verified rooted-tree DP.

Enumerates every unlabeled tree in the requested order range with
NetworkX's nonisomorphic_trees generator and stores graph6, edge lists,
counts, extremizers, and per-order timings.
"""

from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from pathlib import Path

import networkx as nx

from tree_dp_recurrence import count_tree_dp


KNOWN_UNLABELED_TREE_COUNTS = {
    13: 1301,
    14: 3159,
    15: 7741,
    16: 19320,
    17: 48629,
    18: 123867,
    19: 317955,
    20: 823065,
}


def graph6(tree: nx.Graph) -> str:
    return nx.to_graph6_bytes(tree, header=False).decode("ascii").strip()


def edges(tree: nx.Graph) -> list[list[int]]:
    return [list(e) for e in sorted(tuple(sorted(e)) for e in tree.edges())]


def path(n: int) -> nx.Graph:
    return nx.path_graph(n)


def subdivided_star(k: int) -> nx.Graph:
    graph = nx.Graph()
    graph.add_node(0)
    for i in range(k):
        x, y = 2 * i + 1, 2 * i + 2
        graph.add_edges_from(((0, x), (x, y)))
    return graph


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start-order", type=int, default=13)
    parser.add_argument("--max-order", type=int, required=True)
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="JSON output path (default: tree_census_extension_through_N.json)",
    )
    args = parser.parse_args()
    if args.start_order < 1 or args.max_order < args.start_order:
        parser.error("require 1 <= start-order <= max-order")
    output = args.output or Path(
        __file__
    ).resolve().parent / f"tree_census_extension_through_{args.max_order}.json"
    log = output.with_suffix(".log")
    all_records: list[dict] = []
    summaries: list[dict] = []
    log_lines = [
        f"Started UTC: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}",
        f"Python: {platform.python_version()}",
        f"NetworkX: {nx.__version__}",
        f"Canonical generator: networkx.generators.nonisomorphic_trees",
        f"Orders: {args.start_order}..{args.max_order}",
        f"Counter: verified rooted-tree DP from tree_dp_recurrence.py",
    ]
    run_start = time.perf_counter()

    for n in range(args.start_order, args.max_order + 1):
        order_start = time.perf_counter()
        records: list[dict] = []
        maximum = -1
        extremizers: list[str] = []
        for tree in nx.generators.nonisomorphic_trees(n):
            if not nx.is_tree(tree):
                raise AssertionError(f"generator produced a non-tree at n={n}")
            count = count_tree_dp(tree)
            code = graph6(tree)
            if count > maximum:
                maximum = count
                extremizers = [code]
            elif count == maximum:
                extremizers.append(code)
            records.append(
                {
                    "n": n,
                    "graph6": code,
                    "edges": edges(tree),
                    "m_dp": count,
                }
            )

        elapsed = time.perf_counter() - order_start
        expected = KNOWN_UNLABELED_TREE_COUNTS.get(n)
        if expected is not None and len(records) != expected:
            raise AssertionError(
                f"canonical class count mismatch at n={n}: "
                f"got {len(records)}, expected {expected}"
            )
        path_tree = path(n)
        path_count = count_tree_dp(path_tree)
        k = (n - 1) // 2
        tk_count = count_tree_dp(subdivided_star(k)) if n % 2 else None
        summary = {
            "n": n,
            "classes": len(records),
            "C_n": maximum,
            "extremizer_graph6": extremizers,
            "path_count": path_count,
            "path_is_extremal": path_count == maximum,
            "T_k_count": tk_count,
            "T_k_is_extremal": tk_count == maximum if tk_count is not None else None,
            "seconds": elapsed,
            "expected_A000055_count": expected,
            "class_count_check": "passed" if expected is not None else "not available",
        }
        summaries.append(summary)
        all_records.extend(records)
        log_lines.append(
            f"n={n}: classes={len(records)}; C(n)={maximum}; "
            f"extremizers={len(extremizers)}; path={path_count}; "
            f"T_k={tk_count}; seconds={elapsed:.6f}; "
            f"known_class_count={expected}"
        )
        output.write_text(
            json.dumps(
                {
                    "scope": f"complete unlabeled tree census n={args.start_order}..{args.max_order}",
                    "counter": "rooted-tree DP in tree_dp_recurrence.py",
                    "python": platform.python_version(),
                    "networkx": nx.__version__,
                    "summaries": summaries,
                    "trees": all_records,
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        log.write_text("\n".join(log_lines) + "\n", encoding="utf-8")
        print(log_lines[-1], flush=True)

    log_lines.append(f"Total seconds: {time.perf_counter() - run_start:.6f}")
    log_lines.append(
        f"Finished UTC: {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime())}"
    )
    log.write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    print(f"Saved {len(all_records)} records to {output}", flush=True)
    print(f"Saved run log to {log}", flush=True)


if __name__ == "__main__":
    main()
