#!/usr/bin/env python3
"""Record the size and prefix maximum of an intentionally incomplete run."""

import gzip
import json
from pathlib import Path


path = Path(__file__).resolve().parent / "tree_census_n20_partial_oldmemo.jsonl.gz"
recovered = path.with_name("tree_census_n20_partial_oldmemo_recovered.jsonl.gz")
count = 0
maximum = -1
maximizers = []
try:
    with gzip.open(path, "rt", encoding="utf-8") as stream, gzip.open(
        recovered, "wt", encoding="utf-8", compresslevel=6
    ) as clean:
        for line in stream:
            record = json.loads(line)
            clean.write(json.dumps(record, separators=(",", ":")) + "\n")
            count += 1
            if record["m_dp"] > maximum:
                maximum = record["m_dp"]
                maximizers = [record["graph6"]]
            elif record["m_dp"] == maximum:
                maximizers.append(record["graph6"])
except EOFError:
    # Ctrl-C may have left the gzip footer unwritten; complete rows remain
    # independently parseable up to that point.
    pass
result = {
    "order": 20,
    "records_in_canonical_generator_prefix": count,
    "prefix_maximum_only_not_C20": maximum,
    "prefix_maximizer_graph6": maximizers,
    "exhaustive": False,
    "stopped_reason": "The unbounded rooted-shape memo table exceeded approximately 1.1 GB during the exploratory run. Replaced by cache-bounded DP.",
    "data_file": path.name,
    "recovered_complete_rows_file": recovered.name,
}
out = path.with_suffix(".summary.json")
out.write_text(json.dumps(result, indent=2), encoding="utf-8")
path.with_suffix(".log").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, indent=2))
