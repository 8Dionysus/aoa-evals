# Boundary Bridge Direction

Boundary Bridge in `aoa-evals` keeps sibling references, compatibility posture,
owner-facing proof anchors, and Phase Alpha bridge readouts current by routing
boundary pressure to local compatibility checks, bundle-local review, or the
stronger sibling owner.

Sibling authority stays with the repository that owns the referenced truth.

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
- Keep canary checks as local compatibility evidence below sibling approval.
- Keep orchestrator proof anchors local to eval obligations and route
  orchestrator identity pressure to `aoa-agents`.
- Keep Phase Alpha matrix work as a bridge from sibling playbook truth to local
  eval anchors below playbook approval.

## Growth rule

Add new bridge parts only when a repeated boundary operation spans several
surfaces and needs local validation. One broken link belongs in the
compatibility map before package growth.

## Stop-lines

| Pressure | Route |
| --- | --- |
| sibling repository needs an edit | sibling-owner route before local compatibility repair |
| local compatibility checks read as sibling owner acceptance | accepting sibling repository or bundle-local proof review |
| role, playbook, memo, runtime, or routing authority appears in bridge wording | `aoa-agents`, `aoa-playbooks`, `aoa-memo`, runtime owner, or `aoa-routing` owner route |
| one broken sibling ref appears | compatibility map, current/legacy/rejected/unresolved posture, and latest-sibling canary before package growth |

## Validation

Use the validation lane in [mechanics/boundary-bridge/AGENTS.md](AGENTS.md#validation).
