#!/usr/bin/env python3
"""Check whether the incomplete order-20 prefix already refutes path extremality."""

import json
from pathlib import Path

import networkx as nx

from verify_extended_extremizers import direct_subset_count
from tree_dp_recurrence import count_tree_dp


ROOT = Path(__file__).resolve().parent
partial = json.loads((ROOT / "tree_census_n20_partial_oldmemo.jsonl.summary.json").read_text(encoding="utf-8"))
code = partial["prefix_maximizer_graph6"][0]
candidate = nx.from_graph6_bytes(code.encode("ascii"))
path = nx.path_graph(20)
result = {
    "n": 20,
    "exhaustive_order20_census": False,
    "prefix_records": partial["records_in_canonical_generator_prefix"],
    "candidate_graph6": code,
    "candidate_edges": [list(e) for e in sorted(tuple(sorted(e)) for e in candidate.edges())],
    "candidate_count_rooted_dp": count_tree_dp(candidate),
    "candidate_count_independent_subset_counter": direct_subset_count(candidate),
    "path_count_rooted_dp": count_tree_dp(path),
    "path_count_independent_subset_counter": direct_subset_count(path),
}
result["strict_path_counterexample"] = (
    result["candidate_count_independent_subset_counter"] > result["path_count_independent_subset_counter"]
)
(ROOT / "partial_n20_path_counterexample_check.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
(ROOT / "partial_n20_path_counterexample_check.log").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))
