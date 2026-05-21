# Route Smoke Part

## Role

This part owns the first public-safe proof-loop route-smoke report.

## Source Surfaces

- `mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md`

## Inputs

- one bounded proof question about local proof-loop routeability;
- selected source bundle `aoa-verification-honesty` and its `EVAL.md` plus
  `eval.yaml`;
- support contract refs from proof-object and proof-infra surfaces;
- public-safe candidate evidence limited to repo-local route surfaces;
- explicit no-receipt, no-runtime, no-sibling-approval, and no-bundle-promotion
  posture.

## Outputs

- one bounded route-smoke report artifact;
- routeability evidence that one local proof-loop path can reach a bounded
  report;
- explicit defer/handoff posture for any actual eval-result run;
- validation failures when route-smoke wording implies receipt publication,
  bundle promotion, runtime intake, sibling-owner approval, or full proof-loop
  completeness.

## Stronger Owner Split

The selected bundle owns the verification-truthfulness claim and any real
eval-result report.

`proof-loop` owns only the route coordination. `proof-object`, `proof-infra`,
`audit`, `boundary-bridge`, and `publication-receipts` keep ownership of their
step contracts and evidence classes.

## Boundary

The report records one bounded routeability read for the proof-loop mechanic.
It records no eval result receipt. It does not create bundle promotion, runtime
intake, sibling-owner approval, or full proof-loop completeness proof.

## Stop-Lines

- Do not treat the route-smoke report as a new eval-result run.
- Do not publish or imply an eval result receipt.
- Do not promote `aoa-verification-honesty` or any other bundle.
- Do not accept runtime evidence, live dispatch, sibling-owner approval, or
  generated-reader authority.
- Do not use this part to claim full proof-loop completeness or goal
  completion.

## Validation

Payload coverage anchor: `mechanics/proof-loop/parts/route-smoke/`.

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
python -m pytest -q tests/test_validate_repo.py -k proof_loop
```
