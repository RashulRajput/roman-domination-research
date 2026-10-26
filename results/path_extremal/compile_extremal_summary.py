#!/usr/bin/env python3
"""Assemble maxima and all extremizer encodings from the census artifacts."""

from __future__ import annotations

import json
from pathlib import Path

import networkx as nx

from verify_extended_extremizers import load_legacy_summary


ROOT = Path(__file__).resolve().parent
TREE_CLASS_COUNTS = {
    1: 1, 2: 1, 3: 1, 4: 2, 5: 3, 6: 6, 7: 11, 8: 23, 9: 47, 10: 106,
    11: 235, 12: 551, 13: 1301, 14: 3159, 15: 7741, 16: 19320,
    17: 48629, 18: 123867, 19: 317955, 20: 823065,
}


def tree_edges(code: str) -> list[list[int]]:
    graph = nx.from_graph6_bytes(code.encode("ascii"))
    return [list(e) for e in sorted(tuple(sorted(e)) for e in graph.edges())]


def header_for(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    marker = '  "trees": ['
    prefix = text[: text.index(marker)].rstrip()
    if prefix.endswith(","):
        prefix = prefix[:-1]
    return json.loads(prefix + "\n}")["summaries"]


def main() -> None:
    orders: dict[int, dict] = {}
    old = json.loads((ROOT / "tree_census_through_12.json").read_text(encoding="utf-8"))
    for row in old["orders"]:
        codes = [tree["graph6"] for tree in row["extremizers"]]
        orders[row["order"]] = {
            "n": row["order"],
            "classes": row["unlabeled_tree_classes"],
            "C_n": row["C_n"],
            "path_count": row["path_count"],
            "extremizers_graph6": codes,
        }
    for file_name in (
        "tree_census_extension_through_16.json",
        "tree_census_extension_through_18.json",
    ):
        for row in header_for(ROOT / file_name):
            n = row["n"]
            orders[n] = {
                "n": n,
                "classes": TREE_CLASS_COUNTS[n],
                "C_n": row["C_n"],
                "path_count": row["path_count"],
                "extremizers_graph6": row["extremizer_graph6"],
            }
    for n in (19, 20):
        summary_path = ROOT / f"tree_census_n{n}_summary.json"
        if summary_path.exists():
            row = json.loads(summary_path.read_text(encoding="utf-8"))
            orders[n] = {
                "n": n,
                "classes": row["classes_emitted"],
                "C_n": row["C_n"],
                "path_count": row["path_count"],
                "extremizers_graph6": row["extremizers_graph6"],
            }
    sorted_orders = []
    for n in sorted(orders):
        row = orders[n]
        row["expected_unlabeled_tree_classes"] = TREE_CLASS_COUNTS[n]
        row["class_count_agrees"] = row["classes"] == TREE_CLASS_COUNTS[n]
        row["extremizers"] = [
            {"graph6": code, "edges": tree_edges(code)}
            for code in row.pop("extremizers_graph6")
        ]
        sorted_orders.append(row)
    complete_through = max(row["n"] for row in sorted_orders)
    result = {
        "complete_census_through_order": complete_through,
        "orders": sorted_orders,
        "note": "Finite exhaustive census only; no extrapolation beyond complete_census_through_order.",
    }
    out = ROOT / f"extremal_summary_through_{complete_through}.json"
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Saved {out}")
    for row in sorted_orders:
        print(
            f"n={row['n']} classes={row['classes']} C(n)={row['C_n']} "
            f"path={row['path_count']} extremizers={len(row['extremizers'])} "
            f"graph6={','.join(x['graph6'] for x in row['extremizers'])}"
        )


if __name__ == "__main__":
    main()
