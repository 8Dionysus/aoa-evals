# Publication Receipts Validator Module Boundary

- Decision ID: AOA-EV-D-0120
- Status: Accepted
- Date: 2026-06-03
- Owner surface: focused publication-receipts validators, `mechanics/publication-receipts/`

## Index Metadata

- Original date: 2026-06-03
- Surface classes: validation guard, publication/receipt, boundary/runtime
- Mechanic parents: publication-receipts, proof-loop, cross-parent
- Guard families: generated/report/receipt/runtime, report/release/receipt
- Posture: active rationale

## Context

Publication receipt validation remained inside `scripts/validate_repo.py` after
the first generated-reader and boundary-bridge validator splits.

The checks form one coherent owner surface: eval-result receipt payload shape,
local stats-envelope mirror posture, owner-local live receipt JSONL validation,
and receipt-intake dry-review posture.

## Options Considered

- Keep receipt validation inside `scripts/validate_repo.py` because it touches
  live JSONL and source bundle reports.
- Split payload schema, live log, and dry-review into three validator modules.
- Move the publication-receipts boundary into
  `scripts/validators/publication_receipts.py` while keeping `validate_repo.py`
  as the compatibility entrypoint.

## Decision

Publication receipt validation lives in
`scripts/validators/publication_receipts.py`.

`scripts/validate_repo.py` keeps compatibility aliases for receipt paths and
wrappers for `validate_eval_result_receipt_surfaces`,
`validate_live_receipt_log`, and
`validate_receipt_intake_dry_review_surface`.

The module validates receipt payload shape, stats-envelope mirror alignment,
and dry-review non-publication posture. It keeps
`validate_live_receipt_log` as a compatibility adapter while live JSONL
inspection is owned by `scripts/validators/publication_receipts_live.py`.

## Rationale

Publication receipts are weaker than bundle-local reports and source bundles.
They record bounded publication facts; they do not own verdict meaning, proof
quality, runtime acceptance, or repo-global scoring.

Naming the module keeps receipt checks visible as a publication sidecar organ
instead of a generic report validator or runtime bucket. It also preserves the
local rule that dry-review payload previews are not publishable receipt
envelopes.

## Consequences

- Positive: publication-receipts validation leaves the root validator.
- Positive: live-log validation remains append-inspection only and does not
  publish or mutate receipt state.
- Tradeoff: compatibility wrappers remain because tests still import through
  `scripts/validate_repo.py`.
- Follow-up: release-support reports and runtime integrity review should remain
  separate owner surfaces.

## Current Applicability

As of 2026-06-04:

- Still valid: `scripts/validate_repo.py` remains the repo-wide validation
  entrypoint.
- Changed: receipt payload and route checks moved from the compatibility
  publication-receipts facade into focused payload and route validators;
  dry-review checks first moved to
  `scripts/validators/publication_receipts_intake.py` and later split across
  focused intake route, artifact, preview, and boundary validators; live JSONL
  inspection moved to `scripts/validators/publication_receipts_live.py`; shared
  schema/ref helpers moved to `scripts/validators/publication_receipts_common.py`.
- Superseded in part by: AOA-EV-D-0161 for the live receipt log validator
  boundary; AOA-EV-D-0169 for the intake dry-review validator boundary;
  AOA-EV-D-0180 for the route/payload subvalidator boundary; AOA-EV-D-0191 for
  publication-receipts facade removal; AOA-EV-D-0214 for aggregate intake
  dry-review validator shape; AOA-EV-D-0222 for route support-layer ownership.

## Review Log

### 2026-06-04 - Live receipt validator split

- Previous assumption: one focused publication-receipts validator could carry
  payload shape, stats-envelope mirror, dry-review posture, and live-log
  inspection.
- New reality: live receipt JSONL inspection is an observability/audit boundary
  around owner-local append memory, while receipt payload/dry-review checks are
  publication-receipts source-fast route contracts.
- Reason: keeping both in one file recreated historical bulk after the validator
  refactor; the live path deserves its own validator organ and topology entry.
- Source surfaces updated:
  `scripts/validators/publication_receipts.py`,
  `scripts/validators/publication_receipts_live.py`,
  `scripts/validators/publication_receipts_common.py`,
  `docs/validation/VALIDATOR_TOPOLOGY.md`,
  `docs/validation/script_inventory.json`,
  `docs/validation/validator_inventory.json`, and
  `mechanics/EVIDENCE_CLUSTERS.md`.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

### 2026-06-04 - Intake dry-review validator split

- Previous assumption: `publication_receipts.py` owned both route/payload checks
  and intake dry-review artifact validation.
- New reality: intake dry-review validation lives in
  `scripts/validators/publication_receipts_intake.py`.
- Reason: dry review is an advisory non-publication report and source-alignment
  check; it should not remain in the same implementation block as receipt
  payload schema and stats-envelope mirror checks.
- Source surfaces updated:
  `scripts/validators/publication_receipts.py`,
  `scripts/validators/publication_receipts_intake.py`,
  validation inventories, and `mechanics/EVIDENCE_CLUSTERS.md`.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

### 2026-06-04 - Route and payload subvalidator split

- Previous assumption: after live and intake moved out, `publication_receipts.py`
  could remain the route/payload validator.
- New reality: route-card/provenance/part-contract checks and receipt
  payload/schema-mirror checks are separate owner boundaries.
- Reason: keeping route tokens and JSON schema/example validation in one file
  preserved a broad historical container after the first split.
- Source surfaces updated:
  `scripts/validators/publication_receipts.py`,
  `scripts/validators/publication_receipts_routes.py`,
  `scripts/validators/publication_receipts_payload.py`,
  validation inventories, and `mechanics/EVIDENCE_CLUSTERS.md`.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

## Boundaries

This decision does not make receipts stronger than reviewed reports.

It does not make dry-review output a live publication; dry-review validation now
lives in focused publication-receipts intake validators.

It does not change canonical `aoa-stats` ownership of the shared
stats-event-envelope vocabulary.

It does not append, rewrite, or publish `.aoa/live_receipts/` entries.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
