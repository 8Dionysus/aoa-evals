# Latest Sibling Canary Part

## Role

This part owns the latest-sibling checkout canary for local compatibility
checks.

It turns sibling path drift into bounded evidence for local repair without
editing sibling repositories or replacing the pinned public validation lane.

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
- no sibling edits and no proof acceptance.

## Stronger Owner Split

`aoa-evals` owns the canary matrix, local runner, diagnostics, and local repair
decision.

Sibling repositories keep source truth. GitHub `Repo Validation` remains the
public pinned-lane check when workflow pins change.

## Stop-Lines

- Do not edit sibling repositories from canary output.
- Do not replace GitHub `Repo Validation` with local canary success.
- Do not treat path resolution as sibling owner acceptance, bundle verdict,
  receipt publication, runtime truth, or proof promotion.
- Do not let the artifact form `latest-sibling-canary` become a parent
  mechanic.

## Validation

```bash
python mechanics/boundary-bridge/parts/latest-sibling-canary/scripts/run_sibling_canary.py --repo-root . --format json
python -m pytest -q mechanics/boundary-bridge/parts/latest-sibling-canary/tests/test_sibling_canary.py
python scripts/validate_repo.py
```
