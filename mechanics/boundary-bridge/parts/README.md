# Boundary Bridge Parts

This directory holds package-local parts for the sibling-reference compatibility
and proof-anchor boundary operation.

Use these parts when a proof surface cites a sibling repository and needs a
current, legacy, rejected, or unresolved posture before it can support a local
bounded claim.

## Active Parts

- `compatibility-map/`: the authored compatibility map and posture vocabulary.
- `latest-sibling-canary/`: the current-sibling matrix and runner.
- `orchestrator-proof-anchors/`: the orchestrator-facing proof-anchor map and
  quest owner-surface binding.
- `phase-alpha-eval-matrix/`: the bridge from sibling-owned Phase Alpha
  playbook runs to local eval anchors and support refs.

## Validation

```bash
python scripts/validate_repo.py
python mechanics/boundary-bridge/parts/latest-sibling-canary/scripts/run_sibling_canary.py --repo-root . --format json
python mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py --check
```
