# Local Eval Port Standard

- Decision ID: AOA-EV-D-0240
- Status: Accepted
- Date: 2026-06-11
- Owner surface: `docs/guides/LOCAL_EVAL_PORT_STANDARD.md`

## Index Metadata

- Original date: 2026-06-11
- Surface classes: proof topology, validation guard, sibling reference
- Mechanic parents: proof-object
- Guard families: source/topology, sibling-reference, validation
- Posture: active rationale

## Context

AoA sibling repositories now produce repo-local eval pressure while their owner
surfaces are being edited: memory guardrails in `aoa-memo`, routing eval cases
in `aoa-routing`, derived proof expectations in `aoa-kag`, role and handoff
posture in `aoa-agents`, movement summaries in `aoa-stats`, and typed
control-plane helpers in `aoa-sdk`.

Before this decision, that pressure had two bad routes: jump immediately into
`aoa-evals`, losing the local owner context, or leave ad hoc notes in each
sibling repo with no validator-backed proof boundary.

## Options Considered

- Put every local proof pressure packet directly in `aoa-evals`.
- Give every sibling repo a full local copy of the `aoa-evals` source bundle
  district.
- Add a small sibling-local `evals/` port standard owned by `aoa-evals`, with
  local owner evidence below central proof authority.

## Decision

Use a local `evals/` port in first-wave sibling repositories.

`aoa-evals` owns the shared standard and validator. Sibling repositories own
their local cases, fixtures, intake, suites, reports, and evidence shape.
Central verdict, scoring, regression, and proof-doctrine authority remains in
`aoa-evals`.

The pre-bundle layer is named `intake/`. It accepts `eval_need_v1` packets and
other route-first pressure without implying that every packet is a candidate
for central adoption.

## Rationale

This keeps proof topology convex across the workspace. Local ports preserve the
evidence where it is born, while `aoa-evals` keeps the bounded proof vocabulary,
portable source-bundle format, validator route, and future adoption decision.

The `intake/` name is intentionally weaker than `candidates/`: the input may be
a trace failure, blind spot, suite need, local fixture family, existing eval
route, selected evidence packet, quest pressure, or draft bundle request.

## Consequences

- Positive: agents can create local eval pressure without leaving the repo they
  are working in.
- Positive: `aoa-evals` gets one deterministic validator for local port shape.
- Tradeoff: first-wave skeleton ports add a visible but intentionally thin root
  district in several repositories.
- Follow-up: future waves may add `aoa-skills`, `aoa-techniques`,
  `aoa-playbooks`, `Agents-of-Abyss`, `Tree-of-Sophia`, and runtime surfaces
  after the first-wave validator proves stable.

## Current Applicability

As of 2026-06-11:

- Still valid: local ports preserve repo-local eval pressure below central
  proof authority.
- Changed: none.
- Superseded by: none.

## Boundaries

Future agents must not infer that a sibling-local `evals/` port owns proof
doctrine, final verdicts, scoring, regression truth, or central starter-bundle
promotion.

Future agents must not infer that a skeleton port carries active eval coverage.

Future agents must not infer that `eval_need_v1` intake is proof acceptance.

## Validation

This decision is valid when:

- `docs/guides/LOCAL_EVAL_PORT_STANDARD.md` names the local-vs-central owner
  split;
- `scripts/validate_local_eval_port.py` validates first-wave local ports;
- `aoa-memo` carries the first active local port;
- skeleton first-wave ports declare `status: skeleton` without fake bundles;
- generated decision indexes include this note.
