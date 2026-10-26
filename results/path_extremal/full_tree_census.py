"""Exhaustive unlabeled-tree census with two independent exact counters.

Counter A imports the subset/private-zero test from path_extremal_search.
Counter B independently enumerates every ternary labeling and tests the RDF
definition plus pointwise minimality directly.  The latter is parallelized.
"""

from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from datetime import date
import json
import os
from pathlib import Path
import sys
import time

import networkx as nx

from path_extremal_search import count_direct, count_subset
from tree_dp_recurrence import count_tree_dp


OUTDIR = Path(__file__).resolve().parent
JSON_OUT = OUTDIR / "tree_census_through_12.json"
LOG_OUT = OUTDIR / "tree_census_through_12.log"
MAX_ORDER = 12
WORKERS = min(12, os.cpu_count() or 1)


def _direct_worker(job: tuple[int, tuple[tuple[int, int], ...]]) -> tuple[int, int]:
    n, edges = job
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    graph.add_edges_from(edges)
    return n, count_direct(graph)


def graph_record(graph: nx.Graph, subset: int, direct: int, rooted_dp: int) -> dict:
    n = graph.number_of_nodes()
    edges = sorted(tuple(sorted(edge)) for edge in graph.edges())
    return {
        "order": n,
        "subset_counter": subset,
        "direct_label_counter": direct,
        "rooted_tree_dp_counter": rooted_dp,
        "counters_agree": subset == direct == rooted_dp,
        "edges": [list(edge) for edge in edges],
        "graph6": nx.to_graph6_bytes(graph, header=False).decode("ascii").strip(),
        "prufer_sequence": (
            list(nx.to_prufer_sequence(graph)) if n >= 2 else []
        ),
    }


def path_graph(n: int) -> nx.Graph:
    return nx.path_graph(n)


def subdivided_star(k: int) -> nx.Graph:
    graph = nx.Graph()
    graph.add_node(0)
    for i in range(k):
        middle, leaf = 1 + 2 * i, 2 + 2 * i
        graph.add_edges_from(((0, middle), (middle, leaf)))
    return graph


def main() -> None:
    started = time.time()
    all_graphs: list[nx.Graph] = []
    jobs: list[tuple[int, tuple[tuple[int, int], ...]]] = []
    for n in range(1, MAX_ORDER + 1):
        representatives = [nx.empty_graph(1)] if n == 1 else list(
            nx.generators.nonisomorphic_trees(n)
        )
        all_graphs.extend(representatives)
        for graph in representatives:
            edges = tuple(sorted(tuple(sorted(e)) for e in graph.edges()))
            jobs.append((n, edges))

    print(f"Enumerated {len(all_graphs)} unlabeled trees, orders 1..{MAX_ORDER}.")
    print(f"Running independent ternary-label counter on {WORKERS} workers.")
    direct_results: list[int] = []
    with ProcessPoolExecutor(max_workers=WORKERS) as pool:
        for idx, (_, value) in enumerate(pool.map(_direct_worker, jobs, chunksize=1), 1):
            direct_results.append(value)
            if idx % 100 == 0 or idx == len(jobs):
                print(f"Direct counter completed {idx}/{len(jobs)} trees.")

    cursor = 0
    records_by_order: dict[int, list[dict]] = {}
    summary = []
    for n in range(1, MAX_ORDER + 1):
        representatives = [nx.empty_graph(1)] if n == 1 else list(
            nx.generators.nonisomorphic_trees(n)
        )
        records: list[dict] = []
        for graph in representatives:
            direct = direct_results[cursor]
            cursor += 1
            subset = count_subset(graph)
            rooted_dp = count_tree_dp(graph)
            record = graph_record(graph, subset, direct, rooted_dp)
            if not record["counters_agree"]:
                raise AssertionError({"tree": record, "order": n})
            records.append(record)

        maximum = max(record["subset_counter"] for record in records)
        extremizers = [record for record in records if record["subset_counter"] == maximum]
        path_count = count_subset(path_graph(n))
        path_direct = count_direct(path_graph(n))
        if path_count != path_direct:
            raise AssertionError(("path counters disagree", n, path_count, path_direct))

        tk_record = None
        if n >= 3 and n % 2 == 1:
            k = (n - 1) // 2
            tk = subdivided_star(k)
            tk_count = count_subset(tk)
            tk_direct = count_direct(tk)
            if tk_count != tk_direct:
                raise AssertionError(("T_k counters disagree", k, tk_count, tk_direct))
            matching = next(
                (record for record in records if nx.is_isomorphic(
                    tk, nx.from_graph6_bytes(record["graph6"].encode("ascii"))
                )),
                None,
            )
            if matching is None or matching["subset_counter"] != tk_count:
                raise AssertionError(("T_k missing from census", k, tk_count))
            tk_record = {
                "k": k,
                "count": tk_count,
                "formula": 3**k + 2**k - 1,
                "is_extremal": tk_count == maximum,
                "graph6": matching["graph6"],
                "edges": matching["edges"],
            }

        records_by_order[n] = records
        summary.append({
            "order": n,
            "unlabeled_tree_classes": len(records),
            "C_n": maximum,
            "path_count": path_count,
            "extremizer_class_count": len(extremizers),
            "extremizers": extremizers,
            "T_k": tk_record,
            "all_tree_classes": records,
        })
        print(
            f"n={n}: classes={len(records)} C(n)={maximum}; "
            f"P_n={path_count}; extremizers={len(extremizers)}"
        )

    if cursor != len(direct_results):
        raise AssertionError((cursor, len(direct_results)))

    payload = {
        "generated_on": date.today().isoformat(),
        "maximum_order": MAX_ORDER,
        "unlabeled_tree_classes_total": len(all_graphs),
        "counter_A": "subset/private-zero characterization, path_extremal_search.count_subset",
        "counter_B": "direct exhaustive enumeration of all 3^n vertex labelings, path_extremal_search.count_direct",
        "counter_C": "rooted-tree dynamic program, tree_dp_recurrence.count_tree_dp",
        "all_three_counters_agree": True,
        "python_version": sys.version,
        "networkx_version": nx.__version__,
        "elapsed_seconds": round(time.time() - started, 3),
        "worker_count": WORKERS,
        "orders": summary,
    }
    JSON_OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    log_lines = [
        "Minimal Roman dominating function census of unlabeled trees",
        f"Date: {payload['generated_on']}",
        f"Orders: 1..{MAX_ORDER}",
        f"Unlabeled tree classes checked: {len(all_graphs)}",
        f"Counter A: {payload['counter_A']}",
        f"Counter B: {payload['counter_B']}",
        f"Counter C: {payload['counter_C']}",
        "Agreement: every tree class and every path count was checked by all three counters.",
        f"Python: {sys.version.split()[0]}; NetworkX: {nx.__version__}",
        f"Elapsed seconds: {payload['elapsed_seconds']}",
        "",
        "order classes C(n) path extremizer_classes T_k_extremal",
    ]
    for row in summary:
        log_lines.append(
            f"{row['order']:>5} {row['unlabeled_tree_classes']:>7} "
            f"{row['C_n']:>5} {row['path_count']:>5} "
            f"{row['extremizer_class_count']:>18} "
            f"{row['T_k']['is_extremal'] if row['T_k'] else 'n/a'}"
        )
    log_lines.extend([
        "",
        f"Full edge lists, graph6 encodings, and Prüfer sequences: {JSON_OUT.name}",
    ])
    LOG_OUT.write_text("\n".join(log_lines) + "\n", encoding="utf-8")
    print(f"Saved {JSON_OUT}")
    print(f"Saved {LOG_OUT}")


if __name__ == "__main__":
    main()
