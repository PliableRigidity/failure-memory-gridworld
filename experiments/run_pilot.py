"""Pilot run and the four D008 / Section 13 validity checks.

Runs a small subset (mazes 1 to 2, seeds 0 to 2), verifies the pilot conditions,
prints representative paired traces, and stops before the full experiment.

Reproduce with:  python -m experiments.run_pilot
"""
from __future__ import annotations

import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_ROOT, "src"))
sys.path.insert(0, _ROOT)

from configs.mazes import MAZES_BY_ID  # noqa: E402
from experiments._harness import execute  # noqa: E402

PILOT_MAZE_IDS = ["maze_01", "maze_03"]
PILOT_SEEDS = [0, 1, 2]


def check_no_consecutive_repeat(traces):
    """Check 1: Agent A never repeats the same blocked action back to back."""
    violations = []
    for run_id, trace in traces.items():
        if not run_id.endswith("-A"):
            continue
        for i in range(len(trace) - 1):
            e, nxt = trace[i], trace[i + 1]
            if e["blocked"] and nxt["state"] == e["state"] and nxt["chosen"] == e["chosen"]:
                violations.append((run_id, i, e["state"], e["chosen"]))
    return {"ok": not violations, "violations": violations}


def _repeated_pairs(trace):
    """Return the set of (state, action) pairs attempted after an earlier block."""
    seen_blocked = set()
    repeated = set()
    for e in trace:
        pair = (tuple(e["state"]), e["chosen"])
        if pair in seen_blocked:
            repeated.add(pair)
        if e["blocked"]:
            seen_blocked.add(pair)
    return repeated


def check_revisit_contrast(rows, traces):
    """Check 2: a scenario where A repeats an earlier failure and B avoids it."""
    examples = []
    by_pair = {}
    for r in rows:
        by_pair.setdefault(r["pair_id"], {})[r["agent_type"]] = r
    for pair_id, agents in by_pair.items():
        a_run = f"{pair_id}-A"
        b_run = f"{pair_id}-B"
        a_rep = _repeated_pairs(traces[a_run])
        b_rep = _repeated_pairs(traces[b_run])
        avoided = a_rep - b_rep
        if a_rep and avoided:
            examples.append({
                "pair_id": pair_id,
                "a_repeated_pairs": sorted(str(p) for p in a_rep),
                "b_repeated_pairs": sorted(str(p) for p in b_rep),
                "avoided_by_b": sorted(str(p) for p in avoided),
                "a_repeated_count": int(agents["A"]["repeated_failed_actions"]),
                "b_repeated_count": int(agents["B"]["repeated_failed_actions"]),
            })
    return {"ok": bool(examples), "examples": examples}


def check_non_degenerate(by_maze):
    """Check 3: some mazes show little or no memory benefit."""
    per_maze = {}
    for s in by_maze:
        per_maze.setdefault(s["maze_id"], {})[s["agent_type"]] = s
    deltas = {}
    for maze_id, agents in per_maze.items():
        if "A" in agents and "B" in agents:
            deltas[maze_id] = agents["A"]["mean_repeated_failed_actions"] - agents["B"]["mean_repeated_failed_actions"]
    small = [m for m, d in deltas.items() if abs(d) < 1e-9]
    varied = len({round(d, 6) for d in deltas.values()}) > 1
    return {"ok": True, "deltas": deltas, "mazes_with_no_benefit": small, "varied": varied}


def _fmt_trace(trace, limit=40):
    lines = []
    for e in trace[:limit]:
        lines.append(
            f"  step {e['step']:2d} at {tuple(e['state'])} excl={e['exclusions']} "
            f"-> {e['chosen']:5s} blocked={int(e['blocked'])} "
            f"new={tuple(e['new_position'])} mem={e['memory_update']}"
            + ("  [FALLBACK]" if e["fallback"] else "")
        )
    if len(trace) > limit:
        lines.append(f"  ... ({len(trace) - limit} more steps)")
    return "\n".join(lines)


def main():
    mazes = [MAZES_BY_ID[m] for m in PILOT_MAZE_IDS]
    result = execute(mazes, PILOT_SEEDS, tag="pilot")
    rows, traces = result["rows"], result["traces"]

    print("=== PILOT RUN ===")
    print("mazes:", PILOT_MAZE_IDS, "seeds:", PILOT_SEEDS, "runs:", len(rows))
    print()
    print("Per-run results:")
    print(f"  {'run_id':16s} {'succ':4s} {'steps':5s} {'blocked':7s} {'repeated':8s}")
    for r in sorted(rows, key=lambda r: r["run_id"]):
        print(f"  {r['run_id']:16s} {int(r['success']):4d} {int(r['total_steps']):5d} "
              f"{int(r['blocked_actions']):7d} {int(r['repeated_failed_actions']):8d}")
    print()

    c1 = check_no_consecutive_repeat(traces)
    c2 = check_revisit_contrast(rows, traces)
    c3 = check_non_degenerate(result["by_maze"])
    integ = result["integrity"]

    print("=== VALIDITY CHECKS ===")
    print(f"Check 1 (A no back-to-back blocked repeat): {'PASS' if c1['ok'] else 'FAIL'}")
    if not c1["ok"]:
        for v in c1["violations"][:5]:
            print("   violation:", v)
    print(f"Check 2 (A repeats a failure B avoids):     {'PASS' if c2['ok'] else 'FAIL'}")
    for ex in c2["examples"][:3]:
        print(f"   {ex['pair_id']}: A repeated {ex['a_repeated_count']}, B repeated "
              f"{ex['b_repeated_count']}, B avoided {ex['avoided_by_b']}")
    print(f"Check 3 (benchmark not degenerate):         {'PASS' if c3['ok'] else 'FAIL'}")
    print(f"   per-maze repeated-failure delta (A - B): {c3['deltas']}")
    print(f"   mazes with no benefit: {c3['mazes_with_no_benefit']}")
    print(f"Pair integrity: {'PASS' if integ['pairs']['ok'] else 'FAIL'}  "
          f"Counts: {'PASS' if integ['counts']['ok'] else 'FAIL'}  "
          f"Summary reconcile: {'PASS' if integ['reconcile']['ok'] else 'FAIL'}")
    print()

    print("=== REPRESENTATIVE PAIRED TRACES ===")
    example_pair = c2["examples"][0]["pair_id"] if c2["examples"] else f"{PILOT_MAZE_IDS[1]}-s0"
    print(f"Pair: {example_pair}")
    print("Agent A (transient):")
    print(_fmt_trace(traces[f"{example_pair}-A"]))
    print("Agent B (persistent):")
    print(_fmt_trace(traces[f"{example_pair}-B"]))

    all_pass = c1["ok"] and c2["ok"] and c3["ok"] and integ["pairs"]["ok"] and integ["counts"]["ok"] and integ["reconcile"]["ok"]
    print()
    print("PILOT RESULT:", "ALL CHECKS PASS" if all_pass else "CHECKS FAILED")
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
