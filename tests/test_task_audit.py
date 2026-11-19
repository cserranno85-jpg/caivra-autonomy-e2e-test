"""Standard-library regression tests for the task audit CLI."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from task_audit import TaskValidationError, audit_file, summarize_tasks


class TaskAuditTests(unittest.TestCase):
    def test_sample_counts(self):
        self.assertEqual(
            audit_file(ROOT / "sample_tasks.json"),
            {"total": 5, "completed": 3, "pending": 2},
        )

    def test_empty_list(self):
        self.assertEqual(
            summarize_tasks([]), {"total": 0, "completed": 0, "pending": 0}
        )

    def test_non_list_rejected(self):
        with self.assertRaises(TaskValidationError):
            summarize_tasks({"tasks": []})

    def test_invalid_status_rejected(self):
        with self.assertRaises(TaskValidationError):
            summarize_tasks([{"id": "1", "title": "One", "status": "running"}])

    def test_duplicate_ids_rejected(self):
        tasks = [
            {"id": "same", "title": "First", "status": "pending"},
            {"id": "same", "title": "Second", "status": "completed"},
        ]
        with self.assertRaises(TaskValidationError):
            summarize_tasks(tasks)

    def test_missing_field_rejected(self):
        with self.assertRaises(TaskValidationError):
            summarize_tasks([{"id": "1", "status": "pending"}])

    def test_blank_title_rejected(self):
        with self.assertRaises(TaskValidationError):
            summarize_tasks([{"id": "1", "title": " ", "status": "pending"}])

    def test_non_object_rejected(self):
        with self.assertRaises(TaskValidationError):
            summarize_tasks(["task"])

    def run_cli(self, path):
        return subprocess.run(
            [sys.executable, str(ROOT / "task_audit.py"), str(path)],
            capture_output=True, text=True, check=False
        )

    def test_cli_expected_json(self):
        result = self.run_cli(ROOT / "sample_tasks.json")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            json.loads(result.stdout),
            {"total": 5, "completed": 3, "pending": 2},
        )
        self.assertEqual(result.stderr, "")

    def test_cli_malformed_json_nonzero_exit(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "broken.json"
            path.write_text("{not json", encoding="utf-8")
            result = self.run_cli(path)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Task audit error:", result.stderr)
            self.assertEqual(result.stdout, "")

    def test_cli_missing_file_nonzero_exit(self):
        result = self.run_cli(ROOT / "does-not-exist.json")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Task audit error:", result.stderr)


if __name__ == "__main__":
    unittest.main()
