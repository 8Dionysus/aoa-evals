# Agon Verdict Draft Checks

## Role

This note scopes the local checks that can be applied to a future Agon verdict
draft.

The checks ask whether a draft is shaped well enough for review. They do not
decide the arena.

## Check Families

Useful draft checks may inspect:

- declared verdict status;
- delta legitimacy;
- scar request evidence;
- retention request evidence;
- inscription bundle refs;
- forbidden runtime effects;
- missing owner review.

## Boundary

Draft checks can reject or flag malformed proof posture. They cannot issue
closure, mutate rank, write memory, grant scars, or convert draft wording into a
live verdict.

## Route

Start at `mechanics/agon/parts/vds-alignment/README.md`. Use the seed and
generated registry to find the exact draft-status record, then return to the
stronger owner for verdict authority.

## Validation

Use the part `VALIDATION.md` route and parent `parts/AGENTS.md` child validation
block. The registry should make malformed draft effects visible while remaining
below Agon verdict law.
