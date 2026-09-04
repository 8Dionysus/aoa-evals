# AGENTS.md

## Entry Route

When package semantics or direction are relevant, consult the package README and then the `mechanics/boundary-bridge/DIRECTION.md`, `mechanics/boundary-bridge/PARTS.md`, and `mechanics/boundary-bridge/PROVENANCE.md` routes as needed for the touched source.

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

current operating direction `mechanics/boundary-bridge/DIRECTION.md`; active-to-archive bridge `mechanics/boundary-bridge/PROVENANCE.md`.

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

Use the on-demand [VALIDATION.md](VALIDATION.md) route for executable checks.

Use the boundary-bridge checks in [VALIDATION.md](VALIDATION.md).

## Closeout

Report which sibling owner, refs, compatibility posture, canary result, and
local proof surfaces changed. Say explicitly whether sibling repos were left
untouched.
