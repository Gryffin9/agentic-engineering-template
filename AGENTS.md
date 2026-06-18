# AGENTS.md

## Operating principles

- Keep changes scoped to the task contract.
- Prefer small diffs over broad rewrites.
- Do not perform unrelated refactors.
- Read existing project conventions before editing.
- Preserve user changes and do not overwrite work you did not make.
- Run the validation gates listed in the task contract.
- Ask for human review before merging or publishing.

## Required workflow

1. Read the issue or task contract.
2. Identify the smallest coherent implementation slice.
3. Work in an isolated worktree when the host environment supports it.
4. Make focused edits.
5. Run validation commands.
6. Summarize files changed, validation results, and residual risks.
7. Request human review.

## Safety boundaries

- Do not expose secrets, private data, credentials, prompts, or proprietary implementation details.
- Do not invent product claims.
- Do not silently change public APIs, schemas, or migration behavior.
- Do not delete files or reset branches unless explicitly asked.
