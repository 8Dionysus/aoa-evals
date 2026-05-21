# Boundary Bridge Legacy Distillation Log

## 2026-05-20 Mechanics Refactor

Boundary bridge work moved from rejected parent naming and scattered root
bridge paths into the active `mechanics/boundary-bridge/` parent.

Distilled into active route:

- sibling proof-reference compatibility lives under
  `mechanics/boundary-bridge/parts/compatibility-map/`;
- latest sibling canary support lives under
  `mechanics/boundary-bridge/parts/latest-sibling-canary/`;
- orchestrator proof-anchor alignment lives under
  `mechanics/boundary-bridge/parts/orchestrator-proof-anchors/`;
- Phase Alpha eval matrix source plan, schema, builder, and generated readout
  live under `mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/`;
- `mechanics/EVIDENCE_CLUSTERS.md` records why `sibling-proof-refs`,
  `orchestrator`, and `phase-alpha` are not parent mechanics here.

Still historical:

- `mechanics/sibling-proof-refs/` as a parent package name;
- `docs/SIBLING_PROOF_REFS.md` as the old compatibility-map doc path;
- `docs/ORCHESTRATOR_PROOF_ALIGNMENT.md` as the old orchestrator proof-anchor
  path;
- root Phase Alpha eval matrix example, schema, builder, and generated readout
  placement;
- any reading where local bridge evidence becomes sibling-owner acceptance.

Do not create new boundary-bridge work in legacy. Distill into the owning
active part first.
