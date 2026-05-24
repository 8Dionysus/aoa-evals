# Audit / Integrity Review Part

## Role

This part owns the owner-local runtime integrity review contract.

It captures W10-shaped runtime continuity evidence as `candidate_only`, keeps
human review mandatory, and points upward to the stronger Experience owner split
for activation or continuity-owner decisions.

## Source Surfaces

- `mechanics/audit/parts/integrity-review/docs/RUNTIME_INTEGRITY_REVIEW.md`
- `mechanics/audit/parts/integrity-review/schemas/runtime-integrity-review.schema.json`
- `mechanics/audit/parts/integrity-review/examples/runtime_integrity_review.example.json`

## Inputs

- candidate-only W10 runtime continuity evidence refs;
- replay requirement fields and forbidden-claim constraints;
- budget refs, reviewer refs, and owner-route refs;
- selected runtime evidence and trace refs that stay below proof canon.

## Outputs

- schema-backed `runtime_integrity_review.example.json`;
- a review guide for owner-local runtime continuity inspection;
- explicit replay and authority-jump requirements;
- bounded candidate posture for later Experience or bundle-local review.

## Stronger Owner Split

`aoa-evals` owns the runtime integrity review contract and candidate-only
interpretation limits.

Runtime activation, continuity truth, memory canon, and Experience owner truth
route through their owning surfaces before this candidate review can support a
stronger read.

## Boundary

The review surface is a candidate inspection route. Proof canon, runtime
activation authority, owner override, and canon write pressure all hand off to
their owner routes.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| runtime continuity activation is requested | route to Experience and runtime-owner gates after review |
| memory canon, owner approval, or proof verdict pressure appears | route to `aoa-memo`, the owning repo, or bundle-local eval review |
| replay or human review is skipped | return to selected evidence, owner-local replay, and reviewer signoff |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
