"""Memory-strategy behaviour and the A/B contrast (D008, rules 1 and 2)."""
from fmgw.memory import PersistentMemory, TransientExclusion
from fmgw.agents import make_agent
from fmgw.policies import action_priority_permutation
from fmgw.runner import run_single
from configs.mazes import MAZES_BY_ID


def test_transient_clears_after_one_decision():
    m = TransientExclusion()
    m.reset_for_run()
    s = (2, 2)
    m.record_block(s, "right")
    m.after_decision()                 # exclusion now active for the next decision
    assert m.excluded(s) == {"right"}
    # a decision passes with no new block
    m.after_decision()
    assert m.excluded(s) == set()      # transient exclusion cleared


def test_transient_does_not_persist_across_revisit():
    m = TransientExclusion()
    m.reset_for_run()
    s = (2, 2)
    m.record_block(s, "right")
    m.after_decision()
    m.after_decision()                 # leaves state, exclusion cleared
    assert m.excluded(s) == set()


def test_persistent_keeps_excluding_across_revisits():
    m = PersistentMemory()
    m.reset_for_run()
    s = (2, 2)
    m.record_block(s, "right")
    m.after_decision()
    for _ in range(10):
        m.after_decision()
    assert m.excluded(s) == {"right"}


def test_memory_clears_between_runs():
    for cls in (TransientExclusion, PersistentMemory):
        m = cls()
        m.reset_for_run()
        m.record_block((1, 1), "up")
        m.after_decision()
        m.reset_for_run()
        assert m.excluded((1, 1)) == set()


def test_fallback_when_all_actions_excluded():
    # Persistent memory blocking all four actions -> agent ignores exclusions.
    agent = make_agent("B")
    agent.reset_for_run()
    s = (2, 2)
    for a in ("up", "down", "left", "right"):
        agent.memory.record_block(s, a)
    perm = action_priority_permutation(0)
    decision = agent.decide(s, (5, 5), perm)
    assert decision.used_fallback is True
    assert decision.chosen in ("up", "down", "left", "right")


def test_agent_a_never_repeats_blocked_action_consecutively():
    # Run Agent A on every maze/seed and check the trace for back-to-back repeats.
    for maze in MAZES_BY_ID.values():
        for seed in range(5):
            agent = make_agent("A")
            _, trace = run_single(maze, seed, agent)
            for i in range(len(trace) - 1):
                e, nxt = trace[i], trace[i + 1]
                if e["blocked"] and nxt["state"] == e["state"]:
                    assert nxt["chosen"] != e["chosen"], (maze["id"], seed, i)


def test_persistent_avoids_a_repeat_that_transient_makes():
    # maze_03 is a serpentine corridor where the greedy reducing move is often a
    # wall; Agent B repeats fewer blocked pairs than Agent A on every seed.
    maze = MAZES_BY_ID["maze_03"]
    found = False
    for seed in range(5):
        _, ta = run_single(maze, seed, make_agent("A"))
        _, tb = run_single(maze, seed, make_agent("B"))

        def repeats(trace):
            seen, rep = set(), 0
            for e in trace:
                pair = (tuple(e["state"]), e["chosen"])
                if pair in seen:
                    rep += 1
                if e["blocked"]:
                    seen.add(pair)
            return rep

        if repeats(ta) > repeats(tb):
            found = True
            break
    assert found
