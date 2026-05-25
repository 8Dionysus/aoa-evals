# AGENTS.md

## Entry Route

Start with the package README. Then read `mechanics/boundary-bridge/DIRECTION.md` for current operating direction, `mechanics/boundary-bridge/PARTS.md` for active parts, and `mechanics/boundary-bridge/PROVENANCE.md` as the active-to-archive bridge for legacy or former-placement lookup.

## Applies to

`mechanics/boundary-bridge/`, sibling proof-reference compatibility,
orchestrator proof-anchor routes, and Phase Alpha eval matrix bridge routes.

## Role

This package protects the sibling-reference loop:

`repo-qualified ref -> sibling owner route -> compatibility posture -> latest-sibling canary -> bundle-local review`

It also protects the orchestrator proof-anchor loop:

`orchestrator quest -> aoa-agents class ref -> local proof-anchor map -> generated quest reader -> deferred proof review`

It also protects the Phase Alpha eval matrix bridge:

`aoa-playbooks run matrix -> local eval-surface plan -> generated eval matrix -> release or recurrence verification`

## Operating Card

| Field | Route |
| --- | --- |
| role | boundary-bridge route for sibling refs, orchestrator proof anchors, and Phase Alpha eval matrix bridges |
| input | repo-qualified ref, sibling owner route, compatibility posture, latest-sibling canary, orchestrator proof anchor, generated quest reader, or Phase Alpha eval matrix pressure |
| output | compatibility map update, sibling canary check, generated bridge check, bundle-local review handoff, or sibling-owner handoff |
| owner | `aoa-evals` owns local compatibility/readout posture; sibling repos and stronger owners keep their source truth and acceptance |
| next route | `mechanics/boundary-bridge/README.md`, `DIRECTION.md`, `PARTS.md`, affected part docs/config/scripts, and sibling owner route |
| tools | root validator, catalog builder, latest-sibling canary runner, phase-alpha matrix generator, semantic AGENTS validator |
| validation | this card's `Validation` section |

## Read before editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `docs/architecture/PROOF_TOPOLOGY.md`
5. `mechanics/boundary-bridge/parts/compatibility-map/docs/SIBLING_PROOF_REFS.md`
6. `mechanics/boundary-bridge/PARTS.md`
7. `mechanics/boundary-bridge/parts/README.md`
8. `mechanics/README.md`
9. `mechanics/boundary-bridge/README.md`
10. `docs/decisions/0003-sibling-proof-reference-compatibility.md`
11. `docs/decisions/0008-boundary-bridge-mechanic-package.md`
12. `mechanics/boundary-bridge/parts/orchestrator-proof-anchors/docs/ORCHESTRATOR_PROOF_ALIGNMENT.md`
13. `mechanics/boundary-bridge/parts/latest-sibling-canary/config/sibling_canary_matrix.json`
14. `mechanics/boundary-bridge/parts/latest-sibling-canary/scripts/run_sibling_canary.py`
15. `mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/README.md`
16. `mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py`

## Route Rules

- Edit sibling repos only through an explicit sibling-owner route.
- Treat sibling path existence as compatibility evidence below proof authority
  and owner acceptance.
- Repair generated readers through their builders and source surfaces.
- Keep old sibling paths in legacy posture unless a current route adopts them.
- Use latest-sibling canary output as compatibility evidence below bundle
  verdicts.
- Keep class-facing proof anchors under `boundary-bridge`; the active parent
  remains `boundary-bridge`.
- Route role identity, playbook authority, memo truth, and quest verdict
  authority to their stronger owners.
- Treat Phase Alpha eval matrix entries as planning/verification bridges below
  playbook approval, runtime verdicts, bundle-local eval results, and
  sibling-owner acceptance.

## Validation

Run:

```bash
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python mechanics/boundary-bridge/parts/latest-sibling-canary/scripts/run_sibling_canary.py --repo-root . --format json
python mechanics/boundary-bridge/parts/phase-alpha-eval-matrix/scripts/generate_phase_alpha_eval_matrix.py --check
python scripts/validate_semantic_agents.py
```

## Closeout

Report which sibling owner, refs, compatibility posture, canary result, and
local proof surfaces changed. Say explicitly whether sibling repos were left
untouched.
