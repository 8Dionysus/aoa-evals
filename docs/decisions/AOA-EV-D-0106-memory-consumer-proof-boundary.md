# Memory Consumer Proof Boundary

- Decision ID: AOA-EV-D-0106
- Status: Accepted
- Date: 2026-05-24
- Owner surface: `README.md`, `docs/guides/EVAL_PHILOSOPHY.md`, `docs/architecture/PROOF_TOPOLOGY.md`, `scripts/validate_repo.py`

## Index Metadata

- Original date: 2026-05-24
- Surface classes: proof topology, boundary/runtime/sibling
- Mechanic parents: none
- Guard families: none
- Posture: active rationale

## Context

`aoa-evals` increasingly cites memory-shaped evidence from `aoa-memo`, `.aoa`
session archives, runtime candidate readers, and sibling routes.
That is useful for recall and source discovery, but it can blur the proof
boundary if reviewed memory starts to read like verdict support by itself.

`aoa_memo` originally reported `aoa-evals` as route-only: the repo had no
local memo port, and reviewed memory had to be consumed through `aoa-memo`
rather than written locally from eval-side paths.

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

This slice did not create a local memo port.
AOA-EV-D-0243 later adds one explicit local `write_candidate_only` memo port.
Do not create local memo candidates, reviewed-intake exports, or durable memory
records from hidden eval-side paths outside that port.
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

The original route_only memory posture matched the workspace memory map at the
time and avoided creating a local write path before `aoa-evals` had a real
owner need for one.

## Consequences

- Positive: proof claims can cite reviewed memory without letting memory become
  verdict authority.
- Positive: future agents get a clear route for `.aoa` evidence, reviewed
  `aoa-memo` recall, and durable memory landing.
- Tradeoff: eval-side memory writeback remained unavailable until a separate
  owner decision added a local memo port.
- Follow-up: recurring eval work now uses AOA-EV-D-0243 and `memo/` before
  writing candidates or exports.

## Current Applicability

As of 2026-05-24:

- Still valid: `aoa-evals` is a route_only memory consumer.
- Changed: root proof guidance now names memory context as recall context, not
  proof authority.
- Current root-entry placement: `README.md` carries the concise memory owner
  route, while detailed memory-consumer law stays in `docs/guides/EVAL_PHILOSOPHY.md`,
  `docs/architecture/PROOF_TOPOLOGY.md`, and this decision.
- Superseded by: none.

As of 2026-05-24 route-language review:

- Still valid: reviewed memory can enter proof review only as bounded recall
  context with object ids, provenance, lifecycle, and generated read models.
- Changed: `docs/guides/EVAL_PHILOSOPHY.md` now expresses the active memory route by
  naming recall context, source evidence, owner surfaces, and visible
  provenance directly.
- Historical text: the original decision, rationale, and boundaries remain as
  the record of why the consumer boundary was adopted.
- Superseded by: none.

As of 2026-06-05:

- Still valid: `aoa-evals` consumes memory context only for bounded proof
  review.
- Changed: memo-shaped runtime selected-evidence packets now carry a
  `memory_context_boundary` that names provenance, freshness, retention,
  permission, authority stop-lines, and bundle-local review pressure before
  runtime candidate readers may project them.
- Superseded by: none.

As of 2026-06-21:

- Still valid: memory can support bounded proof review only as recall context,
  source refs, provenance, lifecycle, and reviewed evidence context.
- Changed: AOA-EV-D-0243 creates a local `write_candidate_only` memo port at
  `memo/` for proof-layer memory candidates, receipts, exports, and local notes.
- Superseded by: AOA-EV-D-0243 only for the original route_only/no-local-port
  operational clause. The memory-consumer proof boundary remains active.

## Review Log

### 2026-05-24 - Memory consumer boundary landed

- Previous assumption: memory references were handled by general sibling-owner
  and proof-boundary rules.
- New reality: reviewed memory and session evidence now have an explicit
  consumer route inside the proof organ.
- Reason: eval/KAG/stats/playbooks/agents are being connected as memory
  consumers while `aoa-memo` remains reviewed memory authority.
- Source surfaces updated: `README.md`, `docs/guides/EVAL_PHILOSOPHY.md`,
  `docs/architecture/PROOF_TOPOLOGY.md`, `scripts/validate_repo.py`,
  `tests/test_validate_repo.py`.
- Validation: `python scripts/validate_repo.py` and
  `python scripts/validate_semantic_agents.py`.

### 2026-05-24 - Root entry surface slimmed

- Previous assumption: the public README had to carry the full route_only
  memory posture token set for validation.
- New reality: the public README carries the memory owner route; detailed
  memory-proof law remains in the evaluation philosophy, proof topology, and
  this decision.
- Reason: root entry surfaces should orient a low-context agent without
  becoming the detailed boundary atlas.
- Source surfaces updated: `README.md`, `scripts/validate_repo.py`,
  `tests/test_validate_repo.py`.
- Validation: `python scripts/validate_repo.py`,
  `python scripts/validate_semantic_agents.py`,
  `python -m pytest -q tests/test_root_surface_roles.py -k 'root_readme or memory_consumer_proof_boundary'`,
  `python scripts/build_catalog.py --check`,
  `python scripts/generate_eval_report_index.py --check`,
  `git diff --check`, and `python -m pytest -q`.

### 2026-05-24 - Evaluation philosophy memory route made positive

- Previous assumption: the active philosophy guide needed the short boundary
  slogan to keep memory outside proof authority.
- New reality: the guide now gives the operational route directly: reviewed
  memory supplies recall context, proof authority stays with source evidence
  and owner surfaces, and durable write authority stays visible.
- Reason: agent-facing proof philosophy should let a low-context agent know the
  route, owner, and validation pressure without relying on repeated negative
  self-description.
- Source surfaces updated: `docs/guides/EVAL_PHILOSOPHY.md`,
  `scripts/validate_repo.py`, `tests/test_validate_repo.py`, and this
  decision.
- Validation: root validation, semantic AGENTS validation, and focused memory
  consumer tests.

### 2026-06-05 - Runtime selected-evidence memory context boundary

- Previous assumption: the memory-consumer proof boundary lived mainly in root
  proof guidance and bundle-local memo eval wording.
- New reality: memo recall, contradiction, and writeback selected-evidence
  packets now expose `memory_context_boundary` metadata before generated
  runtime-candidate readers project them.
- Reason: memory context can become hidden authority if provenance, freshness,
  retention, permission, and stop-lines disappear at the runtime evidence
  selection layer.
- Source surfaces updated:
  `mechanics/audit/parts/selected-evidence-packets/schemas/runtime-evidence-selection.schema.json`,
  selected memo evidence examples, `scripts/validators/runtime_evidence_selection.py`,
  runtime-candidate reader builders, generated reader surfaces, validation
  inventories, and focused runtime evidence tests.
- Validation: focused runtime evidence tests, runtime-candidate reader tests,
  generated-reader checks, source-fast validation, and release check.

### 2026-06-21 - Local memo port added below proof authority

- Previous assumption: `aoa-evals` had no local memo port and all durable or
  candidate memory writeback should route away immediately.
- New reality: `aoa-evals` has a minimal `write_candidate_only` local memo port
  for proof-layer lessons.
- Reason: repeated proof-boundary, validator, eval-port, and landing lessons
  need a near-field holding surface before any reviewed `aoa-memo` landing.
- Source surfaces updated: `memo/`, `README.md`, `AGENTS.md`,
  `docs/guides/EVAL_PHILOSOPHY.md`, `docs/architecture/PROOF_TOPOLOGY.md`,
  this decision, and AOA-EV-D-0243.
- Validation: local memo port validation, local memo port index check,
  generated decision indexes, root validation, and semantic AGENTS validation.

## Boundaries

This decision does not make `aoa-evals` a memory object owner.
It does not let reviewed memory replace source eval bundles, selected evidence,
fixtures, reports, scoring, verdict logic, or mechanic-owned proof
interpretation.
The original decision did not create a local memo port; AOA-EV-D-0243 now
creates one explicit `write_candidate_only` local memo port.
It does not let `memory_context_boundary` authorize tool use, durable memory
writeback, source-truth settlement, private or stale context promotion, or
hidden memo ports.
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
