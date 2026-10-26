"""
Mathematical analysis of minimal Roman dominating functions on paths.

The path P_n appears to be the connected chordal graph maximizing m(G).
Let's derive the exact recurrence for m(P_n).

Also: develop the KEY STRUCTURAL LEMMA that could prove the conjecture.
"""

import math
import networkx as nx
from count_minimal_rdf import count_minimal_rdfs_subset_v2, list_minimal_rdfs_brute


def path_rdf_analysis():
    """Compute m(P_n) for paths and find the recurrence."""
    print("=" * 70)
    print("Path P_n: Exact count of minimal Roman dominating functions")
    print("=" * 70)
    
    counts = []
    for n in range(1, 22):
        G = nx.path_graph(n)
        c = count_minimal_rdfs_subset_v2(G)
        rate = c ** (1/n) if n > 0 else 1
        counts.append(c)
        print(f"  P_{n:2d}: m(G) = {c:8d}, rate = {rate:.6f}")
    
    # Check for linear recurrence
    print("\n--- Checking linear recurrences ---")
    
    # Try recurrence of order 2: a_n = p*a_{n-1} + q*a_{n-2}
    # a_3 = p*a_2 + q*a_1
    # a_4 = p*a_3 + q*a_2
    # From the data: a_1=1, a_2=3, a_3=4, a_4=7, a_5=12, a_6=20, a_7=34
    
    # 4 = 3p + q
    # 7 = 4p + 3q
    # From first: q = 4 - 3p
    # Into second: 7 = 4p + 3(4-3p) = 4p + 12 - 9p = -5p + 12
    # 5p = 5, p = 1, q = 1
    # Check: a_n = a_{n-1} + a_{n-2}??
    # a_5 should be a_4 + a_3 = 7 + 4 = 11 != 12. NO.
    
    # Try order 3: a_n = p*a_{n-1} + q*a_{n-2} + r*a_{n-3}
    # 7 = 4p + 3q + r*1        ... (i)  [a_4 from a_3,a_2,a_1]
    # 12 = 7p + 4q + r*3       ... (ii) [a_5 from a_4,a_3,a_2]
    # 20 = 12p + 7q + r*4      ... (iii)[a_6 from a_5,a_4,a_3]
    
    # From (i): 7 = 4p + 3q + r
    # From (ii): 12 = 7p + 4q + 3r
    # From (iii): 20 = 12p + 7q + 4r
    
    # (ii) - (i): 5 = 3p + q + 2r     ... (iv)
    # (iii) - (ii): 8 = 5p + 3q + r    ... (v)
    # (v) - (iv): 3 = 2p + 2q - r      ... (vi)
    # From (iv): r = (5 - 3p - q) / 2
    # Into (vi): 3 = 2p + 2q - (5 - 3p - q)/2
    #            6 = 4p + 4q - 5 + 3p + q
    #            11 = 7p + 5q
    #            q = (11 - 7p) / 5
    # Into (iv): 5 = 3p + (11-7p)/5 + 2*(5 - 3p - (11-7p)/5)/2
    #            5 = 3p + (11-7p)/5 + 5 - 3p - (11-7p)/5
    #            5 = 5  ???
    
    # Hmm, that means the system is underdetermined with order 3.
    # This happens when order 3 is not the right recurrence order.
    
    # Let me try direct checking of various recurrences
    a = counts  # a[0] = m(P_1), a[1] = m(P_2), etc.
    
    for order in range(2, 7):
        print(f"\n  Checking order-{order} recurrence:")
        # Solve a[n] = sum c_i * a[n-i] for i=1..order
        # Using first 'order+1' equations
        import numpy as np
        
        # Set up system: for n = order, order+1, ..., 2*order-1
        rows = min(order + 2, len(a) - order)
        if rows < order:
            break
        
        A = []
        b = []
        for n in range(order, order + rows):
            row = [a[n - i - 1] for i in range(order)]
            A.append(row)
            b.append(a[n])
        
        A = np.array(A, dtype=float)
        b = np.array(b, dtype=float)
        
        try:
            coeffs, residuals, rank, sv = np.linalg.lstsq(A, b, rcond=None)
            
            # Verify on all data
            errors = []
            for n in range(order, len(a)):
                pred = sum(coeffs[i] * a[n - i - 1] for i in range(order))
                errors.append(abs(pred - a[n]))
            
            max_err = max(errors) if errors else 0
            print(f"    Coefficients: {[f'{c:.4f}' for c in coeffs]}")
            print(f"    Max error: {max_err:.6f}")
            
            if max_err < 0.01:
                print(f"    *** EXACT RECURRENCE FOUND! ***")
                # Compute characteristic root
                # For order 2: x^2 = c1*x + c2
                if order == 2:
                    c1, c2 = coeffs
                    disc = c1**2 + 4*c2
                    if disc >= 0:
                        r1 = (c1 + math.sqrt(disc)) / 2
                        r2 = (c1 - math.sqrt(disc)) / 2
                        print(f"    Characteristic roots: {r1:.6f}, {r2:.6f}")
                        print(f"    Growth rate: {abs(r1):.6f}")
        except Exception as e:
            print(f"    Error: {e}")


def investigate_general_graph_structure():
    """
    Key structural analysis for the proof.
    
    For chordal graphs, we can decompose using:
    1. Simplicial vertices (PEO)
    2. Clique separators (clique tree decomposition)
    
    Key question: How does removing a simplicial vertex affect m(G)?
    """
    print("\n" + "=" * 70)
    print("STRUCTURAL ANALYSIS: Effect of simplicial vertex removal")
    print("=" * 70)
    
    atlas = nx.graph_atlas_g()
    
    for n in range(3, 8):
        print(f"\n--- Order n = {n} ---")
        
        for i in range(1, len(atlas)):
            G = atlas[i]
            if G.number_of_nodes() != n or not nx.is_connected(G):
                continue
            try:
                if not nx.is_chordal(G):
                    continue
            except:
                continue
            
            m_G = count_minimal_rdfs_subset_v2(G)
            
            # Find simplicial vertices
            simplicial = []
            for v in G.nodes():
                nbrs = list(G.neighbors(v))
                is_simp = all(G.has_edge(u, w) for u in nbrs for w in nbrs if u != w)
                if is_simp:
                    simplicial.append(v)
            
            if not simplicial:
                continue
            
            for v in simplicial[:1]:  # Test first simplicial vertex
                H = G.copy()
                H.remove_node(v)
                
                if H.number_of_nodes() == 0:
                    continue
                
                m_H = count_minimal_rdfs_subset_v2(H)
                
                deg_v = G.degree(v)
                ratio = m_G / m_H if m_H > 0 else float('inf')
                
                print(f"  Atlas #{i:4d}: m(G)={m_G:5d}, deg(v)={deg_v}, "
                      f"m(G-v)={m_H:5d}, ratio={ratio:.4f}, "
                      f"sqrt(3)={math.sqrt(3):.4f}")
                
                if ratio > math.sqrt(3) + 0.001:
                    print(f"    *** Ratio exceeds sqrt(3)! ***")
                break


def investigate_clique_separator_decomposition():
    """
    For the proof: decompose at clique separators.
    
    Theorem (Tarjan): Every chordal graph can be decomposed into
    atoms (no clique separator) by splitting at clique separators.
    The atoms are complete graphs.
    
    Key question: If G = G1 cup G2 with G1 cap G2 = clique C,
    does m(G) <= m(G1) * m(G2) / m(C)?
    """
    print("\n" + "=" * 70)
    print("STRUCTURAL ANALYSIS: Clique separator decomposition")
    print("=" * 70)
    
    # Test this on specific examples
    # Graph: two triangles sharing a vertex (butterfly graph, n=5)
    # G1 = K3 (vertices 0,1,2), G2 = K3 (vertices 0,3,4), shared = {0}
    G = nx.Graph()
    G.add_edges_from([(0,1),(0,2),(1,2),(0,3),(0,4),(3,4)])
    
    assert nx.is_chordal(G)
    
    G1 = nx.complete_graph(3)  # K3
    G2 = nx.complete_graph(3)  # K3
    C = nx.Graph(); C.add_node(0)  # K1
    
    m_G = count_minimal_rdfs_subset_v2(G)
    m_G1 = count_minimal_rdfs_subset_v2(G1)
    m_G2 = count_minimal_rdfs_subset_v2(G2)
    m_C = count_minimal_rdfs_subset_v2(C)
    
    print(f"\nButterfly (two K3 sharing vertex):")
    print(f"  m(G) = {m_G}")
    print(f"  m(G1) = {m_G1}, m(G2) = {m_G2}, m(C) = {m_C}")
    print(f"  m(G1)*m(G2)/m(C) = {m_G1*m_G2/m_C:.2f}")
    print(f"  Ratio m(G) / (m(G1)*m(G2)/m(C)) = {m_G / (m_G1*m_G2/m_C):.4f}")
    
    # Two K3 sharing an edge
    G = nx.Graph()
    G.add_edges_from([(0,1),(0,2),(1,2),(0,1),(0,3),(1,3)])  # K4 minus one edge? No.
    # Actually two triangles sharing edge (0,1) = diamond graph
    G = nx.Graph()
    G.add_edges_from([(0,1),(0,2),(1,2),(0,3),(1,3)])
    
    assert nx.is_chordal(G)
    
    G1 = nx.Graph()
    G1.add_edges_from([(0,1),(0,2),(1,2)])  # K3
    G2 = nx.Graph()
    G2.add_edges_from([(0,1),(0,3),(1,3)])  # K3
    C = nx.Graph()
    C.add_edges_from([(0,1)])  # K2
    
    m_G = count_minimal_rdfs_subset_v2(G)
    m_G1 = count_minimal_rdfs_subset_v2(G1)
    m_G2 = count_minimal_rdfs_subset_v2(G2)
    m_C = count_minimal_rdfs_subset_v2(C)
    
    print(f"\nDiamond (two K3 sharing edge):")
    print(f"  m(G) = {m_G}")
    print(f"  m(G1) = {m_G1}, m(G2) = {m_G2}, m(C) = {m_C}")
    print(f"  m(G1)*m(G2)/m(C) = {m_G1*m_G2/m_C:.2f}")
    print(f"  Ratio m(G) / (m(G1)*m(G2)/m(C)) = {m_G / (m_G1*m_G2/m_C):.4f}")
    
    # Path P_4: vertices 0-1-2-3. Clique separator {1}: G1 = 0-1, G2 = 1-2-3
    G = nx.path_graph(4)
    G1 = nx.path_graph(2)  # 0-1
    G2 = nx.path_graph(3)  # 1-2-3
    C = nx.Graph(); C.add_node(0)  # {1}
    
    m_G = count_minimal_rdfs_subset_v2(G)
    m_G1 = count_minimal_rdfs_subset_v2(G1)
    m_G2 = count_minimal_rdfs_subset_v2(G2)
    m_C = count_minimal_rdfs_subset_v2(C)
    
    print(f"\nP_4 (split at vertex 1):")
    print(f"  m(G) = {m_G}")
    print(f"  m(G1=P2) = {m_G1}, m(G2=P3) = {m_G2}, m(C=K1) = {m_C}")
    print(f"  m(G1)*m(G2)/m(C) = {m_G1*m_G2/m_C:.2f}")
    print(f"  Ratio m(G) / (m(G1)*m(G2)/m(C)) = {m_G / (m_G1*m_G2/m_C):.4f}")
    
    # Test on more examples
    print("\n--- Systematic test: all clique separators in connected chordal graphs ---")
    atlas = nx.graph_atlas_g()
    
    decomp_ratios = []
    for i in range(1, len(atlas)):
        G = atlas[i]
        n = G.number_of_nodes()
        if n < 3 or not nx.is_connected(G):
            continue
        try:
            if not nx.is_chordal(G):
                continue
        except:
            continue
        
        m_G = count_minimal_rdfs_subset_v2(G)
        
        # Find clique separators using NetworkX
        try:
            complete, atoms = nx.complete_to_chordal_graph(G.copy())
        except:
            continue
    
    return


def compute_exact_path_sequence():
    """Compute m(P_n) for large n and analyze growth rate."""
    print("\n" + "=" * 70)
    print("EXACT PATH SEQUENCE m(P_n)")
    print("=" * 70)
    
    vals = []
    for n in range(1, 25):
        G = nx.path_graph(n)
        c = count_minimal_rdfs_subset_v2(G)
        vals.append(c)
        rate = c ** (1/n)
        ratio_to_prev = c / vals[-2] if len(vals) >= 2 else 0
        print(f"  m(P_{n:2d}) = {c:10d}  rate^(1/n) = {rate:.6f}  "
              f"a_n/a_(n-1) = {ratio_to_prev:.6f}")
    
    # Check OEIS-style: differences, ratios, etc.
    print("\n  Sequence:", vals)
    
    # Check if this matches any known sequence
    # 1, 3, 4, 7, 12, 20, 34, 57, 96, ...
    # Let's check: is this related to tribonacci or similar?
    print("\n  Checking recurrence a_n = a_{n-1} + a_{n-2} + a_{n-3}:")
    for i in range(3, len(vals)):
        pred = vals[i-1] + vals[i-2] + vals[i-3]
        diff = vals[i] - pred
        print(f"    a_{i+1} = {vals[i]}, pred = {pred}, diff = {diff}")


if __name__ == "__main__":
    # Need numpy for recurrence analysis
    try:
        import numpy as np
        path_rdf_analysis()
    except ImportError:
        print("NumPy not available, skipping recurrence analysis")
        # Still compute the sequence
        for n in range(1, 20):
            G = nx.path_graph(n)
            c = count_minimal_rdfs_subset_v2(G)
            rate = c ** (1/n)
            print(f"  m(P_{n:2d}) = {c:8d}  rate^(1/n) = {rate:.6f}")
    
    compute_exact_path_sequence()
    investigate_general_graph_structure()
    investigate_clique_separator_decomposition()
