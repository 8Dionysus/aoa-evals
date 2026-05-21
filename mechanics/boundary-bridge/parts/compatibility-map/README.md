# Boundary Bridge / Compatibility Map Part

## Role

This part owns the authored compatibility map for proof references that point
from `aoa-evals` into sibling repositories.

It keeps sibling refs in a local compatibility posture without making local
path repair into sibling owner acceptance.

## Source Surfaces

- `mechanics/boundary-bridge/parts/compatibility-map/docs/SIBLING_PROOF_REFS.md`
- `mechanics/boundary-bridge/README.md`
- `mechanics/boundary-bridge/PARTS.md`
- `docs/decisions/0003-sibling-proof-reference-compatibility.md`

## Inputs

- repo-qualified proof refs from bundles, notes, reports, generated readers,
  runtime candidates, and quest surfaces;
- sibling owner route hints and current local checkout evidence;
- legacy, rejected, unresolved, or accepted-input sibling path vocabulary;
- latest-sibling canary results when path drift needs confirmation.

## Outputs

- authored compatibility map entries with current, legacy, rejected, or
  unresolved posture;
- current, legacy, rejected, or unresolved posture wording that future agents can
  route through directly;
- local guidance for whether a sibling ref may support bundle-local review;
- owner-route repair notes for future proof-ref updates;
- explicit non-authority-transfer wording for sibling path existence.

## Stronger Owner Split

`aoa-evals` owns local reference posture, local proof interpretation, and
whether a sibling ref can support an eval-side proof claim.

Sibling repositories own the referenced object meaning, current source truth,
and whether a path or concept is accepted in their owner lane.

## Stop-Lines

- Do not edit sibling repositories from this part.
- Do not treat path existence as sibling owner acceptance.
- Do not treat compatibility posture as bundle promotion, proof verdict,
  runtime truth, or generated-reader authority.
- Do not use legacy sibling refs as active topology without a current owner
  route or explicit accepted-input posture.

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
