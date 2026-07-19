"""Full experiment (100 runs) with the pre-registered 30-run fallback (D007).

Reproduce with:  python -m experiments.run_full

The fallback (mazes 1 to 5, seeds 0 to 2) is used only when the environment,
agents, tests, and pilot are not complete and passing by the deadline. It is
selected by the operator via --fallback, never from observed results.
"""
from __future__ import annotations

import argparse
import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_ROOT, "src"))
sys.path.insert(0, _ROOT)

from configs.mazes import FALLBACK_MAZES, FALLBACK_SEEDS, MAZES, SEEDS  # noqa: E402
from experiments._harness import FIG_DIR, execute  # noqa: E402
from fmgw import analysis  # noqa: E402
from configs.mazes import MAZES_BY_ID  # noqa: E402


def _positions_from_trace(trace):
    positions = [tuple(trace[0]["state"])] if trace else []
    for e in trace:
        positions.append(tuple(e["new_position"]))
    return positions


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fallback", action="store_true",
                        help="use the pre-registered 30-run fallback subset")
    args = parser.parse_args()

    if args.fallback:
        mazes, seeds, tag = FALLBACK_MAZES, FALLBACK_SEEDS, "full"
        print("Using FALLBACK design (D007): 5 mazes x 3 seeds x 2 agents = 30 runs")
    else:
        mazes, seeds, tag = MAZES, SEEDS, "full"
        print("Using MAIN design (D007): 10 mazes x 5 seeds x 2 agents = 100 runs")

    result = execute(mazes, seeds, tag=tag)
    rows, traces, overall = result["rows"], result["traces"], result["overall"]

    # The six figures used by the paper, generated from summary and raw data only.
    # This matches experiments/make_figures.py so the reproduction is consistent.
    analysis.figure_repeated(overall, os.path.join(FIG_DIR, "repeated_failed_actions.png"))
    analysis.figure_steps(overall, os.path.join(FIG_DIR, "total_steps.png"))
    analysis.figure_blocked(overall, os.path.join(FIG_DIR, "blocked_actions.png"))
    analysis.figure_by_maze_repeated(result["by_maze"], os.path.join(FIG_DIR, "repeated_by_maze.png"))
    analysis.figure_agent_comparison(os.path.join(FIG_DIR, "agent_comparison.png"))

    # Representative pair: the largest A-minus-B repeated-failure gap. Used for the
    # printed summary line and the open-cell oscillation figure.
    best_pair = None
    best_gap = -1
    by_pair = {}
    for r in rows:
        by_pair.setdefault(r["pair_id"], {})[r["agent_type"]] = r
    for pair_id, agents in by_pair.items():
        if "A" in agents and "B" in agents:
            gap = int(agents["A"]["repeated_failed_actions"]) - int(agents["B"]["repeated_failed_actions"])
            if gap > best_gap:
                best_gap = gap
                best_pair = pair_id

    # Open-cell oscillation figure: Agent B on maze_08, seed 3.
    osc_run = "maze_08-s3-B"
    if osc_run in traces:
        positions = _positions_from_trace(traces[osc_run])
        cycle = set(positions[-8:])
        analysis.figure_oscillation(MAZES_BY_ID["maze_08"], positions, cycle,
                                    os.path.join(FIG_DIR, "oscillation_example.png"))

    print("\n=== FULL EXPERIMENT SUMMARY ===")
    print(f"runs: {len(rows)}   fingerprint: {result['integrity']['fingerprint'][:16]}...")
    for s in overall:
        print(f"  Agent {s['agent_type']}: success_rate={s['success_rate']:.3f} "
              f"mean_steps={s['mean_total_steps']:.2f} "
              f"mean_blocked={s['mean_blocked_actions']:.2f} "
              f"mean_repeated={s['mean_repeated_failed_actions']:.3f} (n={s['n_runs']})")
    integ = result["integrity"]
    print(f"  integrity: pairs={'OK' if integ['pairs']['ok'] else 'BAD'} "
          f"counts={'OK' if integ['counts']['ok'] else 'BAD'} "
          f"reconcile={'OK' if integ['reconcile']['ok'] else 'BAD'}")
    print(f"  representative pair: {best_pair} (A-B repeated gap = {best_gap})")
    print("  outputs in results/ and paper/figures/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
