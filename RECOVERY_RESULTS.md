# CAIVRA-AET-002 — Verified execution evidence

## Test objective

Test whether an interruption in a repository workflow can trigger a **separate automatic execution** that restores and validates a persisted checkpoint without another user instruction.

The workflow is intentionally synthetic and does **not** run an AI agent. Therefore its results must not be interpreted as proof of ChatGPT/Codex self-restart after context or token exhaustion.

## Immutable starting evidence

- Repository: [caivra-autonomy-e2e-test](https://github.com/cserranno85-jpg/caivra-autonomy-e2e-test)
- Starting main before AET-002: `2797f80ab68baa8435bf56cb0c3d2281e3b3aa92`.
- [Implementation PR #2](https://github.com/cserranno85-jpg/caivra-autonomy-e2e-test/pull/2), proposed head `2249039ae7a60e0816391692e61312e849813c5c`.
- Verified merged main for the experiment: `af2f554a511fc72770811081ee171a6bcf662a9c`.
- PR CI [run 44486881065](https://github.com/cserranno85-jpg/caivra-autonomy-e2e-test/actions/runs/44486881065): success.

## Experiment observed

| Evidence | Observed result |
| --- | --- |
| [Initial workflow run 44486964945](https://github.com/cserranno85-jpg/caivra-autonomy-e2e-test/actions/runs/44486964945) | `push` event on main, **failure as intended** after checkpoint upload |
| Source checkpoint | `aet-002-checkpoint`, artifact ID `14511515515`, created successfully |
| [Recovery workflow run 44486997721](https://github.com/cserranno85-jpg/caivra-autonomy-e2e-test/actions/runs/44486997721) | Independent `workflow_run` trigger, **success** |
| Recovery report | `aet-002-resume-report`, artifact ID `14511430817`, uploaded successfully |
| Recovery log | `state: resumed-verified`, SHA `af2f554a511fc72770811081ee171a6bcf662a9c` |
| Recovery report counts | `total=5, completed=3, pending=2` |
| [Post-merge task CI run 44486964950](https://github.com/cserranno85-jpg/caivra-autonomy-e2e-test/actions/runs/44486964950) | **success**, 16 tests, `OK` |

The checkpoint was carried between **different GitHub Actions workflow runs** rather than merely between steps in the same job. Recovery executed without a subsequent user "proceed" message.

## Conclusions and limits

**Confirmed:** GitHub re-triggered execution following an intentionally failed workflow and the second run verified a persisted checkpoint against the original immutable commit SHA.

**Not tested:** Automatic restart of a terminated ChatGPT/Codex model invocation. For that, a genuine Codex Goal or equivalent durable agent executor must be separately configured and observed.

**Unfinished branch-protection condition:** At the time of inspection, `main.protected=false` and the repository had zero active rulesets (`[]`). PR CI passed and was voluntarily checked before merge, but a required-status-check rule was **not enforced by GitHub**. The connected GitHub mutation tools do not expose branch-protection/ruleset administration. Do not count protected-branch enforcement as passed.

**Security:** The two workflows use read-only GitHub token permissions, synthetic data and no new secrets. The deliberately failed workflow remains red by test design and is scoped to changes to the experiment paths.

## Next optional validation

Configure a branch rule or active ruleset targeting `main` that requires a PR and the existing `unit-tests` check, with no bypass and no forced updates or deletion. Then create a harmless test PR and verify GitHub actually enforces these rules. Keep this separate from claims about an AI model auto-resuming.
