# aoa-memo Writeback Decision Quality Eval

- Decision ID: AOA-EV-D-0113
- Status: Accepted
- Date: 2026-05-26
- Owner surface: `evals/workflow/aoa-memo-writeback-decision-quality/`

## Index Metadata

- Original date: 2026-05-26
- Surface classes: proof topology, generated/readout, boundary/runtime/sibling
- Mechanic parents: proof-infra
- Guard families: part and payload, generated/report/receipt/runtime, sibling and boundary
- Posture: active rationale

## Context

The workspace memory route now asks agents to run `aoa-memo-writeback` after
meaningful landings. That created a proof pressure inside `aoa-evals`: reviewers
need a bounded way to ask whether a writeback decision was well made before a
candidate, export, route-only debt note, or no-writeback stop line is trusted.

Existing neighboring bundles are narrower. `aoa-memo-writeback-act-integrity`
checks a confirmed writeback act after adoption. `aoa-memo-write-path-guardrails`
belongs to memo-side write safety and promotion posture. Neither directly checks
whether the initial `aoa-memo-writeback` judgment searched enough evidence,
chose the right outcome, rejected noise, preserved owner boundaries, and kept
private session material out of public packets.

## Options Considered

- Extend `aoa-memo-writeback-act-integrity` to also judge decision quality
  before a writeback act exists.
- Route the whole concern to `aoa-memo` as a memory-quality harness topic.
- Add a separate draft workflow eval for `aoa-memo-writeback` decision quality
  in `aoa-evals`, with explicit boundaries around memory truth and durable
  landing.

## Decision

Add `aoa-memo-writeback-decision-quality` as a draft workflow eval under
`evals/workflow/`.

The eval checks one `aoa-memo-writeback` application for invocation fit, owner
route clarity, evidence search coverage, memory-worthiness filtering, outcome
selection, missed-evidence disclosure, and privacy posture. It uses
bundle-local fixture, runner, report schema, example report, support notes, and
generated readers.

This decision also serves as the route-only writeback marker for this
`aoa-evals` landing. `aoa-evals` does not currently write a local memo packet
for this repository; the reviewed memory owner remains `aoa-memo`.

## Rationale

A separate draft eval keeps the proof question narrow. It lets `aoa-evals`
evaluate the quality of the memory-writeback judgment without claiming that the
memo content is true, that durable reviewed memory is approved, or that local
memo-port schemas are safe after a packet is written.

Routing the whole concern to `aoa-memo` would blur proof authority with memory
authority. Expanding the writeback-act bundle would also blur stages: a
pre-write decision review is not the same proof object as a confirmed
writeback-act integrity review.

## Consequences

- Positive: agents and reviewers get a bounded proof surface for the judgment
  step that precedes candidate/export/debt/stop-line output.
- Positive: `aoa-evals` keeps proof authority local while pointing memory truth
  and durable landing back to `aoa-memo`.
- Positive: the workspace writeback debt readout can treat this decision as the
  current route-only marker for the `aoa-evals` landing.
- Tradeoff: the bundle is draft and supports only decision-quality review, not
  final memo correctness or durable memory acceptance.
- Follow-up: stronger memory-quality evals can later cover recall precision,
  stale-memory behavior, contradiction handling, permission leakage, and
  hallucinated merges through their own bounded bundles or memo-owned harnesses.

## Current Applicability

As of 2026-05-26:

- Still valid: source proof meaning lives in
  `evals/workflow/aoa-memo-writeback-decision-quality/EVAL.md` and
  `eval.yaml`.
- Changed: `aoa-evals` now has a bounded proof route for memory writeback
  decision quality, separate from writeback-act integrity.
- Superseded by: none.

## Review Log

### 2026-05-26 - Initial landing

- Previous assumption: the remaining closeout/writeback proof pressure was
  tracked mainly as ingress and neighboring writeback-act proof.
- New reality: the system also needs a pre-write decision-quality eval for
  `aoa-memo-writeback` applications.
- Reason: workspace memory writeback is becoming an operational route, so its
  judgment step needs bounded proof before agents trust candidate/export/debt
  outcomes.
- Source surfaces updated:
  `evals/workflow/aoa-memo-writeback-decision-quality/`,
  `mechanics/proof-infra/parts/fixture-families/fixtures/memo-writeback-decision-quality-v1/`,
  generated eval readers, and `Repo Validation` sibling pin for the current
  `aoa-agents` continuity-lane source path.
- Validation: `python scripts/validate_repo.py`,
  `python scripts/build_catalog.py --check`,
  `python scripts/generate_eval_report_index.py --check`,
  `python scripts/validate_semantic_agents.py`, and `python -m pytest -q`.

## Boundaries

This decision does not make `aoa-evals` the owner of memory truth.

It does not approve durable reviewed memory landing, local candidate promotion,
or direct writes into `aoa-memo`.

It does not evaluate general recall precision, stale-memory behavior,
contradiction handling, permission leakage, or hallucinated merge behavior.

It does not convert `.aoa` raw session evidence into reviewed memory.

## Validation

- The source eval bundle is indexed by generated eval readers.
- The proof-infra fixture-family route names the new fixture family.
- The validator and tests accept the bounded bundle and generated surfaces.
- `Repo Validation` passed on PR #350 after the sibling checkout pin matched the
  evidence reference used by the runtime integrity review example.
