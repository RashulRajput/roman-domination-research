"""
Verify the exact recurrence for m(P_n) and compute the characteristic root.

DISCOVERED RECURRENCE: a_n = a_{n-1} + a_{n-3} + a_{n-4} + a_{n-5}

This recurrence has characteristic polynomial:
x^5 = x^4 + x^2 + x + 1
i.e., x^5 - x^4 - x^2 - x - 1 = 0

We need to verify:
1. The recurrence is exact (check on computed data)
2. Compute the dominant root (growth rate of m(P_n))
3. This root is less than sqrt(3)

Also: investigate whether the recurrence can be proven directly from 
the structure of Roman dominating functions on paths.
"""

import math
import numpy as np
from count_minimal_rdf import count_minimal_rdfs_subset_v2
import networkx as nx


def verify_recurrence():
    """Verify a_n = a_{n-1} + a_{n-3} + a_{n-4} + a_{n-5} exactly."""
    print("=" * 70)
    print("VERIFICATION: Recurrence a_n = a_{n-1} + a_{n-3} + a_{n-4} + a_{n-5}")
    print("=" * 70)
    
    # Compute m(P_n) for n = 1 to 24
    vals = {}
    for n in range(1, 25):
        G = nx.path_graph(n)
        vals[n] = count_minimal_rdfs_subset_v2(G)
    
    print("\nDirect computation:")
    for n in sorted(vals.keys()):
        print(f"  a({n:2d}) = {vals[n]:10d}")
    
    print("\nRecurrence check:")
    all_match = True
    for n in range(6, 25):
        pred = vals[n-1] + vals[n-3] + vals[n-4] + vals[n-5]
        match = pred == vals[n]
        if not match:
            all_match = False
        print(f"  a({n:2d}) = {vals[n]:10d}, "
              f"a({n-1})+a({n-3})+a({n-4})+a({n-5}) = "
              f"{vals[n-1]}+{vals[n-3]}+{vals[n-4]}+{vals[n-5]} = {pred}, "
              f"{'OK' if match else 'FAIL'}")
    
    if all_match:
        print("\n*** RECURRENCE VERIFIED EXACTLY for n = 6, ..., 24 ***")
    else:
        print("\n*** RECURRENCE FAILS ***")
    
    return vals, all_match


def characteristic_polynomial():
    """
    Analyze the characteristic polynomial x^5 - x^4 - x^2 - x - 1 = 0.
    """
    print("\n" + "=" * 70)
    print("CHARACTERISTIC POLYNOMIAL: x^5 - x^4 - x^2 - x - 1 = 0")
    print("=" * 70)
    
    # Find roots
    coeffs = [1, -1, 0, -1, -1, -1]  # x^5 - x^4 + 0*x^3 - x^2 - x - 1
    roots = np.roots(coeffs)
    
    print("\nRoots:")
    for i, r in enumerate(roots):
        print(f"  r_{i+1} = {r:.10f}  (|r| = {abs(r):.10f})")
    
    # Dominant root
    dominant = max(roots, key=abs)
    print(f"\nDominant root: {dominant.real:.10f}")
    print(f"|dominant root| = {abs(dominant):.10f}")
    print(f"sqrt(3) = {math.sqrt(3):.10f}")
    print(f"Dominant root < sqrt(3): {abs(dominant) < math.sqrt(3)}")
    print(f"Gap: sqrt(3) - dominant = {math.sqrt(3) - abs(dominant):.10f}")
    
    # Verify it's a root
    val = np.polyval(coeffs, dominant)
    print(f"\nVerification: p(dominant) = {val:.2e}")
    
    return roots


def search_oeis():
    """Check if the sequence is in OEIS."""
    print("\n" + "=" * 70)
    print("OEIS CHECK")
    print("=" * 70)
    
    seq = [1, 3, 4, 7, 12, 20, 34, 57, 96, 162, 273, 460, 775, 1306, 2201]
    print(f"Sequence: {seq}")
    print("Search OEIS for: 1,3,4,7,12,20,34,57,96,162,273")
    print("(Manual search needed at https://oeis.org/search?q=1,3,4,7,12,20,34,57,96)")


def decompose_path_rdfs():
    """
    Understand WHY the recurrence holds by analyzing the structure of 
    minimal RDFs on paths.
    
    For a path v_1 - v_2 - ... - v_n:
    - The value of v_n can be 0, 1, or 2
    - But it must be consistent with minimality
    
    Case analysis for the last vertex v_n:
    
    Case 1: f(v_n) = 0
      Then v_n must have a neighbor with value 2. The only neighbor is v_{n-1}.
      So f(v_{n-1}) = 2.
      For minimality of v_{n-1}: v_{n-1} must have a private zero-neighbor.
      v_n is zero and its only S-neighbor is v_{n-1}, so v_n IS the private zero.
      Now, v_{n-2}'s assignment is constrained by whether it's zero or not:
      
    Case 2: f(v_n) = 1
      v_n has no neighbor assigned 2 (otherwise we could reduce to 0).
      Wait, minimality says: reducing v_n from 1 to 0 must break the RDF.
      If f(v_n) = 1 -> 0: then v_n = 0 needs a neighbor with value 2.
      So it breaks iff v_{n-1} != 2. Hence f(v_{n-1}) != 2.
      
    Case 3: f(v_n) = 2
      For minimality: reducing from 2 to 1 must break the RDF.
      Reducing v_n from 2 to 1: any neighbor of v_n that had value 0 and 
      was relying on v_n being 2 loses its dominator.
      So v_n must have a neighbor with value 0 whose only neighbor in S is v_n.
      The only neighbor of v_n is v_{n-1}. So either:
        - f(v_{n-1}) = 0 and v_{n-1}'s only S-neighbor is v_n.
        OR
        - v_n has no such private zero (but then it's not minimal -> contradiction)
      
      Wait, but v_n has only one neighbor (v_{n-1}), so v_n's only potential 
      private zero-neighbor is v_{n-1}. So f(v_{n-1}) = 0 is required.
      But also, v_{n-1}'s only S-neighbor must be v_n, which means v_{n-2} is 
      not in S (not assigned 2). So f(v_{n-2}) != 2.
    
    This case analysis should lead to the recurrence!
    """
    print("\n" + "=" * 70)
    print("STRUCTURAL DECOMPOSITION: Why the recurrence holds for paths")
    print("=" * 70)
    
    # List all minimal RDFs on P_n and categorize by last few values
    for n in range(2, 9):
        G = nx.path_graph(n)
        from count_minimal_rdf import list_minimal_rdfs_brute
        rdfs = list_minimal_rdfs_brute(G)
        
        print(f"\nP_{n} ({len(rdfs)} minimal RDFs):")
        
        # Group by (f(n-1), f(n-2)) - last two values
        from collections import Counter
        if n >= 2:
            tail_patterns = Counter()
            for f in rdfs:
                if n >= 3:
                    tail = (f[n-3], f[n-2], f[n-1])
                else:
                    tail = (f[n-2], f[n-1])
                tail_patterns[tail] += 1
            
            print(f"  Tail patterns (last {'3' if n >= 3 else '2'} values) -> count:")
            for pattern in sorted(tail_patterns.keys()):
                print(f"    {pattern}: {tail_patterns[pattern]}")
        
        # Group by last 5 values
        if n >= 5:
            tail5 = Counter()
            for f in rdfs:
                tail = tuple(f[n-5+i] for i in range(5))
                tail5[tail] += 1
            
            print(f"  Last 5 values -> count (top 10):")
            for pattern, cnt in tail5.most_common(10):
                print(f"    {pattern}: {cnt}")


def prove_path_recurrence():
    """
    Attempt to prove the recurrence for paths via case analysis.
    
    Define state at position i as the "signature" that determines how the 
    remaining path i+1, ..., n can be filled.
    
    For a path v_1 - v_2 - ... - v_n, the signature at position i depends on:
    - f(v_i): the value at position i (0, 1, or 2)
    - Whether v_i has been "satisfied" (its minimality constraint is met)
    - Whether v_i needs a private zero-neighbor from the right
    
    Let's define states more carefully:
    
    After assigning values to v_1, ..., v_i, the state captures:
    - f(v_i): value at last assigned vertex
    - Whether v_i assigned 2 still needs a private zero-neighbor
    - Whether v_i assigned 0 is properly dominated
    
    State = (last_value, needs_private_zero, is_dominated)
    
    But we can simplify using the path structure.
    """
    print("\n" + "=" * 70)
    print("PROOF ATTEMPT: Transfer matrix method for paths")
    print("=" * 70)
    
    # Use transfer matrix: define states based on the last few vertices
    # State = tuple of last k values, with validity constraints
    
    # For each possible "state" at position i, count transitions to position i+1
    
    # A state needs to encode enough information to determine validity of extensions.
    # For paths, the relevant information at position i is:
    #   - f(v_i): 0, 1, or 2
    #   - For f(v_i) = 0: is v_i dominated? (has a neighbor with value 2)
    #     On a path, v_i's neighbors are v_{i-1} (already assigned) and v_{i+1} (not yet).
    #     If f(v_{i-1}) = 2, then v_i is already dominated.
    #     If f(v_{i-1}) != 2, then v_i NEEDS v_{i+1} = 2.
    #   - For f(v_i) = 2: does v_i already have a private zero-neighbor?
    #     v_i's already-assigned neighbor is v_{i-1}.
    #     If f(v_{i-1}) = 0 and v_{i-1}'s only S-neighbor is v_i, then YES.
    #     Otherwise, v_i needs v_{i+1} = 0 with v_i as its only S-neighbor.
    
    # State encoding:
    #   (val, need_two, need_private)
    # val: value of current vertex (0, 1, 2)
    # need_two: True if current vertex is 0 and not yet dominated (needs right neighbor = 2)
    # need_private: True if current vertex is 2 and doesn't yet have a private zero
    
    # Actually let me think about this with TWO vertices of state
    # since the private zero condition depends on the relationship between adjacent vertices
    
    # State = (f(v_{i-1}), f(v_i), constraint_flag)
    # where constraint_flag encodes pending obligations
    
    # Let me just build the transfer matrix empirically
    
    print("\nBuilding transfer matrix from computed data...")
    
    from count_minimal_rdf import list_minimal_rdfs_brute
    
    # For each n, list all minimal RDFs and identify the "states"
    # State at position i = (f(v_i), f(v_{i-1}), some flags)
    
    # Actually, let's just list all valid length-2 suffixes and see how they 
    # relate to m(P_{n-1}), m(P_{n-2}), etc.
    
    for n in range(2, 9):
        G = nx.path_graph(n)
        rdfs = list_minimal_rdfs_brute(G)
        
        # Group by value of last vertex
        by_last = {0: 0, 1: 0, 2: 0}
        for f in rdfs:
            by_last[f[n-1]] += 1
        
        print(f"\nP_{n} (m={len(rdfs)}): by last value: {by_last}")
        
        if n >= 2:
            by_last2 = {}
            for f in rdfs:
                key = (f[n-2], f[n-1])
                by_last2[key] = by_last2.get(key, 0) + 1
            print(f"  by last 2 values: {dict(sorted(by_last2.items()))}")
        
        if n >= 3:
            by_last3 = {}
            for f in rdfs:
                key = (f[n-3], f[n-2], f[n-1])
                by_last3[key] = by_last3.get(key, 0) + 1
            print(f"  by last 3 values: {dict(sorted(by_last3.items()))}")


if __name__ == "__main__":
    vals, verified = verify_recurrence()
    roots = characteristic_polynomial()
    search_oeis()
    decompose_path_rdfs()
    prove_path_recurrence()
