# Agentic Engineering Template

A generic template for safer AI-assisted development using repo-specific agent rules, task contracts, validation gates, isolated worktrees, and human review loops.

This is a synthetic public teaching template. Its examples and data are invented for this repository; they do not describe or reproduce a private production system.

## Why this exists

AI-assisted development works best when the repo gives agents clear boundaries. A good setup defines what to read, what to change, what to avoid, how to validate work, and where human review is required.

This template collects those guardrails in one small public repo.

## Run the executable example

Requires Python 3.10 or newer; only the standard library is used. From the repository root:

```bash
python3 -m unittest discover -s tests -v
python3 scripts/validate_contract.py \
  --contract examples/valid-task/contract.json \
  --changed-files examples/valid-task/changed-files.json
```

Expected output from the gate (exit status **0**):

```text
PASS: 1 changed file(s), 2 built-in check(s); human review still required
```

Now run the deliberately invalid example:

```bash
python3 scripts/validate_contract.py \
  --contract examples/invalid-task/contract.json \
  --changed-files examples/invalid-task/changed-files.json
```

Expected error (exit status **1**):

```text
FAIL: changed_files: file outside allowed_files
```

The invalid report is valid JSON but falls outside its contract's exact file allowlist. CI asserts this rejection, so the overall workflow passes when both examples behave as expected. Argument usage errors exit with status 2.

## What the example teaches

| Before: written guidance | After: observable check | Human review still covers |
| --- | --- | --- |
| “Keep the change in scope” | Every supplied changed path must match an exact allowed file | Whether the manifest contains the entire real diff |
| “Run validation” | Fixed `nonempty_utf8` and `json_object` checks inspect each changed file | Whether those checks establish the intended behavior |
| “Use safe paths” | Reject traversal, absolute paths, malformed paths, and symlink components | The trustworthiness and stability of the checkout |
| “Request review” | The contract must explicitly require human review; passing output repeats that requirement | Actual approval and the merge decision |

The runnable slice is a synthetic JSON report, not a general agent executor. The [machine contract reference](docs/executable-contract.md) explains its schema, path rules, and limits. The prose templates below remain useful for broader engineering tasks.

## What this template includes

- `AGENTS.md`: repo-specific instructions for coding agents
- `.agent/rules/core-rules.md`: compact rules for scoped implementation
- `docs/agentic-workflow.md`: issue-to-implementation workflow
- `docs/task-contract-template.md`: task contract format
- `docs/review-checklist.md`: human review gate checklist
- `docs/worktree-workflow.md`: isolated worktree guidance
- `examples/`: example task contracts and validation gates
- `scripts/validate_contract.py`: executable contract, boundary, and content checks
- `tests/test_validation.py`: acceptance, rejection, and malformed-input cases
- `.github/workflows/validate.yml`: tests and both expected fixture outcomes

## Recommended workflow

1. Write a short task contract before implementation.
2. Identify in-scope and out-of-scope files or behaviors.
3. Work in an isolated worktree when appropriate.
4. Keep diffs small and avoid unrelated refactors.
5. Run validation gates before claiming completion.
6. Use human review loops for behavior, architecture, and safety-sensitive changes.

## Repository structure

- `.agent/rules/`: reusable agent rules
- `docs/`: workflow, task, review, and worktree documents
- `examples/`: concrete examples of task contracts and validation gates
- `AGENTS.md`: top-level agent instructions
- `CLAUDE.md`: equivalent guidance for Claude-oriented environments

## Agent rules philosophy

Repo-specific agent rules should be boring, explicit, and close to the code. They should help an agent make smaller changes, preserve existing project conventions, avoid private or unrelated material, and report validation evidence clearly.

## Human review gates

Human review is required before accepting changes that affect public APIs, data migrations, authentication, user-visible behavior, research outputs, confidentiality boundaries, or production release paths.

For this executable example, human review is always required. A passing gate does not record approval or authorize a merge.

## What this is not

- It is not a replacement for engineering judgment.
- It is not a prompt pack or automation framework.
- It is not a copy of any private production repo.
- It is not a place for proprietary architecture, private implementation details, user data, or roadmaps.
