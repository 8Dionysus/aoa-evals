# AGENTS.md

## Applies to

This card applies to `memo/`.

## Role

`memo/` is the `aoa-evals` local memory port. It holds proof-layer memory
candidates, receipts, exports, and local notes before reviewed landing in
`aoa-memo`.

## Read before editing

1. Root `AGENTS.md`
2. `README.md`
3. `docs/decisions/AOA-EV-D-0106-memory-consumer-proof-boundary.md`
4. `docs/decisions/AOA-EV-D-0243-local-memo-port.md`
5. This `README.md`
6. `PORT.yaml`
7. `aoa-memo/docs/memory/LOCAL_MEMO_PORT_STANDARD.md` when a candidate should
   move centrally

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

```bash
AOA_MEMO_ROOT="${AOA_MEMO_ROOT:-/srv/AbyssOS/aoa-memo}"
python "$AOA_MEMO_ROOT/scripts/memory/validate_local_memo_port.py" --path memo
python "$AOA_MEMO_ROOT/scripts/memory/build_local_memo_port_index.py" --path memo --check
```

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
