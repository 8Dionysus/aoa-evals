# Route-First Eval Birth Protocol

- Decision ID: AOA-EV-D-0112
- Status: Accepted
- Date: 2026-05-25
- Owner surface: `mechanics/proof-object/parts/eval-authoring/`

## Index Metadata

- Original date: 2026-05-25
- Surface classes: mechanic part, validation guard, quest/lane, generated/readout
- Mechanic parents: proof-object, audit, proof-loop, questbook, cross-parent
- Guard families: part and payload, generated/report/receipt/runtime, decision index/read-model
- Posture: active rationale

## Context

`aoa-evals` already has source eval bundles, generated catalogs, chooser
surfaces, audit candidate readers, quest records, proof-loop routes, and
proof-object authoring templates. The new pressure is to let OS Abyss grow evals
quickly from runtime work without creating duplicate proof surfaces.

The risky route would be to treat every missing proof question as a new bundle.
That would bypass existing evals, candidate-evidence routes, and quest records,
and it would make authoring convenient at the cost of proof-organ clarity.

## Options Considered

- Add a new top-level `eval birth` mechanic: visible, but it duplicates
  proof-object, audit, questbook, and proof-loop responsibilities.
- Let MCP create source bundles: convenient for OS Abyss, but it moves source
  mutation into a runtime access plane.
- Extend `proof-object/parts/eval-authoring` with a route-first protocol,
  proposal schema, example packet, scaffold helper, and focused tests.

## Decision

Choose the third option.

Eval growth starts with a route-first `eval_need_v1` packet and a duplicate-fit
pass over existing catalog routes. The scaffold helper may create a draft source
bundle only after existing evals, candidate evidence, and quest routes are
considered, and only when the operator explicitly allows a new draft.

The active authoring support lives under
`mechanics/proof-object/parts/eval-authoring/`. Source eval meaning remains in
`evals/**/EVAL.md` and `eval.yaml`.

## Rationale

This preserves the proof organ's convex shape. `proof-object` remains the owner
for source proof-object authoring; `audit` remains the owner for runtime
candidate evidence; `questbook` remains the owner for deferred proof pressure;
`proof-loop` remains the owner for review and report routing.

The helper makes the desired action concrete: first search, then route, then
scaffold only when warranted. That gives OS Abyss a fast eval-growth path
without turning MCP, runtime exports, generated readers, or proposal packets
into proof authority.

## Consequences

- Positive: future eval authoring has a reusable route-first packet and helper.
- Positive: duplicate eval pressure is visible before scaffold creation.
- Positive: runtime and trace inputs route through candidate evidence before
  bundle-local proof review.
- Tradeoff: authoring now has a small extra preflight step.
- Tradeoff: the duplicate-fit check is heuristic and must not be treated as a
  final applicability verdict.
- Follow-up fulfilled: MCP may return read-only proposal context, but source
  mutation remains repo-local unless a future decision changes that boundary.

## Current Applicability

As of 2026-05-25:

- Still valid: source bundle meaning stays in `evals/**/EVAL.md` and
  `eval.yaml`.
- Changed: eval authoring now has an explicit `eval_need_v1` route and scaffold
  helper before new draft bundle creation.
- Changed: the MCP access plane may now expose read-only find-or-propose
  context that routes into this protocol without writing source files.
- Changed: comparative-summary drafts with a non-`none` baseline mode now scaffold
  their minimum comparison notes, fixture contract, runner contract, report
  schema, and example report in the first draft plan.
- Superseded by: none.

## Review Log

### 2026-05-25 - Initial route-first authoring support

- Previous assumption: the authoring template was enough to start a new eval
  bundle once proof pressure appeared.
- New reality: OS Abyss needs a faster route that still checks existing evals,
  candidate evidence, and quest pressure before new bundle creation.
- Reason: route-first authoring prevents parallel proof surfaces and keeps MCP
  read-only.
- Source surfaces updated:
  - `mechanics/proof-object/PARTS.md`
  - `mechanics/proof-object/parts/AGENTS.md`
  - `mechanics/proof-object/parts/eval-authoring/README.md`
  - `mechanics/proof-object/parts/eval-authoring/docs/EVAL_BIRTH_PROTOCOL.md`
  - `mechanics/proof-object/parts/eval-authoring/schemas/eval-need.schema.json`
  - `mechanics/proof-object/parts/eval-authoring/examples/eval_need.example.json`
  - `mechanics/proof-object/parts/eval-authoring/scripts/scaffold_eval_bundle.py`
  - `mechanics/proof-object/parts/eval-authoring/tests/test_scaffold_eval_bundle.py`
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

### 2026-05-25 - Read-only MCP proposal context

- Previous assumption: MCP would stop at selection, inspection, candidate
  evidence validation, runtime export reading, and report skeletons.
- New reality: OS Abyss needs one callable route that starts from a proof
  question and returns either existing eval routes or a candidate
  `eval_need_v1` proposal context.
- Reason: eval growth should be easy from any OS surface without letting the
  runtime service create source bundles.
- Source surfaces updated:
  - `docs/architecture/AOA_EVALS_MCP_CONTRACT.md`
  - `abyss-stack:mcp/services/aoa-evals-mcp/`
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

### 2026-05-25 - Validator-ready comparative scaffolds

- Previous assumption: every new draft could start from the same four-file
  scaffold and fill comparison contracts later.
- New reality: fixed-baseline and other comparative-summary drafts are not
  authoring-ready unless their support note, baseline-readiness note, fixture
  contract, runner contract, report schema, and example report exist from the
  first scaffold plan.
- Reason: OS Abyss runtime pressure should be able to become a reviewable eval
  draft without making the next agent rediscover the validator contract by
  trial and error.
- Source surfaces updated:
  - `mechanics/proof-object/parts/eval-authoring/docs/EVAL_BIRTH_PROTOCOL.md`
  - `mechanics/proof-object/parts/eval-authoring/scripts/scaffold_eval_bundle.py`
  - `mechanics/proof-object/parts/eval-authoring/tests/test_scaffold_eval_bundle.py`
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

## Boundaries

Future agents must not infer that `eval_need_v1` is proof, acceptance,
promotion, or starter-bundle approval.

Future agents must not infer that a duplicate-fit match proves applicability.
It only routes the reviewer to inspect the existing source eval before creating
another one.

Future agents must not infer that MCP may mutate source bundles. MCP may expose
selection, inspection, candidate validation, and proposal context only under
the current access-plane contract.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
