"""Rooted-tree DP for counting minimal Roman dominating functions.

The DP counts subsets S=V_2. Such an S determines the unique RDF labeling
V_0=N(S)\\S and V_1=V\\N[S]. It is minimal exactly when every s in S has
an external private neighbor, i.e. a neighbor u with N(u) intersect S={s}.
"""

from __future__ import annotations

import json
from pathlib import Path

import networkx as nx

HERE = Path(__file__).resolve().parent
INPUT = HERE / "tree_census_through_12.json"
OUTPUT = HERE / "tree_dp_verification.log"


def cap2(value: int) -> int:
    return min(2, value)


def count_tree_dp(tree: nx.Graph, root: int = 0) -> int:
    """Count valid V2-sets using parent-selection and private-witness states.

    For v and p in {0,1}, a table entry D_v^p(s,c,q) counts assignments in
    the rooted subtree at v where p records whether its parent is selected,
    s records whether v is selected, c=min(2,# selected children), and q=1
    means v is selected but has no private zero witness among its children.
    All selected descendants have already had their witness requirement met.
    """
    if tree.number_of_nodes() == 0:
        return 1

    parent = {root: None}
    order = [root]
    for v in order:
        for w in tree.neighbors(v):
            if w != parent[v]:
                parent[w] = v
                order.append(w)
    if len(order) != tree.number_of_nodes():
        raise ValueError("input must be a tree")

    # dp[v][p] maps (s, c, q) to its number of subtree assignments.
    dp: dict[int, dict[int, dict[tuple[int, int, int], int]]] = {}
    for v in reversed(order):
        children = [w for w in tree.neighbors(v) if parent.get(w) == v]
        dp[v] = {}
        for p in (0, 1):
            table: dict[tuple[int, int, int], int] = {}
            for s in (0, 1):
                # Aggregate all child combinations by:
                # selected-child count (capped at 2), whether any selected
                # child needs v as its private witness, and whether a zero
                # child already witnesses v (when v is selected).
                states = {(0, False, False): 1}
                for child in children:
                    nxt: dict[tuple[int, bool, bool], int] = {}
                    for (c_acc, needs_v, has_witness), ways in states.items():
                        for (s_child, c_child, q_child), child_ways in dp[child][s].items():
                            key = (
                                cap2(c_acc + s_child),
                                needs_v or bool(q_child),
                                has_witness or (s == 1 and s_child == 0 and c_child == 0),
                            )
                            nxt[key] = nxt.get(key, 0) + ways * child_ways
                    states = nxt

                for (c, needs_v, has_witness), ways in states.items():
                    # A child with q=1 can only be rescued by v when v is
                    # zero and has that child as its unique selected neighbor.
                    if needs_v and not (s == 0 and p == 0 and c == 1):
                        continue
                    q = int(s == 1 and not has_witness)
                    key = (s, c, q)
                    table[key] = table.get(key, 0) + ways
            dp[v][p] = table

    # The root has no parent, so a selected root with q=1 has no witness.
    return sum(
        ways
        for (s, c, q), ways in dp[root][0].items()
        if q == 0
    )


def main() -> None:
    payload = json.loads(INPUT.read_text(encoding="utf-8"))
    checked = 0
    lines = [
        "Rooted-tree dynamic-program verification",
        f"Input census: {INPUT.name}",
        "State recurrence: parent-selected bit; root selected bit; capped selected-child count; root-witness-needed bit.",
    ]
    for row in payload["orders"]:
        n = row["order"]
        for record in row["all_tree_classes"]:
            graph = nx.from_graph6_bytes(record["graph6"].encode("ascii"))
            value = count_tree_dp(graph)
            if value != record["subset_counter"] or value != record["direct_label_counter"]:
                raise AssertionError({
                    "order": n,
                    "graph6": record["graph6"],
                    "tree_dp": value,
                    "subset": record["subset_counter"],
                    "direct": record["direct_label_counter"],
                })
            record["rooted_tree_dp_counter"] = value
            checked += 1
        row["rooted_tree_dp_verified_all_classes"] = True
    payload["counter_C"] = "rooted-tree DP derived in tree_dp_recurrence.py"
    payload["all_three_counters_agree"] = True
    INPUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    lines.extend([
        f"Tree classes checked: {checked}",
        "Agreement: rooted DP = subset/private-zero counter = direct ternary-label counter for every class.",
        "",
        "DP recurrence proof is recorded in EXTREMAL_TREES.md.",
    ])
    OUTPUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("Verified all", checked, "tree classes with the rooted DP.")
    print("Updated", INPUT)
    print("Saved", OUTPUT)


if __name__ == "__main__":
    main()
