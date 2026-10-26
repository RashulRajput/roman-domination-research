"""Exact tree DP with shape memoization capped by rooted-subtree order."""

from __future__ import annotations

import networkx as nx


class BoundedMemoizedTreeCounter:
    """Memoize rooted message tables only for shapes up to cache_limit."""

    def __init__(self, cache_limit: int = 10) -> None:
        self.cache_limit = cache_limit
        self.shape_ids: dict[tuple[int, ...], int] = {(): 0}
        self.messages: list[tuple[dict, dict]] = [self._leaf_message()]

    @staticmethod
    def _leaf_message() -> tuple[dict, dict]:
        result = []
        for _p in (0, 1):
            table = {}
            for s in (0, 1):
                q = int(s == 1)
                table[(s, 0, q)] = 1
            result.append(table)
        return (result[0], result[1])

    @staticmethod
    def _combine(child_messages: list[tuple[dict, dict]]) -> tuple[dict, dict]:
        output = []
        for p in (0, 1):
            table = {}
            for s in (0, 1):
                states = {(0, False, False): 1}
                for child_message in child_messages:
                    child_table = child_message[s]
                    nxt = {}
                    for (c, needs, has), ways in states.items():
                        for (child_s, child_c, child_q), child_ways in child_table.items():
                            new_c = min(2, c + child_s)
                            new_needs = needs or bool(child_q)
                            new_has = has or (child_s == 0 and child_c == 0)
                            key = (new_c, new_needs, new_has)
                            nxt[key] = nxt.get(key, 0) + ways * child_ways
                    states = nxt
                for (c, needs, has), ways in states.items():
                    if needs and not (s == 0 and p == 0 and c == 1):
                        continue
                    q = int(s == 1 and not has)
                    key = (s, c, q)
                    table[key] = table.get(key, 0) + ways
            output.append(table)
        return (output[0], output[1])

    def count(self, tree: nx.Graph, root: int = 0) -> int:
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

        subtree_size: dict[int, int] = {}
        rooted_id: dict[int, int | None] = {}
        local_messages: dict[int, tuple[dict, dict]] = {}
        for v in reversed(order):
            children = [w for w in tree.neighbors(v) if parent.get(w) == v]
            size = 1 + sum(subtree_size[w] for w in children)
            subtree_size[v] = size
            child_messages = [local_messages[w] for w in children]
            if size <= self.cache_limit:
                child_ids = tuple(sorted(rooted_id[w] for w in children))
                sid = self.shape_ids.get(child_ids)
                if sid is None:
                    sid = len(self.messages)
                    self.shape_ids[child_ids] = sid
                    self.messages.append(self._combine([self.messages[cid] for cid in child_ids]))
                local_messages[v] = self.messages[sid]
                rooted_id[v] = sid
            else:
                local_messages[v] = self._combine(child_messages)
                rooted_id[v] = None

        root_table = local_messages[root][0]
        return sum(ways for (s, c, q), ways in root_table.items() if q == 0)
