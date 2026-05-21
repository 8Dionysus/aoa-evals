# 0060 Proof Loop Route-Smoke Contract

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/proof-loop/parts/route-smoke/`

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

## Validation

- `python scripts/validate_repo.py`
- `python scripts/validate_semantic_agents.py`
- `python -m pytest -q tests/test_validate_repo.py -k proof_loop_route_smoke_part_readme`
