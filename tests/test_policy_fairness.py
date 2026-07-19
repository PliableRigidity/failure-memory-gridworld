"""Shared-policy fairness and determinism (D005, rules 3 and 4)."""
import random

from configs.mazes import SEEDS
from fmgw.agents import make_agent
from fmgw.policies import (action_priority_permutation, manhattan,
                           rank_candidates)
from fmgw.environment import ACTIONS


def test_same_seed_same_permutation():
    for seed in SEEDS:
        assert action_priority_permutation(seed) == action_priority_permutation(seed)


def test_five_seeds_five_unique_permutations():
    perms = {action_priority_permutation(s) for s in SEEDS}
    assert len(perms) == len(SEEDS) == 5


def test_permutation_is_a_full_permutation():
    for seed in SEEDS:
        perm = action_priority_permutation(seed)
        assert sorted(perm) == sorted(ACTIONS)


def test_selection_consumes_no_rng():
    # If selection drew from the global RNG, the state would change.
    random.seed(1234)
    before = random.getstate()
    perm = action_priority_permutation(0)
    for _ in range(50):
        rank_candidates((2, 3), (5, 5), list(ACTIONS), perm)
    after = random.getstate()
    assert before == after


def test_manhattan_ranking_prefers_distance_reduction():
    perm = action_priority_permutation(0)
    # Goal is below-right; down and right reduce distance, up and left increase it.
    ranked = rank_candidates((0, 0), (5, 5), list(ACTIONS), perm)
    assert set(ranked[:2]) == {"down", "right"}
    assert set(ranked[2:]) == {"up", "left"}


def test_ties_broken_only_by_permutation():
    # From (0,0) to goal (0,5): 'right' reduces, others do not reduce equally;
    # use a symmetric goal so up/down tie and left/right differ.
    perm = action_priority_permutation(0)  # up, down, left, right
    # goal straight down: only 'down' reduces; up increases; left/right tie at 0 change.
    ranked = rank_candidates((3, 3), (9, 3), list(ACTIONS), perm)
    assert ranked[0] == "down"
    # left and right both leave manhattan unchanged; permutation order decides.
    assert ranked.index("left") < ranked.index("right")


def test_empty_memory_agents_select_identically():
    perm = action_priority_permutation(2)
    a = make_agent("A")
    b = make_agent("B")
    a.reset_for_run()
    b.reset_for_run()
    da = a.decide((1, 1), (5, 5), perm)
    db = b.decide((1, 1), (5, 5), perm)
    assert da.chosen == db.chosen
