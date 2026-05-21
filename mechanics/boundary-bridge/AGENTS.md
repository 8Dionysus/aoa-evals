# AGENTS.md

## Entry Route

Start with the package README. Then read `mechanics/boundary-bridge/DIRECTION.md` for current operating direction, `mechanics/boundary-bridge/PARTS.md` for active parts, and `mechanics/boundary-bridge/PROVENANCE.md` only when legacy or former placement matters.

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

## Read before editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `docs/PROOF_TOPOLOGY.md`
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

## Boundaries

- Do not edit sibling repos unless the user explicitly routes that owner work.
- Do not treat sibling path existence as proof authority or owner acceptance.
- Do not repair generated readers by hand.
- Do not keep old sibling paths as active topology without legacy posture.
- Do not use latest-sibling canary output as a bundle verdict.
- Do not create an `orchestrator` parent mechanic from class-facing proof
  anchors.
- Do not use orchestrator proof anchors as role identity, playbook authority,
  memo truth, or quest verdict authority.
- Do not use Phase Alpha eval matrix entries as playbook approval, runtime
  verdicts, bundle-local eval results, or sibling-owner acceptance.

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
