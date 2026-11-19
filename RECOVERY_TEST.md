# AET-002: Controlled interruption and recovery

This project tests a new GitHub Actions run triggered without a second chat instruction.

The main-branch push workflow saves a JSON checkpoint as an artifact, then deliberately exits 78 (expected failure). The independent workflow_run workflow is triggered by that failed run, downloads its checkpoint, checks the source commit SHA and expected counts, and uploads a recovered-state report. Both workflows use read-only permissions and synthetic data.

Evidence required: an interrupted run with a checkpoint artifact, a separate workflow_run recovery run with conclusion success, an uploaded resume report, matching source SHA, and passing task-audit CI.

This verifies automation recovery across GitHub Actions runs, NOT the ability of a terminated AI session to restart itself.

The intentionally failed run will remain red by design; it is not a product defect.
