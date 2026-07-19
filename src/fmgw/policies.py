"""Shared deterministic action-selection policy (D005, rules 3 and 4).

Both agents use this policy. Selection consumes no random values. A single
action-priority permutation is derived from the run seed and used only to break
ties in Manhattan-distance reduction.
"""
from __future__ import annotations

import itertools
from typing import Dict, List, Sequence, Tuple

from .environment import ACTIONS, DELTAS, Action, Position

# Fixed enumeration of the 24 permutations of the four actions, in a stable
# order. The permutation for a seed is index (seed mod 24). Distinct small seeds
# therefore yield distinct permutations, satisfying the five-unique-permutation
# requirement in EXPERIMENT_PROTOCOL Section 6.
_PERMUTATIONS: Tuple[Tuple[Action, ...], ...] = tuple(itertools.permutations(ACTIONS))


def action_priority_permutation(seed: int) -> Tuple[Action, ...]:
    """Return the fixed action-priority permutation for a run seed (D005)."""
    return _PERMUTATIONS[seed % len(_PERMUTATIONS)]


def format_permutation(permutation: Sequence[Action]) -> str:
    """Serialise a permutation for the raw-result and trace records."""
    return "|".join(permutation)


def manhattan(a: Position, b: Position) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def _geometric_target(state: Position, action: Action) -> Position:
    """Target cell of an action ignoring walls and bounds (rule 3)."""
    dr, dc = DELTAS[action]
    return (state[0] + dr, state[1] + dc)


def rank_candidates(state: Position, goal: Position,
                    candidates: Sequence[Action],
                    permutation: Sequence[Action]) -> List[Action]:
    """Rank candidate actions by Manhattan-distance reduction, then permutation.

    Reduction is computed from the geometric target position, so the agent uses
    no wall knowledge (rule 3). All supplied candidates are ranked, including
    distance-increasing actions. Ties are broken only by the permutation
    (rule 4).
    """
    priority: Dict[Action, int] = {a: i for i, a in enumerate(permutation)}
    here = manhattan(state, goal)

    def reduction(action: Action) -> int:
        return here - manhattan(_geometric_target(state, action), goal)

    return sorted(candidates, key=lambda a: (-reduction(a), priority[a]))
