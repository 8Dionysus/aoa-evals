# Release-support Helper Layer Split

- Decision ID: AOA-EV-D-0217
- Status: Accepted
- Date: 2026-06-05
- Owner surface: focused `scripts/validators/release_support_*` helper modules

## Index Metadata

- Original date: 2026-06-05
- Surface classes: validation guard, release/support, observability/audit
- Mechanic parents: release-support, cross-parent
- Guard families: report/release/receipt, source/topology, release/nightly
- Posture: active rationale

## Context

AOA-EV-D-0182 correctly split release-support route/provenance checks from
shared report helpers. After the release-support facade was removed, the helper
module `scripts/validators/release_support_common.py` still carried several
different support surfaces:

- report artifact path and required-token constants;
- verification command constants;
- route-token loading with decision-index companion text;
- repo-qualified reference and markdown-anchor parsing; and
- shared report list/object-id/snapshot/claim-limit structure checks.

That was no longer one owner boundary. It was a smaller version of the broad
historical helper shape this refactor is removing.

## Decision

Remove `scripts/validators/release_support_common.py`.

Release-support helper behavior is split into focused modules:

- `scripts/validators/release_support_report_constants.py` owns report artifact
  paths, report decision paths, and required-token sets.
- `scripts/validators/release_support_report_commands.py` owns report
  verification command constants.
- `scripts/validators/release_support_route_tokens.py` owns required-token
  lookup with decision-index companion text.
- `scripts/validators/release_support_refs.py` owns repo-qualified reference
  parsing and markdown-anchor checks.
- `scripts/validators/release_support_report_checks.py` owns shared report
  list/object-id, repo-ref-list, verification-snapshot, joined-list-token, and
  claim-limit checks.

The focused release-support report validators import only the helper surface
they need.

## Rationale

Report constants, command constants, route-token lookup, repo-ref parsing, and
report-structure checks change for different reasons. Keeping them in one
module made future edits look like generic release-support helper work and kept
a hidden aggregate after facade removal.

The split preserves report validation behavior while making the helper layer
honest about what each file owns.

## Consequences

- Positive: helper imports now name the actual support surface.
- Positive: repo-ref parsing no longer sits beside report constants.
- Positive: verification command constants no longer sit beside JSON structure
  checks.
- Positive: the old common helper is removed instead of kept as a compatibility
  facade.
- Tradeoff: report validators import more small modules.

## Boundaries

This split does not change release-support report semantics, create live
release evidence, publish a release, accept runtime evidence, mutate sibling
repos, or mark a goal complete.

The helper modules do not own release-support route/provenance meaning,
readiness audit meaning, strategic closeout meaning, or PR handoff meaning.

## Validation

- `python -m py_compile scripts/validators/release_support_refs.py scripts/validators/release_support_report_checks.py scripts/validators/release_support_report_commands.py scripts/validators/release_support_report_constants.py scripts/validators/release_support_route_tokens.py scripts/validators/release_support_routes.py scripts/validators/release_support_readiness_report.py scripts/validators/release_support_strategic_closeout_report.py scripts/validators/release_support_pr_handoff_report.py`
- `python -m pytest -q mechanics/release-support/parts/readiness-audit/tests/test_release_support_readiness_audit.py mechanics/release-support/parts/strategic-closeout/tests/test_strategic_closeout_audit.py mechanics/release-support/parts/pr-handoff/tests/test_release_prep_pr_handoff.py`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_mechanics_topology.py`
- `python scripts/generate_decision_indexes.py`
- `python scripts/generate_decision_indexes.py --check`
- `python scripts/ci_gate.py --mode source-fast`
- `python scripts/release_check.py`
