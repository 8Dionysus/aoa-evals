# Release Support Report Validator Boundary

- Decision ID: AOA-EV-D-0162
- Status: Accepted
- Date: 2026-06-04
- Owner surface: focused release-support report validators, `mechanics/release-support/parts/`

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, release/support, observability/audit
- Mechanic parents: release-support, cross-parent
- Guard families: report/release/receipt, release/nightly
- Posture: active rationale

## Context

`scripts/validators/release_support.py` carried both release-support route
checks and three part-local report artifact validators:

- readiness audit;
- strategic closeout audit; and
- release-prep PR handoff snapshot.

Those reports are release-support payloads, but they are not route cards,
provenance bridges, or legacy mapping. Keeping all of them in one module made
the validator grow back toward the historical broad-gate pattern.

## Decision

Readiness, strategic closeout, and PR handoff report validation moved out of
`scripts/validators/release_support.py`.

The module owns:

- report top-level identity checks;
- release publication, GitHub, tag, receipt, runtime, sibling, and
  goal-completion boundary checks;
- required requirement/group/trap ids;
- repo-qualified evidence refs;
- verification snapshot command coverage; and
- claim-limit wording that keeps the reports below live owner evidence.

AOA-EV-D-0182 later moves release-support route-card, part-contract,
provenance, and legacy checks into `release_support_routes.py`; shared
constants and helpers first move into `release_support_common.py`.
AOA-EV-D-0190 then removes the remaining `release_support.py` compatibility
facade. AOA-EV-D-0217 later splits the shared helper layer into focused
`release_support_*` helper modules.

Follow-up AOA-EV-D-0179 splits the report meaning into
`release_support_readiness_report.py`,
`release_support_strategic_closeout_report.py`, and
`release_support_pr_handoff_report.py`. AOA-EV-D-0189 removes the remaining
`release_support_reports.py` compatibility facade.

## Rationale

Release-support reports are bounded audit artifacts. They can say local
readiness is reviewable; they cannot create a tag, open a PR, observe GitHub
`Repo Validation`, publish a GitHub Release, accept runtime evidence, mutate a
sibling repo, or mark a goal complete.

Moving the report checks into their own module makes that boundary visible and
prevents route/provenance validation from becoming a container for every
release-support artifact.

## Consequences

- Positive: release-support route, part-contract, provenance, and legacy
  posture now live in `release_support_routes.py`.
- Positive: report behavior is tested and imported through focused report
  validators.
- Positive: validation topology and mechanics residual ledgers classify the
  report boundary separately.
- Tradeoff resolved later: shared constants and helpers first move into
  `release_support_common.py`, then split across focused helper modules.

## Current Applicability

As of 2026-06-04:

- Still valid: release-support reports remain bounded local artifacts below
  live git/GitHub/tag/release/goal evidence.
- Changed: report validators moved out of `release_support.py`.
- Changed: AOA-EV-D-0179 moves report-specific behavior into three focused
  modules.
- Changed: AOA-EV-D-0189 removes the remaining `release_support_reports.py`
  compatibility facade.
- Changed: AOA-EV-D-0190 removes the remaining `release_support.py`
  compatibility facade.
- Changed: AOA-EV-D-0217 removes the remaining `release_support_common.py`
  aggregate helper.
- Superseded in part by: AOA-EV-D-0179 for focused report modules and
  AOA-EV-D-0189/AOA-EV-D-0190 for facade removal; AOA-EV-D-0217 for helper
  splitting.

## Boundaries

This decision does not make release-support reports live release evidence.

It does not create a branch, commit, PR, merge, tag, GitHub Release, eval
receipt, runtime acceptance, sibling mutation, or goal completion.

It does not move route-card, provenance, or legacy validation out of
`release_support_routes.py`.

It does not make the facade the semantic owner of readiness, strategic
closeout, or PR handoff report meaning.

## Validation

- `python -m py_compile scripts/validators/release_support_refs.py scripts/validators/release_support_report_checks.py scripts/validators/release_support_report_commands.py scripts/validators/release_support_report_constants.py scripts/validators/release_support_route_tokens.py scripts/validators/release_support_routes.py scripts/validators/release_support_readiness_report.py scripts/validators/release_support_strategic_closeout_report.py scripts/validators/release_support_pr_handoff_report.py scripts/validators/evidence_readouts.py`
- `python -m pytest -q mechanics/release-support/parts/readiness-audit/tests/test_release_support_readiness_audit.py mechanics/release-support/parts/strategic-closeout/tests/test_strategic_closeout_audit.py mechanics/release-support/parts/pr-handoff/tests/test_release_prep_pr_handoff.py`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_mechanics_topology.py tests/test_mechanic_root_district_recon.py`
