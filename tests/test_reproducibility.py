"""Reproducibility and paired-run integrity (D005, D007, EXPERIMENT_PROTOCOL S12)."""
from configs.mazes import MAZES, SEEDS
from fmgw.integrity import (check_counts, check_pair_integrity,
                            reconcile_summary, rows_fingerprint)
from fmgw.runner import RAW_COLUMNS, run_matrix
from fmgw.analysis import summarize


def test_matrix_is_deterministic():
    rows1, _ = run_matrix(MAZES, SEEDS)
    rows2, _ = run_matrix(MAZES, SEEDS)
    fp1 = rows_fingerprint(rows1, RAW_COLUMNS)
    fp2 = rows_fingerprint(rows2, RAW_COLUMNS)
    assert fp1 == fp2


def test_run_count_is_100():
    rows, _ = run_matrix(MAZES, SEEDS)
    assert len(rows) == 10 * 5 * 2 == 100


def test_pair_integrity():
    rows, _ = run_matrix(MAZES, SEEDS)
    rep = check_pair_integrity(rows)
    assert rep["ok"] is True
    assert rep["n_pairs"] == 50


def test_counts_equal():
    rows, _ = run_matrix(MAZES, SEEDS)
    assert check_counts(rows)["ok"] is True


def test_summary_reconciles_with_rows():
    rows, _ = run_matrix(MAZES, SEEDS)
    summary = summarize(rows)
    assert reconcile_summary(rows, summary)["ok"] is True


def test_action_priority_matches_seed():
    from fmgw.policies import action_priority_permutation, format_permutation
    rows, _ = run_matrix(MAZES, SEEDS)
    for r in rows:
        expected = format_permutation(action_priority_permutation(r["seed"]))
        assert r["action_priority"] == expected
