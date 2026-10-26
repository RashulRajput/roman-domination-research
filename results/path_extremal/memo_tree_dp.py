"""Memoized rooted-state DP keyed by canonical rooted-tree shape."""

from __future__ import annotations

import networkx as nx


class MemoizedTreeCounter:
    def __init__(self) -> None:
        self.shape_ids: dict[tuple[int, ...], int] = {(): 0}
        self.shape_children: list[tuple[int, ...]] = [()]
        self.messages: list[tuple[dict, dict] | None] = [None]

    def _intern(self, children: tuple[int, ...]) -> int:
        sid = self.shape_ids.get(children)
        if sid is None:
            sid = len(self.shape_children)
            self.shape_ids[children] = sid
            self.shape_children.append(children)
            self.messages.append(None)
        return sid

    def _message(self, sid: int) -> tuple[dict, dict]:
        cached = self.messages[sid]
        if cached is not None:
            return cached
        child_ids = self.shape_children[sid]
        child_messages = [self._message(cid) for cid in child_ids]
        output = []
        for p in (0, 1):
            table = {}
            for s in (0, 1):
                # c, needs_parent_witness, has_child_witness
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
        result = (output[0], output[1])
        self.messages[sid] = result
        return result

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
        rooted_shape: dict[int, int] = {}
        for v in reversed(order):
            children = tuple(
                sorted(
                    rooted_shape[w]
                    for w in tree.neighbors(v)
                    if parent.get(w) == v
                )
            )
            rooted_shape[v] = self._intern(children)
        table = self._message(rooted_shape[root])[0]
        return sum(ways for (s, c, q), ways in table.items() if q == 0)
