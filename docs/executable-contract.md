# Executable synthetic contract

The example follows four observable steps:

1. Write a task contract: [valid contract](../examples/valid-task/contract.json).
2. Implement only the allowed file: [synthetic report](../examples/valid-task/report.json), listed in the [changed-file manifest](../examples/valid-task/changed-files.json).
3. Run `scripts/validate_contract.py` with the contract and manifest.
4. Expect acceptance for the valid fixture and rejection for the [out-of-scope fixture](../examples/invalid-task/changed-files.json), then obtain human review.

All fixture paths are relative to the repository root, not the contract's directory. By default the CLI uses the repository containing the script. `--repo-root PATH` selects a different trusted checkout for local experiments.

## Schema version 1

Contracts are strict JSON objects with exactly these fields; unknown or missing fields are rejected:

| Field | Requirement |
| --- | --- |
| `schema_version` | Integer `1` (a boolean is not accepted) |
| `task_id` | Nonempty string identifying the synthetic task |
| `goal` | Nonempty string describing the intended outcome |
| `allowed_files` | Nonempty list of unique, exact repository-relative file paths; no glob patterns |
| `validations` | Nonempty list of unique names from the table below |
| `human_review_required` | Boolean `true` |

The separate manifest is a nonempty JSON array of unique changed-file paths. Both JSON inputs reject duplicate object keys and nonstandard constants such as `NaN`. The gate checks scope before file contents.

| Validation name | Fixed implementation |
| --- | --- |
| `nonempty_utf8` | Each changed file decodes as UTF-8 and contains non-whitespace text |
| `json_object` | Each changed file parses as a strict JSON object; arrays and scalar roots are rejected |

Every selected check runs on every supplied changed file. Files must be existing regular UTF-8 files. Validation names are allowlisted identifiers, never shell commands. There is no `eval`, command runner, dependency installation, or agent API call.

Paths use `/` separators and only ASCII letters, digits, `_`, `-`, and `.` within components. Empty components, `.` and `..`, `.git` components, absolute paths, backslashes, whitespace, and symlink components are rejected. Allowed paths are checked as well as manifest paths. The checker reads files and does not modify them.

## Deliberate limits

- The manifest is supplied by the caller. This example does not derive changes from Git or detect omitted changes; review the actual diff against the manifest.
- The contract is also supplied by the caller. A reviewer must approve the contract itself so scope cannot simply be widened to accommodate unrelated work.
- Goal text is descriptive. Built-in checks establish file scope and basic content structure, not report correctness or completion of an arbitrary task.
- Deletions, renames, binary files, and directory or glob allowlists are outside this small example's supported scope. A rename would need review of both paths in a fuller integration.
- Path checks assume a stable trusted local checkout. They are not a sandbox against concurrent filesystem mutation, hard-link aliases, or a hostile operating system.
- `human_review_required: true` is a prerequisite, not evidence that someone reviewed the work. CI does not merge or publish changes.

To adapt this template, first define the behavior a reviewer needs to verify, then add a fixed validation with acceptance and rejection tests. Keep arbitrary commands out of untrusted contracts.
