# Agentic Engineering Template

A generic public template for safe AI-assisted and structured multi-agent engineering workflows.

This repo is not copied from any private project. It contains reusable, sanitized workflow documents for repo-specific agent rules, task contracts, isolated worktrees, validation gates, and human review loops.

## What this template provides

- `AGENTS.md`: repo-specific instructions for coding agents.
- `CLAUDE.md`: equivalent guidance for Claude-oriented environments.
- `.agent/rules/core-rules.md`: compact rules for scoped implementation.
- `docs/agentic-workflow.md`: issue-to-implementation workflow.
- `docs/worktree-workflow.md`: isolated worktree guidance.
- `docs/review-checklist.md`: human review gate checklist.
- `docs/task-contract-template.md`: task contract format before implementation begins.
- `examples/`: filled examples for task contracts and validation gates.

## Intended use

Use this as a starting point for small teams or solo builders who want agentic engineering to be disciplined rather than chaotic:

- small diffs,
- explicit success criteria,
- no unrelated refactors,
- validation commands,
- human-in-the-loop review,
- traceable task contracts.

## Non-goals

- This is not a broad service-business starter kit.
- This is not a replacement for engineering judgment.
- This does not include private project internals.
- This does not include prompts, model orchestration, source pipelines, schemas, or private implementation contracts.
