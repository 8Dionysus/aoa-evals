# Generated Route Residue Guard

- Decision ID: AOA-EV-D-0073

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-21
- Surface classes: validation guard, generated/readout
- Mechanic parents: none
- Guard families: route residue, generated/report/receipt/runtime
- Posture: generated/readout rationale

## Context

The mechanics refactor moved active payloads out of old root districts and
wrong parent names. Physical route guards catch many regressions, but generated
readers can still carry stale structured references after the old files are
gone.

That failure mode is subtle: `generated/` and part-local `generated/` files are
not authority, but agents read them heavily. If a readout keeps
`mechanics/titan-canaries/...`, `mechanics/agon-proof/...`, or root
`fixtures/...` as a structured route, the old topology can re-enter the next
slice as if it were current.

## Decision

`scripts/validate_repo.py` validates generated/readout JSON routes for two
residue classes:

- legacy mechanic parent routes such as `mechanics/agon-proof/` and
  `mechanics/titan-canaries/`;
- route-card-only root district routes such as `fixtures/`, `schemas/`,
  `config/`, `reports/`, `runners/`, `scorers/`, and `templates/`.

The guard scans root `generated/*.json` and mechanic part-local
`mechanics/**/generated/*.json`.

The guard is context-aware:

- root generated readers may not point at route-card-only root districts;
- part-local generated readers may use local `config/`, `schemas/`, `reports/`,
  or similar sibling routes when those files exist under the same part root;
- `content_markdown` is not treated as a structured route field, so bundle-local
  markdown examples are not over-policed.

## Consequences

- Generated readers remain companions, not source truth, but they cannot carry
  stale active route instructions.
- The root route-card guard does not leak into valid part-local topology.
- A future move must update builders or source metadata, then regenerate, rather
  than hand-editing generated residue.

## Validation

Expected validation route:

```bash
python -m pytest -q tests/test_generated_route_residue.py
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python -m pytest -q
```
