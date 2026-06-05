# Publication Receipts Live Validator Boundary

- Decision ID: AOA-EV-D-0161
- Status: Accepted
- Date: 2026-06-04
- Owner surface: `scripts/validators/publication_receipts_live.py`, `mechanics/publication-receipts/parts/live-publisher/`, `.aoa/live_receipts/`

## Index Metadata

- Original date: 2026-06-04
- Surface classes: validation guard, publication/receipt, boundary/runtime, observability/audit
- Mechanic parents: publication-receipts, cross-parent
- Guard families: generated/report/receipt/runtime, observability/audit
- Posture: active rationale

## Context

After the publication-receipts validator split, `scripts/validators/publication_receipts.py`
still carried receipt payload route checks, stats-envelope mirror checks,
dry-review checks, and owner-local live receipt JSONL inspection.

Those checks share a mechanic, but they protect different boundaries:

- receipt payload and dry-review checks are publication sidecar route
  contracts below reviewed reports; and
- live JSONL inspection is an append-only observability/audit check over
  `.aoa/live_receipts/`.

Keeping them in one file recreated the bulk pattern the validator refactor is
removing.

## Decision

Owner-local live receipt JSONL validation lives in
`scripts/validators/publication_receipts_live.py`.

The module owns:

- loading the local or fallback stats-event-envelope schema for live entries;
- JSONL parsing and non-object entry rejection;
- `event_kind == "eval_result_receipt"` enforcement;
- duplicate `event_id` rejection;
- `object_ref.repo == "aoa-evals"` and `object_ref.kind == "eval_bundle"`;
- primary evidence ref presence;
- repo-qualified evidence, bundle, and report ref checks;
- payload validation against `eval-result-receipt.schema.json`; and
- payload/object-ref alignment checks.

Shared schema, RFC3339, JSON/YAML, and `repo:` reference helpers live in
`scripts/validators/publication_receipts_common.py`. That helper owns no
receipt meaning.

AOA-EV-D-0191 later removes the `publication_receipts.py` compatibility facade
after tests and repo validation routes import `publication_receipts_live.py`
directly.

## Rationale

Live receipt inspection is not payload authorship, dry-review acceptance, or
bundle-local proof meaning. It is an append-only publication memory boundary:
the validator can reject malformed or overclaiming entries, but it must not
publish, rewrite, accept verdict meaning, or promote receipt facts into proof
quality.

Separating the live validator keeps runtime/live evidence pressure visible
without allowing a broad publication-receipts module to become another
historical validator pile.

## Consequences

- Positive: route, payload/schema, intake dry-review, and live-log checks live
  in focused modules without a publication-receipts facade.
- Positive: live JSONL inspection has its own topology, inventory, mechanics
  ledger, and decision rationale.
- Positive: shared schema/ref helpers are explicit and classified, rather than
  hidden inside either validator.
- Tradeoff resolved later: AOA-EV-D-0191 moves direct callers to the live
  validator.

## Current Applicability

As of 2026-06-04:

- Still valid: live receipt publication remains optional, append-only, and
  weaker than bundle-local reports.
- Changed: live-log validation moved out of `publication_receipts.py`.
- Changed: AOA-EV-D-0180 later moved route and payload/schema checks out of
  `publication_receipts.py` too.
- Changed: AOA-EV-D-0191 removes the remaining compatibility facade.
- Superseded in part by: AOA-EV-D-0180 for route/payload split and
  AOA-EV-D-0191 for facade removal.

## Boundaries

This decision does not let `publication_receipts_live.py` publish, append,
rewrite, delete, or supersede live receipt entries.

It does not make receipts stronger than reviewed reports, source bundles,
proof-loop reports, release evidence, runtime acceptance, or canonical
`aoa-stats` schema ownership.

It does not let `publication_receipts_common.py` own receipt meaning.

## Validation

- `python -m py_compile scripts/validators/publication_receipts_common.py scripts/validators/publication_receipts_live.py scripts/validators/publication_receipts_routes.py scripts/validators/publication_receipts_payload.py scripts/validators/mechanics_routes.py`
- `python -m pytest -q mechanics/publication-receipts/parts/live-publisher/tests/test_live_receipt_log.py mechanics/publication-receipts/parts/live-publisher/tests/test_publish_live_receipts.py mechanics/publication-receipts/parts/intake-dry-review/tests/test_receipt_intake_dry_review.py`
- `python -m pytest -q tests/test_validation_topology.py tests/test_script_topology.py tests/test_mechanics_topology.py tests/test_mechanic_root_district_recon.py`
