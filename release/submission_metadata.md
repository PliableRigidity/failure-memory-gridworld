# SSRN submission metadata

## Title

Failure Memory in Grid-World Agents

## Author

Ishaan Verma

ORCID: https://orcid.org/0009-0006-2038-3274

## Affiliation

University of Bristol

## Author role

Undergraduate student

## Research status

Independent research conducted outside a formal university project. The work was
not supervised, funded, or endorsed by the University of Bristol.

## Contact email

ishaan.v554@gmail.com
(Confirm this is the intended public contact address before submission.)

## Paper type

Independent research preprint. Version 1.0, July 2026.

## Peer-review status

Not peer reviewed.

## Abstract

An agent that acts over many steps can waste effort by attempting the same
blocked move more than once. This study measures whether persistent within-run
memory of blocked state-action pairs reduces that waste in a simple grid world,
and whether the reduction changes task outcomes. Two agents share an identical
deterministic policy that ranks moves by Manhattan-distance reduction and breaks
ties with a seeded action permutation. They differ in one respect. The baseline
agent excludes a blocked pair for the next decision only, which gives immediate
reactive recovery. The memory agent excludes a blocked pair for the rest of the
run. The comparison uses 10 fixed mazes and 5 seeds, giving 100 paired runs.
Persistent memory removed repeated blocked actions, reducing the mean from 35.12
to 0.00 per run, and cut mean blocked actions from 37.00 to 2.04. Success rate
and mean total steps did not change: both agents reached the goal in 56 percent
of runs and used 65.5 steps on average. The two agents behaved identically on the
five mazes that both solve. They differed only on the five mazes where the
baseline became trapped. On those mazes both agents still failed, because the
greedy policy fell into oscillations between valid, unblocked cells, which
blocked-action memory cannot detect. Persistent failure memory therefore reduced
one class of repeated error without improving overall navigation. All code, data,
and figures are released, and the full run reproduces to an identical fingerprint.

## Keywords

embodied agents, agent memory, failure memory, grid-world navigation, persistent
memory, autonomous agents, reactive navigation, navigation planning, reproducible
evaluation

## Repository link

https://github.com/PliableRigidity/failure-memory-gridworld

## Suggested SSRN subject areas

These are suggestions under the Computer Science Research Network (CompSciRN) and
should be confirmed against the current SSRN network list at submission time:

- Artificial Intelligence (agents and memory)
- Machine Learning
- Robotics (navigation and planning)

## Generative AI assistance disclosure

Generative AI tools were used for software-development assistance, literature
discovery, and language editing. The author designed and verified the experiments,
reviewed the sources, interpreted the results, and takes responsibility for the
final work.

## Reproducibility

The code and experiment are reproducible from the repository. The full run is
deterministic and produces the raw-row fingerprint
a40f7100e1406a6a0b1d06a2826752bafc7a6570b195c850c752d1cdc0efd93c. Reproduce with:

    python -m pip install -r requirements.txt
    python -m experiments.run_full
    python -m pytest

## Final file checklist for SSRN upload

- [ ] final_paper.pdf (the typeset paper, this folder)
- [ ] Title entered exactly as above
- [ ] Author name: Ishaan Verma
- [ ] Affiliation: University of Bristol; role: Undergraduate student
- [ ] Research status noted as independent (not supervised, funded, or endorsed)
- [ ] Contact email confirmed
- [ ] Abstract pasted from abstract.txt
- [ ] Keywords pasted from keywords.txt
- [ ] AI-assistance disclosure pasted from ai_disclosure.txt
- [ ] Repository URL added
- [ ] SSRN subject areas selected
- [ ] Peer-review status marked as not peer reviewed
