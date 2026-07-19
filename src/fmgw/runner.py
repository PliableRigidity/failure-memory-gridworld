"""Single-run and paired-run execution with full trace logging.

Each trace step exposes the candidate actions, the active exclusions, the chosen
action, the environment outcome, and the memory update (EXPERIMENT_PROTOCOL and
the D009 trace requirement).
"""
from __future__ import annotations

import csv
import json
import os
from typing import Dict, List, Sequence, Tuple

from .agents import Agent, make_agent
from .environment import GridWorld
from .metrics import compute_metrics
from .policies import action_priority_permutation, format_permutation

RAW_COLUMNS: Tuple[str, ...] = (
    "run_id", "pair_id", "maze_id", "agent_type", "seed", "action_priority",
    "step_limit", "success", "total_steps", "blocked_actions",
    "repeated_failed_actions",
)


def _build_env(maze: Dict[str, object]) -> GridWorld:
    rows, cols = maze["size"]  # type: ignore[misc]
    return GridWorld(
        rows=rows, cols=cols,
        start=tuple(maze["start"]),  # type: ignore[arg-type]
        goal=tuple(maze["goal"]),  # type: ignore[arg-type]
        walls=set(tuple(w) for w in maze["walls"]),  # type: ignore[arg-type]
    )


def run_single(maze: Dict[str, object], seed: int, agent: Agent) -> Tuple[Dict, List[Dict]]:
    """Run one agent on one maze with one seed. Returns (row, trace)."""
    env = _build_env(maze)
    permutation = action_priority_permutation(seed)
    perm_str = format_permutation(permutation)
    agent.reset_for_run()
    state = env.reset()
    step_limit = env.step_limit()
    log: List[Dict[str, object]] = []
    success = False

    for step_index in range(step_limit):
        decision = agent.decide(state, env.goal, permutation)
        chosen = decision.chosen
        outcome = env.step(chosen)
        blocked = bool(outcome["blocked"])
        if blocked:
            agent.memory.record_block(state, chosen)
        agent.memory.after_decision()
        log.append({
            "step": step_index,
            "state": state,
            "candidates": decision.candidates,
            "exclusions": decision.exclusions,
            "chosen": chosen,
            "blocked": blocked,
            "new_position": outcome["new_position"],
            "goal_reached": bool(outcome["goal_reached"]),
            "memory_update": f"add({state},{chosen})" if blocked else "none",
            "fallback": decision.used_fallback,
        })
        state = outcome["new_position"]
        if outcome["goal_reached"]:
            success = True
            break

    metrics = compute_metrics(log, success)
    maze_id = maze["id"]
    pair_id = f"{maze_id}-s{seed}"
    row = {
        "run_id": f"{pair_id}-{agent.agent_type}",
        "pair_id": pair_id,
        "maze_id": maze_id,
        "agent_type": agent.agent_type,
        "seed": seed,
        "action_priority": perm_str,
        "step_limit": step_limit,
        **metrics,
    }
    return row, log


def run_pair(maze: Dict[str, object], seed: int) -> Tuple[List[Dict], Dict[str, List[Dict]]]:
    """Run the matched pair (Agent A and Agent B) for one (maze, seed)."""
    rows: List[Dict] = []
    traces: Dict[str, List[Dict]] = {}
    for agent_type in ("A", "B"):
        agent = make_agent(agent_type)
        row, trace = run_single(maze, seed, agent)
        rows.append(row)
        traces[row["run_id"]] = trace
    return rows, traces


def run_matrix(mazes: Sequence[Dict[str, object]], seeds: Sequence[int]
               ) -> Tuple[List[Dict], Dict[str, List[Dict]]]:
    """Run every (maze, seed) matched pair. Deterministic ordering."""
    all_rows: List[Dict] = []
    all_traces: Dict[str, List[Dict]] = {}
    for maze in mazes:
        for seed in seeds:
            rows, traces = run_pair(maze, seed)
            all_rows.extend(rows)
            all_traces.update(traces)
    return all_rows, all_traces


def write_raw_csv(rows: Sequence[Dict], path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(RAW_COLUMNS))
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row[k] for k in RAW_COLUMNS})


def write_traces(traces: Dict[str, List[Dict]], path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)

    def _norm(value):
        if isinstance(value, tuple):
            return list(value)
        return value

    with open(path, "w") as handle:
        for run_id, trace in traces.items():
            for entry in trace:
                record = {"run_id": run_id, **{k: _norm(v) for k, v in entry.items()}}
                handle.write(json.dumps(record) + "\n")
