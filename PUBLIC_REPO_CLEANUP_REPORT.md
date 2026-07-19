# Public repository cleanup report

Date: 2026-07-19. Goal: prepare the repository for a clean public GitHub release
containing only the files needed to understand, reproduce, cite, and inspect the
project. Nothing was committed, tagged, pushed, or published.

## Files removed

Internal workflow, audit, spec, and process files (none held unique reproducibility
information; all of it is covered by the manuscript, source code, and results):
- COMPLETION_REPORT.md
- DECISIONS.md
- EXPERIMENT_PROTOCOL.md
- FINAL_AUDIT.md
- final_validation.json
- PROJECT_SPEC.md
- PUBLICATION_PREP_REPORT.md
- STATUS.md
- manuscript/ (claims_audit.md, method_notes.md, results_notes.md) internal notes
- skills/ (empty directory)

Submission packaging and duplicates:
- release/ (final_paper.pdf duplicate, abstract.txt, keywords.txt,
  ai_disclosure.txt, submission_metadata.md). The paper PDF is retained at
  paper/final_paper.pdf; the extracts are derivable from the manuscript.

Regenerable pilot intermediates (produced by `experiments.run_pilot`, not paper
data):
- results/raw_results_pilot.csv, results/summary_pilot.csv,
  results/summary_by_maze_pilot.csv, results/manifest_pilot.json,
  results/traces_pilot.jsonl

Caches:
- .pytest_cache/, all __pycache__/ and *.pyc

## Files moved

None. The public layout was reached by removal only; paper figures were already
under paper/figures/.

## Files retained

- configs/ (mazes), experiments/ (run_pilot, run_full, make_figures, _harness),
  src/fmgw/ (all modules), tests/ (all tests)
- paper/: figures/ (six PNGs), final_paper.pdf, manuscript.md, references.bib,
  source_notes.md
- results/: raw_results.csv, summary.csv, summary_by_maze.csv, traces.jsonl,
  manifest.json
- .gitignore, CITATION.cff, LICENSE, README.md, pyproject.toml, requirements.txt

## Files added

- PUBLIC_REPO_CLEANUP_REPORT.md (this file, temporary)
- README.md rewritten for public release (14 sections: title, summary, main
  result, structure, install, tests, reproduce, outputs, paper link, citation,
  licence, limitations, preprint statement, AI-disclosure note)
- .gitignore expanded (.env, .env.*, .vscode/, .idea/, *.tmp, *.log, and the
  existing cache and venv entries)

## AI-tool remnants

Found: none. A recursive case-insensitive search for claude, anthropic, humanizer,
SKILL.md, chatgpt, openai, system prompt, chain of thought, ai detector, and
bypass detection returned no matches in the retained files.

Removed as part of the internal files above: the humanizer skill directory
(skills/) was already empty; internal reports and notes that described the process
were deleted.

## Legitimate AI disclosure retained

Yes. paper/manuscript.md keeps Section 9, "Declaration of generative AI
assistance", using generic "generative AI tools" language. README also notes that
AI assistance is disclosed in the paper. No tool names or internal prompts are
exposed.

## Sensitive data findings

- No "Ashish" anywhere.
- No API keys, tokens, passwords, private keys, or .env files.
- No local Windows or home-directory paths.
- The only email present is the approved public contact ishaan.v554@gmail.com
  (CITATION.cff).

## Git-history findings

Only README.md has ever been committed (single "Initial commit", content "# paper").
Every removed file was untracked and therefore never entered git history. A scan of
all history blobs for sensitive terms returned nothing. No history rewrite is
required.

## Validation

- Tests: 34 passed.
- Reproduction: `python -m experiments.run_full` produced 100 runs, integrity
  pairs/counts/reconcile OK.
- Fingerprint: a40f7100e1406a6a0b1d06a2826752bafc7a6570b195c850c752d1cdc0efd93c
  (unchanged).
- README links resolve; manuscript figure paths resolve; final PDF opens (10 pages,
  Author Ishaan Verma); all package modules import cleanly.

## Final public tree

```text
.
├── .gitignore
├── CITATION.cff
├── LICENSE
├── README.md
├── pyproject.toml
├── requirements.txt
├── configs/            __init__.py, mazes.py
├── experiments/        __init__.py, _harness.py, make_figures.py, run_full.py, run_pilot.py
├── paper/
│   ├── figures/        agent_comparison, blocked_actions, oscillation_example,
│   │                   repeated_by_maze, repeated_failed_actions, total_steps (.png)
│   ├── final_paper.pdf
│   ├── manuscript.md
│   ├── references.bib
│   └── source_notes.md
├── results/            raw_results.csv, summary.csv, summary_by_maze.csv,
│                       traces.jsonl, manifest.json
├── src/fmgw/           __init__, environment, policies, memory, agents, metrics,
│                       runner, analysis, integrity
└── tests/              conftest + test_environment, test_failure_memory,
                        test_metrics, test_policy_fairness, test_reproducibility
```

## Remaining manual actions

- Confirm https://github.com/PliableRigidity/paper is the intended public remote.
- Decide whether to keep or remove this PUBLIC_REPO_CLEANUP_REPORT.md before the
  first public commit.
- If the SSRN submission package (previously in release/) is still wanted for
  submission, keep a local copy outside the public repo; its content is derivable
  from the manuscript.
- Stage, commit, and push when ready (not done here).
