# Caivra Task Audit — AET-001

Temporary, zero-dependency Python project for testing end-to-end autonomous execution: implementation, unit tests, CI, documentation, PR, eligible merge, and final verification.

## Run

Requires Python 3.9 or later. No external dependencies, credentials, or paid services.

```bash
python task_audit.py sample_tasks.json
```

Expected output:

```json
{
  "total": 5,
  "completed": 3,
  "pending": 2
}
```

The input must be a UTF-8 JSON array. Every entry must contain **exactly** three string fields: `id` (unique, nonempty), `title` (nonempty), and `status` (either `completed` or `pending`). An empty array is allowed. Invalid files produce an error on stderr and exit code 2.

## Test

```bash
python -m unittest discover -s tests -v
```

GitHub Actions runs the same tests and independently checks the sample report on pull requests and pushes to `main`.

## Autonomous execution experiment

Read [TEST_PLAN.md](TEST_PLAN.md) for the full eight-phase objective and verification standards. A complete pass requires evidence of implementation, passing CI, a merged PR, and final verification on `main`. An agent's claim that it continued across a hard execution limit is **not evidence** of automatic resumption.

Synthetic inputs only. This experiment must not access unrelated repositories, production services, secrets, or paid infrastructure.
