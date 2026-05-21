# Assistant Certification Judge

## Role

This source note scopes the judge surface for Experience certification-gate
proof.

The judge emits bounded readiness verdicts for review. It does not replace
operator certification authority.

## Reads

Use this surface when a certification gate packet needs to explain how
regression results, rollback evidence, compatibility claims, and authority refs
were interpreted for operator review.

## Boundary

`aoa-evals` owns the judge contract shape, schema/example support, and
bundle-local interpretation.

Owner repositories keep certification, release approval, deployment approval,
rollout promotion, rollback permission, and runtime health authority.

## Validation

Route through `mechanics/experience/parts/certification-gate/README.md` for the
part-level checks. A judge verdict is review evidence; it is not certification
itself.
