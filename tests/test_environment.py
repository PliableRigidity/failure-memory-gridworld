"""Environment behaviour and validation-only BFS (EXPERIMENT_PROTOCOL S1, D006)."""
from fmgw.environment import GridWorld, bfs_shortest_path, validate_maze


def make_env():
    # 3x3, wall at (1,1). start (0,0) goal (2,2).
    return GridWorld(rows=3, cols=3, start=(0, 0), goal=(2, 2), walls={(1, 1)})


def test_open_move_updates_position():
    env = make_env()
    env.reset()
    obs = env.step("right")
    assert obs["new_position"] == (0, 1)
    assert obs["blocked"] is False
    assert obs["goal_reached"] is False


def test_out_of_bounds_is_blocked_and_stays():
    env = make_env()
    env.reset()
    obs = env.step("up")
    assert obs["blocked"] is True
    assert obs["new_position"] == (0, 0)


def test_wall_is_blocked():
    env = make_env()
    env.reset()
    env.step("right")  # (0,1)
    obs = env.step("down")  # into wall (1,1)
    assert obs["blocked"] is True
    assert obs["new_position"] == (0, 1)


def test_goal_detection():
    env = make_env()
    env.reset()
    for a in ("right", "right", "down", "down"):
        obs = env.step(a)
    assert obs["goal_reached"] is True


def test_determinism_same_actions_same_outcome():
    seq = ("right", "down", "down", "right")
    outs = []
    for _ in range(2):
        env = make_env()
        env.reset()
        outs.append([env.step(a)["new_position"] for a in seq])
    assert outs[0] == outs[1]


def test_environment_has_no_history():
    env = make_env()
    env.reset()
    env.step("right")
    env.reset()
    assert env.position == (0, 0)


def test_traversable_and_step_limit():
    env = make_env()
    assert env.traversable_cells() == 9 - 1
    assert env.step_limit() == 4 * 8


def test_bfs_shortest_path():
    assert bfs_shortest_path(3, 3, {(1, 1)}, (0, 0), (2, 2)) == 4
    # fully wall off the goal
    assert bfs_shortest_path(3, 3, {(2, 1), (1, 2)}, (0, 0), (2, 2)) is None


def test_validate_maze_report():
    maze = {"id": "t", "size": (3, 3), "start": (0, 0), "goal": (2, 2), "walls": {(1, 1)}}
    rep = validate_maze(maze)
    assert rep["ok"] is True
    assert rep["shortest_path"] == 4
    assert rep["step_limit"] == 32
