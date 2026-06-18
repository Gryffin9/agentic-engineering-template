# Example Task Contract

## Goal

Add a deterministic CSV export command for a synthetic analysis report.

## Context

The repo already has analysis functions and tests. The task is only to expose a small command-line export path.

## In scope

- Add one CLI entrypoint.
- Add one test for generated CSV headers.
- Update README run instructions.

## Out of scope

- Changing the analysis formula.
- Adding external dependencies.
- Reformatting unrelated files.

## Success criteria

- Running the command writes a CSV file to the documented output path.
- The generated CSV has stable column order.
- Existing tests still pass.

## Validation gates

```bash
python3 -m unittest
python3 examples/export_report.py
```

## Human review focus

Confirm the command is easy to run and the output path is documented.
