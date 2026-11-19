"""Synthetic AET-002 checkpoint and fresh-process recovery."""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from task_audit import audit_file

EXPECTED = {"total": 5, "completed": 3, "pending": 2}


def create(sha):
    if not isinstance(sha, str) or re.fullmatch("[a-f0-9]{40}", sha) is None:
        raise ValueError("invalid commit SHA")
    actual = audit_file(ROOT / "sample_tasks.json")
    if actual != EXPECTED:
        raise ValueError("unexpected task counts")
    return {"experiment": "AET-002", "sha": sha, "state": "checkpointed",
            "next": "resume", "report": actual}


def resume(checkpoint, sha):
    if checkpoint != create(sha):
        raise ValueError("stale, forged, or invalid checkpoint")
    return {"experiment": "AET-002", "sha": sha, "state": "resumed-verified",
            "report": EXPECTED}


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("create", "resume"))
    parser.add_argument("--sha", required=True)
    parser.add_argument("--input")
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv)
    try:
        if args.mode == "create":
            record = create(args.sha)
        else:
            if not args.input:
                raise ValueError("missing checkpoint")
            record = resume(json.loads(Path(args.input).read_text(encoding="utf-8")), args.sha)
        Path(args.output).write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(record))
    except (ValueError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print("AET-002 error: " + str(exc), file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
