"""Metrics computed from the external action log only (D002).

Nothing here reads an agent's internal memory, so both agents are scored by one
identical external rule.
"""
from __future__ import annotations

from typing import Dict, List, Sequence, Set, Tuple

from .environment import Action, Position

Pair = Tuple[Position, Action]


def repeated_failed_actions(log: Sequence[Dict[str, object]]) -> int:
    """Count attempts of a (state, action) pair that already blocked earlier.

    A repeated failed action occurs when the same state-action pair has already
    produced a blocked outcome earlier in the same run (D002). Membership is
    checked before the current attempt is recorded.
    """
    seen_blocked: Set[Pair] = set()
    count = 0
    for entry in log:
        pair = (entry["state"], entry["chosen"])  # type: ignore[index]
        if pair in seen_blocked:
            count += 1
        if entry["blocked"]:  # type: ignore[index]
            seen_blocked.add(pair)
    return count


def compute_metrics(log: List[Dict[str, object]], success: bool) -> Dict[str, int]:
    total_steps = len(log)
    blocked_actions = sum(1 for e in log if e["blocked"])
    return {
        "success": 1 if success else 0,
        "total_steps": total_steps,
        "blocked_actions": blocked_actions,
        "repeated_failed_actions": repeated_failed_actions(log),
    }
