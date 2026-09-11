#!/usr/bin/env python3
"""Validate a synthetic task contract and supplied changed-file manifest.

This is a deterministic teaching gate, not a sandbox or a merge authorization.
Contract validation names select fixed checks; no contract commands are executed.
"""

import argparse
import json
from pathlib import Path
import re
import sys


FIELDS = {"schema_version", "task_id", "goal", "allowed_files", "validations",
          "human_review_required"}
VALIDATIONS = {"nonempty_utf8", "json_object"}
REPO_ROOT = Path(__file__).resolve().parents[1]


class ValidationError(ValueError):
    """A task failed the gate."""


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValidationError("duplicate JSON key")
        result[key] = value
    return result


def reject_constant(value):
    raise ValidationError("nonstandard JSON constant")


def parse_json(text):
    return json.loads(text, object_pairs_hook=unique_object, parse_constant=reject_constant)


def load_json(path, label):
    try:
        return parse_json(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, RecursionError) as exc:
        raise ValidationError(f"{label}: cannot read strict JSON") from exc


def string_list(value, label):
    if (not isinstance(value, list) or not value
            or any(not isinstance(item, str) or not item.strip() for item in value)):
        raise ValidationError(f"{label}: expected a nonempty list of strings")
    if len(set(value)) != len(value):
        raise ValidationError(f"{label}: duplicate entries")
    return value


def safe_path(value, root):
    # Use a deliberately portable subset: exact POSIX-style relative file paths.
    parts = value.split("/")
    if (not re.fullmatch(r"[A-Za-z0-9_./-]+", value)
            or any(part.lower() in {"", ".", "..", ".git"} for part in parts)):
        raise ValidationError("unsafe repository-relative path")
    path = root
    for part in parts:
        path = path / part
        if path.is_symlink():
            raise ValidationError("unsafe symlink in repository-relative path")
    if not path.resolve().is_relative_to(root):
        raise ValidationError("unsafe path escapes repository root")
    return path


def validate(contract, changed, root):
    if not isinstance(contract, dict) or set(contract) != FIELDS:
        raise ValidationError("contract: expected exactly the documented schema fields")
    if type(contract["schema_version"]) is not int or contract["schema_version"] != 1:
        raise ValidationError("contract: schema_version must be integer 1")
    for field in ("task_id", "goal"):
        if not isinstance(contract[field], str) or not contract[field].strip():
            raise ValidationError(f"contract: {field} must be a nonempty string")
    if contract["human_review_required"] is not True:
        raise ValidationError("contract: human_review_required must be true")
    allowed = string_list(contract["allowed_files"], "contract allowed_files")
    checks = string_list(contract["validations"], "contract validations")
    if set(checks) - VALIDATIONS:
        raise ValidationError("contract: unknown validation; only nonempty_utf8 and json_object are allowed")
    changed = string_list(changed, "changed_files")
    for name in allowed:
        safe_path(name, root)
    paths = [safe_path(name, root) for name in changed]
    if set(changed) - set(allowed):
        raise ValidationError("changed_files: file outside allowed_files")
    for path in paths:
        if not path.is_file():
            raise ValidationError("changed_files: expected an existing regular file")
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeError as exc:
            raise ValidationError("validation: file must be UTF-8") from exc
        if "nonempty_utf8" in checks and not content.strip():
            raise ValidationError("validation nonempty_utf8: file is empty")
        if "json_object" in checks:
            try:
                parsed = parse_json(content)
            except (ValueError, RecursionError) as exc:
                raise ValidationError("validation json_object: expected a strict JSON object") from exc
            if not isinstance(parsed, dict):
                raise ValidationError("validation json_object: expected a JSON object")
    return len(changed), len(checks)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--changed-files", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, default=REPO_ROOT)
    args = parser.parse_args()
    try:
        root = args.repo_root.resolve(strict=True)
        if not root.is_dir():
            raise ValidationError("repository root must be a directory")
        count, checks = validate(load_json(args.contract, "contract"),
                                 load_json(args.changed_files, "changed_files"), root)
    except (OSError, ValueError, RuntimeError) as exc:
        # Do not echo input contents or absolute filesystem paths in diagnostics.
        reason = str(exc) if isinstance(exc, ValidationError) else "cannot inspect repository files"
        print(f"FAIL: {reason}", file=sys.stderr)
        return 1
    print(f"PASS: {count} changed file(s), {checks} built-in check(s); human review still required")
    return 0


if __name__ == "__main__":
    sys.exit(main())
