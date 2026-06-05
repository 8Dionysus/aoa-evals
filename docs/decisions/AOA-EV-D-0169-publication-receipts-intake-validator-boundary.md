# Publication Receipts Intake Validator Boundary

- Decision ID: AOA-EV-D-0169
- Status: Superseded
- Superseded by: AOA-EV-D-0214-publication-receipts-intake-layer-split
- Date: 2026-06-04
- Owner surface: `scripts/validators/publication_receipts_intake.py`, publication receipt intake dry-review guard family

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, observability/audit
- Mechanic parents: publication-receipts
- Guard families: source/topology, observability/audit
- Posture: superseded rationale

## Context

After the live receipt log split, `scripts/validators/publication_receipts.py`
still carried intake dry-review validation beside route-card, receipt payload,
and stats-envelope mirror checks.

The intake dry-review artifact is intentionally weaker than a published receipt:
it validates a candidate payload preview, source report alignment, report-index
presence, and non-publication boundary. It must not become live receipt
authority or proof verdict acceptance.

## Decision

Publication receipt intake dry-review validation lives in
`scripts/validators/publication_receipts_intake.py`.

The module owns:

- `mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json`;
- candidate payload preview validation against the receipt payload schema;
- source report and source manifest alignment checks;
- generated report-index presence checks;
- intake check result posture; and
- publication boundary and claim-limit non-publication checks.

AOA-EV-D-0191 later removes the `publication_receipts.py` compatibility facade.
Repo-wide orchestration calls `publication_receipts_intake.py` directly.

## Rationale

Dry review is an audit/readout artifact, not a receipt publication. Keeping it
inside the publication receipt route validator made the parent module carry
both payload schema posture and an advisory non-publication report.

The split keeps three adjacent questions separate:

- `publication_receipts_routes.py` and `publication_receipts_payload.py`: are
  the route cards, receipt payload schema, and stats-envelope mirror coherent?
- `publication_receipts_intake.py`: does the dry-review artifact prove
  non-publication posture and source alignment?
- `publication_receipts_live.py`: is owner-local live receipt JSONL evidence
  shaped and append-only without appending during validation?

## Consequences

- Positive: dry-review validation has a named validator, inventory entries,
  mechanics ledger row, and decision rationale.
- Positive: `publication_receipts.py` no longer contains dry-review artifact
  and report-index alignment logic.
- Positive: existing callers now import
  `validate_receipt_intake_dry_review_surface` from
  `publication_receipts_intake.py`.

## Current Applicability

As of 2026-06-04:

- Still valid: intake dry-review artifacts must remain non-published and must
  not imply live receipt publication.
- Changed: intake dry-review logic moved out of `publication_receipts.py` and
  into `publication_receipts_intake.py`.
- Changed: AOA-EV-D-0180 later narrowed `publication_receipts.py` to a facade
  and moved route/payload checks into focused modules.
- Changed: AOA-EV-D-0191 removes the remaining compatibility facade.
- Changed: AOA-EV-D-0214 splits intake dry-review validation across route,
  artifact, candidate-preview, boundary, and helper-only common modules.
- Superseded in part by: AOA-EV-D-0180 for route/payload split and
  AOA-EV-D-0191 for facade removal.
- Superseded by: AOA-EV-D-0214 for aggregate intake dry-review validator shape.

## Boundaries

This decision does not let `publication_receipts_intake.py` publish receipts,
append to `.aoa/live_receipts/`, accept proof verdict meaning, define source
bundle truth, or become release evidence.

It does not move live receipt JSONL inspection out of
`publication_receipts_live.py`.

## Validation

- `python -m py_compile scripts/validators/publication_receipts_intake_common.py scripts/validators/publication_receipts_intake_route.py scripts/validators/publication_receipts_intake_artifact.py scripts/validators/publication_receipts_intake_preview.py scripts/validators/publication_receipts_intake_boundary.py scripts/validators/publication_receipts_live.py scripts/validators/publication_receipts_common.py scripts/validators/publication_receipts_routes.py scripts/validators/publication_receipts_payload.py`
- `python -m pytest -q mechanics/publication-receipts/parts/intake-dry-review/tests/test_receipt_intake_dry_review.py mechanics/publication-receipts/parts/live-publisher/tests/test_live_receipt_log.py`
