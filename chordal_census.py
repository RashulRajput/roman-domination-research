"""
Census of minimal Roman dominating functions on ALL non-isomorphic chordal graphs.

Strategy:
  1. Use NetworkX graph_atlas for orders 1-7 (all non-isomorphic graphs)
  2. Filter to chordal graphs
  3. Count minimal RDFs using the validated subset method
  4. Track the maximum count and growth rate per order
  5. Cross-validate with brute force on small orders

For orders 8+, we generate chordal graphs systematically.
"""

import math
import time
import networkx as nx
from count_minimal_rdf import count_minimal_rdfs_brute, count_minimal_rdfs_subset_v2


def is_chordal(G):
    """Check if G is chordal using NetworkX."""
    return nx.is_chordal(G)


def generate_chordal_from_atlas():
    """
    Generate all non-isomorphic connected chordal graphs from the graph atlas.
    NetworkX graph_atlas_g() contains all graphs on 0-7 vertices.
    """
    results = {}  # order -> list of (graph, count)
    
    for i in range(len(nx.graph_atlas_g())):
        G = nx.graph_atlas_g()[i]
        n = G.number_of_nodes()
        if n == 0:
            continue
        
        # Check chordality (works on disconnected graphs too)
        # A graph is chordal iff every connected component is chordal
        if not all(is_chordal(G.subgraph(c).copy()) for c in nx.connected_components(G)):
            continue
        
        if n not in results:
            results[n] = []
        
        count = count_minimal_rdfs_subset_v2(G)
        results[n].append((i, G, count))
    
    return results


def generate_specific_chordal_graphs(n):
    """
    Generate specific families of chordal graphs on n vertices.
    Chordal graphs include: complete graphs, trees, interval graphs,
    split graphs, threshold graphs, etc.
    """
    graphs = []
    
    # 1. Complete graph K_n
    G = nx.complete_graph(n)
    graphs.append(("K_" + str(n), G))
    
    # 2. Path P_n (tree, hence chordal)
    if n >= 2:
        G = nx.path_graph(n)
        graphs.append(("P_" + str(n), G))
    
    # 3. Star K_{1,n-1} (tree, hence chordal)
    if n >= 2:
        G = nx.star_graph(n - 1)
        graphs.append(("Star_" + str(n), G))
    
    # 4. Disjoint edges (matching): floor(n/2) edges
    G = nx.Graph()
    G.add_nodes_from(range(n))
    for i in range(0, n - 1, 2):
        G.add_edge(i, i + 1)
    graphs.append(("Matching_" + str(n), G))
    
    # 5. Complete bipartite graph (only chordal if one side has size ≤ 1, or it's K_{1,1})
    # K_{1,n-1} = star (already done)
    # K_{2,n-2} has C4 subgraph without chord if n >= 4, so NOT chordal for n >= 4
    
    # 6. Caterpillar graphs (trees, hence chordal)
    if n >= 4:
        # Caterpillar: path spine with pendant vertices
        spine_len = n // 2
        G = nx.path_graph(spine_len)
        v = spine_len
        for i in range(n - spine_len):
            G.add_edge(i % spine_len, v)
            v += 1
        graphs.append(("Caterpillar_" + str(n), G))
    
    # 7. Split graph: complete graph on k vertices + independent set of n-k vertices
    # each connected to some vertices in the clique
    for k in range(1, n):
        G = nx.complete_graph(k)
        for i in range(k, n):
            # Connect to vertex 0 in the clique (simplest split graph)
            G.add_node(i)
            G.add_edge(i, 0)
        graphs.append((f"Split_{k}_{n-k}", G))
    
    # 8. Threshold graphs
    # Build by repeatedly adding isolated or universal vertices
    if n >= 2:
        G = nx.Graph()
        G.add_node(0)
        for i in range(1, n):
            G.add_node(i)
            if i % 2 == 1:
                # Add as universal (connected to all existing)
                for j in range(i):
                    G.add_edge(i, j)
            # else: add as isolated
        graphs.append(("Threshold_" + str(n), G))
    
    # 9. Block graph (cliques joined at cut vertices)
    # Two cliques sharing one vertex
    if n >= 3:
        k1 = (n + 1) // 2
        k2 = n - k1 + 1  # shared vertex
        G = nx.complete_graph(k1)
        for i in range(k1, k1 + k2 - 1):
            G.add_node(i)
            G.add_edge(0, i)  # connect to shared vertex
            for j in range(k1, i):
                G.add_edge(i, j)
        graphs.append(("Block_" + str(n), G))
    
    # 10. Windmill graph: k copies of K3 sharing a common vertex
    if n >= 3 and (n - 1) % 2 == 0:
        k = (n - 1) // 2
        G = nx.Graph()
        G.add_node(0)
        for i in range(k):
            u = 2 * i + 1
            v = 2 * i + 2
            G.add_edges_from([(0, u), (0, v), (u, v)])
        graphs.append(("Windmill_" + str(k), G))
    
    return graphs


def run_atlas_census():
    """Run the complete census on the graph atlas."""
    print("=" * 70)
    print("CENSUS: Minimal Roman Dominating Functions on Chordal Graphs")
    print("Source: NetworkX Graph Atlas (all non-isomorphic graphs, n <= 7)")
    print("=" * 70)
    
    start = time.time()
    results = generate_chordal_from_atlas()
    elapsed = time.time() - start
    
    print(f"\nCompleted in {elapsed:.2f} seconds.\n")
    
    overall_max_rate = 0
    overall_max_graph = None
    
    for n in sorted(results.keys()):
        entries = results[n]
        max_count = max(c for _, _, c in entries)
        max_graphs = [(i, G, c) for i, G, c in entries if c == max_count]
        bound = 3 ** (n / 2)
        rate = max_count ** (1 / n) if n > 0 else 1
        
        if rate > overall_max_rate:
            overall_max_rate = rate
            overall_max_graph = max_graphs[0]
        
        exceeds = max_count > bound
        
        print(f"n={n}: {len(entries)} chordal graphs, "
              f"max m(G)={max_count}, "
              f"3^(n/2)={bound:.2f}, "
              f"rate={rate:.6f}, "
              f"{'EXCEEDS' if exceeds else 'OK'}")
        
        if exceeds:
            idx, G, c = max_graphs[0]
            print(f"  *** COUNTEREXAMPLE: Atlas #{idx}, edges={list(G.edges())}")
        
        # Show top graphs
        entries_sorted = sorted(entries, key=lambda x: -x[2])
        for idx, G, c in entries_sorted[:3]:
            r = c ** (1/n) if n > 0 else 1
            print(f"  Atlas #{idx}: m(G)={c}, rate={r:.4f}, "
                  f"edges={G.number_of_edges()}, "
                  f"connected={'Y' if nx.is_connected(G) else 'N'}")
    
    print(f"\nOverall maximum growth rate: {overall_max_rate:.6f}")
    print(f"sqrt(3) = {math.sqrt(3):.6f}")
    
    # Cross-validate with brute force on n <= 5
    print("\n" + "=" * 70)
    print("CROSS-VALIDATION: brute force vs subset method, n <= 5")
    print("=" * 70)
    
    mismatches = 0
    total_checked = 0
    for n in sorted(results.keys()):
        if n > 5:
            break
        for idx, G, subset_count in results[n]:
            brute_count = count_minimal_rdfs_brute(G)
            if brute_count != subset_count:
                print(f"  MISMATCH: Atlas #{idx}, n={n}, "
                      f"brute={brute_count}, subset={subset_count}")
                mismatches += 1
            total_checked += 1
    
    print(f"Checked {total_checked} graphs, {mismatches} mismatches.")
    
    return results


def run_specific_families_census(max_n=18):
    """Test specific chordal graph families for larger n."""
    print("\n" + "=" * 70)
    print(f"CENSUS: Specific Chordal Graph Families (n <= {max_n})")
    print("=" * 70)
    
    for n in range(2, max_n + 1):
        families = generate_specific_chordal_graphs(n)
        max_count = 0
        max_name = ""
        bound = 3 ** (n / 2)
        
        for name, G in families:
            # Verify chordality
            if not all(is_chordal(G.subgraph(c).copy()) for c in nx.connected_components(G)):
                continue
            
            if G.number_of_nodes() != n:
                continue
            
            count = count_minimal_rdfs_subset_v2(G)
            rate = count ** (1 / n)
            exceeds = count > bound
            
            if count > max_count:
                max_count = count
                max_name = name
            
            if exceeds:
                print(f"  n={n}, {name}: m(G)={count}, 3^(n/2)={bound:.2f}, "
                      f"rate={rate:.6f} *** EXCEEDS ***")
        
        rate = max_count ** (1 / n) if max_count > 0 else 0
        print(f"n={n}: best={max_name}, m(G)={max_count}, "
              f"3^(n/2)={bound:.2f}, rate={rate:.6f}, "
              f"{'EXCEEDS' if max_count > bound else 'OK'}")


if __name__ == "__main__":
    run_atlas_census()
    run_specific_families_census(max_n=16)
