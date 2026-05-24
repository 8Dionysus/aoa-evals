# Boundary Bridge / Latest Sibling Canary Part

## Role

This part owns the latest-sibling checkout canary for local compatibility
checks.

It turns sibling path drift into bounded evidence for local repair while
sibling edits and public validation replacement stay in their owner routes.

## Source Surfaces

- `mechanics/boundary-bridge/parts/latest-sibling-canary/config/sibling_canary_matrix.json`
- `mechanics/boundary-bridge/parts/latest-sibling-canary/scripts/run_sibling_canary.py`
- `mechanics/boundary-bridge/parts/latest-sibling-canary/tests/test_sibling_canary.py`
- `.github/workflows/repo-validation.yml`

## Inputs

- canary matrix entries that name sibling repos, checkout roots, and required
  proof-ref paths;
- local sibling checkout state;
- configured source-checkout resolution for `abyss-stack`;
- repo validation pin posture when public-lane drift needs comparison.

## Outputs

- latest-sibling canary readout for local compatibility;
- missing-path or stale-checkout diagnostics;
- evidence for local proof-ref repair or GitHub `Repo Validation` pin refresh;
- sibling edit and proof acceptance pressure routed to stronger owner paths.

## Stronger Owner Split

`aoa-evals` owns the canary matrix, local runner, diagnostics, and local repair
decision.

Sibling repositories keep source truth. GitHub `Repo Validation` remains the
public pinned-lane check when workflow pins change.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| sibling edit pressure appears | sibling-owner change path, with canary output kept as local compatibility evidence |
| GitHub `Repo Validation` replacement pressure appears | keep local canary success below the pinned public validation lane |
| path resolution reads as sibling owner acceptance, bundle verdict, receipt publication, runtime truth, or proof promotion | return to sibling owner review, bundle-local review, receipt publication, runtime owner, or proof owner |
| artifact form `latest-sibling-canary` reads as a parent mechanic | keep it under the `boundary-bridge` part map |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
