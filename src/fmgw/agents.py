"""Shared agent. Agent A and Agent B are the same class with a different memory.

Putting the sole difference in the injected ``Memory`` object structurally
guarantees that the agents differ only by exclusion horizon (D008).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Sequence

from .environment import ACTIONS, Action, Position
from .memory import Memory, PersistentMemory, TransientExclusion
from .policies import rank_candidates


@dataclass
class Decision:
    candidates: List[Action]
    exclusions: List[Action]
    ranked: List[Action]
    chosen: Action
    used_fallback: bool


class Agent:
    def __init__(self, agent_type: str, memory: Memory) -> None:
        self.agent_type = agent_type
        self.memory = memory

    def reset_for_run(self) -> None:
        self.memory.reset_for_run()

    def decide(self, state: Position, goal: Position,
               permutation: Sequence[Action]) -> Decision:
        exclusions = self.memory.excluded(state)
        candidates = [a for a in ACTIONS if a not in exclusions]
        used_fallback = False
        if not candidates:
            # Rule 2: if exclusions remove every action, ignore them this
            # decision and rank the full action set.
            candidates = list(ACTIONS)
            used_fallback = True
        ranked = rank_candidates(state, goal, candidates, permutation)
        return Decision(
            candidates=sorted(candidates),
            exclusions=sorted(exclusions),
            ranked=ranked,
            chosen=ranked[0],
            used_fallback=used_fallback,
        )


def make_agent(agent_type: str) -> Agent:
    if agent_type == "A":
        return Agent("A", TransientExclusion())
    if agent_type == "B":
        return Agent("B", PersistentMemory())
    raise ValueError(f"unknown agent_type {agent_type!r}")
