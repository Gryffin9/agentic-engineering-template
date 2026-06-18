# Worktree Workflow

Isolated worktrees help keep parallel agent tasks from stepping on each other.

## Recommended flow

```bash
git fetch origin
git worktree add ../repo-task-name -b codex/task-name origin/main
cd ../repo-task-name
```

Run setup and baseline validation before editing:

```bash
git status --short --branch
# project-specific install command
# project-specific test command
```

## Rules

- One task contract per worktree.
- No unrelated branch cleanup from inside a task worktree.
- No force-push unless explicitly approved.
- Keep generated artifacts out of commits unless the task contract asks for them.
- Preserve the worktree until review feedback is resolved.

## Completion

Before opening a pull request, include:

- changed files,
- validation commands and outcomes,
- known limitations,
- review risks,
- screenshots or logs when relevant.
