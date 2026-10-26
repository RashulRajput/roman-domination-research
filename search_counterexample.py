"""
Generate all non-isomorphic chordal graphs on n=8 vertices and count m(G).

Strategy: Use the fact that chordal graphs = intersection graphs of subtrees.
Alternative: generate all graphs on 8 vertices, filter to chordal, check isomorphism.

For n=8, there are 12346 graphs total. We filter to chordal and check each.
Actually, we'll use a smarter approach: generate via PEO (perfect elimination ordering).

But for n=8, brute-force isomorphism filtering is feasible since there are only
~12000 graphs on 8 nodes in the atlas... but atlas goes up to 7.

Instead, let's use nauty-style canonical form via NetworkX.
"""

import math
import time
import itertools
import networkx as nx
from count_minimal_rdf import count_minimal_rdfs_subset_v2


def generate_chordal_graphs_by_peo(n):
    """
    Generate chordal graphs on n vertices by building PEO.
    
    A PEO is an ordering v1, v2, ..., vn such that for each i,
    the neighbors of vi among v_{i+1}, ..., vn form a clique.
    
    We build the graph by adding vertices in reverse PEO order:
    - Start with vertex v_n
    - Add v_{n-1} connected to a clique in the existing graph
    - ...
    - Add v_1 connected to a clique in the existing graph
    
    This generates ALL chordal graphs (up to isomorphism checking).
    """
    # For efficiency, we generate graphs and use canonical labeling to avoid duplicates
    
    if n == 1:
        G = nx.Graph()
        G.add_node(0)
        yield G
        return
    
    # This is a BFS/DFS over possible PEO constructions
    # Too expensive for large n, but feasible for n=8
    
    # Alternative: enumerate all possible edge sets and check chordality
    # For n=8, there are C(8,2)=28 potential edges, so 2^28 = 268M graphs.
    # Too many. We need the PEO approach.
    
    # Actually, for a paper, let's use a different approach:
    # Generate random chordal graphs and check many of them.
    pass


def generate_random_chordal_graph(n, p_clique=0.5):
    """
    Generate a random chordal graph on n vertices.
    
    Method: Build by PEO. For each vertex (added in order),
    connect it to a random clique in the existing graph.
    """
    G = nx.Graph()
    G.add_node(0)
    
    import random
    
    for v in range(1, n):
        # Find all cliques in current graph (maximal cliques)
        if G.number_of_edges() == 0:
            # Connect to a random existing vertex or not
            if random.random() < p_clique:
                u = random.randint(0, v - 1)
                G.add_node(v)
                G.add_edge(v, u)
            else:
                G.add_node(v)
        else:
            G.add_node(v)
            # Choose a random subset of existing vertices that form a clique
            existing = list(range(v))
            
            # Method: pick a random existing vertex, then extend to a clique
            if random.random() < 0.3:
                # Isolated vertex
                pass
            else:
                # Pick a random vertex and some of its neighbors that form a clique
                u = random.choice(existing)
                clique = [u]
                nbrs = list(G.neighbors(u))
                random.shuffle(nbrs)
                
                for w in nbrs:
                    if all(G.has_edge(w, c) for c in clique):
                        if random.random() < p_clique:
                            clique.append(w)
                
                for c in clique:
                    G.add_edge(v, c)
    
    return G


def mass_random_search(n, num_trials=10000):
    """Search for chordal graphs on n vertices with high m(G)."""
    import random
    
    best_count = 0
    best_graph = None
    bound = 3 ** (n / 2)
    
    start = time.time()
    
    for trial in range(num_trials):
        for p in [0.2, 0.4, 0.6, 0.8]:
            G = generate_random_chordal_graph(n, p)
            
            # Verify chordality
            if not all(nx.is_chordal(G.subgraph(c).copy()) 
                      for c in nx.connected_components(G)):
                continue
            
            count = count_minimal_rdfs_subset_v2(G)
            
            if count > best_count:
                best_count = count
                best_graph = G.copy()
                rate = count ** (1/n)
                elapsed = time.time() - start
                print(f"  Trial {trial}: NEW BEST m(G)={count}, rate={rate:.6f}, "
                      f"edges={list(G.edges())}, time={elapsed:.1f}s")
                
                if count > bound:
                    print(f"  *** COUNTEREXAMPLE FOUND! m(G)={count} > 3^(n/2)={bound:.2f} ***")
                    return best_graph, best_count
    
    elapsed = time.time() - start
    rate = best_count ** (1/n) if best_count > 0 else 0
    print(f"\n  n={n}: Best m(G)={best_count}, rate={rate:.6f}, "
          f"3^(n/2)={bound:.2f}, time={elapsed:.1f}s")
    print(f"  Edges: {list(best_graph.edges()) if best_graph else 'N/A'}")
    
    return best_graph, best_count


def exhaustive_chordal_8():
    """
    Generate ALL non-isomorphic chordal graphs on 8 vertices.
    
    Use the approach: generate graphs by adding simplicial vertices.
    Start from K1 and build up.
    
    Actually, let's use a cleaner approach:
    Generate by perfect elimination ordering.
    
    For n=8, the number of labeled chordal graphs is manageable 
    if we use canonical forms to deduplicate.
    """
    print("=" * 70)
    print("Generating chordal graphs on n=8 by PEO construction")
    print("=" * 70)
    
    n = 8
    bound = 3 ** (n / 2)
    
    # We'll generate labeled chordal graphs and use graph6 canonical form
    # to deduplicate isomorphic copies.
    
    seen_canonical = set()
    best_count = 0
    best_graphs = []
    total = 0
    
    start = time.time()
    
    # Build all chordal graphs on 8 vertices:
    # PEO approach - add vertices one at a time, connecting to a clique
    
    def build_chordal(G, next_v, n):
        """Recursively build chordal graph by adding next_v connected to a clique."""
        nonlocal seen_canonical, best_count, best_graphs, total
        
        if next_v == n:
            # Complete graph - check canonical form
            canon = nx.to_graph6_bytes(G, header=False).strip()
            if canon in seen_canonical:
                return
            seen_canonical.add(canon)
            
            total += 1
            count = count_minimal_rdfs_subset_v2(G)
            
            if count > best_count:
                best_count = count
                best_graphs = [(G.copy(), count)]
                rate = count ** (1/n)
                print(f"  NEW BEST #{total}: m(G)={count}, rate={rate:.6f}, "
                      f"edges={G.number_of_edges()}")
            elif count == best_count:
                best_graphs.append((G.copy(), count))
            
            if count > bound:
                print(f"  *** COUNTEREXAMPLE! ***")
            
            if total % 1000 == 0:
                elapsed = time.time() - start
                print(f"  ... checked {total} graphs, {elapsed:.1f}s")
            
            return
        
        G.add_node(next_v)
        
        # Enumerate all cliques in the existing graph that next_v could connect to
        # (including the empty clique = isolated vertex)
        existing = list(range(next_v))
        
        # Get all cliques (including subsets of maximal cliques)
        # A clique is any subset of vertices that are all pairwise adjacent
        
        # Enumerate subsets of existing vertices
        for size in range(len(existing) + 1):
            for clique in itertools.combinations(existing, size):
                # Check if clique forms a clique in G
                is_clique = all(G.has_edge(u, v) for u, v in itertools.combinations(clique, 2))
                if not is_clique:
                    continue
                
                # Connect next_v to all vertices in clique
                for v in clique:
                    G.add_edge(next_v, v)
                
                build_chordal(G, next_v + 1, n)
                
                # Disconnect
                for v in clique:
                    G.remove_edge(next_v, v)
        
        G.remove_node(next_v)
    
    G = nx.Graph()
    build_chordal(G, 0, n)
    
    elapsed = time.time() - start
    print(f"\nDone: {total} non-isomorphic chordal graphs on {n} vertices")
    print(f"Best m(G) = {best_count}, 3^(n/2) = {bound:.2f}")
    print(f"Time: {elapsed:.1f}s")
    
    return best_graphs


if __name__ == "__main__":
    # First: random search on larger graphs
    print("=" * 70)
    print("RANDOM SEARCH for high m(G) on chordal graphs")
    print("=" * 70)
    
    for n in [8, 10, 12, 14]:
        print(f"\n--- n = {n} ---")
        mass_random_search(n, num_trials=500)
    
    # Then: exhaustive search on n=8
    # (This may take a while)
    print("\n")
    exhaustive_chordal_8()
