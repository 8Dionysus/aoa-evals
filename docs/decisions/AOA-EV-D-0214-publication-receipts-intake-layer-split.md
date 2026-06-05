# Publication Receipts Intake Layer Split

- Decision ID: AOA-EV-D-0214
- Status: Accepted
- Date: 2026-06-04
- Owner surface: focused publication receipt intake validators

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, observability/audit, publication/receipt
- Mechanic parents: publication-receipts, proof-loop, cross-parent
- Guard families: source/topology, observability/audit, generated/report/receipt/runtime
- Posture: active rationale

## Context

AOA-EV-D-0169 moved receipt-intake dry-review validation out of the broad
publication-receipts validator into `scripts/validators/publication_receipts_intake.py`.

That file still mixed several different dry-review layers:

- route and decision-token checks for the intake dry-review artifact;
- non-publishable artifact identity and expected source references;
- candidate payload preview schema validation, source report alignment,
  manifest alignment, and generated report-index presence; and
- `source_alignment`, `intake_checks`, `publication_boundary`, and
  `claim_limit` non-publication posture.

The dry-review artifact is one report, but these checks fail through different
owner routes.

## Options Considered

- Keep `publication_receipts_intake.py` as the single intake dry-review
  validator.
- Keep `publication_receipts_intake.py` as a delegating compatibility facade.
- Remove the aggregate and let `evidence_readouts.py` call focused intake
  validators directly.

## Decision

`scripts/validators/publication_receipts_intake.py` is removed.

Active intake dry-review validation now routes through:

- `publication_receipts_intake_route.py` for route, decision, proof-loop,
  publication-receipts, reports, roadmap, changelog, and decision-index tokens.
- `publication_receipts_intake_artifact.py` for non-publishable envelope shape,
  expected source refs, local target presence, and top-level artifact identity.
- `publication_receipts_intake_preview.py` for candidate payload preview schema
  validation, source report alignment, source manifest alignment, report-index
  presence, bundle/report refs, and interpretation-bound text.
- `publication_receipts_intake_boundary.py` for `source_alignment`,
  `intake_checks`, `publication_boundary`, and `claim_limit`.
- `publication_receipts_intake_common.py` for helper-only constants and payload
  loading.

`evidence_readouts.py` calls the focused validators directly. The
intake-dry-review tests collect those focused validators explicitly.

## Rationale

Dry review is weaker than publication. Its route card should not own the
candidate payload preview. Its candidate preview should not own the
non-publication boundary. Its boundary checks should not become receipt
publication or live memory append authority.

Splitting the validator keeps dry-review as an audit/readout artifact and makes
each failure route concrete.

## Consequences

- Positive: route-token, artifact-shape, candidate-preview, and
  non-publication-boundary failures now route to separate validators.
- Positive: no replacement intake facade remains.
- Positive: common code is helper-only and does not own receipt meaning.
- Tradeoff: repo-wide readout orchestration imports more publication-receipts
  intake modules.

## Current Applicability

As of 2026-06-04:

- Still valid: intake dry-review artifacts must remain non-published and must
  not imply live receipt publication.
- Changed: the broad `publication_receipts_intake.py` module no longer exists.
- Supersedes: AOA-EV-D-0169 for aggregate intake dry-review validator shape.

## Boundaries

This decision does not publish receipts, create stats envelopes, append
`.aoa/live_receipts/`, accept proof verdict meaning, define source bundle truth,
or become release evidence.

It also does not move live receipt JSONL inspection out of
`publication_receipts_live.py`, route/provenance posture out of
`publication_receipts_routes.py`, or receipt payload/schema ownership out of
`publication_receipts_payload.py`.

## Validation

- `python -m py_compile scripts/validators/publication_receipts_intake_common.py scripts/validators/publication_receipts_intake_route.py scripts/validators/publication_receipts_intake_artifact.py scripts/validators/publication_receipts_intake_preview.py scripts/validators/publication_receipts_intake_boundary.py scripts/validators/evidence_readouts.py mechanics/publication-receipts/parts/intake-dry-review/tests/test_receipt_intake_dry_review.py`
- `python -m pytest -q mechanics/publication-receipts/parts/intake-dry-review/tests/test_receipt_intake_dry_review.py`
- `python -m json.tool docs/validation/script_inventory.json`
- `python -m json.tool docs/validation/validator_inventory.json`
- `python scripts/generate_decision_indexes.py`
- `python scripts/ci_gate.py --mode source-fast`
- `python scripts/release_check.py`
