"""Cross-check every stored order 13--20 count with the array-based tree DP.

The census values were produced by the dictionary/bounded-memo DP. This uses
the separately implemented fixed-array DP and streams the larger JSON files so
the full census need not be loaded into memory.
"""

from __future__ import annotations

import gzip
import argparse
import json
import time
from pathlib import Path
from typing import Iterator

import networkx as nx

from fast_tree_dp import count_tree_dp_fast


HERE = Path(__file__).resolve().parent
EXPECTED = {
    13: 1_301,
    14: 3_159,
    15: 7_741,
    16: 19_320,
    17: 48_629,
    18: 123_867,
    19: 317_955,
    20: 823_065,
}


def iter_json_array(path: Path, key: str) -> Iterator[dict]:
    """Yield objects from one top-level JSON array without loading the file."""
    decoder = json.JSONDecoder()
    marker = f'"{key}"'
    with path.open("r", encoding="utf-8") as source:
        buffer = ""
        while marker not in buffer:
            chunk = source.read(1 << 20)
            if not chunk:
                raise ValueError(f"array {key!r} not found in {path}")
            buffer += chunk
        pos = buffer.index(marker) + len(marker)
        while True:
            while pos < len(buffer) and (buffer[pos].isspace() or buffer[pos] in ":[,"):
                pos += 1
            if pos < len(buffer) and buffer[pos] == "]":
                return
            try:
                item, end = decoder.raw_decode(buffer, pos)
            except json.JSONDecodeError:
                chunk = source.read(1 << 20)
                if not chunk:
                    raise
                buffer = buffer[pos:] + chunk
                pos = 0
                continue
            yield item
            pos = end
            if pos > (1 << 20):
                buffer = buffer[pos:]
                pos = 0


def census_records() -> Iterator[dict]:
    for name in (
        "tree_census_extension_through_16.json",
        "tree_census_extension_through_18.json",
    ):
        yield from iter_json_array(HERE / name, "trees")
    for n in (19, 20):
        with gzip.open(HERE / f"tree_census_n{n}.jsonl.gz", "rt", encoding="utf-8") as source:
            for line in source:
                if line.strip():
                    yield json.loads(line)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--reconcile-previous",
        action="store_true",
        help="correct expected class totals in a completed prior run without recounting",
    )
    args = parser.parse_args()
    output = HERE / "full_extended_census_independent_check.json"
    log = HERE / "full_extended_census_independent_check.log"
    if args.reconcile_previous:
        result = json.loads(output.read_text(encoding="utf-8"))
        assert result["mismatch_count"] == 0, "cannot reconcile a run with mismatches"
        for n, expected in EXPECTED.items():
            row = result["orders"][str(n)]
            row["expected_classes"] = expected
            row["all_counts_agree"] = row["trees_checked"] == expected
        result["orders"].update(
            {str(n): result["orders"][str(n)] for n in EXPECTED}
        )
        output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
        lines = [
            "Full extended tree census cross-check: fixed-array DP vs stored memo-DP counts",
            *(
                f"n={n}: checked {result['orders'][str(n)]['trees_checked']} / {EXPECTED[n]} classes"
                for n in EXPECTED
            ),
            "Mismatches: 0",
            f"Seconds: {result['seconds']:.6f}",
        ]
        log.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print("\n".join(lines), flush=True)
        if not all(row["all_counts_agree"] for row in result["orders"].values()):
            raise SystemExit("class-total check failed")
        return

    start = time.perf_counter()
    seen = {n: 0 for n in EXPECTED}
    mismatches: list[dict] = []
    for record in census_records():
        n = int(record.get("n", record.get("order")))
        if n not in EXPECTED:
            continue
        graph = nx.from_graph6_bytes(record["graph6"].encode("ascii"))
        actual = count_tree_dp_fast(graph)
        stored = int(record["m_dp"])
        seen[n] += 1
        if actual != stored:
            mismatches.append(
                {"n": n, "graph6": record["graph6"], "stored": stored, "array_dp": actual}
            )

    elapsed = time.perf_counter() - start
    result = {
        "independent_counter": "fixed-array exact rooted-tree DP in fast_tree_dp.py",
        "compared_against": "bounded-memo or dictionary rooted-tree DP census values",
        "orders": {
            str(n): {
                "trees_checked": seen[n],
                "expected_classes": EXPECTED[n],
                "all_counts_agree": seen[n] == EXPECTED[n]
                and not any(item["n"] == n for item in mismatches),
            }
            for n in EXPECTED
        },
        "mismatch_count": len(mismatches),
        "mismatches": mismatches[:20],
        "seconds": elapsed,
    }
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    lines = [
        "Full extended tree census cross-check: fixed-array DP vs stored memo-DP counts",
        *(f"n={n}: checked {seen[n]} / {EXPECTED[n]} classes" for n in EXPECTED),
        f"Mismatches: {len(mismatches)}",
        f"Seconds: {elapsed:.6f}",
    ]
    log.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines), flush=True)
    if any(seen[n] != EXPECTED[n] for n in EXPECTED) or mismatches:
        raise SystemExit(f"cross-check failed; details in {output}")


if __name__ == "__main__":
    main()
