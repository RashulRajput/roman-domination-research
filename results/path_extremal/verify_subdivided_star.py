"""Verify the exact count for subdivided stars using the research counters."""

from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

import networkx as nx

from path_extremal_search import count_direct, count_subset


HERE = Path(__file__).resolve().parent
OUT = HERE / "subdivided_star_results.json"


def subdivided_star(k: int) -> nx.Graph:
    """Return the tree with k arms, each consisting of two edges."""
    graph = nx.Graph()
    graph.add_node(0)
    for i in range(k):
        middle = 1 + i
        leaf = 1 + k + i
        graph.add_edges_from(((0, middle), (middle, leaf)))
    return graph


def main() -> None:
    rows = []
    for k in range(1, 9):
        graph = subdivided_star(k)
        formula = 3**k + 2**k - 1
        subset_count = count_subset(graph)
        path_count = count_subset(nx.path_graph(2 * k + 1))
        if subset_count != formula:
            raise AssertionError((k, subset_count, formula))

        direct_count = count_direct(graph) if k <= 5 else None
        if direct_count is not None and direct_count != formula:
            raise AssertionError((k, direct_count, formula))
        path_direct_count = (
            count_direct(nx.path_graph(2 * k + 1)) if k <= 5 else None
        )
        if path_direct_count is not None and path_direct_count != path_count:
            raise AssertionError((k, path_direct_count, path_count))

        rows.append(
            {
                "k": k,
                "order": 2 * k + 1,
                "formula": formula,
                "subset_counter": subset_count,
                "path_count_same_order": path_count,
                "family_minus_path": formula - path_count,
                "direct_label_counter": direct_count,
                "path_direct_label_counter": path_direct_count,
                "tree_and_chordal": nx.is_tree(graph),
            }
        )

    spider = subdivided_star(3)
    leaf_vertices = (4, 5, 6)
    one_leaf_counts = []
    for leaf in leaf_vertices:
        reduced = spider.copy()
        reduced.remove_node(leaf)
        one_leaf_counts.append(count_subset(reduced))
    two_leaf_counts = []
    for pair in combinations(leaf_vertices, 2):
        reduced = spider.copy()
        reduced.remove_nodes_from(pair)
        two_leaf_counts.append(count_subset(reduced))
    if one_leaf_counts != [17, 17, 17] or two_leaf_counts != [9, 9, 9]:
        raise AssertionError((one_leaf_counts, two_leaf_counts))

    tree_census = []
    first_tree_counterexample = None
    for n in range(1, 13):
        path_count = count_subset(nx.path_graph(n))
        maximum = -1
        extremizers = []
        violation_count = 0
        tree_count = 0
        trees = [nx.empty_graph(1)] if n == 1 else nx.generators.nonisomorphic_trees(n)
        for tree in trees:
            tree_count += 1
            count = count_subset(tree)
            if count > path_count:
                violation_count += 1
                if first_tree_counterexample is None:
                    first_tree_counterexample = {
                        "order": n,
                        "count": count,
                        "path_count": path_count,
                        "edges": [list(edge) for edge in tree.edges()],
                    }
            if count > maximum:
                maximum = count
                extremizers = [[list(edge) for edge in tree.edges()]]
            elif count == maximum:
                extremizers.append([list(edge) for edge in tree.edges()])
        tree_census.append(
            {
                "order": n,
                "unlabeled_trees": tree_count,
                "path_count": path_count,
                "maximum_tree_count": maximum,
                "number_of_maximizing_tree_classes": len(extremizers),
                "path_is_tree_maximal": maximum <= path_count,
                "violating_tree_classes": violation_count,
                "one_maximizer_edges": extremizers[0],
            }
        )
    if first_tree_counterexample is None or first_tree_counterexample["order"] != 11:
        raise AssertionError(first_tree_counterexample)

    result = {
        "statement": "m(T_k) = 3^k + 2^k - 1 for the k-arm length-2 spider",
        "verification": (
            "subset counter k=1..8; independent direct-label counters for T_k and "
            "P_(2k+1) through k=5; exhaustive unlabeled-tree census through order 12"
        ),
        "rows": rows,
        "unlabeled_tree_census_through_12": tree_census,
        "first_tree_counterexample": first_tree_counterexample,
        "T3_deletion_checks": {
            "m_T3": rows[2]["subset_counter"],
            "counts_after_deleting_each_leaf": one_leaf_counts,
            "counts_after_deleting_each_pair_of_leaves": two_leaf_counts,
        },
    }
    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
    print(f"Saved exact data: {OUT}")


if __name__ == "__main__":
    main()
