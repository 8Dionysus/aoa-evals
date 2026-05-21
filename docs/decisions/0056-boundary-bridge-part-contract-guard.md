# 0056 Boundary Bridge Part Contract Guard

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/boundary-bridge/parts/`

## Context

`boundary-bridge` owns the eval-side operation for sibling proof refs,
latest-sibling compatibility checks, orchestrator proof anchors, and Phase Alpha
eval matrix bridging.

The parent README and `PARTS.md` already named the owner split. The risk was
that three active part README files still exposed that split too weakly:
`compatibility-map`, `latest-sibling-canary`, and
`orchestrator-proof-anchors`. Those parts touch sibling refs, local checkout
evidence, quest owner-surface bindings, generated readers, and class-facing
proof anchors. Without local contracts, a future repair could turn bridge
evidence into sibling authority or invent an `orchestrator` or canary parent.

## Decision

Make the three thin Boundary Bridge part README files carry explicit
part-level contracts:

- `mechanics/boundary-bridge/parts/compatibility-map/README.md`;
- `mechanics/boundary-bridge/parts/latest-sibling-canary/README.md`;
- `mechanics/boundary-bridge/parts/orchestrator-proof-anchors/README.md`.

Each part must expose inputs, outputs, stronger owner split, stop-lines, and
validation. The existing `phase-alpha-eval-matrix` part already carries that
shape and remains under the same validator surface.

## Rationale

Boundary Bridge is a translation and compatibility mechanic. It must stay
convex as `boundary-bridge`, with canary, compatibility-map, orchestrator-anchor,
and matrix forms as parts.

`aoa-evals` may decide whether a sibling ref can support local proof review.
It may not make sibling path existence into owner acceptance, rewrite
orchestrator role identity, promote quests into verdicts, or replace the pinned
public validation lane with local checkout success.

## Consequences

- Positive: future sibling path repair starts from a part contract instead of
  path archaeology.
- Positive: canary output and proof anchors remain bridge evidence, not owner
  truth.
- Positive: `python scripts/validate_repo.py` now catches drift in the three
  high-risk Boundary Bridge part README files.
- Tradeoff: part README wording is tighter where sibling authority is at risk.

## Boundaries

This decision does not edit sibling repositories, create an `orchestrator`
parent mechanic, create a `latest-sibling-canary` parent mechanic, accept
sibling refs as proof, promote bundles, publish receipts, approve playbooks, or
turn generated quest readers into source truth.

It does not transfer `aoa-agents`, `aoa-playbooks`, `aoa-memo`, `aoa-kag`,
`abyss-stack`, or other sibling owner authority into `aoa-evals`.

## Validation

- `python scripts/validate_repo.py`
- `python -m pytest -q tests/test_validate_repo.py -k 'boundary_bridge_part_readmes or boundary_bridge_provenance'`
- `python mechanics/boundary-bridge/parts/latest-sibling-canary/scripts/run_sibling_canary.py --repo-root . --format json`
- `python mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py --check`
