# Local Memo Port

- Decision ID: AOA-EV-D-0243
- Status: Accepted
- Date: 2026-06-21
- Owner surface: `memo/AGENTS.md`, `memo/PORT.yaml`, `docs/guides/EVAL_PHILOSOPHY.md`, `docs/architecture/PROOF_TOPOLOGY.md`

## Index Metadata

- Original date: 2026-06-21
- Surface classes: memory context, proof topology, boundary/runtime/sibling, validation guard
- Mechanic parents: none
- Guard families: memory boundary, local memo port, validation
- Posture: active rationale

## Context

AOA-EV-D-0106 kept `aoa-evals` in route_only memory posture because reviewed
memory context was starting to look like proof authority. That boundary remains
right: memory is not proof.

The recurring local problem is different. `aoa-evals` now repeatedly produces
near-field lessons about proof boundaries, local eval-port routing, validator
topology, generated reader drift, and landing failures. Without a local memo
port, those lessons either remain only in session evidence or pressure durable
`aoa-memo` too early.

`aoa-memo` now defines a local memo port standard, and sibling repositories use
small `memo/` ports for candidate memory without becoming memory authorities.
`aoa-evals` needs the same near-field holding surface, but only below proof
authority and durable memory authority.

## Options Considered

- Keep route_only memory posture and write no local candidates.
- Create a full reviewed memory corpus inside `aoa-evals`.
- Add a minimal `write_candidate_only` local `memo/` port.
- Write durable reviewed memory directly into `aoa-memo` from eval-side work.

## Decision

Create a minimal local `memo/` port for `aoa-evals`.

The port uses the shared local memo port contract:

- `memo/AGENTS.md`
- `memo/README.md`
- `memo/PORT.yaml`
- `memo/INDEX.md`
- `memo/index.min.json`
- `memo/candidates/`
- `memo/receipts/`
- `memo/exports/`
- `memo/local/`

Its default mode is `write_candidate_only`. It may hold proof-layer memory
candidates, validation or handoff receipts, reviewed-intake exports for
`aoa-memo`, and local notes that should remain below durable memory.

## Rationale

This keeps useful lessons close to the proof work that produced them while
preserving the stronger owner split.

`aoa-evals` owns proof-layer source surfaces: eval bundles, mechanics,
validators, generated proof readers, reports, and decisions. It can therefore
own local memory candidates about those surfaces. It must not own durable
cross-system memory truth. That remains `aoa-memo`.

The port also gives agents a concrete place to stop. A lesson can become a
local candidate with source refs and evidence refs without being promoted into
a proof verdict, a central memory object, or a hidden writeback approval.

## Consequences

- Positive: proof-boundary and validator lessons can be captured locally before
  central review.
- Positive: memory writeback pressure no longer has to jump from session
  evidence directly to `aoa-memo`.
- Tradeoff: `aoa-evals` now has one more root district and must keep its port
  index generated from packets.
- Follow-up: future `aoa-memo` tooling can inspect pending `aoa-evals` exports
  and prepare reviewed intake plans, but durable landing still belongs in
  `aoa-memo`.

## Current Applicability

As of 2026-06-21:

- Still valid: AOA-EV-D-0106 keeps reviewed memory below proof authority.
- Changed: `aoa-evals` now has a local `write_candidate_only` memo port.
- Supersedes: AOA-EV-D-0106 only for the operational route_only/no-local-port
  clause. It does not supersede the memory-consumer proof boundary.

## Boundaries

This decision does not make memory proof.
It does not let local memo candidates replace eval bundles, selected evidence,
fixtures, reports, scoring, verdict logic, generated proof readers, or
mechanic-owned proof interpretation.
It does not create durable reviewed memory in `aoa-evals`.
It does not authorize direct durable writes to `aoa-memo`.
It does not let MCP packets bypass owner review.
It does not require every landing to create a memo candidate.

## Validation

This decision is valid when:

- `memo/PORT.yaml` validates against the `aoa-memo` local memo port contract;
- `memo/INDEX.md` and `memo/index.min.json` are generated from the port;
- `README.md`, `AGENTS.md`, `docs/guides/EVAL_PHILOSOPHY.md`, and
  `docs/architecture/PROOF_TOPOLOGY.md` keep proof authority separate from
  local memo candidate capture;
- generated decision indexes include this note;
- `python scripts/validate_repo.py` and
  `python scripts/validate_semantic_agents.py` pass.
