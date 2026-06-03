# Proof Loop Route-Smoke Contract

- Decision ID: AOA-EV-D-0060
- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/proof-loop/parts/route-smoke/`

## Index Metadata

- Original date: 2026-05-20
- Surface classes: proof topology
- Mechanic parents: proof-loop
- Guard families: none
- Posture: active rationale

## Context

Decision `0030` moved the first proof-loop route-smoke report into
`mechanics/proof-loop/parts/route-smoke/`. The report itself already says it is
routeability evidence with no eval result receipt, bundle promotion, runtime
intake, sibling-owner approval, or proof of full proof-loop completeness.

The part README still needed a part-level contract so future proof-loop work
does not treat route-smoke as completion proof or as a generic eval-result
example.

## Decision

Make `mechanics/proof-loop/parts/route-smoke/README.md` expose inputs, outputs,
`stronger owner split`, stop-lines, and validation.

## Rationale

The active parent is `proof-loop`. `route-smoke` is one part inside it and
proves only that one local path can reach a bounded report. The selected bundle
keeps the verification-truthfulness claim. The step-owner packages keep their
own evidence classes and source contracts.

## Consequences

- Positive: route-smoke stays visibly bounded to routeability.
- Positive: `python scripts/validate_repo.py` now catches drift in the
  route-smoke part README.
- Tradeoff: the README repeats stop-lines that the report already carries, but
  this is useful because low-context edits often start from the part card.

## Boundaries

This decision does not create a new eval-result run, publish a receipt, promote
`aoa-verification-honesty`, accept runtime evidence, approve sibling truth,
strengthen generated readers, claim full proof-loop completeness, or complete
the strategic goal.

## Current Applicability

As of 2026-05-24:

- Still valid: `route-smoke` remains a bounded proof-loop part for routeability
  evidence.
- Clarified: the parent parts index now names proof-loop parts as bounded part
  contracts inside the parent mechanic, with promotion, publication, runtime
  acceptance, sibling approval, and coordinator-strength pressure routed back to
  step owners.
- Source surfaces updated: `mechanics/proof-loop/PARTS.md` and
  `scripts/validate_repo.py`.
- Validation route: proof-loop route-smoke part validation plus root repo
  validation.

## Review Log

### 2026-05-24 - Proof-loop parts boundary language clarified

- Previous assumption: the parent parts index could state the route-smoke
  boundary through a standalone-mechanic contrast.
- New reality: low-context agents need the lower index to name the positive
  part contract: bounded part contracts inside the parent mechanic, route-smoke
  report output, owner-routed promotion/publication/runtime/sibling pressure,
  and step-owner authority.
- Reason: `mechanics/proof-loop/PARTS.md` is an active index surface for the
  proof-loop lower tree; it should route part pressure directly before the
  agent enters the part.
- Source surfaces updated: proof-loop parent parts index and root validator
  token.
- Validation: proof-loop route-smoke part validation and root repo validation.

## Validation

- `python scripts/validate_repo.py`
- `python scripts/validate_semantic_agents.py`
- `python -m pytest -q tests/test_mechanic_surface_contracts.py -k proof_loop_route_smoke_part_readme`
