"""Shared execution harness for the pilot and full experiment scripts."""
from __future__ import annotations

import json
import os
import platform
import sys
from datetime import datetime, timezone
from typing import Dict, List, Sequence

# Make the src-layout package importable without installation.
_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_ROOT, "src"))

from fmgw import analysis, integrity  # noqa: E402
from fmgw.runner import RAW_COLUMNS, run_matrix, write_raw_csv, write_traces  # noqa: E402

RESULTS_DIR = os.path.join(_ROOT, "results")
FIG_DIR = os.path.join(_ROOT, "paper", "figures")


def execute(mazes: Sequence[Dict], seeds: Sequence[int], tag: str) -> Dict[str, object]:
    rows, traces = run_matrix(mazes, seeds)

    raw_path = os.path.join(RESULTS_DIR, f"raw_results{'' if tag == 'full' else '_' + tag}.csv")
    trace_path = os.path.join(RESULTS_DIR, f"traces{'' if tag == 'full' else '_' + tag}.jsonl")
    write_raw_csv(rows, raw_path)
    write_traces(traces, trace_path)

    overall = analysis.summarize(rows)
    by_maze = analysis.summarize_by_maze(rows)
    summary_path = os.path.join(RESULTS_DIR, f"summary{'' if tag == 'full' else '_' + tag}.csv")
    by_maze_path = os.path.join(RESULTS_DIR, f"summary_by_maze{'' if tag == 'full' else '_' + tag}.csv")
    analysis.write_summary_csv(overall, summary_path)
    analysis.write_summary_by_maze_csv(by_maze, by_maze_path)

    integrity_report = {
        "pairs": integrity.check_pair_integrity(rows),
        "counts": integrity.check_counts(rows),
        "reconcile": integrity.reconcile_summary(rows, overall),
        "fingerprint": integrity.rows_fingerprint(rows, RAW_COLUMNS),
    }

    manifest = {
        "tag": tag,
        "generated_utc": datetime.now(timezone.utc).isoformat(),
        "python": platform.python_version(),
        "n_mazes": len(mazes),
        "n_seeds": len(seeds),
        "seeds": list(seeds),
        "maze_ids": [m["id"] for m in mazes],
        "n_runs": len(rows),
        "raw_fingerprint_sha256": integrity_report["fingerprint"],
        "files": {
            "raw": os.path.basename(raw_path),
            "traces": os.path.basename(trace_path),
            "summary": os.path.basename(summary_path),
            "summary_by_maze": os.path.basename(by_maze_path),
        },
    }
    manifest_path = os.path.join(RESULTS_DIR, f"manifest{'' if tag == 'full' else '_' + tag}.json")
    with open(manifest_path, "w") as handle:
        json.dump(manifest, handle, indent=2)

    return {
        "rows": rows,
        "traces": traces,
        "overall": overall,
        "by_maze": by_maze,
        "integrity": integrity_report,
        "manifest": manifest,
        "paths": {
            "raw": raw_path, "traces": trace_path, "summary": summary_path,
            "by_maze": by_maze_path, "manifest": manifest_path,
        },
    }
