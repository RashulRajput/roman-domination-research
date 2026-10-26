# Structural proof attempts

## Exact rooted-state recurrence

The count \(m(T)\) is the number of subsets \(S\subseteq V(T)\) such that
each \(s\in S\) has an external private zero \(u\notin S\) with
\(u\in N(s)\) and \(N(u)\cap S=\{s\}\). This is the established
minimal-RDF/\(V_2\) characterization.

Root \(T\) at \(r\). For a rooted subtree \(T_v\), define
\[
D_v^p(s,c,q)
\]
to count assignments of \(S\cap V(T_v)\) with the following boundary data:

- \(p\in\{0,1\}\): whether the parent of \(v\) belongs to \(S\);
- \(s\in\{0,1\}\): whether \(v\in S\);
- \(c=\min(2,\#\{\text{selected children of }v\})\);
- \(q=1\): \(v\in S\) and it has no private zero among its children, so it
  still needs its parent to witness it.

All selected vertices strictly below \(v\) already have a private zero, or
their one possible unresolved requirement has been recorded by \(q\) at
their subtree root.

For each child \(w\) of \(v\), choose a state
\((s_w,c_w,q_w)\) counted by \(D_w^s\). Aggregate these choices by
\[
c=\min(2,\sum_w s_w),\qquad
R=\bigvee_w q_w,\qquad
H=\bigvee_w [s_w=0\text{ and }c_w=0].
\]
Here \(R\) says that some selected child still needs \(v\) as its private
zero. Such a child can be rescued exactly when \(v\) is zero and has that
child as its unique selected neighbor:
\[
R=1\ \Longrightarrow\ (s,p,c)=(0,0,1).
\]
Reject the combination if this implication fails. Otherwise put
\[
q=[s=1\text{ and }H=0]
\]
and add the product of the child-state multiplicities to
\(D_v^p(s,c,q)\).
For the root, no parent can rescue it, so
\[
m(T)=\sum_{s\in\{0,1\}}\sum_{c=0}^2 D_r^0(s,c,0).
\]

### Why this recurrence is exact

Assume the tables for the children are exact. A selected child with \(q_w=1\)
has no private zero below it; its only remaining possible witness is \(v\).
The conditions \(s=0\), \(p=0\), and \(c=1\) are precisely that \(v\) is a
zero vertex adjacent to that selected child and to no other selected vertex.
For a selected \(v\), a child \(w\) is a private zero for \(v\) precisely
when \(w\notin S\) and none of \(w\)'s children is selected, which is the
condition \(s_w=0,c_w=0\). Thus \(H\) records exactly whether a child has
already witnessed \(v\). The recurrence resolves every selected vertex
except a possible root requirement recorded by \(q\). Induction from the
leaves proves the tables, and the root sum counts exactly the admissible
sets. The implementation in
[tree_dp_recurrence.py](results/path_extremal/tree_dp_recurrence.py) is the
audited sparse-state version. Array and shape-memoized implementations were
cross-checked against it on all 987 unlabeled trees through order 12.

## Tested transformations that fail

The local operations below preserve the number of vertices and produce
trees. Each count was computed first by the rooted DP and then checked by
an independent exhaustive subset/private-zero counter.

### Leaf-to-leaf transfer

Proposed lemma: if \(\ell\) is a leaf adjacent to \(v\), and \(x\ne\ell,v\)
is another leaf, replacing \(v\ell\) by \(x\ell\) never decreases \(m\).
This would be a natural path-smoothing move. It is false, first at order 6.

- Before: graph6 EqD?; edges
  \(\{01,03,05,12,34\}\); \(m=17\), with subset-size histogram
  \((1,6,8,2,0,0,0)\).
- Move the leaf \(2\) from \(1\) to leaf \(4\).
- After: graph6 EaL?; edges
  \(\{01,03,05,24,34\}\); \(m=15\), with histogram
  \((1,6,8,0,0,0,0)\).

The exhaustive move test found no decrease on any tree of orders 3, 4, or
5; it tested 600 moves in total over orders 3–8. The exact records are in
[leaf_transfer_order_8.json](results/path_extremal/leaf_transfer_order_8.json).

### Splitting a long spider arm

Proposed lemma: replacing one spider leg of length \(r\ge3\) by legs of
lengths \(2\) and \(r-2\) never decreases \(m\). This would create more
length-two branches toward the odd-order candidate. It is false first at
order 5:

- Leg lengths \((1,3)\) give \(P_5\), graph6 DpC, with \(m=12\) and
  histogram \((1,5,6,0,0,0)\).
- Replacing the length-three leg by lengths \(2,1\) gives leg lengths
  \((1,1,2)\), graph6 DsC, with \(m=9\) and histogram
  \((1,5,3,0,0,0)\).

All integer partitions of \(n-1\) were tested at each order \(4\le n\le19\).
The complete test is
[test_spider_arm_split.py](results/path_extremal/test_spider_arm_split.py),
with counts in
[spider_arm_split_results.json](results/path_extremal/spider_arm_split_results.json).

### Balancing two spider legs

Proposed lemma: for two leg lengths \(a\ge b+2\), replacing \((a,b)\) by
\((a-1,b+1)\) never decreases \(m\). It is false first at order 9:

- Legs \((1,1,2,4)\), graph6 HsE?GC@, have \(m=57\) and histogram
  \((1,9,25,19,3,0,0,0,0,0)\).
- Transfer one edge from the length-four leg to the length-two leg, giving
  \((1,1,3,3)\), graph6 HsCK?C@, with \(m=56\) and histogram
  \((1,9,25,21,0,0,0,0,0,0)\).

Every integer partition of \(n-1\) and every such balancing move was tested
for \(4\le n\le19\). The exhaustive records are in
[spider_leg_balance_results.json](results/path_extremal/spider_leg_balance_results.json).

These counterexamples rule out the stated monotonicity lemmas. They do not
rule out more carefully conditioned transformations whose hypotheses
control the boundary states in the recurrence.

## Previously attempted scalar inductions

The scalar leaf-deletion inequality
\[
m(T)\le m(T-v)+m(P_n)-m(P_{n-1})
\]
fails on \(T_3\) at order 7: \(m(T_3)=34\), while deleting any leaf gives
17 and the path increment is 14, producing only \(31\) on the right.
Likewise the proposed scalar recurrence
\[
C(n)\le C(n-1)+m(P_n)-m(P_{n-1})
\]
fails at order 11: \(274>162+(273-162)=273\).
The rooted witness states retain information that these scalar inequalities
discard.

## Proof status

The recurrence is an exact counting theorem and supports a complete finite
census. No local transformation tested here yields an all-order reduction
to paths or subdivided stars. No pointwise formula for \(C(n)\), structural
characterization of all extremizers, or tree-specific upper bound sharper
than the published forest bound has been proved.
