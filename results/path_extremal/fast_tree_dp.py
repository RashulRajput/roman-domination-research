"""Array-based implementation of the rooted private-witness recurrence."""

from __future__ import annotations

import networkx as nx


def count_tree_dp_fast(tree: nx.Graph, root: int = 0) -> int:
    """Count minimal RDFs using the exact same states with fixed-size arrays.

    This avoids dictionaries and Cartesian products in the original audited
    implementation. It is intended for the larger canonical census.
    """
    if tree.number_of_nodes() == 0:
        return 1
    adjacency = {v: tuple(tree.neighbors(v)) for v in tree}
    parent = {root: None}
    order = [root]
    for v in order:
        for w in adjacency[v]:
            if w != parent[v]:
                parent[w] = v
                order.append(w)
    if len(order) != tree.number_of_nodes():
        raise ValueError("input must be a tree")

    # State code for a child-root entry (selected, capped selected children,
    # unresolved-witness bit) is ((s*3+c)*2+q); twelve slots include the
    # unreachable q=1,s=0 combinations for simple indexing.
    dp: dict[int, tuple[list[int], list[int]]] = {}
    for v in reversed(order):
        children = [w for w in adjacency[v] if parent.get(w) == v]
        tables: list[list[int]] = []
        for p in (0, 1):
            result = [0] * 12
            for s in (0, 1):
                # Aggregator index ((c*2+needs_parent)*(2)+has_witness).
                states = [0] * 12
                states[0] = 1
                for child in children:
                    nxt = [0] * 12
                    child_table = dp[child][s]
                    for c in range(3):
                        for needs in (0, 1):
                            for has in (0, 1):
                                ways = states[(c * 2 + needs) * 2 + has]
                                if not ways:
                                    continue
                                for child_s in (0, 1):
                                    for child_c in range(3):
                                        for child_q in (0, 1):
                                            child_ways = child_table[(child_s * 3 + child_c) * 2 + child_q]
                                            if not child_ways:
                                                continue
                                            new_c = min(2, c + child_s)
                                            new_needs = int(bool(needs or child_q))
                                            child_witness = int(child_s == 0 and child_c == 0)
                                            new_has = int(bool(has or child_witness))
                                            index = (new_c * 2 + new_needs) * 2 + new_has
                                            nxt[index] += ways * child_ways
                    states = nxt
                for c in range(3):
                    for needs in (0, 1):
                        for has in (0, 1):
                            ways = states[(c * 2 + needs) * 2 + has]
                            if not ways:
                                continue
                            if needs and not (s == 0 and p == 0 and c == 1):
                                continue
                            q = int(s == 1 and has == 0)
                            result[(s * 3 + c) * 2 + q] += ways
            tables.append(result)
        dp[v] = (tables[0], tables[1])
    root_table = dp[root][0]
    return sum(root_table[(s * 3 + c) * 2] for s in (0, 1) for c in range(3))
