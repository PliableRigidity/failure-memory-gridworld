# Failure Memory in Grid-World Navigation

Paper: **Learning What Not to Do: Evaluating Persistent Failure Memory in
Grid-World Navigation Agents**. Author: Ishaan Verma (Independent Researcher).
This is an independent research preprint.

## Summary

This project studies whether an explicit memory of failed state-action pairs
reduces repeated navigation errors in a simple grid world. Two agents share an
identical deterministic policy and differ in one respect: how long a blocked move
is remembered. Agent A (transient) avoids a blocked move for the next decision
only. Agent B (persistent) avoids it for the rest of the run. The comparison runs
10 fixed mazes with 5 seeds, giving 100 paired runs, and measures success rate,
total steps, blocked actions, and repeated failed actions from an external action
log.

## Main result

Persistent memory removed repeated blocked actions and cut blocked actions, but
did not change task outcomes.

| Metric | Agent A (transient) | Agent B (persistent) |
|:-----------------------------|--------------------:|---------------------:|
| Success rate | 0.56 | 0.56 |
| Mean total steps | 65.50 | 65.50 |
| Mean blocked actions | 37.00 | 2.04 |
| Mean repeated failed actions | 35.12 | 0.00 |

The agents behaved identically on the five mazes both solve. They diverged only
on the five mazes where Agent A became trapped in oscillation. Agent B removed the
repeated blocked actions there but still failed those mazes, because the greedy
base policy falls into oscillations between open cells that failure memory does
not address. The hypothesis is partially supported: fewer repeated blocked
actions, but not fewer steps or higher success.

## Repository structure

```text
.
├── configs/            fixed maze definitions
├── experiments/        pilot, full experiment, and figure scripts
├── paper/
│   ├── figures/        the six figures used by the paper
│   ├── final_paper.pdf typeset paper
│   ├── manuscript.md   manuscript source
│   ├── references.bib  verified bibliography (11 entries)
│   └── source_notes.md per-source verification notes
├── results/            raw_results.csv, summary.csv, summary_by_maze.csv,
│                       traces.jsonl, manifest.json
├── src/fmgw/           environment, policy, memory, agents, metrics, runner,
│                       analysis, integrity checks
├── tests/              environment, fairness, memory, metrics, reproducibility
├── CITATION.cff
├── LICENSE
├── pyproject.toml
└── requirements.txt
```

## Installation

```bash
python -m pip install -r requirements.txt
```

Python 3.9 or newer. The package uses a src layout; the experiment scripts add
`src/` to the path, so no install step is required to run them.

## Tests

```bash
python -m pytest
```

## Reproduce the experiment

```bash
python -m experiments.run_pilot     # pilot plus the four validity checks
python -m experiments.run_full      # full 100-run experiment
python -m experiments.make_figures  # regenerate the six paper figures
```

The full run is deterministic. Two runs produce the identical raw-row fingerprint
recorded in `results/manifest.json`.

## Outputs

- `results/raw_results.csv`: one row per run (100 rows).
- `results/summary.csv` and `results/summary_by_maze.csv`: aggregated metrics.
- `results/traces.jsonl`: full per-step traces.
- `results/manifest.json`: run manifest and raw-row fingerprint.
- `paper/figures/`: the six figures used by the paper.

## The paper

The typeset paper is at [paper/final_paper.pdf](paper/final_paper.pdf); the source
is [paper/manuscript.md](paper/manuscript.md).

## Citation

Citation metadata is in [CITATION.cff](CITATION.cff). Please cite the preprint:

> Verma, I. (2026). Learning What Not to Do: Evaluating Persistent Failure Memory
> in Grid-World Navigation Agents. Independent research preprint.

## Licence

Code is released under the MIT Licence; see [LICENSE](LICENSE).

## Limitations

A small deterministic grid world with no sensor noise and no real-robot dynamics.
A greedy Manhattan base policy with no memory of visited cells, so failures on hard
mazes come from open-cell oscillation rather than repeated blocked actions. A plain
set memory with no decay or confidence. A small hand-designed maze set. Findings
describe behaviour in these grid worlds and are not evidence about physical robots.
No statistical significance is claimed; the design does not sample a population.

## AI-assistance disclosure

Generative AI assistance is disclosed in the paper (Section 9). The author verified
the cited sources, executed and inspected the experiments, interpreted the results,
revised the manuscript, and takes responsibility for the final content.
