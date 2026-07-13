# Release Support Report Facade Removal

- Decision ID: AOA-EV-D-0189
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `scripts/validators/release_support_readiness_report.py`, `scripts/validators/release_support_strategic_closeout_report.py`, `scripts/validators/release_support_pr_handoff_report.py`

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, release/support, observability/audit
- Mechanic parents: release-support, cross-parent
- Guard families: report/release/receipt, release/nightly
- Posture: active rationale

## Context

AOA-EV-D-0179 split release-support report validation into three focused
modules, but `scripts/validators/release_support_reports.py` remained as a
compatibility facade. It delegated readiness audit, strategic closeout audit,
and PR handoff checks without owning any report meaning.

After `evidence_readouts.py` and part-local tests can call the focused report
validators directly, the facade has no durable boundary left.

## Decision

`scripts/validators/release_support_reports.py` is removed.

Repo-wide evidence readout orchestration now imports the focused report
validators directly:

- `release_support_readiness_report.validate_release_support_readiness_audit_surface`;
- `release_support_strategic_closeout_report.validate_strategic_closeout_audit_surface`; and
- `release_support_pr_handoff_report.validate_release_prep_pr_handoff_surface`.

Part-local tests also import the focused validator that owns the report artifact
under test.

## Rationale

Release-support reports are separate audit artifacts below live release
evidence. Their hard checks must remain attached to the part-local report
boundary that owns the artifact.

Keeping an empty facade would turn compatibility into topology noise and invite
future rules to land in a generic report bucket instead of the owning report
validator.

## Consequences

- Positive: report validators are direct source-fast gates, not hidden behind a
  compatibility path.
- Positive: validation inventories and mechanics evidence ledger no longer list
  a facade as a blocking validator.
- Positive: AOA-EV-D-0190 later removes the remaining route/helper
  compatibility facade as well.
- Tradeoff: `evidence_readouts.py` has explicit imports for three report
  validators because it is the repo-wide evidence orchestration surface.

## Current Applicability

As of 2026-06-04:

- Still valid: release-support report checks remain blocking source-fast
  validation below live git/GitHub/tag/release/runtime/goal evidence.
- Changed: callers no longer route through `release_support_reports.py`.
- Changed: AOA-EV-D-0190 removes the remaining `release_support.py` facade.
- Supersedes: the compatibility-facade shape left by AOA-EV-D-0162 and
  AOA-EV-D-0179; refined by AOA-EV-D-0190.

## Boundaries

This decision does not make any report validator live release evidence.

It does not create a branch, commit, PR, merge, tag, GitHub Release, eval
receipt, runtime acceptance, sibling mutation, or goal completion.

It does not add a replacement aggregate report facade under another name.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
