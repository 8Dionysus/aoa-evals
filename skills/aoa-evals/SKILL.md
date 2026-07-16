---
name: aoa-evals
description: Select, review, or evolve bounded proof through the `aoa-evals` owner boundary. Use for central eval-bundle choice, claim or verdict interpretation, report and evidence review, comparison or maturity pressure, Eval Forge owner review, proof-canon admission or retirement, and drift between source bundles and generated readers. Do not use for ordinary tests, running an already selected repo-local eval, generic analytics, or treating readiness, candidate, receipt, MCP, or generated output as proof.
---

# aoa-evals

## Intent

Provide one owner-local front door for bounded proof work without turning an
eval catalog, green command, report, receipt, readiness check, candidate, or
access plane into stronger proof than its source bundle and evidence allow.
Select exactly one internal mode: `select`, `review`, or `evolve`.

## Contract

| Field | Value |
| --- | --- |
| identity | `aoa-evals` owner bundle |
| owner | `aoa-evals` repository |
| version / lifecycle | `0.1.0` / `admitted` |
| provenance | owner admission `AOA-EV-D-0247`; canonical source `skills/aoa-evals`; repo projection declared by `skills/port.manifest.json` |
| trust | source eval bundles and admitted evidence own bounded proof meaning; later read models remain weaker |
| freedom | read-only in `select` and `review`; source mutation only with explicit owner authority in `evolve` |
| tool requirements | no fixed tool or technique dependency; use only the owner sources, builders, and access planes required by the selected task |
| effects | no effects in `select` or `review`; `evolve` may change owner source and declared projections after its gates pass |
| composition | consumes owner needs, local eval ports, candidate packets, source bundles, evidence, reports, receipts, and runtime observations as typed task-local DAG nodes |
| relations | see `Typed Relations`; relations route composition and handoff but do not transfer proof authority |
| conflicts | green-as-proof, readiness-as-verdict, candidate-as-bundle, report-as-source, generated-as-authority, implicit maturity promotion |
| health | rerun manual trigger, negative, held-out, coexistence, and bounded-effect trials after a material model, workflow, or bundle change |
| termination | one exact/partial/no-fit selection, bounded review disposition, owner-authorized source change, no-change result, handoff, or blocker |

## Applicability

Use this bundle when the task materially depends on one or more of:

- selecting a central `aoa-evals` proof bundle for a bounded claim, comparison,
  regression, artifact, trajectory, boundary, stress, or repeated-window need;
- interpreting an eval's claim, maturity, baseline, evidence, scorer, verdict,
  report, blind spots, portability, or public reading;
- reviewing local-port or session-derived pressure after its origin owner has
  routed it toward central proof review;
- reviewing Eval Forge output, central bundle admission, maturity change,
  comparison posture, supersession, retirement, or public chooser impact;
- diagnosing drift between source `EVAL.md` / `eval.yaml`, support evidence,
  reports, generated readers, receipts, MCP, KAG, or consumers.

Do not use it for ordinary unit or contract tests, merely running an exact
repo-local suite, generic data analysis, raw session retrieval, owner metric
definition, workflow execution, routing or role policy, or a request whose
only need is to run an already named validator.

For cross-repository eval selection, exact local application, or owner-local
no-fit proposal, compose with shared `aoa-eval` when it is available. Begin
this owner bundle only when the question reaches central proof meaning or an
`aoa-evals` owner decision.

No technique package is a prerequisite for invoking this skill. If a selected
eval cites a technique, treat that reference as bundle-local lineage or support
whose relevance must be inspected, not as procedural baggage inherited by this
owner bundle.

## Typed Relations

- `primary-capability-parent`: the `aoa-evals` bounded-proof owner capability,
  not another advertised skill;
- `consumes`: origin needs, selected evidence, local-port candidates, source
  eval bundles, execution support, reviewed reports, and weaker read models;
- `produces`: one bounded selection, review, evolution, no-change, or handoff
  disposition using the output ABI below;
- `composes-with`: shared `aoa-eval` for cross-repo selection and local apply,
  `aoa-decision` for durable rationale, and session-memory routing only for
  locating candidate evidence;
- `hands-off-to`: the origin owner, `aoa-skills`, `aoa-memo`, `aoa-stats`,
  `abyss-stack`, or another stronger owner named by the inspected object;
- `conflicts-with`: any route that lets a candidate, readiness surface,
  receipt, report, generated reader, MCP result, or green command outrank its
  source proof and admitted evidence.

Within the bundle, `select` may produce the source contract consumed by
`review`; an accepted `review` disposition may become an input to `evolve`.
These edges are assembled only when the task needs them, never as a mandatory
three-stage workflow.

## Inputs

- exactly one intent: select, review, or evolve;
- one bounded proof question, object under evaluation, candidate, source
  bundle, report, failure, or desired owner change;
- origin and stronger owner, source/evidence refs, time and environment posture;
- comparison or baseline semantics when relevant;
- explicit effect authority and required human confirmation for mutation.

## Output ABI

Every result states:

- selected mode and bounded proof question;
- object under evaluation, claim class, origin owner, and proof owner;
- strongest source bundle and evidence refs used, plus weaker surfaces inspected;
- fit, evidence, freshness, environment, baseline, lifecycle, maturity,
  uncertainty, and blind-spot posture relevant to the question;
- one disposition: `not_applicable`, `exact_fit`, `partial_fit`, `no_fit`,
  `candidate_only`, `supported_bounded`, `insufficient_evidence`, `defer`,
  `owner_handoff`, `no_change`, `blocked`, or `verified_bounded`;
- effect performed, verification, skipped checks, next owner route, claim
  limit, and exact stop line.

## Procedure

### 1. Select exactly one mode

| Mode | Select when | Primary output |
| --- | --- | --- |
| `select` | A bounded proof need has no exact central source bundle selected. | Exact, partial, or no-fit route with rejected neighbors. |
| `review` | A bundle, evidence packet, report, verdict, readiness surface, comparison, or maturity pressure must be interpreted. | Source-backed review disposition with explicit proof ceiling. |
| `evolve` | Accepted owner review requires a central bundle, lifecycle, comparison, chooser, or source-contract change. | Smallest source-first change or explicit no-change/blocker. |

Keep the modes internal until held-out work proves that separate advertised
skills add independent trigger, ABI, composition, and outcome value.

### 2. Build the smallest typed proof DAG

Use only the nodes needed from this chain:

```text
origin owner need or captured evidence
  -> local eval port / candidate packet / selected runtime evidence
  -> Eval Forge routing or owner review
  -> source EVAL.md + eval.yaml + admitted support evidence
  -> fixture / runner / scorer / report contract
  -> reviewed report or bounded verdict
  -> generated catalog / chooser / receipt
  -> MCP / KAG / downstream consumer
```

Classify each node as owner need, candidate evidence, routing worksheet, source
proof contract, execution support, reviewed result, deterministic projection,
runtime observation, or consumer view. A later node cannot repair or
strengthen an earlier one. Stop as soon as the selected disposition and output
ABI are directly supported.

### Mode: select

1. Restate the exact proof question, object, claim class, evidence posture,
   comparison need, and acceptance target.
2. Use `EVAL_SELECTION.md` for the first bounded choice, then inspect the
   selected bundle's `EVAL.md` and `eval.yaml`. Use generated catalogs only to
   navigate back to source.
3. Compare the nearest alternatives by object under evaluation, claim,
   maturity, baseline mode, inputs, execution/report contract, blind spots,
   owner, and proof limit. Reject tempting neighbors explicitly.
4. Return `exact_fit`, `partial_fit`, or `no_fit`. Do not execute, scaffold, or
   alter maturity during selection.

### Mode: review

1. Read source bundle meaning before a report, dashboard, receipt, MCP result,
   KAG node, or generated reader.
2. Inspect every material evidence ref and the actual report or artifact when
   the request names one. Preserve repository revision, model/host/tools,
   environment, fixture, baseline, accepted exits, scorer, and review posture.
3. Distinguish source-contract readiness, execution success, evidence
   acceptance, report validity, bounded verdict, public maturity, and central
   proof admission. None implies the next.
4. For maturity or comparison pressure, use the owner review guide and require
   the bundle-local evidence kind and explicit human confirmation named by the
   root owner law. A green integrity sidecar cannot promote its neighbor.
5. Return the narrowest supported disposition and claim limit. Do not mutate a
   source bundle, chooser, status, baseline, or generated reader in this mode.

### Mode: evolve

1. Require a stable bounded need, duplicate/no-fit or review record, resolved
   owner, acceptance criteria, explicit effect authority, and any human
   confirmation required by root `AGENTS.md`. Otherwise stop.
2. Decide the owner before the artifact:
   - local pressure, suites, fixtures, and reports stay in the origin repo port;
   - candidate packets and Eval Forge worksheets remain non-proof;
   - reusable central proof meaning belongs in a source eval bundle;
   - repeatable proof operations belong to their mechanic;
   - generated readers, receipts, MCP, and KAG remain derived or access layers.
3. Compare reuse, extension, new bundle, maturity change, supersession,
   retirement, and no-change. Prefer an existing narrower surface when it
   answers the bounded question.
4. Exercise the motivating case, strongest negative, nearest competing bundle,
   evidence-gap case, and intended consumer manually. Add permanent automation
   only for a stable long-lived invariant exposed by those trials.
5. If authorized, change source before generated companions, rebuild only its
   declared projections, inspect the actual bundle and outputs, and state what
   green checks cannot prove. Otherwise return an owner-ready bounded proposal.

## Failure Modes and Stops

- `not_applicable`: the task is an ordinary test, local apply, workflow,
  analytics, route, role, runtime, or raw-session question.
- `candidate_only`: useful pressure exists but source proof review has not
  admitted it.
- `insufficient_evidence`: the claim outruns its sources, environment, cases,
  scorer, report, or review trail.
- `defer`: maturity, comparison, or publication pressure lacks one named gate.
- `owner_handoff`: the strongest next decision belongs to the origin owner,
  local eval port, `aoa-skills`, runtime, stats, memo, or another proof owner.
- `no_change`: an existing bundle or route already handles the need.
- `blocked`: ownership, evidence, acceptance, confirmation, or effect authority
  is missing.
- `verified_bounded`: the selected result or owner-authorized source change
  satisfies its stated criteria without widening the claim.

## Manual Verification

- trace each material claim to the strongest source bundle and evidence ref;
- inspect the named report, packet, or artifact rather than trusting a catalog
  row or exit code;
- for selection, reject the nearest plausible alternative;
- for review, replay the strongest overread or evidence-gap case;
- for evolution, replay the motivating, negative, collision, and consumer cases;
- report skipped live, cross-owner, model, host, security, and portability work;
- keep raw trials, task-local DAGs, temporary rubrics, and session notes out of
  the owner skill home.
