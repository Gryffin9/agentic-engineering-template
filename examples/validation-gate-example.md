# Validation Gate Example

A validation gate should be concrete enough that a different agent or human can run it without guessing.

## Good

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
PYTHONPATH=src python3 examples/run_numerical_integration.py
```

Expected result:

- Unit tests exit with status 0.
- Example prints decreasing numerical integration error as intervals increase.

## Weak

```text
Check that the code works.
```

This is too vague. It does not define the command, expected behavior, or acceptance criteria.
