# Proof Loop / Route Smoke Part

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
- explicit route-smoke-only posture for receipt, runtime, sibling approval,
  generated reader, and bundle-promotion pressure.

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
Its recorded posture is no eval result receipt. Bundle promotion, runtime
intake, sibling-owner approval, generated-reader authority, and full proof-loop
completeness proof each route to their owning surface before adoption.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| route-smoke report read as eval-result run | bundle-local eval-result run route |
| eval-result receipt or publication pressure | `mechanics/publication-receipts/` after a reviewed bounded report exists |
| `aoa-verification-honesty` or another bundle needs promotion | bundle-local review and promotion route |
| runtime evidence, live dispatch, sibling-owner approval, or generated-reader authority enters the read | audit/runtime owner, boundary-bridge sibling route, or generated-reader source route |
| full proof-loop completeness or goal completion pressure | full loop route: source bundle review, evidence contract, bounded report, and optional receipt |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
