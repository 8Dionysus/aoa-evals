# AGENTS.md

## Entry Route

When package semantics or direction are relevant, consult the package README and then the `mechanics/audit/DIRECTION.md`, `mechanics/audit/PARTS.md`, and `mechanics/audit/PROVENANCE.md` routes as needed for the touched source.

## Applies to

`mechanics/audit/` and the runtime evidence intake route.

## Role

This package protects the candidate-evidence loop:

`runtime or trace artifact -> selected evidence packet -> runtime candidate reader -> bundle-local review`

## Operating Card

| Field | Route |
| --- | --- |
| role | audit candidate-evidence loop for runtime and trace artifacts |
| input | runtime or trace artifact, selected evidence packet, artifact-to-verdict hook, runtime candidate reader drift, schema change, or stronger-owner evidence question |
| output | selected evidence route, generated reader check, bundle-local review handoff, integrity review, or stronger-owner handoff |
| owner | `aoa-evals` owns candidate evidence routing; runtime owners keep runtime truth and bundle-local review owns accepted proof |
| next route | `mechanics/audit/README.md`, `DIRECTION.md`, `PARTS.md`, affected part docs/schemas/scripts, and affected source bundle |
| tools | candidate reader builders, root validator, semantic AGENTS validator |
| validation | this card's `Validation` section |

current operating direction `mechanics/audit/DIRECTION.md`; active-to-archive bridge `mechanics/audit/PROVENANCE.md`.

## Route Rules

- Keep runtime evidence candidate-scoped until bundle-local review accepts it.
- Rebuild generated runtime candidate readers from their source surfaces.
- Keep raw private logs, secrets, and host fingerprints out of public examples.
- Route `abyss-stack` evidence through eval review before verdict adoption.
- Keep artifact-to-verdict hooks as review metadata, below runtime judge
  implementation.
- Keep candidate evidence bounded to its local claim instead of global
  capability, safety, intelligence, or agent-quality ranking.

## Validation

Use the on-demand [VALIDATION.md](VALIDATION.md) route for executable checks.

Use the audit and candidate-reader checks in [VALIDATION.md](VALIDATION.md).

If source examples changed and generated readers are intentionally refreshed,
use the rebuild route in [VALIDATION.md](VALIDATION.md) before rerunning the checks.

## Closeout

Report whether the change touched runtime evidence examples, artifact hooks,
schemas, generated readers, review docs, accepted legacy names, or stronger
owner boundaries.
