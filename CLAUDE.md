# CLAUDE.md

This file mirrors the generic repo guardrails in `AGENTS.md` for Claude-oriented coding environments.

## Default behavior

- Treat every task as a scoped engineering change with explicit success criteria.
- Use repo-specific instructions before general preferences.
- Keep implementation and review notes grounded in observable code behavior.
- Prefer deterministic validation over confidence.

## Before editing

- Read the relevant files.
- Confirm the task contract.
- Identify validation commands.
- Check for uncommitted user changes.

## Before completion

- Run the requested validation gates.
- Report exact commands and outcomes.
- List any unverified assumptions.
- Leave the branch ready for human review.
