"""Unit and fresh-process tests for resumption."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from recovery.checkpoint import create, resume

SHA = "a" * 40


class RecoveryTests(unittest.TestCase):
    def test_checkpoint(self):
        self.assertEqual(create(SHA)["report"], {"total": 5, "completed": 3, "pending": 2})

    def test_resume(self):
        self.assertEqual(resume(create(SHA), SHA)["state"], "resumed-verified")

    def test_stale_sha_rejected(self):
        with self.assertRaises(ValueError):
            resume(create(SHA), "b" * 40)

    def test_tampering_rejected(self):
        record = create(SHA)
        record["report"]["pending"] = 0
        with self.assertRaises(ValueError):
            resume(record, SHA)

    def test_two_independent_processes(self):
        script = str(ROOT / "recovery" / "checkpoint.py")
        with tempfile.TemporaryDirectory() as tmp:
            checkpoint = str(Path(tmp) / "saved.json")
            result = str(Path(tmp) / "result.json")
            for cmd in (["create", "--sha", SHA, "--output", checkpoint],
                        ["resume", "--sha", SHA, "--input", checkpoint, "--output", result]):
                p = subprocess.run([sys.executable, script, *cmd],
                                   capture_output=True, text=True, check=False)
                self.assertEqual(p.returncode, 0, p.stderr)
            self.assertEqual(json.loads(Path(result).read_text())["state"], "resumed-verified")


if __name__ == "__main__":
    unittest.main()
