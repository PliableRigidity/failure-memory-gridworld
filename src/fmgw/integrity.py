"""Paired-run and reproducibility integrity checks (EXPERIMENT_PROTOCOL S12)."""
from __future__ import annotations

import hashlib
from collections import Counter, defaultdict
from typing import Dict, List, Sequence, Tuple


def check_pair_integrity(rows: Sequence[Dict]) -> Dict[str, object]:
    """Every pair_id must hold exactly one Agent A row and one Agent B row."""
    by_pair: Dict[str, List[str]] = defaultdict(list)
    for r in rows:
        by_pair[r["pair_id"]].append(r["agent_type"])
    bad = {p: agents for p, agents in by_pair.items()
           if sorted(agents) != ["A", "B"]}
    return {"n_pairs": len(by_pair), "ok": not bad, "bad_pairs": bad}


def check_counts(rows: Sequence[Dict]) -> Dict[str, object]:
    counts = Counter(r["agent_type"] for r in rows)
    ok = counts.get("A", 0) == counts.get("B", 0) and counts.get("A", 0) > 0
    return {"counts": dict(counts), "ok": ok}


def rows_fingerprint(rows: Sequence[Dict], columns: Sequence[str]) -> str:
    """Order-independent hash of the raw rows for reproducibility checks."""
    lines = sorted("|".join(str(r[c]) for c in columns) for r in rows)
    digest = hashlib.sha256("\n".join(lines).encode()).hexdigest()
    return digest


def reconcile_summary(rows: Sequence[Dict], summary: Sequence[Dict]) -> Dict[str, object]:
    """Recompute summary means from rows and compare against the provided summary."""
    problems = []
    for s in summary:
        subset = [r for r in rows if r["agent_type"] == s["agent_type"]]
        n = len(subset)
        recomputed = {
            "n_runs": n,
            "success_rate": sum(int(r["success"]) for r in subset) / n,
            "mean_total_steps": sum(int(r["total_steps"]) for r in subset) / n,
            "mean_blocked_actions": sum(int(r["blocked_actions"]) for r in subset) / n,
            "mean_repeated_failed_actions": sum(int(r["repeated_failed_actions"]) for r in subset) / n,
        }
        for key, value in recomputed.items():
            if abs(float(s[key]) - value) > 1e-9:
                problems.append((s["agent_type"], key, s[key], value))
    return {"ok": not problems, "problems": problems}
