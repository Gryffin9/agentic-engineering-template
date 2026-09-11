"""Exercise the public gate as a CLI, including adversarial task inputs."""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "validate_contract.py"


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "output").mkdir()
        (self.root / "output/report.json").write_text('{"status": "ready"}\n')
        self.contract = {
            "schema_version": 1,
            "task_id": "synthetic-report",
            "goal": "Add a synthetic JSON report.",
            "allowed_files": ["output/report.json"],
            "validations": ["nonempty_utf8", "json_object"],
            "human_review_required": True,
        }
        self.changed = ["output/report.json"]

    def run_gate(self, contract_text=None, manifest_text=None):
        contract = self.root / "contract.json"
        manifest = self.root / "changed-files.json"
        contract.write_text(contract_text if contract_text is not None else json.dumps(self.contract))
        manifest.write_text(manifest_text if manifest_text is not None else json.dumps(self.changed))
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--repo-root", str(self.root),
             "--contract", str(contract), "--changed-files", str(manifest)],
            capture_output=True, text=True, check=False,
        )

    def assert_rejected(self, result, reason):
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("FAIL:", result.stderr)
        self.assertIn(reason, result.stderr)

    def test_accepts_valid_change_but_requires_human_review(self):
        result = self.run_gate()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS:", result.stdout)
        self.assertIn("human review still required", result.stdout)

    def test_rejects_out_of_scope_file(self):
        self.changed = ["output/other.json"]
        self.assert_rejected(self.run_gate(), "outside allowed_files")

    def test_rejects_unsafe_paths_in_contract_and_manifest(self):
        for path in ["../outside.json", "/tmp/outside.json", "output/../report.json",
                     "output//report.json", "./output/report.json", "output/",
                     "C:/report.json", "output\\report.json", ".git/config", ".GIT/config",
                     "output/\nreport.json", "output/\x00report.json"]:
            for field in ["allowed_files", "changed_files"]:
                with self.subTest(path=path, field=field):
                    self.contract["allowed_files"] = ["output/report.json"]
                    self.changed = ["output/report.json"]
                    if field == "allowed_files":
                        self.contract[field] = [path]
                    else:
                        self.changed = [path]
                    self.assert_rejected(self.run_gate(), "unsafe")

    def test_rejects_symlink_file_and_directory(self):
        for name, target in [("linked.json", "output/report.json"), ("linked-dir", "output")]:
            with self.subTest(name=name):
                (self.root / name).symlink_to(self.root / target)
                path = name if name.endswith(".json") else name + "/report.json"
                self.contract["allowed_files"] = [path]
                self.changed = [path]
                self.assert_rejected(self.run_gate(), "symlink")

    def test_rejects_bad_contract_schema(self):
        for key, value in [("schema_version", True), ("schema_version", 2),
                           ("task_id", ""), ("goal", None),
                           ("allowed_files", []), ("allowed_files", "output/report.json"),
                           ("validations", []), ("human_review_required", False),
                           ("human_review_required", "true"), ("unknown", "field")]:
            with self.subTest(key=key, value=value):
                original = self.contract.copy()
                self.contract[key] = value
                self.assert_rejected(self.run_gate(), "contract")
                self.contract = original
        del self.contract["goal"]
        self.assert_rejected(self.run_gate(), "contract")

    def test_rejects_arbitrary_validation_commands(self):
        self.contract["validations"] = ["python3 -c 'raise SystemExit(0)'"]
        self.assert_rejected(self.run_gate(), "unknown validation")

    def test_rejects_malformed_json_duplicate_keys_and_wrong_shapes(self):
        for body in ["{", "[]", '{"goal":"first","goal":"second"}']:
            with self.subTest(body=body):
                self.assert_rejected(self.run_gate(contract_text=body), "contract")
        for body in ["{", "{}", "[]", '[1]', '["output/report.json", "output/report.json"]']:
            with self.subTest(body=body):
                self.assert_rejected(self.run_gate(manifest_text=body), "changed_files")

    def test_rejects_missing_files_and_directories(self):
        for path in ["output/missing.json", "output"]:
            with self.subTest(path=path):
                self.contract["allowed_files"] = [path]
                self.changed = [path]
                self.assert_rejected(self.run_gate(), "regular file")

    def test_runs_builtin_content_checks(self):
        for body, reason in [(b"", "empty"), (b"\xff", "UTF-8"),
                             (b"not json", "JSON object"), (b"[]", "JSON object"),
                             (b'{"value": NaN}', "JSON object")]:
            with self.subTest(body=body):
                (self.root / "output/report.json").write_bytes(body)
                self.assert_rejected(self.run_gate(), reason)

    def test_public_fixtures_have_expected_outcomes(self):
        for name, expected in [("valid-task", 0), ("invalid-task", 1)]:
            with self.subTest(name=name):
                fixture = ROOT / "examples" / name
                result = subprocess.run(
                    [sys.executable, str(SCRIPT), "--contract", str(fixture / "contract.json"),
                     "--changed-files", str(fixture / "changed-files.json")],
                    capture_output=True, text=True, check=False,
                )
                self.assertEqual(result.returncode, expected, result.stderr)
                self.assertIn("PASS:" if expected == 0 else "outside allowed_files",
                              result.stdout if expected == 0 else result.stderr)


if __name__ == "__main__":
    unittest.main()
