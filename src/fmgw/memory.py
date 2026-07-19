"""Two failure-exclusion strategies behind one interface (D008).

The only intended behavioural difference between the agents is the horizon of
the exclusion, so both strategies share the same interface and the agent code is
identical for A and B.
"""
from __future__ import annotations

from typing import Set, Tuple

from .environment import Action, Position

Pair = Tuple[Position, Action]


class Memory:
    """Interface used by the shared agent."""

    def reset_for_run(self) -> None:
        raise NotImplementedError

    def excluded(self, state: Position) -> Set[Action]:
        raise NotImplementedError

    def record_block(self, state: Position, action: Action) -> None:
        raise NotImplementedError

    def after_decision(self) -> None:
        raise NotImplementedError


class TransientExclusion(Memory):
    """Agent A: a blocked pair is excluded for exactly the next decision (D008).

    A block recorded during the current decision enters ``_pending``. At the end
    of the decision ``after_decision`` promotes ``_pending`` to ``_current`` and
    discards the previous ``_current``, so any exclusion lasts one decision.
    """

    def __init__(self) -> None:
        self._current: Set[Pair] = set()
        self._pending: Set[Pair] = set()

    def reset_for_run(self) -> None:
        self._current = set()
        self._pending = set()

    def excluded(self, state: Position) -> Set[Action]:
        return {action for (s, action) in self._current if s == state}

    def record_block(self, state: Position, action: Action) -> None:
        self._pending.add((state, action))

    def after_decision(self) -> None:
        self._current = self._pending
        self._pending = set()


class PersistentMemory(Memory):
    """Agent B: blocked pairs are excluded for the rest of the run (D008).

    The store is cleared only at the start of each run, so memory is within-run
    only (D003, Agent B clause).
    """

    def __init__(self) -> None:
        self._store: Set[Pair] = set()

    def reset_for_run(self) -> None:
        self._store = set()

    def excluded(self, state: Position) -> Set[Action]:
        return {action for (s, action) in self._store if s == state}

    def record_block(self, state: Position, action: Action) -> None:
        self._store.add((state, action))

    def after_decision(self) -> None:
        return None
