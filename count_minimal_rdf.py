"""
Exact counting of minimal Roman dominating functions on graphs.

A Roman dominating function (RDF) f: V -> {0,1,2} satisfies:
  every vertex v with f(v)=0 has a neighbor u with f(u)=2.

A RDF is MINIMAL if no function g < f (pointwise, with g != f) is also an RDF.
Equivalently, for every vertex v with f(v) > 0, reducing f(v) by 1 yields a non-RDF.

Two independent counting methods are implemented for cross-validation:
  1. Brute-force: enumerate all 3^n assignments
  2. Subset-based: iterate over 2^n subsets S (vertices assigned 2)
"""

import itertools
import networkx as nx
from collections import defaultdict


def is_rdf(G, f):
    """Check if assignment f: dict {vertex: 0/1/2} is a Roman dominating function."""
    for v in G.nodes():
        if f[v] == 0:
            has_two_neighbor = any(f[u] == 2 for u in G.neighbors(v))
            if not has_two_neighbor:
                return False
    return True


def is_minimal_rdf(G, f):
    """Check if RDF f is minimal: reducing any positive value by 1 breaks the RDF property."""
    if not is_rdf(G, f):
        return False
    for v in G.nodes():
        if f[v] > 0:
            g = dict(f)
            g[v] = f[v] - 1
            if is_rdf(G, g):
                return False
    return True


def count_minimal_rdfs_brute(G):
    """Count minimal RDFs by enumerating all 3^n assignments. O(3^n * n)."""
    nodes = list(G.nodes())
    n = len(nodes)
    count = 0
    for vals in itertools.product([0, 1, 2], repeat=n):
        f = {nodes[i]: vals[i] for i in range(n)}
        if is_minimal_rdf(G, f):
            count += 1
    return count


def list_minimal_rdfs_brute(G):
    """List all minimal RDFs by enumerating all 3^n assignments."""
    nodes = list(G.nodes())
    n = len(nodes)
    result = []
    for vals in itertools.product([0, 1, 2], repeat=n):
        f = {nodes[i]: vals[i] for i in range(n)}
        if is_minimal_rdf(G, f):
            result.append(dict(f))
    return result


def count_minimal_rdfs_subset(G):
    """
    Count minimal RDFs using subset enumeration.
    
    Given a subset S of vertices assigned 2:
    - Every vertex NOT in S that has a neighbor in S: assigned 0 (dominated by S)
    - Every vertex NOT in S with NO neighbor in S: assigned 1 (self-dominating)
    - For this to be minimal: every vertex in S must have a "private zero-neighbor"
      i.e., a neighbor assigned 0 whose ONLY neighbor in S is that vertex.
    
    But this is slightly more subtle. The function values for vertices in S are 2,
    and for minimality we also need that we can't reduce a 2 to a 1 and still have 
    an RDF. A vertex v in S with f(v)=2 can be reduced to 1 without breaking the RDF
    if and only if every neighbor u of v with f(u)=0 has another neighbor in S besides v.
    So for minimality of vertices in S: each must have a private zero-neighbor.
    
    Additionally, vertices assigned 1 (not in S, no neighbor in S) could potentially
    be reduced to 0. Reducing f(v) from 1 to 0 requires v to have a neighbor assigned 2,
    i.e., a neighbor in S. But we said v has no neighbor in S, so reducing to 0 is invalid.
    Hence vertices assigned 1 are automatically minimal.
    
    Wait — we also need to handle the case S = empty set.
    If S is empty, then every vertex gets 1 (since no vertex has a neighbor in S).
    f = all-ones. Is this a valid RDF? Yes: no vertex has value 0.
    Is it minimal? We need: reducing any vertex from 1 to 0 breaks RDF.
    Reducing v from 1 to 0: v now has value 0, and v needs a neighbor with value 2.
    No vertex has value 2 (S is empty), so the RDF is broken. Hence all-ones is minimal.
    """
    nodes = list(G.nodes())
    n = len(nodes)
    if n == 0:
        return 1  # empty function is trivially minimal
    
    index = {v: i for i, v in enumerate(nodes)}
    
    # Precompute adjacency bitmasks
    adj = [0] * n
    for v in nodes:
        iv = index[v]
        for u in G.neighbors(v):
            adj[iv] |= 1 << index[u]
    
    count = 0
    for S in range(1 << n):
        valid = True
        
        # Check each vertex in S for private zero-neighbor
        remaining = S
        while remaining:
            bit = remaining & -remaining
            v = bit.bit_length() - 1
            remaining ^= bit
            
            # Zero-neighbors of v: neighbors of v NOT in S
            zero_nbrs = adj[v] & ~S
            
            # But wait: a neighbor not in S is assigned 0 ONLY IF it has a neighbor in S.
            # If it has no neighbor in S, it's assigned 1, not 0.
            # Actually, let me reconsider. Given S:
            #   - v in S: f(v) = 2
            #   - v not in S, v has neighbor in S: f(v) = 0
            #   - v not in S, v has NO neighbor in S: f(v) = 1
            # So zero-neighbors of v are: neighbors of v that are NOT in S AND have a neighbor in S.
            
            # Zero vertices: not in S, but adjacent to S
            # For vertex u not in S: u is zero iff adj[u] & S != 0
            
            has_private_zero = False
            candidates = zero_nbrs  # neighbors of v not in S
            while candidates:
                u_bit = candidates & -candidates
                u = u_bit.bit_length() - 1
                candidates ^= u_bit
                
                # u is zero only if it has a neighbor in S
                if adj[u] & S == 0:
                    continue  # u is assigned 1, not 0
                
                # u is a zero-neighbor of v. Check if v is u's ONLY neighbor in S.
                if (adj[u] & S) == bit:
                    has_private_zero = True
                    break
            
            if not has_private_zero:
                valid = False
                break
        
        if valid:
            count += 1
    
    return count


def count_minimal_rdfs_subset_v2(G):
    """
    Improved subset-based counting with better handling of edge cases.
    Includes the S=empty case (all-ones function).
    """
    nodes = list(G.nodes())
    n = len(nodes)
    if n == 0:
        return 1
    
    index = {v: i for i, v in enumerate(nodes)}
    
    adj = [0] * n
    for v in nodes:
        iv = index[v]
        for u in G.neighbors(v):
            adj[iv] |= 1 << index[u]
    
    count = 0
    for S in range(1 << n):
        if S == 0:
            # All-ones function: always a minimal RDF
            count += 1
            continue
        
        valid = True
        remaining = S
        while remaining:
            bit = remaining & -remaining
            v = bit.bit_length() - 1
            remaining ^= bit
            
            # Find private zero-neighbor
            has_private = False
            nbrs_not_in_S = adj[v] & ~S
            while nbrs_not_in_S:
                u_bit = nbrs_not_in_S & -nbrs_not_in_S
                u = u_bit.bit_length() - 1
                nbrs_not_in_S ^= u_bit
                
                # u is a zero vertex only if it has a neighbor in S
                if adj[u] & S == 0:
                    continue
                
                # u's only S-neighbor is v
                if (adj[u] & S) == bit:
                    has_private = True
                    break
            
            if not has_private:
                valid = False
                break
        
        if valid:
            count += 1
    
    return count


if __name__ == "__main__":
    # Quick self-test on small graphs
    print("=== Self-test: Cross-validating counting methods ===")
    
    # Test on K2 (single edge)
    G = nx.Graph()
    G.add_edge(0, 1)
    b = count_minimal_rdfs_brute(G)
    s = count_minimal_rdfs_subset_v2(G)
    print(f"K2: brute={b}, subset={s}, match={b==s}")
    assert b == s
    
    # Test on K3
    G = nx.complete_graph(3)
    b = count_minimal_rdfs_brute(G)
    s = count_minimal_rdfs_subset_v2(G)
    print(f"K3: brute={b}, subset={s}, match={b==s}")
    assert b == s
    
    # Test on P3 (path on 3 vertices)
    G = nx.path_graph(3)
    b = count_minimal_rdfs_brute(G)
    s = count_minimal_rdfs_subset_v2(G)
    print(f"P3: brute={b}, subset={s}, match={b==s}")
    assert b == s
    
    # Test on P4
    G = nx.path_graph(4)
    b = count_minimal_rdfs_brute(G)
    s = count_minimal_rdfs_subset_v2(G)
    print(f"P4: brute={b}, subset={s}, match={b==s}")
    assert b == s
    
    # Test on K4
    G = nx.complete_graph(4)
    b = count_minimal_rdfs_brute(G)
    s = count_minimal_rdfs_subset_v2(G)
    print(f"K4: brute={b}, subset={s}, match={b==s}")
    assert b == s
    
    # Test on K1 (single vertex)
    G = nx.Graph()
    G.add_node(0)
    b = count_minimal_rdfs_brute(G)
    s = count_minimal_rdfs_subset_v2(G)
    print(f"K1: brute={b}, subset={s}, match={b==s}")
    assert b == s
    
    # Test on 2K2 (two disjoint edges)
    G = nx.Graph()
    G.add_edges_from([(0,1), (2,3)])
    b = count_minimal_rdfs_brute(G)
    s = count_minimal_rdfs_subset_v2(G)
    print(f"2K2: brute={b}, subset={s}, match={b==s}, expected=9")
    assert b == s
    assert b == 9  # 3^2
    
    # Test on 3K2 (three disjoint edges)
    G = nx.Graph()
    G.add_edges_from([(0,1), (2,3), (4,5)])
    b = count_minimal_rdfs_brute(G)
    s = count_minimal_rdfs_subset_v2(G)
    print(f"3K2: brute={b}, subset={s}, match={b==s}, expected=27")
    assert b == s
    assert b == 27  # 3^3
    
    print("\n=== All self-tests passed! ===")
    
    # Show the actual minimal RDFs of K2
    G = nx.Graph()
    G.add_edge(0, 1)
    rdfs = list_minimal_rdfs_brute(G)
    print(f"\nMinimal RDFs of K2:")
    for f in rdfs:
        print(f"  {f}")
