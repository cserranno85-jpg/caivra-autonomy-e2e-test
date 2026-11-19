"""Validate a JSON task list and produce a deterministic count report."""

import argparse
import json
import sys
from pathlib import Path


class TaskValidationError(ValueError):
    """The supplied task list does not match the documented schema."""


def summarize_tasks(payload):
    """Return total/completed/pending counts for a validated task list."""
    if not isinstance(payload, list):
        raise TaskValidationError("Top-level JSON value must be a list of tasks")

    seen_ids = set()
    completed = 0
    for index, task in enumerate(payload, start=1):
        if not isinstance(task, dict):
            raise TaskValidationError(f"Task {index} must be an object")
        if set(task) != {"id", "title", "status"}:
            raise TaskValidationError(f"Task {index} must have exactly id, title, status")
        for field in ("id", "title"):
            if not isinstance(task[field], str) or not task[field].strip():
                raise TaskValidationError(f"Task {index} {field} must be a nonempty string")
        if task["id"] in seen_ids:
            raise TaskValidationError(f"Duplicate task id: {task['id']}")
        seen_ids.add(task["id"])
        if task["status"] not in ("completed", "pending"):
            raise TaskValidationError(f"Task {index} has invalid status")
        completed += task["status"] == "completed"

    return {"total": len(payload), "completed": completed, "pending": len(payload) - completed}


def audit_file(path):
    """Read and validate a UTF-8 JSON task file."""
    with Path(path).open("r", encoding="utf-8") as handle:
        return summarize_tasks(json.load(handle))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Audit a JSON list of tasks")
    parser.add_argument("tasks_file", help="Path to a JSON array of tasks")
    args = parser.parse_args(argv)

    try:
        report = audit_file(args.tasks_file)
    except (OSError, UnicodeError, json.JSONDecodeError, TaskValidationError) as exc:
        print(f"Task audit error: {exc}", file=sys.stderr)
        return 2

    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
