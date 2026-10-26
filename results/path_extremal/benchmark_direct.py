import time
import networkx as nx
from path_extremal_search import count_direct, count_subset

for n in (10, 11, 12):
    graph = next(iter(nx.generators.nonisomorphic_trees(n)))
    started = time.perf_counter()
    direct = count_direct(graph)
    elapsed = time.perf_counter() - started
    subset = count_subset(graph)
    print({"n": n, "direct": direct, "subset": subset, "seconds": round(elapsed, 3)})
