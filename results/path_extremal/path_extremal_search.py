"""Exact small-order pressure test for a path-extremality conjecture.

Candidate:
    For every connected chordal graph G of order n, m(G) <= m(P_n).

The census uses the NetworkX Graph Atlas (all unlabeled simple graphs through
order 7), an independent induced-cycle chordality test, direct 3^n RDF
enumeration, and subset enumeration via private zero-neighbors. It also checks
an exact simplicial-vertex deletion identity and the proposed local increment
lemma needed for induction.
"""

from __future__ import annotations

import itertools
import json
import platform
import sys
import time
from pathlib import Path

import networkx as nx


HERE = Path(__file__).resolve().parent
OUT = HERE / "path_extremal_results.json"
ATLAS_COUNTS = {0: 1, 1: 1, 2: 2, 3: 4, 4: 11, 5: 34, 6: 156, 7: 1044}


def adjacency_masks(graph: nx.Graph) -> tuple[list[int], list[object]]:
    nodes = list(graph.nodes())
    index = {v: i for i, v in enumerate(nodes)}
    adj = [0] * len(nodes)
    for v in nodes:
        i = index[v]
        for u in graph.neighbors(v):
            adj[i] |= 1 << index[u]
    return adj, nodes


def rdf_valid(labels: tuple[int, ...] | list[int], adj: list[int]) -> bool:
    for v, value in enumerate(labels):
        if value == 0:
            nbrs = adj[v]
            has_two = False
            while nbrs:
                bit = nbrs & -nbrs
                nbrs ^= bit
                if labels[bit.bit_length() - 1] == 2:
                    has_two = True
                    break
            if not has_two:
                return False
    return True


def count_direct(graph: nx.Graph) -> int:
    """Method A: enumerate all 3^n functions and test coordinate decreases."""
    adj, _ = adjacency_masks(graph)
    n = len(adj)
    total = 0
    for labels in itertools.product((0, 1, 2), repeat=n):
        if not rdf_valid(labels, adj):
            continue
        minimal = True
        for v, value in enumerate(labels):
            if value == 0:
                continue
            lowered = list(labels)
            lowered[v] -= 1
            if rdf_valid(lowered, adj):
                minimal = False
                break
        total += minimal
    return total


def subset_is_valid(mask: int, adj: list[int]) -> bool:
    """Method B predicate: every selected vertex has an external private zero."""
    selected = mask
    while selected:
        bit = selected & -selected
        selected ^= bit
        v = bit.bit_length() - 1
        candidates = adj[v] & ~mask
        has_private = False
        while candidates:
            u_bit = candidates & -candidates
            candidates ^= u_bit
            u = u_bit.bit_length() - 1
            if adj[u] & mask == bit:
                has_private = True
                break
        if not has_private:
            return False
    return True


def count_subset(graph: nx.Graph) -> int:
    adj, _ = adjacency_masks(graph)
    return sum(subset_is_valid(mask, adj) for mask in range(1 << len(adj)))


def induced_cycle_exists(adj: list[int]) -> bool:
    """Independent chordality test: search for an induced cycle of length >= 4."""
    n = len(adj)
    for size in range(4, n + 1):
        for vertices in itertools.combinations(range(n), size):
            vertex_mask = sum(1 << v for v in vertices)
            if any((adj[v] & vertex_mask).bit_count() != 2 for v in vertices):
                continue
            reached = 1 << vertices[0]
            frontier = reached
            while frontier:
                new_frontier = 0
                bits = frontier
                while bits:
                    bit = bits & -bits
                    bits ^= bit
                    v = bit.bit_length() - 1
                    new_frontier |= adj[v] & vertex_mask
                new_frontier &= ~reached
                reached |= new_frontier
                frontier = new_frontier
            if reached == vertex_mask:
                return True
    return False


def is_simplicial(v: int, adj: list[int]) -> bool:
    neighbors = adj[v]
    bits = neighbors
    while bits:
        bit = bits & -bits
        bits ^= bit
        u = bit.bit_length() - 1
        if (adj[u] & neighbors) != (neighbors ^ bit):
            return False
    return True


def private_witnesses_avoiding(
    mask: int, adj: list[int], forbidden_vertices: int
) -> bool:
    """Every selected vertex has a private zero outside a forbidden set."""
    selected = mask
    while selected:
        bit = selected & -selected
        selected ^= bit
        v = bit.bit_length() - 1
        candidates = adj[v] & ~mask & ~forbidden_vertices
        found = False
        while candidates:
            u_bit = candidates & -candidates
            candidates ^= u_bit
            u = u_bit.bit_length() - 1
            if adj[u] & mask == bit:
                found = True
                break
        if not found:
            return False
    return True


def induced_relabel(adj: list[int], keep: list[int]) -> list[int]:
    new_index = {old: new for new, old in enumerate(keep)}
    new_adj = [0] * len(keep)
    for old_v in keep:
        new_v = new_index[old_v]
        old_neighbors = adj[old_v]
        for old_u in keep:
            if old_neighbors & (1 << old_u):
                new_adj[new_v] |= 1 << new_index[old_u]
    return new_adj


def deletion_terms(adj: list[int], v: int) -> tuple[int, int]:
    """Return D_v and R_v in the simplicial deletion identity.

    D_v counts valid subsets S of G-v with S disjoint from N(v), for which
    some neighbor u of v has no neighbor in S. Such an S permits v to be 2.

    R_v counts subsets with N(v) intersect S = {s}, where s is the only
    selected vertex lacking a private zero-neighbor in G-v. The deleted v,
    assigned 0, rescues s.
    """
    keep = [u for u in range(len(adj)) if u != v]
    old_to_new = {old: new for new, old in enumerate(keep)}
    h_adj = induced_relabel(adj, keep)
    v_neighbors_old = [u for u in range(len(adj)) if adj[v] & (1 << u)]
    v_neighbors = [old_to_new[u] for u in v_neighbors_old]
    v_neighbor_mask = sum(1 << u for u in v_neighbors)
    n_h = len(h_adj)
    d_term = 0
    r_term = 0

    for mask in range(1 << n_h):
        if subset_is_valid(mask, h_adj):
            # Adding v to S can destroy private-zero witnesses of S. Any
            # witness adjacent to v would gain a second selected neighbor.
            if (
                mask & v_neighbor_mask == 0
                and private_witnesses_avoiding(mask, h_adj, v_neighbor_mask)
                and any(h_adj[u] & mask == 0 for u in v_neighbors)
            ):
                d_term += 1
            continue

        intersection = [u for u in v_neighbors if mask & (1 << u)]
        if len(intersection) != 1:
            continue
        rescued = intersection[0]
        all_others_valid = True
        selected = mask
        while selected:
            bit = selected & -selected
            selected ^= bit
            u = bit.bit_length() - 1
            if u == rescued:
                continue
            candidates = h_adj[u] & ~mask
            if not any(
                h_adj[w] & mask == bit
                for w in range(n_h)
                if candidates & (1 << w)
            ):
                all_others_valid = False
                break
        rescued_has_witness = False
        candidates = h_adj[rescued] & ~mask
        while candidates:
            bit = candidates & -candidates
            candidates ^= bit
            w = bit.bit_length() - 1
            if h_adj[w] & mask == 1 << rescued:
                rescued_has_witness = True
                break
        if all_others_valid and not rescued_has_witness:
            r_term += 1

    return d_term, r_term


def path_graph_count(n: int) -> int:
    return count_subset(nx.path_graph(n))


def run() -> dict:
    started = time.perf_counter()
    atlas = nx.graph_atlas_g()
    order_histogram: dict[int, int] = {}
    for graph in atlas:
        order_histogram[graph.number_of_nodes()] = (
            order_histogram.get(graph.number_of_nodes(), 0) + 1
        )
    if order_histogram != ATLAS_COUNTS:
        raise RuntimeError(f"Unexpected graph-atlas order counts: {order_histogram}")

    path_counts = {n: path_graph_count(n) for n in range(1, 8)}
    result = {
        "candidate": "For every connected chordal G of order n, m(G) <= m(P_n).",
        "local_lemma": (
            "For every connected chordal G of order n>=2, some simplicial v "
            "satisfies m(G)-m(G-v) <= m(P_n)-m(P_{n-1})."
        ),
        "software": {
            "python": sys.version.split()[0],
            "networkx": nx.__version__,
            "platform": platform.platform(),
            "atlas_graphs": len(atlas),
            "atlas_order_histogram": {str(k): v for k, v in order_histogram.items()},
        },
        "path_counts": {str(k): v for k, v in path_counts.items()},
        "orders": {},
        "engine_mismatches": [],
        "chordality_mismatches": [],
        "deletion_identity_mismatches": [],
        "path_extremality_violations": [],
        "local_lemma_violations": [],
        "local_lemma_all_simplicial_violations": [],
        "pair_lemma_violations": [],
        "pair_lemma_no_eligible_pair": [],
        "pair_lemma_all_pairs_violations": [],
        "nonchordal_boundary_examples": [],
    }

    # Compare with inherited implementations only through order 5; the two
    # independent engines below are used throughout the atlas.
    sys.path.insert(0, str(HERE.parents[1]))
    from count_minimal_rdf import (
        count_minimal_rdfs_brute as old_direct,
        count_minimal_rdfs_subset_v2 as old_subset,
    )

    connected_chordal = {n: [] for n in range(1, 8)}
    connected_all = {n: [] for n in range(1, 8)}
    for atlas_id, graph in enumerate(atlas):
        n = graph.number_of_nodes()
        if n == 0:
            if count_direct(graph) != 1 or count_subset(graph) != 1:
                result["engine_mismatches"].append(
                    {"atlas_id": atlas_id, "n": 0, "expected": 1}
                )
            continue
        adj, nodes = adjacency_masks(graph)
        custom_chordal = not induced_cycle_exists(adj)
        nx_chordal = nx.is_chordal(graph)
        if custom_chordal != nx_chordal:
            result["chordality_mismatches"].append(
                {"atlas_id": atlas_id, "n": n, "edges": list(graph.edges())}
            )
        direct = count_direct(graph)
        subset = count_subset(graph)
        if direct != subset:
            result["engine_mismatches"].append(
                {
                    "atlas_id": atlas_id,
                    "n": n,
                    "direct": direct,
                    "subset": subset,
                    "edges": list(graph.edges()),
                }
            )
        if n <= 5:
            old_a = old_direct(graph)
            old_b = old_subset(graph)
            if (direct, subset) != (old_a, old_b):
                result["engine_mismatches"].append(
                    {
                        "atlas_id": atlas_id,
                        "n": n,
                        "new": [direct, subset],
                        "inherited": [old_a, old_b],
                        "edges": list(graph.edges()),
                    }
                )
        if not nx.is_connected(graph):
            continue
        connected_all[n].append((atlas_id, graph, subset))
        if custom_chordal:
            connected_chordal[n].append((atlas_id, graph, subset))

    for n in range(1, 8):
        candidates = connected_chordal[n]
        max_count = max(count for _, _, count in candidates)
        extremizers = [
            {"atlas_id": atlas_id, "edges": list(graph.edges()), "count": count}
            for atlas_id, graph, count in candidates
            if count == max_count
        ]
        path_count = path_counts[n]
        if max_count > path_count:
            for atlas_id, graph, count in candidates:
                if count > path_count:
                    result["path_extremality_violations"].append(
                        {
                            "atlas_id": atlas_id,
                            "n": n,
                            "count": count,
                            "path_count": path_count,
                            "edges": list(graph.edges()),
                        }
                    )

        path_increment = path_counts[n] - path_counts[n - 1] if n >= 2 else None
        path_pair_increment = path_counts[n] - path_counts[n - 2] if n >= 3 else None
        per_vertex = []
        per_pair = []
        if n >= 2:
            for atlas_id, graph, count in candidates:
                adj, nodes = adjacency_masks(graph)
                for v in range(n):
                    if not is_simplicial(v, adj):
                        continue
                    keep = [u for u in range(n) if u != v]
                    h = graph.subgraph([nodes[u] for u in keep]).copy()
                    h_count = count_subset(h)
                    d_term, r_term = deletion_terms(adj, v)
                    if d_term + r_term != count - h_count:
                        result["deletion_identity_mismatches"].append(
                            {
                                "atlas_id": atlas_id,
                                "n": n,
                                "vertex": nodes[v],
                                "m_G": count,
                                "m_G_minus_v": h_count,
                                "D": d_term,
                                "R": r_term,
                                "edges": list(graph.edges()),
                            }
                        )
                    per_vertex.append(
                        {
                            "atlas_id": atlas_id,
                            "vertex": nodes[v],
                            "delta": count - h_count,
                            "path_increment": path_increment,
                            "edge_count": graph.number_of_edges(),
                            "edges": list(graph.edges()),
                        }
                    )

                if n >= 3:
                    simplicial = [x for x in range(n) if is_simplicial(x, adj)]
                    for u, v in itertools.combinations(simplicial, 2):
                        if adj[u] & (1 << v):
                            continue
                        keep = [x for x in range(n) if x not in (u, v)]
                        h = graph.subgraph([nodes[x] for x in keep]).copy()
                        per_pair.append(
                            {
                                "atlas_id": atlas_id,
                                "vertices": [nodes[u], nodes[v]],
                                "delta": count - count_subset(h),
                                "path_pair_increment": path_pair_increment,
                                "remaining_connected": (
                                    h.number_of_nodes() > 0 and nx.is_connected(h)
                                ),
                                "edges": list(graph.edges()),
                            }
                        )

            best_vertex_delta = min(entry["delta"] for entry in per_vertex)
            for entry in per_vertex:
                if entry["delta"] > path_increment:
                    result["local_lemma_all_simplicial_violations"].append(
                        {"n": n, **entry}
                    )
            best_per_graph: dict[int, int] = {}
            for entry in per_vertex:
                best_per_graph[entry["atlas_id"]] = min(
                    entry["delta"],
                    best_per_graph.get(entry["atlas_id"], entry["delta"]),
                )
            for atlas_id, delta in best_per_graph.items():
                if delta > path_increment:
                    found = next(g for i, g, _ in candidates if i == atlas_id)
                    result["local_lemma_violations"].append(
                        {
                            "atlas_id": atlas_id,
                            "n": n,
                            "best_simplicial_delta": delta,
                            "path_increment": path_increment,
                            "edges": list(found.edges()),
                        }
                    )

            if n >= 3:
                by_graph_pairs: dict[int, list[dict]] = {}
                for entry in per_pair:
                    by_graph_pairs.setdefault(entry["atlas_id"], []).append(entry)
                    if entry["delta"] > path_pair_increment:
                        result["pair_lemma_all_pairs_violations"].append(
                            {"n": n, **entry}
                        )
                for atlas_id, graph, _ in candidates:
                    if graph.number_of_edges() == n * (n - 1) // 2:
                        continue  # the pair statement is scoped to noncomplete graphs
                    entries = by_graph_pairs.get(atlas_id, [])
                    eligible = [
                        entry for entry in entries if entry["remaining_connected"]
                    ]
                    if not eligible:
                        adj, nodes = adjacency_masks(graph)
                        simplicial = [x for x in range(n) if is_simplicial(x, adj)]
                        pairs = [
                            [nodes[u], nodes[v]]
                            for u, v in itertools.combinations(simplicial, 2)
                            if not adj[u] & (1 << v)
                        ]
                        result["pair_lemma_no_eligible_pair"].append(
                            {
                                "atlas_id": atlas_id,
                                "n": n,
                                "reason": (
                                    "no nonadjacent simplicial pair"
                                    if not pairs
                                    else "every such pair disconnects G-{u,v}"
                                ),
                                "simplicial_pairs": pairs,
                                "edges": list(graph.edges()),
                            }
                        )
                    elif min(entry["delta"] for entry in eligible) > path_pair_increment:
                        result["pair_lemma_violations"].append(
                            {
                                "atlas_id": atlas_id,
                                "n": n,
                                "best_pair_delta": min(
                                    entry["delta"] for entry in eligible
                                ),
                                "path_pair_increment": path_pair_increment,
                                "eligible_pairs": eligible,
                                "edges": list(graph.edges()),
                            }
                        )

        result["orders"][str(n)] = {
            "connected_chordal_graphs": len(candidates),
            "connected_graphs": len(connected_all[n]),
            "path_count": path_count,
            "maximum_count": max_count,
            "path_is_maximal": max_count <= path_count,
            "number_of_extremizers": len(extremizers),
            "extremizers": extremizers,
            "path_increment": path_increment,
            "path_pair_increment": path_pair_increment,
            "minimum_simplicial_deletion_increment": (
                min(entry["delta"] for entry in per_vertex) if per_vertex else None
            ),
            "maximum_simplicial_deletion_increment": (
                max(entry["delta"] for entry in per_vertex) if per_vertex else None
            ),
        }

    # Smallest boundary example showing why chordality matters.
    for n in range(1, 8):
        for atlas_id, graph, count in connected_all[n]:
            if not nx.is_chordal(graph) and count > path_counts[n]:
                result["nonchordal_boundary_examples"].append(
                    {
                        "atlas_id": atlas_id,
                        "n": n,
                        "count": count,
                        "path_count": path_counts[n],
                        "edges": list(graph.edges()),
                    }
                )
        if result["nonchordal_boundary_examples"]:
            break

    result["elapsed_seconds"] = round(time.perf_counter() - started, 3)
    result["checks"] = {
        "all_atlas_graphs_direct_equals_subset": not result["engine_mismatches"],
        "independent_chordality_matches_networkx": not result["chordality_mismatches"],
        "simplicial_deletion_identity_holds": not result[
            "deletion_identity_mismatches"
        ],
        "path_extremal_candidate_survives_atlas": not result[
            "path_extremality_violations"
        ],
        "existential_local_increment_lemma_survives_atlas": not result[
            "local_lemma_violations"
        ],
        "universal_local_increment_lemma_survives_atlas": not result[
            "local_lemma_all_simplicial_violations"
        ],
        "existential_connected_pair_increment_lemma_survives_atlas": not result[
            "pair_lemma_violations"
        ],
        "every_connected_chordal_graph_has_an_eligible_pair": not result[
            "pair_lemma_no_eligible_pair"
        ],
        "universal_pair_increment_lemma_survives_atlas": not result[
            "pair_lemma_all_pairs_violations"
        ],
    }

    OUT.write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    report = run()
    summary = {
        "software": report["software"],
        "path_counts": report["path_counts"],
        "orders": {
            n: {
                key: value
                for key, value in row.items()
                if key != "extremizers"
            }
            for n, row in report["orders"].items()
        },
        "checks": report["checks"],
        "first_local_lemma_failure": (
            report["local_lemma_violations"][0]
            if report["local_lemma_violations"]
            else None
        ),
        "first_pair_lemma_failure": (
            report["pair_lemma_violations"][0]
            if report["pair_lemma_violations"]
            else None
        ),
        "first_nonchordal_boundary_example": (
            report["nonchordal_boundary_examples"][0]
            if report["nonchordal_boundary_examples"]
            else None
        ),
        "elapsed_seconds": report["elapsed_seconds"],
    }
    print(json.dumps(summary, indent=2))
    print(f"\nSaved exact data: {OUT}")
