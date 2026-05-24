# Memory Consumer Proof Boundary

- Status: Accepted
- Date: 2026-05-24
- Owner surface: `README.md`, `docs/EVAL_PHILOSOPHY.md`, `docs/PROOF_TOPOLOGY.md`, `scripts/validate_repo.py`

## Context

`aoa-evals` increasingly cites memory-shaped evidence from `aoa-memo`, `.aoa`
session archives, runtime candidate readers, and sibling routes.
That is useful for recall and source discovery, but it can blur the proof
boundary if reviewed memory starts to read like verdict support by itself.

`aoa_memo` currently reports `aoa-evals` as route-only: the repo has no local
memo port, and reviewed memory should be consumed through `aoa-memo` rather
than written locally from eval-side paths.

## Options Considered

- Add a local memo port now so eval runs can prepare memo candidates directly.
- Treat reviewed memory read models as proof support whenever an eval references
  them.
- Keep `aoa-evals` in route_only memory posture, consuming reviewed memory only
  as cited recall context while proof authority stays in source eval bundles,
  mechanics, selected evidence, reports, and validators.

## Decision

`aoa-evals` stays a memory consumer, not a memory authority.

Memory can inform proof review only when it is cited as reviewed `aoa-memo`
object ids, provenance, lifecycle, and generated read models, or as `.aoa`
session evidence that remains source evidence until reviewed memory intake.
Memory is not proof.

The repo does not create a local memo port in this slice.
Until a future owner decision adds one, do not create local memo candidates,
reviewed-intake exports, or durable memory records from hidden eval-side paths.
Durable memory lands only in `aoa-memo`.

`aoa_memo` MCP brief/search/status/validation/landing-plan dry-runs may support
proof-side inspection and source discovery. They are access-plane evidence only:
they do not make memory into proof, create eval-side write authority, or land
durable memory.

## Rationale

This keeps the proof layer honest.
Eval verdicts need fixtures, selected evidence, scoring or verdict logic,
bundle-local reports, mechanic-owned interpretation, and validation.
Reviewed memory helps reviewers find prior context and source refs, but it does
not prove the bounded claim on its own.

Keeping route_only memory posture also matches the current workspace memory map
and avoids creating a local write path before `aoa-evals` has a real owner need
for one.

## Consequences

- Positive: proof claims can cite reviewed memory without letting memory become
  verdict authority.
- Positive: future agents get a clear route for `.aoa` evidence, reviewed
  `aoa-memo` recall, and durable memory landing.
- Tradeoff: eval-side memory writeback remains unavailable until a separate
  owner decision adds a local memo port.
- Follow-up: if recurring eval work truly needs local memory candidates, add a
  reviewed memo port contract in a separate slice before writing candidates or
  exports.

## Current Applicability

As of 2026-05-24:

- Still valid: `aoa-evals` is a route_only memory consumer.
- Changed: root proof guidance now names memory context as recall context, not
  proof authority.
- Superseded by: none.

## Review Log

### 2026-05-24 - Memory consumer boundary landed

- Previous assumption: memory references were handled by general sibling-owner
  and proof-boundary rules.
- New reality: reviewed memory and session evidence now have an explicit
  consumer route inside the proof organ.
- Reason: eval/KAG/stats/playbooks/agents are being connected as memory
  consumers while `aoa-memo` remains reviewed memory authority.
- Source surfaces updated: `README.md`, `docs/EVAL_PHILOSOPHY.md`,
  `docs/PROOF_TOPOLOGY.md`, `scripts/validate_repo.py`,
  `tests/test_validate_repo.py`.
- Validation: `python scripts/validate_repo.py` and
  `python scripts/validate_semantic_agents.py`.

## Boundaries

This decision does not make `aoa-evals` a memory object owner.
It does not let reviewed memory replace source eval bundles, selected evidence,
fixtures, reports, scoring, verdict logic, or mechanic-owned proof
interpretation.
It does not create a local memo port.
It does not change `aoa-memo` durable reviewed memory authority.
It does not treat `aoa_memo` MCP outputs as proof authority or direct durable
write authority.

## Validation

The validator requires the memory-consumer boundary in the public README,
evaluation philosophy, proof topology, this decision note, and the decision
index.
Run:

- `python scripts/validate_repo.py`
- `python scripts/validate_semantic_agents.py`
