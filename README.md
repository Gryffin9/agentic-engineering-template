# Agentic Engineering Template

A generic template for safer AI-assisted development using repo-specific agent rules, task contracts, validation gates, isolated worktrees, and human review loops.

This is a generic public template inspired by my experience building private production-scale systems. It does not include proprietary Clymber or PRA internals.

## Why this exists

AI-assisted development works best when the repo gives agents clear boundaries. A good setup defines what to read, what to change, what to avoid, how to validate work, and where human review is required.

This template collects those guardrails in one small public repo.

## What this template includes

- `AGENTS.md`: repo-specific instructions for coding agents
- `.agent/rules/core-rules.md`: compact rules for scoped implementation
- `docs/agentic-workflow.md`: issue-to-implementation workflow
- `docs/task-contract-template.md`: task contract format
- `docs/review-checklist.md`: human review gate checklist
- `docs/worktree-workflow.md`: isolated worktree guidance
- `examples/`: example task contracts and validation gates

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

## What this is not

- It is not a replacement for engineering judgment.
- It is not a prompt pack or automation framework.
- It is not a copy of any private production repo.
- It is not a place for proprietary architecture, private implementation details, user data, or roadmaps.
