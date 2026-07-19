"""Deterministic grid-world environment and validation-only BFS helpers.

The environment is a passive simulator. It applies identical movement rules to
both agents and holds no memory of agent history (EXPERIMENT_PROTOCOL Section 1).
The BFS helpers in this module are used only to validate mazes and to compute a
reference shortest-path length. Agents never receive a reference to them
(D006).
"""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Dict, Optional, Set, Tuple

Position = Tuple[int, int]
Action = str

# Action -> (row_delta, col_delta). Row increases downward.
DELTAS: Dict[Action, Position] = {
    "up": (-1, 0),
    "down": (1, 0),
    "left": (0, -1),
    "right": (0, 1),
}
ACTIONS: Tuple[Action, ...] = ("up", "down", "left", "right")


@dataclass
class GridWorld:
    """A bounded rectangular grid with fixed walls and deterministic movement."""

    rows: int
    cols: int
    start: Position
    goal: Position
    walls: Set[Position] = field(default_factory=set)
    _position: Position = field(init=False, default=(0, 0))

    def __post_init__(self) -> None:
        if not self._in_bounds(self.start):
            raise ValueError(f"start {self.start} out of bounds")
        if not self._in_bounds(self.goal):
            raise ValueError(f"goal {self.goal} out of bounds")
        if self.start in self.walls:
            raise ValueError("start cell is a wall")
        if self.goal in self.walls:
            raise ValueError("goal cell is a wall")
        self._position = self.start

    def _in_bounds(self, pos: Position) -> bool:
        r, c = pos
        return 0 <= r < self.rows and 0 <= c < self.cols

    def reset(self) -> Position:
        self._position = self.start
        return self._position

    @property
    def position(self) -> Position:
        return self._position

    def traversable_cells(self) -> int:
        """Total grid cells minus blocked cells (D006)."""
        return self.rows * self.cols - len(self.walls)

    def step_limit(self) -> int:
        """Four times the traversable-cell count (D006)."""
        return 4 * self.traversable_cells()

    def step(self, action: Action) -> Dict[str, object]:
        """Attempt one move. Blocked moves leave the agent in place.

        Returns a fresh observation dict; the environment stores no history
        beyond the current position.
        """
        if action not in DELTAS:
            raise ValueError(f"unknown action {action!r}")
        dr, dc = DELTAS[action]
        target = (self._position[0] + dr, self._position[1] + dc)
        blocked = (not self._in_bounds(target)) or (target in self.walls)
        if blocked:
            new_position = self._position
        else:
            new_position = target
            self._position = target
        return {
            "new_position": new_position,
            "blocked": blocked,
            "goal_reached": new_position == self.goal,
        }


def bfs_shortest_path(rows: int, cols: int, walls: Set[Position],
                      start: Position, goal: Position) -> Optional[int]:
    """Return the shortest-path length in steps, or None if unreachable.

    Validation only. Never called by an agent (D006).
    """
    if start == goal:
        return 0
    seen = {start}
    queue = deque([(start, 0)])
    while queue:
        (r, c), dist = queue.popleft()
        for dr, dc in DELTAS.values():
            nxt = (r + dr, c + dc)
            if not (0 <= nxt[0] < rows and 0 <= nxt[1] < cols):
                continue
            if nxt in walls or nxt in seen:
                continue
            if nxt == goal:
                return dist + 1
            seen.add(nxt)
            queue.append((nxt, dist + 1))
    return None


def validate_maze(maze: Dict[str, object]) -> Dict[str, object]:
    """Check reachability and that the shortest path is below the step limit.

    Validation only. Returns a report; raises nothing so callers can decide.
    """
    rows, cols = maze["size"]  # type: ignore[misc]
    walls = set(maze["walls"])  # type: ignore[arg-type]
    start = maze["start"]  # type: ignore[assignment]
    goal = maze["goal"]  # type: ignore[assignment]
    traversable = rows * cols - len(walls)
    step_limit = 4 * traversable
    shortest = bfs_shortest_path(rows, cols, walls, start, goal)  # type: ignore[arg-type]
    reachable = shortest is not None
    below_limit = reachable and shortest < step_limit
    return {
        "maze_id": maze.get("id"),
        "reachable": reachable,
        "shortest_path": shortest,
        "step_limit": step_limit,
        "traversable_cells": traversable,
        "shortest_below_limit": below_limit,
        "ok": reachable and below_limit,
    }
