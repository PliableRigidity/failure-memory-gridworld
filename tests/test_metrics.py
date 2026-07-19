"""Metric correctness from the external action log (D002)."""
from fmgw.metrics import compute_metrics, repeated_failed_actions


def entry(state, chosen, blocked, new_position=None, goal=False):
    return {
        "state": state, "chosen": chosen, "blocked": blocked,
        "new_position": new_position if new_position is not None else state,
        "goal_reached": goal,
    }


def test_repeated_counts_only_after_prior_block():
    log = [
        entry((0, 0), "right", True),   # first block, not a repeat
        entry((0, 0), "down", False, (1, 0)),
        entry((1, 0), "up", False, (0, 0)),
        entry((0, 0), "right", True),   # repeat of a previously blocked pair
    ]
    assert repeated_failed_actions(log) == 1


def test_no_repeat_for_distinct_pairs():
    log = [
        entry((0, 0), "right", True),
        entry((0, 0), "up", True),      # different action, not a repeat
        entry((1, 1), "right", True),   # different state, not a repeat
    ]
    assert repeated_failed_actions(log) == 0


def test_total_steps_counts_blocked_attempts():
    log = [
        entry((0, 0), "right", True),
        entry((0, 0), "down", False, (1, 0)),
    ]
    m = compute_metrics(log, success=False)
    assert m["total_steps"] == 2
    assert m["blocked_actions"] == 1


def test_success_flag():
    log = [entry((0, 0), "down", False, (1, 0), goal=True)]
    assert compute_metrics(log, success=True)["success"] == 1
    assert compute_metrics(log, success=False)["success"] == 0


def test_metric_independent_of_agent_identity():
    # The same log yields the same numbers regardless of which agent produced it.
    log = [
        entry((0, 0), "right", True),
        entry((0, 0), "right", True),   # repeat
        entry((0, 0), "down", False, (1, 0)),
    ]
    m1 = compute_metrics(log, success=False)
    m2 = compute_metrics(list(log), success=False)
    assert m1 == m2
    assert m1["repeated_failed_actions"] == 1
