"""Fixed maze set for the experiment (EXPERIMENT_PROTOCOL Section 5).

Mazes are authored as ASCII layouts and parsed into immutable dictionaries.
Legend: '#' wall, 'S' start, 'G' goal, '.' open cell. Every maze is validated for
reachability and for a shortest path below its step limit before runs
(configs are treated as fixed data once runs begin, D005/D006).

The fallback subset (D007) is mazes 1 to 5.
"""
from __future__ import annotations

from typing import Dict, List

_LAYOUTS: Dict[str, str] = {
    # 1. Easy, mostly open. A direct greedy path exists.
    "maze_01": """
S.....
......
..##..
..##..
......
.....G
""",
    # 2. Dead-end pockets branching off a main corridor.
    "maze_02": """
S.....#
.####.#
.#..#.#
.#.##.#
.#....#
.####.#
......G
""",
    # 3. Narrow serpentine corridor. Single-cell connectors between rows.
    "maze_03": """
S......
######.
.......
.######
.......
######.
G......
""",
    # 4. Misleading route: vertical walls block the greedy rightward move,
    #    forcing a downward detour to the open bottom row.
    "maze_04": """
S.#.#.#
..#.#.#
..#.#.#
..#.#.#
..#.#.#
..#.#.#
......G
""",
    # 5. Repeat-block prone: the goal sits in an alcove entered from below.
    "maze_05": """
S.....
.####.
.#..#.
.#G.#.
.#.##.
......
""",
    # 6. Open room with a central block (multiple equal-length paths).
    "maze_06": """
S.......
........
..####..
..#..#..
..#..#..
..####..
........
.......G
""",
    # 7. Comb of vertical walls forcing lateral detours.
    "maze_07": """
S.#.#.#.
..#.#.#.
..#.#.#.
..#.#.#.
..#.#.#.
..#.#.#.
........
#######G
""",
    # 8. Spiral-like inward path.
    "maze_08": """
S.......
.#####.#
.#...#.#
.#.#.#.#
.#.#...#
.#.####.
.#......
.######G
""",
    # 9. Two candidate corridors, one a dead end.
    "maze_09": """
S.....#
.#.##.#
.#.#..#
.#.#.##
.#.#..#
.#.##.#
...#..G
""",
    # 10. Larger sparse field with scattered obstacles.
    "maze_10": """
S........
.##.##.#.
....#....
.#.##.##.
.#....#..
.####.#.#
....#...#
.##.###..
........G
""",
}


def _parse(maze_id: str, layout: str) -> Dict[str, object]:
    grid: List[str] = [line for line in layout.splitlines() if line != ""]
    rows = len(grid)
    cols = max(len(line) for line in grid)
    walls = set()
    start = None
    goal = None
    for r, line in enumerate(grid):
        for c in range(cols):
            ch = line[c] if c < len(line) else "."
            if ch == "#":
                walls.add((r, c))
            elif ch == "S":
                start = (r, c)
            elif ch == "G":
                goal = (r, c)
    if start is None or goal is None:
        raise ValueError(f"{maze_id}: layout must contain S and G")
    return {
        "id": maze_id,
        "size": (rows, cols),
        "start": start,
        "goal": goal,
        "walls": frozenset(walls),
    }


MAZES: List[Dict[str, object]] = [_parse(mid, layout) for mid, layout in _LAYOUTS.items()]
MAZES_BY_ID: Dict[str, Dict[str, object]] = {m["id"]: m for m in MAZES}

# Fallback subset (D007): mazes 1 to 5.
FALLBACK_MAZES: List[Dict[str, object]] = MAZES[:5]

# Seeds (D005/D007). Full uses all five; fallback uses seeds 0 to 2.
SEEDS: List[int] = [0, 1, 2, 3, 4]
FALLBACK_SEEDS: List[int] = [0, 1, 2]
