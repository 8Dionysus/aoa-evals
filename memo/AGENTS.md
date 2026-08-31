# AGENTS.md

## Applies to

This card applies to `memo/`.

## Role

`memo/` is the `aoa-evals` local memory port. It holds proof-layer memory
candidates, receipts, exports, and local notes before reviewed landing in
`aoa-memo`.

## Read before editing
Read only the route needed for the touched source: consult the nearest README when its human or semantic contract is required, then follow the source-owner and validation routes conditionally.
## Boundaries

Use this port for `write_candidate_only` work. Keep proof claims, verdicts,
fixtures, scoring, reports, and mechanic-owned proof interpretation in their
owning `aoa-evals` source surfaces. Use this port only for recall, candidate
memory, receipts, and reviewed handoff.

This port is not proof authority and is not durable reviewed memory.
Durable memory lands only in `aoa-memo` through reviewed intake.

Use `PORT.yaml` for the local port contract and `INDEX.md` / `index.min.json`
as generated read models. Use `candidates/` for proposed memory, `receipts/`
for review or handoff traces, `exports/` for packets meant for `aoa-memo`, and
`local/` for proof-layer memory that stays local for now.

## Validation

Use the on-demand [VALIDATION.md](VALIDATION.md) route for executable checks.

For repo-wide proof posture, use the root `AGENTS.md` validation route.

## Candidate Route

Create candidates only when the lesson has a source ref and should be reviewed
later without becoming a proof verdict.

The normal route is:

```text
candidate -> receipt -> optional export -> reviewed aoa-memo route
```

## Closeout

Report candidate path, evidence refs, validation result, and whether the item
stayed local, was exported for reviewed intake, or was landed in `aoa-memo`.
