"""
Systematic search for chordal graphs that maximize m(G).

Key insight: Chordal graphs have a perfect elimination ordering (PEO).
We can construct chordal graphs by:
  1. Starting from a clique
  2. Adding simplicial vertices (connected to a clique in existing graph)
  
This generates all chordal graphs.

We also investigate specific constructions:
  - Disjoint union of K2s: gives 3^(n/2)
  - Can we beat this with connected chordal graphs?
  - What about disjoint unions of other small chordal graphs?
  
Key question: For which small chordal graph H does m(H)^(1/|V(H)|) maximize?
If we find H with m(H)^(1/|H|) > sqrt(3), then disjoint copies of H beat 3^(n/2).
"""

import math
import itertools
import networkx as nx
from count_minimal_rdf import count_minimal_rdfs_subset_v2, count_minimal_rdfs_brute


def analyze_small_chordal_building_blocks():
    """
    For each small chordal graph, compute m(G) and m(G)^(1/n).
    If any graph achieves rate > sqrt(3), disjoint copies give a counterexample.
    """
    print("=" * 70)
    print("ANALYSIS: Building blocks - which small chordal graph maximizes rate?")
    print("=" * 70)
    print(f"Target rate: sqrt(3) = {math.sqrt(3):.6f}")
    print()
    
    # Collect all small chordal graphs from atlas
    atlas = nx.graph_atlas_g()
    
    best_by_order = {}
    all_results = []
    
    for i in range(1, len(atlas)):
        G = atlas[i]
        n = G.number_of_nodes()
        
        if n == 0:
            continue
        
        # Check chordality for each component
        try:
            chordal = all(nx.is_chordal(G.subgraph(c).copy()) 
                         for c in nx.connected_components(G))
        except:
            continue
        
        if not chordal:
            continue
        
        count = count_minimal_rdfs_subset_v2(G)
        rate = count ** (1 / n)
        
        all_results.append((rate, count, n, i, G))
        
        if n not in best_by_order or count > best_by_order[n][1]:
            best_by_order[n] = (i, count, rate, G)
    
    # Sort by rate descending
    all_results.sort(key=lambda x: -x[0])
    
    print("Top 20 chordal graphs by growth rate:")
    print("-" * 70)
    for rate, count, n, idx, G in all_results[:20]:
        conn = "conn" if nx.is_connected(G) else "disc"
        edges = list(G.edges())
        print(f"  Atlas #{idx:4d}: n={n}, m(G)={count:6d}, rate={rate:.6f}, "
              f"{conn}, edges={edges}")
    
    print()
    print("Best per order:")
    print("-" * 70)
    for n in sorted(best_by_order.keys()):
        idx, count, rate, G = best_by_order[n]
        bound = 3 ** (n / 2)
        status = "EXCEEDS" if count > bound else "OK"
        conn = "conn" if nx.is_connected(G) else "disc"
        print(f"  n={n}: Atlas #{idx}, m(G)={count}, 3^(n/2)={bound:.2f}, "
              f"rate={rate:.6f}, {conn}, {status}")
    
    return all_results


def test_disjoint_unions(max_copies=6):
    """
    Test disjoint unions of small chordal building blocks.
    m(G1 + G2) = m(G1) * m(G2) for disjoint unions.
    So we only need to check: does m(H)^(1/|H|) > sqrt(3) for any H?
    """
    print("\n" + "=" * 70)
    print("ANALYSIS: Disjoint unions of building blocks")
    print("=" * 70)
    
    # Small chordal graphs to test as building blocks
    building_blocks = []
    
    # All connected chordal graphs from atlas
    atlas = nx.graph_atlas_g()
    for i in range(1, len(atlas)):
        G = atlas[i]
        if G.number_of_nodes() == 0:
            continue
        if not nx.is_connected(G):
            continue
        try:
            if not nx.is_chordal(G):
                continue
        except:
            continue
        
        n = G.number_of_nodes()
        count = count_minimal_rdfs_subset_v2(G)
        rate = count ** (1 / n)
        building_blocks.append((rate, count, n, i, G))
    
    building_blocks.sort(key=lambda x: -x[0])
    
    print(f"\nTop 10 connected chordal building blocks:")
    for rate, count, n, idx, G in building_blocks[:10]:
        print(f"  Atlas #{idx}: n={n}, m(G)={count}, rate={rate:.6f}, "
              f"edges={list(G.edges())}")
    
    # The key insight: if ALL connected chordal graphs have rate <= sqrt(3),
    # then disjoint unions also have rate <= sqrt(3).
    # So the conjecture holds iff it holds for connected graphs.
    
    threshold = math.sqrt(3)
    above = [b for b in building_blocks if b[0] > threshold + 1e-9]
    
    if above:
        print(f"\n*** FOUND {len(above)} building blocks with rate > sqrt(3)! ***")
        for rate, count, n, idx, G in above:
            print(f"  Atlas #{idx}: n={n}, m(G)={count}, rate={rate:.6f}")
            print(f"  Edges: {list(G.edges())}")
            print(f"  Disjoint copies would give growth rate {rate:.6f}^n")
    else:
        print(f"\nAll connected chordal graphs on <= 7 vertices have rate <= sqrt(3).")
        print("This is consistent with the conjecture M(n) <= 3^(n/2).")


def explore_graph_operations(max_n=12):
    """
    Explore chordal graphs built from graph operations that might 
    produce high counts of minimal RDFs.
    """
    print("\n" + "=" * 70)
    print(f"ANALYSIS: Graph operations and constructions (n <= {max_n})")
    print("=" * 70)
    
    results = []
    
    for n in range(2, max_n + 1):
        best_count = 0
        best_name = ""
        bound = 3 ** (n / 2)
        
        constructions = []
        
        # 1. Disjoint edges (matching) - the conjectured extremal family
        G = nx.Graph()
        G.add_nodes_from(range(n))
        for i in range(0, n - 1, 2):
            G.add_edge(i, i + 1)
        constructions.append(("Matching", G))
        
        # 2. Complete graph
        constructions.append(("Complete", nx.complete_graph(n)))
        
        # 3. Path
        constructions.append(("Path", nx.path_graph(n)))
        
        # 4. Star
        constructions.append(("Star", nx.star_graph(n - 1)))
        
        # 5. Cocktail party graphs (complete multipartite K_{2,2,...,2})
        # These are NOT chordal for >= 4 vertices (contain C4)
        # Skip
        
        # 6. Disjoint K3's
        if n % 3 == 0:
            G = nx.Graph()
            for i in range(0, n, 3):
                G.add_edges_from([(i, i+1), (i+1, i+2), (i, i+2)])
            constructions.append(("Disjoint_K3s", G))
        
        # 7. Disjoint P3's (paths of length 2)
        if n % 3 == 0:
            G = nx.Graph()
            for i in range(0, n, 3):
                G.add_edges_from([(i, i+1), (i+1, i+2)])
            constructions.append(("Disjoint_P3s", G))
        
        # 8. Mixed: some K2's and some isolated vertices
        for k in range(n // 2 + 1):
            G = nx.Graph()
            G.add_nodes_from(range(n))
            for i in range(k):
                G.add_edge(2 * i, 2 * i + 1)
            name = f"Match_{k}_Iso_{n - 2*k}"
            constructions.append((name, G))
        
        # 9. Disjoint K4's
        if n % 4 == 0 and n >= 4:
            G = nx.Graph()
            for i in range(0, n, 4):
                for a in range(i, i + 4):
                    for b in range(a + 1, i + 4):
                        G.add_edge(a, b)
            constructions.append(("Disjoint_K4s", G))
        
        # 10. Trees: binary tree
        if n >= 3:
            G = nx.balanced_tree(2, max(1, int(math.log2(n))))
            while G.number_of_nodes() > n:
                # Remove leaves to get exactly n vertices
                leaves = [v for v in G.nodes() if G.degree(v) == 1]
                if leaves:
                    G.remove_node(leaves[-1])
                else:
                    break
            while G.number_of_nodes() < n:
                # Add pendant vertices
                v = max(G.nodes()) + 1
                G.add_edge(0, v)
            if G.number_of_nodes() == n:
                constructions.append(("BinaryTree", G))
        
        for name, G in constructions:
            if G.number_of_nodes() != n:
                continue
            
            # Verify chordality
            try:
                chordal = all(nx.is_chordal(G.subgraph(c).copy()) 
                             for c in nx.connected_components(G))
            except:
                continue
            
            if not chordal:
                continue
            
            count = count_minimal_rdfs_subset_v2(G)
            rate = count ** (1 / n)
            exceeds = count > bound
            
            if count > best_count:
                best_count = count
                best_name = name
            
            if exceeds:
                print(f"  n={n}, {name}: m(G)={count}, 3^(n/2)={bound:.2f} *** EXCEEDS ***")
                print(f"    Edges: {list(G.edges())}")
        
        rate = best_count ** (1 / n) if best_count > 0 else 0
        print(f"n={n:2d}: best={best_name:20s}, m(G)={best_count:8d}, "
              f"3^(n/2)={bound:10.2f}, rate={rate:.6f}")
        
        results.append((n, best_name, best_count, bound, rate))
    
    return results


def analyze_clique_tree_structure():
    """
    Analyze the relationship between clique tree structure and m(G).
    
    For a chordal graph G, the clique tree T has:
    - Nodes = maximal cliques of G
    - Edges between cliques that share vertices
    
    Hypothesis: m(G) is maximized when the clique tree has a simple structure
    (e.g., all cliques are edges = matching).
    """
    print("\n" + "=" * 70)
    print("ANALYSIS: Clique tree structure vs m(G)")
    print("=" * 70)
    
    atlas = nx.graph_atlas_g()
    
    for n in range(2, 8):
        print(f"\n--- Order n = {n} ---")
        entries = []
        
        for i in range(1, len(atlas)):
            G = atlas[i]
            if G.number_of_nodes() != n:
                continue
            if not nx.is_connected(G):
                continue
            try:
                if not nx.is_chordal(G):
                    continue
            except:
                continue
            
            count = count_minimal_rdfs_subset_v2(G)
            
            # Get clique information
            cliques = list(nx.find_cliques(G))
            max_clique_size = max(len(c) for c in cliques)
            num_cliques = len(cliques)
            
            # Number of simplicial vertices
            simplicial = sum(1 for v in G.nodes() 
                           if nx.is_chordal(G) and 
                           all(G.has_edge(u, w) 
                               for u in G.neighbors(v) 
                               for w in G.neighbors(v) if u != w))
            
            entries.append((count, i, G, num_cliques, max_clique_size, simplicial))
        
        entries.sort(key=lambda x: -x[0])
        
        bound = 3 ** (n / 2)
        for count, idx, G, nc, mcs, simp in entries[:5]:
            rate = count ** (1/n)
            print(f"  Atlas #{idx:4d}: m(G)={count:5d}, rate={rate:.4f}, "
                  f"cliques={nc}, max_clique={mcs}, simplicial={simp}, "
                  f"edges={list(G.edges())}")


if __name__ == "__main__":
    analyze_small_chordal_building_blocks()
    test_disjoint_unions()
    explore_graph_operations(max_n=14)
    analyze_clique_tree_structure()
