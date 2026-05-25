# 0020 Proof Loop Local Smoke Report

- Status: Accepted
- Date: 2026-05-19
- Owner surface: `mechanics/proof-loop/`

## Index Metadata

- Surface classes: report/release/receipt
- Mechanic parents: proof-loop
- Guard families: generated/report/receipt/runtime
- Posture: report/release/receipt rationale

## Context

`mechanics/proof-loop/` now routes the active proof operation:

`proof question -> selection route -> source proof object -> support contract -> candidate evidence packet -> bundle-local review -> bounded report -> optional receipt`

That route is useful only if a future agent can follow it locally without
turning it into a decorative checklist, a hidden runtime dispatcher, or a new
proof authority above bundles, reports, generated readers, sibling refs, and
receipts.

The next pressure after creating the package was not to add another mechanic.
It was to test the route once.

## Options Considered

- Add a generic proof-loop checklist under `mechanics/proof-loop/`.
- Add a reusable example that pretends to be an eval result.
- Add one public-safe local route-smoke report and validate that it remains
  bounded.

## Decision

Add `mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md`
as the first reviewed local proof-loop route-smoke report.

The report selects `aoa-verification-honesty` as the source proof object,
walks the local proof-loop route through support contracts and candidate
evidence boundaries, and ends in a bounded route-smoke only.

It records no eval result receipt, no bundle promotion, no runtime dispatch,
no sibling-owner approval, and no generated proof authority.

## Rationale

A checklist would make the route look procedural before the repo had one real
reviewed run through it.

A fake result example would make the opposite mistake: it would imply a proof
outcome that did not happen.

A bounded report is the right weight for this step. It tests the route without
claiming that the selected eval bundle passed a new case corpus. It also keeps
the next actual eval-result run honest: that future run must use the selected
bundle's report schema and review guide.

## Consequences

- Positive: the proof-loop route is now exercised once in a public-safe local
  report artifact.
- Positive: future proof-loop examples or checklists have a reviewed report to
  route back to.
- Positive: the active report path now lives in the proof-loop route-smoke
  part, so root `reports/` no longer needs a proof-loop exception.
- Tradeoff: route-smoke provenance now depends on the proof-loop parts map
  added by `docs/decisions/0030-proof-loop-route-smoke-part.md`.
- Follow-up: if a later run wants an eval result, it must produce a
  bundle-local report and only then consider an optional receipt.

## Boundaries

This decision does not promote `aoa-verification-honesty`, create a new eval
case result, publish a receipt, accept runtime evidence, approve sibling truth,
or make `mechanics/proof-loop/` stronger than the packages it coordinates.

It does not turn smoke reports into the default shape for all proof work.
Use this pattern only when the route itself is the object under evaluation.

## Validation

- `mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md`
- `mechanics/proof-loop/README.md`
- `mechanics/proof-loop/PARTS.md`
- `reports/README.md`
- `docs/decisions/README.md`
- `docs/decisions/0030-proof-loop-route-smoke-part.md`
- `scripts/validate_repo.py`
- `python scripts/validate_semantic_agents.py`
