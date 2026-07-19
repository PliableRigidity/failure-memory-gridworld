"""Regenerate all figures from existing raw results and traces.

Does not run the experiment or touch raw data. Reproduce with:
  python -m experiments.make_figures
"""
from __future__ import annotations

import csv
import json
import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_ROOT, "src"))
sys.path.insert(0, _ROOT)

from configs.mazes import MAZES_BY_ID  # noqa: E402
from fmgw import analysis  # noqa: E402

RESULTS = os.path.join(_ROOT, "results")
FIG = os.path.join(_ROOT, "paper", "figures")


def load_rows():
    with open(os.path.join(RESULTS, "raw_results.csv")) as h:
        return list(csv.DictReader(h))


def load_trace(run_id):
    positions = None
    seq = []
    with open(os.path.join(RESULTS, "traces.jsonl")) as h:
        for line in h:
            rec = json.loads(line)
            if rec["run_id"] != run_id:
                continue
            if positions is None:
                positions = [tuple(rec["state"])]
            seq.append(rec)
            positions.append(tuple(rec["new_position"]))
    return positions or [], seq


def main():
    rows = load_rows()
    overall = analysis.summarize(rows)
    by_maze = analysis.summarize_by_maze(rows)

    analysis.figure_repeated(overall, os.path.join(FIG, "repeated_failed_actions.png"))
    analysis.figure_blocked(overall, os.path.join(FIG, "blocked_actions.png"))
    analysis.figure_steps(overall, os.path.join(FIG, "total_steps.png"))
    analysis.figure_by_maze_repeated(by_maze, os.path.join(FIG, "repeated_by_maze.png"))
    analysis.figure_agent_comparison(os.path.join(FIG, "agent_comparison.png"))

    # Open-cell oscillation example: Agent B, maze_08, seed 3.
    positions, _ = load_trace("maze_08-s3-B")
    tail = positions[-8:]
    cycle = set(tail)
    analysis.figure_oscillation(MAZES_BY_ID["maze_08"], positions, cycle,
                                os.path.join(FIG, "oscillation_example.png"))
    print("figures written to", FIG)
    print("cycle cells (maze_08-s3-B):", sorted(cycle))


if __name__ == "__main__":
    raise SystemExit(main())
