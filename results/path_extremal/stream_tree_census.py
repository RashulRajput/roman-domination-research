#!/usr/bin/env python3
"""Stream one complete unlabeled-tree order through the exact rooted DP."""

from __future__ import annotations

import argparse
import gzip
import json
import platform
import time
from pathlib import Path

import networkx as nx

from bounded_memo_tree_dp import BoundedMemoizedTreeCounter


KNOWN_COUNTS = {17: 48629, 18: 123867, 19: 317955, 20: 823065}
OUT_DIR = Path(__file__).resolve().parent


def g6(graph: nx.Graph) -> str:
    return nx.to_graph6_bytes(graph, header=False).decode("ascii").strip()


def edges(graph: nx.Graph) -> list[list[int]]:
    return [list(e) for e in sorted(tuple(sorted(e)) for e in graph.edges())]


def family_path(n: int) -> nx.Graph:
    return nx.path_graph(n)


def family_t(k: int) -> nx.Graph:
    tree = nx.Graph()
    tree.add_node(0)
    for i in range(k):
        x, y = 2 * i + 1, 2 * i + 2
        tree.add_edges_from(((0, x), (x, y)))
    return tree


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("order", type=int)
    args = parser.parse_args()
    n = args.order
    if n < 2:
        parser.error("order must be at least 2")
    data_path = OUT_DIR / f"tree_census_n{n}.jsonl.gz"
    summary_path = OUT_DIR / f"tree_census_n{n}_summary.json"
    log_path = OUT_DIR / f"tree_census_n{n}.log"
    start = time.perf_counter()
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    count = 0
    maximum = -1
    maximizers: list[str] = []
    counter = BoundedMemoizedTreeCounter(cache_limit=10)
    order_start = time.perf_counter()
    with gzip.open(data_path, "wt", encoding="utf-8", compresslevel=6) as out:
        for tree in nx.generators.nonisomorphic_trees(n):
            value = counter.count(tree)
            code = g6(tree)
            row = {"n": n, "graph6": code, "edges": edges(tree), "m_dp": value}
            out.write(json.dumps(row, separators=(",", ":")) + "\n")
            count += 1
            if value > maximum:
                maximum = value
                maximizers = [code]
            elif value == maximum:
                maximizers.append(code)
    elapsed = time.perf_counter() - order_start
    expected = KNOWN_COUNTS.get(n)
    if expected is not None and count != expected:
        raise AssertionError(f"n={n}: generated {count} classes, expected {expected}")
    path_count = counter.count(family_path(n))
    tk_count = counter.count(family_t((n - 1) // 2)) if n % 2 else None
    summary = {
        "order": n,
        "canonical_generator": "networkx.generators.nonisomorphic_trees",
        "counter": "bounded-memo exact rooted-tree DP in bounded_memo_tree_dp.py",
        "python": platform.python_version(),
        "networkx": nx.__version__,
        "classes_emitted": count,
        "known_unlabeled_tree_count": expected,
        "class_count_check": count == expected if expected is not None else None,
        "C_n": maximum,
        "extremizers_graph6": maximizers,
        "path_count": path_count,
        "T_k_count": tk_count,
        "path_is_extremal": path_count == maximum,
        "T_k_is_extremal": tk_count == maximum if tk_count is not None else None,
        "seconds_for_order": elapsed,
        "seconds_total": time.perf_counter() - start,
        "rooted_shapes_cached": len(counter.messages),
        "memo_cache_limit_vertices": counter.cache_limit,
        "data_file": data_path.name,
    }
    summary_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    log_path.write_text(
        "\n".join(
            [
                f"Started UTC: {now}",
                f"Python: {platform.python_version()}",
                f"NetworkX: {nx.__version__}",
                f"Canonical generator: networkx.generators.nonisomorphic_trees",
                f"n={n}; classes={count}; expected={expected}; check={count == expected}",
                f"C(n)={maximum}; extremizers={len(maximizers)}",
                f"path={path_count}; T_k={tk_count}",
                f"Order seconds={elapsed:.6f}; total seconds={time.perf_counter() - start:.6f}",
                f"Exact records: {data_path}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
