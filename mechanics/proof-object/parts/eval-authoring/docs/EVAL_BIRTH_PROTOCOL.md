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
| output | existing bundle route, candidate evidence route, quest route, or explicit new draft scaffold |
| owner | this part owns authoring support; `evals/**/EVAL.md` and `eval.yaml` own source proof meaning |
| next route | `EVAL_SELECTION.md`, `EVAL_INDEX.md`, generated catalog, audit candidate packets, `QUESTBOOK.md`, or source eval bundle |
| validation | parent `mechanics/proof-object/parts/AGENTS.md#validation` |

## Route Ladder

```text
proof pressure
-> search existing eval catalog and chooser/index surfaces
-> if runtime or trace evidence: selected evidence packet or candidate reader
-> if repeated but not authoring-ready: quest source record
-> if new draft is still warranted: eval_need_v1 packet
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

## Scaffold Helper

`scripts/scaffold_eval_bundle.py` is an authoring helper. It may:

- validate an `eval_need_v1` packet;
- return likely existing eval routes;
- produce a dry-run scaffold plan;
- write a draft bundle only when both `--allow-new` and `--write` are present.

It writes only source eval bundle starter files:

- `EVAL.md`;
- `eval.yaml`;
- `notes/origin-need.md`;
- `checks/eval-integrity-check.md`.

It does not add the bundle to `EVAL_INDEX.md`, `EVAL_SELECTION.md`, reports,
receipts, or generated readers. Those routes require separate review and
validation.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| proof pressure fits an existing eval | inspect the existing source bundle before authoring |
| runtime evidence looks ready | keep it candidate-only through audit packets and bundle-local review |
| repeated pressure is still vague | capture or update a quest record |
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
