import json
from pathlib import Path

data = json.loads((Path(__file__).parent / "tree_census_through_12.json").read_text(encoding="utf-8"))
for row in data["orders"]:
    print(f"n={row['order']} C={row['C_n']} classes={row['extremizer_class_count']} T={row['T_k'] and row['T_k']['is_extremal']}")
    for i, tree in enumerate(row["extremizers"], 1):
        print(f"  class {i}: graph6={tree['graph6']} edges={tree['edges']} prufer={tree['prufer_sequence']}")
