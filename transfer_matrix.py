"""
Transfer matrix proof for paths: derive the recurrence from first principles.

For a path P_n = v_1 - v_2 - ... - v_n, we define a state machine that 
processes vertices left to right and tracks the minimal RDFs.

STATE DEFINITION:
After processing vertices v_1, ..., v_i, the state captures ALL information
needed to determine valid extensions to v_{i+1}, ..., v_n.

For a path, the relevant state at position i is:
  (f(v_i), obligation)

where obligation encodes:
  - 'D': v_i has f(v_i) = 0 and is NOT YET DOMINATED (needs v_{i+1} = 2)
  - 'P': v_i has f(v_i) = 2 and does NOT YET have a private zero-neighbor
         (needs v_{i+1} = 0 with v_i as its only S-neighbor)
  - 'N': no pending obligation

But we also need to know if v_i = 2 when checking if v_{i+1} = 0 can have
v_i as its ONLY S-neighbor. So the state needs f(v_i).

More precisely:
  State = (f(v_i), pending_domination, pending_private)
  
  pending_domination: True if v_i = 0 and v_{i-1} != 2
  pending_private: True if v_i = 2 and v_i doesn't have a private zero from left
  
But wait - we need to know f(v_i) to determine transitions. Let me think again...

Actually, the state is determined by examining the RIGHTMOST unresolved obligations.

Let me think about this differently: use a state that captures the "boundary condition"
at the right end of the already-assigned portion.
"""

import itertools
import networkx as nx
from count_minimal_rdf import list_minimal_rdfs_brute, count_minimal_rdfs_subset_v2
from collections import defaultdict


def build_transfer_matrix():
    """
    Build the transfer matrix for minimal RDFs on paths.
    
    We process vertices left to right. After assigning v_i, we maintain a state.
    
    State encoding:
    We need to track:
    1. f(v_i) - the value assigned to the current vertex
    2. Whether v_i = 0 needs future domination (v_i = 0 and no neighbor with value 2 yet)
       On a path, if f(v_{i-1}) = 2, then v_i is dominated. Otherwise, v_i needs v_{i+1} = 2.
    3. Whether v_i = 2 still needs a private zero-neighbor
       v_i has at most 2 neighbors: v_{i-1} and v_{i+1}.
       If v_{i-1} = 0 and v_{i-1}'s only S-neighbor is v_i: private zero from left.
       Otherwise: needs private zero from right (v_{i+1} = 0 with only S-neighbor being v_i).
    
    State: (val_i, needs_dom, needs_private)
    
    But we also need to know if the NEXT vertex being 0 would make v_i its only
    S-neighbor. For that, we need to know if v_i is assigned 2.
    
    Actually, val_i already tells us this.
    
    Let me redefine more carefully:
    
    State = a tuple capturing:
      - value of v_i: 0, 1, or 2
      - open_zero: True if v_i is assigned 0 and has no left neighbor with value 2
                   (so v_{i+1} MUST be 2)
      - open_two: True if v_i is assigned 2 and has no private zero-neighbor from the left
                  (so v_i needs a private zero from the right, OR v_{i+1} provides it)
    
    A state is TERMINAL (can end the path) only if:
      - No open obligations
      - Additionally, for v_n with value 1: reducing to 0 must fail.
        On a path, v_n has only v_{n-1} as neighbor.
        Reducing v_n from 1 to 0: v_n becomes 0, needs neighbor with 2.
        Fails iff v_{n-1} != 2. So v_n can be 1 as final only if v_{n-1} != 2.
        But we already encoded this... Actually the minimality of value-1 vertices:
        
    Wait, I need to reconsider. For vertices with value 1:
    Minimality requires that reducing from 1 to 0 breaks the RDF.
    Reducing v_i from 1 to 0: v_i now 0, needs a neighbor with 2.
    Breaks iff v_i has no neighbor with value 2.
    
    So f(v_i) = 1 is minimal IFF no neighbor of v_i has value 2.
    On a path: f(v_i) = 1 is minimal iff f(v_{i-1}) != 2 and f(v_{i+1}) != 2.
    
    This is an important constraint!
    
    For vertices with value 2:
    Minimality requires that reducing from 2 to 1 breaks the RDF.
    Reducing v_i from 2 to 1: any neighbor of v_i with value 0 that relied on v_i 
    being 2 loses its dominator.
    Breaks iff v_i has a PRIVATE zero-neighbor: a neighbor u with f(u) = 0 whose 
    ONLY neighbor with value 2 is v_i.
    
    So the state must track:
    - The value of v_i
    - Whether v_i has unresolved obligations
    - Constraints on v_{i+1} imposed by minimality of v_i
    """
    print("=" * 70)
    print("TRANSFER MATRIX CONSTRUCTION")
    print("=" * 70)
    
    # Let me define states empirically by examining all minimal RDFs on paths
    # and identifying what "boundary information" is needed.
    
    # For each minimal RDF on P_n, record the state after each prefix
    
    # State after processing v_1, ..., v_i:
    # - f(v_i): value at position i
    # - forced_next_two: True if v_i = 0 and v_{i-1} != 2 (v_{i+1} must be 2)
    # - v_i_needs_private: True if v_i = 2 and no private zero from left
    # - v_i_is_two: needed for checking if v_{i+1} = 0's only S-neighbor
    
    # Actually, I realize the state is:
    # (f(v_i), forced_next_two, v_i_needs_private)
    # This is a tuple in {0,1,2} x {T,F} x {T,F}
    # But not all combinations are valid.
    
    # Let's enumerate by brute force on small paths and see which states arise
    
    for n in range(2, 10):
        G = nx.path_graph(n)
        rdfs = list_minimal_rdfs_brute(G)
        
        # For each RDF, compute the state sequence
        state_counts = defaultdict(int)
        
        for f_dict in rdfs:
            f = [f_dict[i] for i in range(n)]
            
            # Compute state after each position
            for i in range(n):
                val = f[i]
                
                # Is there a pending need for v_{i+1} = 2?
                forced_two = False
                if val == 0:
                    # Check if v_i is dominated from the left
                    if i > 0 and f[i-1] == 2:
                        forced_two = False  # already dominated
                    else:
                        forced_two = True  # needs v_{i+1} = 2
                
                # Does v_i = 2 need a private zero from the right?
                needs_private = False
                if val == 2:
                    # Check if v_i already has a private zero from the left
                    has_private_left = False
                    if i > 0 and f[i-1] == 0:
                        # v_{i-1} = 0, check if v_i is v_{i-1}'s ONLY S-neighbor
                        # v_{i-1}'s neighbors on path: v_{i-2} (if exists) and v_i
                        only_s_nbr = True
                        if i >= 2 and f[i-2] == 2:
                            only_s_nbr = False
                        if only_s_nbr:
                            has_private_left = True
                    
                    if not has_private_left:
                        needs_private = True
                
                state = (val, forced_two, needs_private)
                
                if i == n - 1:
                    state_counts[('FINAL', state)] += 1
                else:
                    state_counts[('MID', i, state)] += 1
        
        # Count distinct states
        final_states = {s for (kind, *rest), cnt in state_counts.items() 
                       if kind == 'FINAL' for s in [rest[0] if isinstance(rest[0], tuple) else rest]}
        
        mid_states = set()
        for (kind, *rest), cnt in state_counts.items():
            if kind == 'MID':
                mid_states.add(rest[1])  # The state tuple
        
        print(f"\nP_{n} (m={len(rdfs)}):")
        print(f"  Final states:")
        for (kind, *rest), cnt in sorted(state_counts.items()):
            if kind == 'FINAL':
                state = rest[0]
                print(f"    {state}: {cnt}")
        
        all_mid_states = set()
        for (kind, *rest), cnt in sorted(state_counts.items()):
            if kind == 'MID':
                all_mid_states.add(rest[1])
        print(f"  Mid states seen: {sorted(all_mid_states)}")


def build_explicit_transfer_matrix():
    """
    Build the transfer matrix T where T[s1][s2] = 1 if state s1 can transition to s2.
    
    States: (val, forced_two, needs_private) where
      val in {0, 1, 2}
      forced_two in {True, False}
      needs_private in {True, False}
    
    But we need to be more careful. Let me re-derive.
    """
    print("\n" + "=" * 70)
    print("EXPLICIT TRANSFER MATRIX")
    print("=" * 70)
    
    # States at position i (AFTER assigning v_i):
    # Encoded as (val_i, must_next_be_two, val_i_two_needs_private)
    #
    # must_next_be_two: v_i = 0 and not dominated yet -> v_{i+1} MUST be 2
    # val_i_two_needs_private: v_i = 2 and no private zero from left -> needs from right
    #
    # Valid states:
    # (0, True, False)  : v_i = 0, undominated, needs v_{i+1} = 2
    # (0, False, False) : v_i = 0, dominated by v_{i-1} = 2
    # (1, False, False) : v_i = 1, no obligations
    # (2, False, False) : v_i = 2, already has private zero
    # (2, False, True)  : v_i = 2, needs private zero from right
    
    # Invalid: (0, True, True) - can't be 0 and 2 simultaneously
    # Invalid: (1, True, *) - forced_two only for val=0
    # Invalid: (0, False, True) - needs_private only for val=2
    # Invalid: (1, False, True) - needs_private only for val=2
    
    # Simplified: 5 states
    # S0u: val=0, undominated (needs next = 2)
    # S0d: val=0, dominated (left neighbor was 2)
    # S1:  val=1, no obligations
    # S2p: val=2, has private zero
    # S2n: val=2, needs private zero from right
    
    states = ['S0u', 'S0d', 'S1', 'S2p', 'S2n']
    
    # Transition from state at position i to state at position i+1
    # When assigning v_{i+1}, we need to check:
    # 1. Constraints from previous state
    # 2. Minimality constraints on v_{i+1}
    # 3. New obligations created
    
    transitions = defaultdict(list)
    
    # From S0u (val_i = 0, undominated): v_{i+1} MUST be 2
    # v_{i+1} = 2: 
    #   - v_i becomes dominated
    #   - v_{i+1} = 2 needs private zero.
    #     Can v_i be private zero for v_{i+1}? v_i = 0, and v_{i+1} is its only S-neighbor
    #     (since v_{i-1} was the one before, and v_i being undominated means v_{i-1} != 2)
    #     Wait: v_i's only neighbors are v_{i-1} and v_{i+1}. 
    #     v_i is assigned 0. v_{i+1} = 2. Is v_{i+1} v_i's only S-neighbor?
    #     v_{i-1}: was it assigned 2? We're in state S0u, which means v_i = 0 
    #     and v_{i-1} != 2 (otherwise v_i would be dominated). So f(v_{i-1}) != 2.
    #     Therefore v_i's only S-neighbor IS v_{i+1}. So v_i is a private zero for v_{i+1}.
    #   -> State: S2p (val=2, has private zero)
    transitions['S0u'].append('S2p')
    
    # From S0d (val_i = 0, dominated): v_{i-1} = 2, v_i = 0
    # v_{i+1} can be 0, 1, or 2, subject to constraints.
    # But wait: if v_{i+1} = 1, then for minimality of v_{i+1}: 
    #   v_{i+1} has no neighbor with value 2.
    #   v_i = 0, v_{i+2} = ??? (unknown). 
    #   Left neighbor of v_{i+1} is v_i = 0 != 2. OK for now, 
    #   but v_{i+2} must not be 2 either (will be handled in next step).
    #   Wait, minimality of v_{i+1} = 1 means that reducing to 0 must break RDF.
    #   v_{i+1} = 0 needs a neighbor with 2. Left neighbor v_i = 0 != 2.
    #   So it breaks iff right neighbor v_{i+2} != 2. 
    #   This is a FUTURE constraint. So f(v_{i+1}) = 1 imposes that v_{i+2} != 2.
    #   We need to track this!
    
    # Hmm, this means our state space needs to also track whether the current 
    # vertex is 1 (which constrains the next to be != 2).
    
    # Let me add this. If val_i = 1, then v_{i+1} != 2 (for minimality of v_i).
    
    # Revised state: (val_i, forced_next_two, needs_private, forbid_next_two)
    # But forced_next_two and forbid_next_two are contradictory!
    # 
    # Actually, forced_next_two only applies when val_i = 0 and undominated.
    # forbid_next_two only applies when val_i = 1.
    # They never coexist.
    
    # REVISED STATES:
    # S0u: val=0, undominated -> v_{i+1} MUST be 2
    # S0d: val=0, dominated by left -> v_{i+1} can be anything (but constraints apply)
    # S1:  val=1 -> v_{i+1} MUST NOT be 2 (for minimality of v_i)
    # S2p: val=2, has private zero -> v_{i+1} can be anything
    # S2n: val=2, needs private zero from right -> v_{i+1} MUST be 0 
    #      (and v_{i+1}'s only S-neighbor must be v_i, meaning v_{i+2} != 2)
    #      Wait: v_{i+1} = 0 and its only S-neighbor is v_i. 
    #      v_{i+1}'s neighbors are v_i and v_{i+2}. For v_i to be v_{i+1}'s 
    #      only S-neighbor, we need v_{i+2} != 2.
    #      But that constraint is on the NEXT transition, not this one!
    #      So the state becomes: S0d_restricted? No...
    #      Actually when v_{i+1} = 0, it transitions to S0d (dominated by v_i = 2).
    #      Then from S0d, we just need v_{i+2} != 2 for the private zero condition.
    #      But that's an additional constraint!
    
    # This is getting complex. Let me add another dimension:
    # restrict_next_not_two: True if v_{i+1} must NOT be 2
    
    # REVISED STATE: (val_i, restrict_next)
    # restrict_next = 'must_two' | 'no_two' | 'free' | 'must_zero_no_two'
    #
    # Let me simplify to just the relevant combinations.
    
    print("\nLet me enumerate states empirically from P_8...")
    
    G = nx.path_graph(8)
    rdfs = list_minimal_rdfs_brute(G)
    
    # For each RDF, track the full state at each position
    all_states = set()
    all_transitions = defaultdict(set)
    initial_states = defaultdict(int)
    final_states_count = defaultdict(int)
    
    for f_dict in rdfs:
        f = [f_dict[i] for i in range(8)]
        
        prev_state = None
        for i in range(8):
            val = f[i]
            
            # Determine the constraint this vertex places on the NEXT vertex
            constraint = 'free'
            
            if val == 0:
                # Is v_i dominated from the left?
                dominated = (i > 0 and f[i-1] == 2)
                if not dominated:
                    constraint = 'must_two'  # next MUST be 2
                # If dominated: depends on whether left (v_{i-1} = 2) needed 
                # v_i as private zero AND v_i's only S-neighbor must be v_{i-1}
                # For that, v_{i+1} must not be 2.
                # Check: was v_{i-1} = 2 needing private zero from v_i?
                if dominated and i > 0:
                    # v_{i-1} = 2. Did it need v_i as private zero?
                    # v_{i-1} had private zero from left?
                    if i >= 2 and f[i-2] == 0:
                        # v_{i-2} = 0, check if v_{i-2}'s only S-neighbor was v_{i-1}
                        v_i2_only_s = True
                        if i >= 3 and f[i-3] == 2:
                            v_i2_only_s = False
                        if v_i2_only_s:
                            pass  # v_{i-1} already has private zero from left
                        else:
                            # v_{i-1} needs private from right = v_i
                            # For v_i to be private: v_i = 0 and only S-nbr is v_{i-1}
                            # => v_{i+1} must not be 2
                            constraint = 'no_two'
                    elif i == 1:
                        # v_0 = 2. Its only neighbor is v_1 = v_i.
                        # v_0 needs private zero. v_1 = 0. 
                        # v_1's S-neighbors: v_0 = 2 (yes). v_2 = ?
                        # For v_1 to be private zero of v_0: v_2 != 2
                        if f[0] == 2:
                            constraint = 'no_two'  # v_{i+1} can't be 2
            
            elif val == 1:
                # For minimality: v_{i+1} must not be 2
                # (reducing v_i from 1 to 0 must fail; it fails iff no neighbor is 2)
                # Left neighbor already assigned. If left = 2, then reducing to 0 
                # would succeed -> v_i = 1 would NOT be minimal!
                # So if we're here, left != 2 (otherwise this isn't a valid minimal RDF).
                # For the right: v_{i+1} must NOT be 2.
                constraint = 'no_two'
            
            elif val == 2:
                # Does v_i have a private zero from the left?
                has_priv_left = False
                if i > 0 and f[i-1] == 0:
                    # Check: is v_{i-1}'s only S-neighbor v_i?
                    only_s = True
                    if i >= 2 and f[i-2] == 2:
                        only_s = False
                    if only_s:
                        has_priv_left = True
                
                if not has_priv_left:
                    # Need private zero from right: v_{i+1} = 0 and v_{i+1}'s
                    # only S-neighbor is v_i => v_{i+2} != 2
                    constraint = 'must_zero'  # next must be 0
            
            state = (val, constraint)
            all_states.add(state)
            
            if i == 0:
                initial_states[state] += 1
            if i == 7:
                final_states_count[state] += 1
            
            if prev_state is not None:
                all_transitions[(prev_state, state)] = True
            
            prev_state = state
    
    print(f"\nStates observed: {sorted(all_states)}")
    print(f"\nTransitions:")
    for (s1, s2) in sorted(all_transitions.keys()):
        print(f"  {s1} -> {s2}")
    print(f"\nInitial states: {dict(initial_states)}")
    print(f"\nFinal states: {dict(final_states_count)}")
    print(f"\nTotal RDFs: {sum(final_states_count.values())}")
    
    return all_states, all_transitions


if __name__ == "__main__":
    build_transfer_matrix()
    build_explicit_transfer_matrix()
