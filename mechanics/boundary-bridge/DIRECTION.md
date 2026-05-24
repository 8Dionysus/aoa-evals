# Boundary Bridge Direction

Boundary Bridge in `aoa-evals` should keep sibling references, compatibility
posture, and owner-facing proof anchors current without absorbing sibling
authority.

Use this file for the package's current operating direction: read it after the
parent entry card and before `PARTS.md`, part contracts, source bundles,
decision records, and `PROVENANCE.md`.

## Source-of-truth split

- `README.md`: package entry card and shortest boundary route.
- `DIRECTION.md`: current operating direction.
- `PARTS.md`: active boundary-bridge part map.
- `parts/`: compatibility map, latest-sibling canary, orchestrator proof
  anchors, and Phase Alpha eval matrix support.
- `PROVENANCE.md`: controlled bridge from active route to old sibling-proof-ref placement.
- `legacy/`: archive-local route for old sibling-proof-ref placement after
  `PROVENANCE.md`.
- sibling repos: stronger owner truth for their own surfaces.

## Current contour

- Keep `repo:<owner>/...` refs explicit and posture-labeled as current,
  legacy, rejected, or unresolved.
- Keep canary checks local compatibility evidence, not sibling approval.
- Keep orchestrator proof anchors local to eval obligations; do not create an
  `orchestrator` parent mechanic.
- Keep Phase Alpha matrix work as a bridge from sibling playbook truth to local
  eval anchors, not a playbook approval surface.

## Growth rule

Add new bridge parts only when a repeated boundary operation spans several
surfaces and needs local validation. One broken link should update the
compatibility map, not create a package.

## Stop-lines

- Do not mutate sibling repos from boundary-bridge work.
- Do not claim sibling owner acceptance from local compatibility checks.
- Do not import role, playbook, memo, runtime, or routing authority.

## Validation

Use the validation lane in [mechanics/boundary-bridge/AGENTS.md](AGENTS.md#validation).
