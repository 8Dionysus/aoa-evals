# 0111 Runtime Evidence Ingestion and Mirror Status

- Status: Accepted
- Date: 2026-05-25
- Owner surface: `docs/architecture/AOA_EVALS_MCP_CONTRACT.md`

## Index Metadata

- Surface classes: root/topology, generated/readout, validation guard, boundary/runtime/sibling
- Mechanic parents: audit, boundary-bridge, proof-loop, cross-parent
- Guard families: generated/report/receipt/runtime, sibling and boundary, decision index/read-model
- Posture: active rationale

## Context

`aoa_evals` can now select and inspect bounded evals from OS Abyss. The next
pressure is runtime evidence ingestion and mirror freshness.

The risky path would be to let MCP accept evidence, write into `aoa-evals`, or
compute verdicts. That would collapse the candidate/review boundary and move
proof authority into the runtime access plane.

## Options Considered

- Add a write-capable MCP ingestion tool: convenient, but it turns runtime
  access into proof mutation.
- Add a general eval runner or verdict tool: tempting, but it violates the
  proof-object authority contract.
- Add a read-only status and candidate-validation layer: narrower, but it
  gives OS Abyss an operational ingress gate without accepting evidence.

## Decision

Choose the third option.

`aoa_evals` adds read-only runtime status, candidate packet validation, and a
read-model over stack-owned private runtime candidate exports. Candidate
validation checks schema shape, provenance refs, review posture, and known
eval/template routing. Runtime export reading surfaces candidate metadata and
optional nested payloads for review routing. It does not persist into
`aoa-evals`, accept, score, compare, or publish evidence.

Mirror refresh remains a stack-owned operation through the federation sync
wrapper. The mirror stays a read cache and must expose freshness/provenance
signals when available.

## Rationale

This keeps the proof loop honest:

`runtime artifact -> stack candidate export -> validation gate -> bundle-local review -> bounded report -> optional receipt`

The status layer also prevents context flooding. An agent can ask whether the
selected source or approved mirror is current enough before trusting generated
readers, instead of manually walking the whole repository or runtime tree.

## Consequences

- Positive: OS Abyss gets a first real ingress gate for runtime evidence
  candidates.
- Positive: agents can see stack-owned runtime candidate exports without
  turning MCP into an evidence acceptance queue.
- Positive: agents can see missing/stale mirror state before relying on MCP
  output.
- Tradeoff: a valid candidate packet is still not accepted proof.
- Tradeoff: actual persistence, review queues, receipts, or verdict workflows
  still require later owner decisions.
- Follow-up: stack-owned sync can add mirror manifests and runtime inboxes, but
  those artifacts must stay subordinate to `aoa-evals` bundle-local review.

## Current Applicability

As of 2026-05-25:

- Still valid: runtime evidence enters as candidate-only packet validation.
- Changed: `aoa_evals` may expose runtime freshness/status and schema-backed
  packet validation.
- Changed: `aoa_evals` may read stack-owned private candidate export metadata
  and details from `abyss-stack/Logs/eval-exports/`.
- Superseded by: none.

## Review Log

### 2026-05-25 - Initial ingestion-status layer

- Previous assumption: `aoa_evals` only selected, inspected, expanded, and
  prepared report skeletons.
- New reality: OS Abyss needs a safe way to preflight runtime evidence packets
  and mirror freshness before bundle-local review.
- Extension: OS Abyss also needs to see existing governed-execution runtime
  candidate exports as candidate records, not only validate caller-provided
  packets.
- Reason: ingestion without a read-only gate would either flood context or
  tempt MCP to become proof authority.
- Source surfaces updated:
  - `docs/architecture/AOA_EVALS_MCP_CONTRACT.md`
  - `docs/decisions/0111-runtime-evidence-ingestion-and-mirror-status.md`
- Validation: decision metadata indexes, repo validation, generated-reader
  checks, runtime-candidate reader checks, and stack service contract tests.

## Boundaries

Future agents must not infer that candidate validation accepts evidence or that
mirror freshness makes mirror output proof authority.

Future agents must not infer that MCP may write runtime evidence into
`aoa-evals`, create or accept review queue entries, compute verdicts, publish
receipts, promote bundles, or edit the approved mirror by hand.

## Validation

This decision is valid only when:

- `docs/architecture/AOA_EVALS_MCP_CONTRACT.md` names the status and validation
  stop-lines;
- generated decision indexes include this note;
- `aoa-evals` repo validation and runtime-candidate reader checks pass;
- the stack-owned MCP service verifies candidate validation and status behavior.
- the stack-owned MCP service verifies runtime candidate export listing/reading
  stays read-only and candidate-only.
