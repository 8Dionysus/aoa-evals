# Eval Birth Protocol

## Role

This protocol defines the route-first path from proof pressure to eval
authoring.

It does not make every proof question a new eval bundle. It decides whether the
pressure routes to an existing bundle, candidate evidence, a quest record, or a
new draft source proof object.

## Operating Card

| Field | Route |
| --- | --- |
| role | route-first eval authoring protocol |
| input | bounded proof pressure, runtime or trace cue, repeated blind spot, missing proof surface, or proposal packet |
| output | existing bundle route, candidate evidence route, quest route, forge design worksheet, or explicit new draft scaffold |
| owner | this part owns authoring support; `evals/**/EVAL.md` and `eval.yaml` own source proof meaning |
| next route | `EVAL_SELECTION.md`, `EVAL_INDEX.md`, generated catalog, audit candidate packets, `QUESTBOOK.md`, or source eval bundle |
| validation | parent `mechanics/proof-object/parts/AGENTS.md#validation` |

## Route Ladder

```text
proof pressure
-> search existing eval catalog and chooser/index surfaces
-> if runtime or trace evidence: selected evidence packet or candidate reader
-> if repeated but not authoring-ready: quest source record
-> if new draft is still plausible: prepare eval_need_v1 case kit
-> if candidate pressure is concrete: Eval Forge archetype route and worksheet
-> if new draft is still warranted: reviewed eval_need_v1 packet
-> scaffold EVAL.md + eval.yaml + minimum support artifacts
-> validate source bundle and generated-reader parity
-> bundle-local review before reports, receipts, or promotion
```

## Reuse Gates

Before creating a draft bundle, the authoring route checks:

- existing generated catalog entries;
- explicit `related_eval_refs` in the proposal packet;
- category, claim type, baseline mode, report format, object, and proof-question
  token overlap;
- public chooser and index posture when a starter route is involved;
- quest and audit routes when the input is not yet a source proof object.

A match does not prove that the existing eval applies. It only means the next
honest route is to inspect that source bundle before authoring a parallel one.

## Eval Need Packet

`eval_need_v1` is the pre-authoring packet for route-first eval growth. It
records:

- the proof question and origin need;
- the object under evaluation;
- proposed category, claim type, baseline mode, and report format;
- existing related evals, candidate evidence refs, quest refs, and source refs;
- expected use boundary and blind spots;
- the requested authoring route.

The packet is not a verdict, not proof acceptance, and not a source bundle.

## Eval Forge Router

`scripts/eval_forge_route.py` is the design router between raw pressure and
source authoring. It may:

- load the Eval Forge archetype registry;
- normalize a candidate packet, local eval-port pressure item, proposal, or
  manual case fields;
- reject keyword-only or ownerless cases before they become system noise;
- choose an archetype such as trajectory, tool correctness, local intake,
  skill trigger, runtime smoke, rubric, or central draft;
- emit an `eval_design_worksheet_v1` payload;
- write only that worksheet when `--write-worksheet` is explicitly passed.

It must not create source bundles, accept proof, score evidence, mint baselines,
promote candidates, or mutate repo-local ports. Its output is design guidance
until an owner accepts the next route.

## Case Preparation Helper

`scripts/prepare_eval_case.py` is the fast collection helper for a fresh case.
It may:

- build an `eval_need_v1` proposal from command-line fields;
- validate an existing proposal file;
- run the same existing-route check used by the scaffold helper;
- include the Eval Forge route and selected archetype for the proposal;
- emit the next scaffold commands;
- write only the proposal JSON when `--write-proposal` is passed.

It must not create `evals/**` bundle files. Bundle creation stays with
`scripts/scaffold_eval_bundle.py`, and only after existing-match review and
explicit human acceptance of the draft route.

## Scaffold Helper

`scripts/scaffold_eval_bundle.py` is an authoring helper. It may:

- validate an `eval_need_v1` packet;
- return likely existing eval routes;
- produce a dry-run scaffold plan;
- write a draft bundle only when both `--allow-new` and `--write` are present.

It writes only source eval bundle starter files. Every draft gets:

- `EVAL.md`;
- `eval.yaml`;
- `notes/origin-need.md`;
- `checks/eval-integrity-check.md`.

For `comparative-summary` drafts with a non-`none` `baseline_mode`, the helper
also materializes the minimum comparison contract surface required by repo
validation:

- `evals/<claim-family>/<eval-name>/notes/comparison-contract.md`;
- `evals/<claim-family>/<eval-name>/notes/baseline-readiness.md`;
- `evals/<claim-family>/<eval-name>/fixtures/contract.json`;
- `evals/<claim-family>/<eval-name>/runners/contract.json`;
- `evals/<claim-family>/<eval-name>/reports/summary.schema.json`;
- `evals/<claim-family>/<eval-name>/reports/example-report.json`.

It does not add the bundle to `EVAL_INDEX.md`, `EVAL_SELECTION.md`, reports,
receipts, or generated readers. Those routes require separate review and
validation.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| proof pressure fits an existing eval | inspect the existing source bundle before authoring |
| runtime evidence looks ready | keep it candidate-only through audit packets and bundle-local review |
| repeated pressure is still vague | capture or update a quest record |
| candidate pressure needs eval design | run Eval Forge and keep the worksheet non-proof until owner review |
| proposal requests a starter bundle | require separate public starter review and chooser/index update |
| scaffold output reads as accepted proof | return to bundle-local review and validation |
| MCP wants to create a source bundle | MCP may return proposal context only; source mutation stays in repo-local authoring |

## Validation

Use the part validation lane:

```bash
python -m pytest -q mechanics/proof-object/parts/eval-authoring/tests
python scripts/validate_repo.py
python scripts/build_catalog.py --check
python scripts/validate_semantic_agents.py
```
