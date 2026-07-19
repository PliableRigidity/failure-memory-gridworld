"""Summaries and figures generated from raw results only (EXPERIMENT_PROTOCOL S11).

Every figure is produced from the raw rows or the summary derived from them. No
values are hand-entered.
"""
from __future__ import annotations

import csv
import os
from typing import Dict, List, Sequence

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

# Consistent publication styling for every figure.
plt.rcParams.update({
    "figure.dpi": 150,
    "savefig.dpi": 150,
    "font.size": 10,
    "axes.titlesize": 12,
    "axes.labelsize": 11,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 9,
    "axes.linewidth": 0.9,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

METRIC_KEYS = ("success", "total_steps", "blocked_actions", "repeated_failed_actions")
SUMMARY_COLUMNS = (
    "agent_type", "n_runs", "success_rate", "mean_total_steps",
    "mean_blocked_actions", "mean_repeated_failed_actions",
)

# One colour per agent, used identically across every plot.
AGENT_COLORS = {"A": "#8c8c8c", "B": "#3b6ea5"}
AGENT_LABELS = {"A": "Agent A (transient)", "B": "Agent B (persistent)"}
BAR_FIGSIZE = (5.0, 3.6)
BAR_EDGE = "#333333"


def _mean(values: Sequence[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def summarize(rows: Sequence[Dict]) -> List[Dict]:
    """Aggregate by agent_type over all runs."""
    out = []
    for agent_type in ("A", "B"):
        subset = [r for r in rows if r["agent_type"] == agent_type]
        n = len(subset)
        out.append({
            "agent_type": agent_type,
            "n_runs": n,
            "success_rate": _mean([int(r["success"]) for r in subset]),
            "mean_total_steps": _mean([int(r["total_steps"]) for r in subset]),
            "mean_blocked_actions": _mean([int(r["blocked_actions"]) for r in subset]),
            "mean_repeated_failed_actions": _mean([int(r["repeated_failed_actions"]) for r in subset]),
        })
    return out


def summarize_by_maze(rows: Sequence[Dict]) -> List[Dict]:
    maze_ids = sorted({r["maze_id"] for r in rows})
    out = []
    for maze_id in maze_ids:
        for agent_type in ("A", "B"):
            subset = [r for r in rows if r["maze_id"] == maze_id and r["agent_type"] == agent_type]
            if not subset:
                continue
            out.append({
                "maze_id": maze_id,
                "agent_type": agent_type,
                "n_runs": len(subset),
                "success_rate": _mean([int(r["success"]) for r in subset]),
                "mean_total_steps": _mean([int(r["total_steps"]) for r in subset]),
                "mean_blocked_actions": _mean([int(r["blocked_actions"]) for r in subset]),
                "mean_repeated_failed_actions": _mean([int(r["repeated_failed_actions"]) for r in subset]),
            })
    return out


def write_summary_csv(summary: Sequence[Dict], path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(SUMMARY_COLUMNS))
        writer.writeheader()
        for row in summary:
            writer.writerow({k: row[k] for k in SUMMARY_COLUMNS})


def write_summary_by_maze_csv(summary: Sequence[Dict], path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    cols = ("maze_id", "agent_type", "n_runs", "success_rate", "mean_total_steps",
            "mean_blocked_actions", "mean_repeated_failed_actions")
    with open(path, "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(cols))
        writer.writeheader()
        for row in summary:
            writer.writerow({k: row[k] for k in cols})


def _bar(summary: Sequence[Dict], key: str, ylabel: str, title: str, path: str) -> None:
    """Single-bar-per-agent chart with dynamic headroom for value labels.

    The y-axis upper limit is set from the tallest bar so every value label sits
    clear of the top of the plot. A zero-valued bar still gets a label placed
    just above the baseline.
    """
    agents = [s["agent_type"] for s in summary]
    values = [float(s[key]) for s in summary]
    colors = [AGENT_COLORS[a] for a in agents]

    fig, ax = plt.subplots(figsize=BAR_FIGSIZE, constrained_layout=True)
    bars = ax.bar([AGENT_LABELS[a] for a in agents], values, color=colors,
                  width=0.6, edgecolor=BAR_EDGE, linewidth=0.8)

    max_value = max(values) if values else 0.0
    upper = max_value * 1.15 if max_value > 0 else 1.0
    ax.set_ylim(0, upper)
    offset = upper * 0.02
    for bar, value in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, value + offset,
                f"{value:.2f}", ha="center", va="bottom")

    ax.set_ylabel(ylabel)
    ax.set_title(title, pad=10)
    ax.margins(x=0.15)
    fig.savefig(path)
    plt.close(fig)


def figure_repeated(summary: Sequence[Dict], path: str) -> None:
    _bar(summary, "mean_repeated_failed_actions",
         "Mean repeated failed actions per run",
         "Repeated failed actions by agent", path)


def figure_steps(summary: Sequence[Dict], path: str) -> None:
    _bar(summary, "mean_total_steps", "Mean total steps per run",
         "Total steps by agent", path)


def figure_blocked(summary, path):
    _bar(summary, "mean_blocked_actions", "Mean blocked actions per run",
         "Blocked actions by agent", path)


def figure_by_maze_repeated(by_maze, path):
    """Grouped bar of mean repeated failed actions per maze, A versus B."""
    import numpy as np
    maze_ids = sorted({s["maze_id"] for s in by_maze})
    lookup = {(s["maze_id"], s["agent_type"]): s["mean_repeated_failed_actions"]
              for s in by_maze}
    a_vals = [lookup.get((m, "A"), 0.0) for m in maze_ids]
    b_vals = [lookup.get((m, "B"), 0.0) for m in maze_ids]
    x = np.arange(len(maze_ids))
    width = 0.38

    fig, ax = plt.subplots(figsize=(8.0, 3.6), constrained_layout=True)
    ax.bar(x - width / 2, a_vals, width, label=AGENT_LABELS["A"],
           color=AGENT_COLORS["A"], edgecolor=BAR_EDGE, linewidth=0.6)
    ax.bar(x + width / 2, b_vals, width, label=AGENT_LABELS["B"],
           color=AGENT_COLORS["B"], edgecolor=BAR_EDGE, linewidth=0.6)

    max_value = max(a_vals + b_vals) if (a_vals or b_vals) else 0.0
    upper = max_value * 1.18 if max_value > 0 else 1.0
    ax.set_ylim(0, upper)

    ax.set_ylabel("Mean repeated failed actions")
    ax.set_title("Repeated failed actions per maze", pad=10)
    ax.set_xticks(x)
    ax.set_xticklabels([m.replace("maze_", "") for m in maze_ids])
    ax.set_xlabel("maze")
    ax.legend(loc="upper right", frameon=False)
    fig.savefig(path)
    plt.close(fig)


def figure_agent_comparison(path):
    """Schematic of the shared policy and the single difference between agents.

    Two labelled zones: the shared pipeline on top and the exclusion-horizon
    difference below. No text is placed on connector lines.
    """
    fig, ax = plt.subplots(figsize=(8.6, 5.4), constrained_layout=True)
    ax.set_xlim(0, 10)
    ax.set_ylim(2.2, 10.0)
    ax.axis("off")

    def box(cx, cy, w, h, text, color, fontsize=8.6):
        ax.add_patch(plt.Rectangle((cx - w / 2, cy - h / 2), w, h, facecolor=color,
                                   edgecolor="#333333", linewidth=1.1))
        ax.text(cx, cy, text, ha="center", va="center", fontsize=fontsize)

    def arrow(x1, y1, x2, y2):
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                    arrowprops=dict(arrowstyle="->", color="#333333", lw=1.1))

    # Zone heading: shared pipeline.
    ax.text(5.0, 9.5, "Shared policy and observations",
            ha="center", va="center", fontsize=11, fontweight="bold")

    # Five shared steps in a row.
    shared = [
        "Observation\n(state, goal)",
        "Manhattan\nranking",
        "Seeded\ntie-break",
        "Remove excluded\npairs",
        "Top available\naction",
    ]
    w, box_y, box_h = 1.7, 8.1, 1.2
    centers = [1.05 + i * 1.975 for i in range(5)]
    for cx, text in zip(centers, shared):
        box(cx, box_y, w, box_h, text, "#eeeeee")
    for i in range(4):
        arrow(centers[i] + w / 2, box_y, centers[i + 1] - w / 2, box_y)

    # Central connector down to the split.
    arrow(5.0, box_y - box_h / 2, 5.0, 6.35)

    # Zone heading: the difference.
    ax.text(5.0, 5.95, "Difference: exclusion horizon",
            ha="center", va="center", fontsize=11, fontweight="bold")

    # Fork to the two agent variants.
    fork_y = 5.55
    agent_top = 4.3
    arrow(5.0, fork_y, 2.3, agent_top)
    arrow(5.0, fork_y, 7.7, agent_top)

    box(2.3, 3.45, 3.9, 1.7,
        "Agent A: transient exclusion\n(one decision, then cleared)",
        "#f2e2d0", fontsize=9)
    box(7.7, 3.45, 3.9, 1.7,
        "Agent B: persistent exclusion\n(whole run, cleared between runs)",
        "#d7e8d2", fontsize=9)

    fig.savefig(path)
    plt.close(fig)


def figure_oscillation(maze, positions, cycle_cells, out):
    """Illustrate open-cell oscillation: a persistent-memory run that still fails.

    positions is the full sequence of visited cells for the run. cycle_cells is
    the small set of cells the run settles into at the end.
    """
    rows, cols = maze["size"]
    walls = set(tuple(w) for w in maze["walls"])
    fig, ax = plt.subplots(figsize=(5.2, 5.4), constrained_layout=True)
    for r in range(rows):
        for c in range(cols):
            if (r, c) in walls:
                ax.add_patch(plt.Rectangle((c, rows - 1 - r), 1, 1, color="#222222"))
    visited = set(positions)
    for (r, c) in visited:
        if (r, c) not in walls:
            ax.add_patch(plt.Rectangle((c, rows - 1 - r), 1, 1,
                                       facecolor="#e8eef6", edgecolor="none"))
    for (r, c) in cycle_cells:
        ax.add_patch(plt.Rectangle((c, rows - 1 - r), 1, 1,
                                   facecolor="#c65b3c", edgecolor="none", alpha=0.8))
    sr, sc = tuple(maze["start"])
    gr, gc = tuple(maze["goal"])
    ax.text(sc + 0.5, rows - 1 - sr + 0.5, "S", ha="center", va="center",
            color="#1a1a1a", fontweight="bold")
    ax.text(gc + 0.5, rows - 1 - gr + 0.5, "G", ha="center", va="center",
            color="#c02020", fontweight="bold")
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    cyc = ", ".join(str(tuple(c)) for c in sorted(cycle_cells))
    ax.set_title(f"Persistent-memory run on {maze['id']} times out\n"
                 f"terminal cycle {cyc} uses valid, never-blocked moves", pad=10)
    fig.savefig(out)
    plt.close(fig)


def figure_maze_route(maze: Dict, path_a: Sequence, path_b: Sequence, out: str) -> None:
    """Draw a maze with the Agent A and Agent B visited cells overlaid.

    Retained for completeness; not used by the paper.
    """
    rows, cols = maze["size"]
    walls = set(tuple(w) for w in maze["walls"])
    fig, axes = plt.subplots(1, 2, figsize=(8, 4), constrained_layout=True)
    for ax, path, label, color in (
        (axes[0], path_a, AGENT_LABELS["A"], AGENT_COLORS["A"]),
        (axes[1], path_b, AGENT_LABELS["B"], AGENT_COLORS["B"]),
    ):
        for r in range(rows):
            for c in range(cols):
                if (r, c) in walls:
                    ax.add_patch(plt.Rectangle((c, rows - 1 - r), 1, 1, color="#222222"))
        xs = [c + 0.5 for (r, c) in path]
        ys = [rows - 1 - r + 0.5 for (r, c) in path]
        ax.plot(xs, ys, "-o", color=color, markersize=3, linewidth=1)
        sr, sc = tuple(maze["start"])
        gr, gc = tuple(maze["goal"])
        ax.text(sc + 0.5, rows - 1 - sr + 0.5, "S", ha="center", va="center", color="white", fontweight="bold")
        ax.text(gc + 0.5, rows - 1 - gr + 0.5, "G", ha="center", va="center", color="#c02020", fontweight="bold")
        ax.set_xlim(0, cols)
        ax.set_ylim(0, rows)
        ax.set_aspect("equal")
        ax.set_xticks([])
        ax.set_yticks([])
        reached = path[-1] == tuple(maze["goal"]) if path else False
        status = "reached goal" if reached else "timed out"
        ax.set_title(f"{label}\n{len(set(path))} distinct cells, {len(path) - 1} steps, {status}")
    fig.suptitle(f"Representative routes on {maze['id']} "
                 f"(greedy policy; cells may be revisited)")
    fig.savefig(out)
    plt.close(fig)
