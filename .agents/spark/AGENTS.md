# AGENTS.md

## Applies to

`.agents/spark/` and bounded Spark lane work in `aoa-evals`.

## Role

This lane is the maintained fast-loop route for narrow proof-surface changes.
It helps Spark-sized work stay scoped to one bounded claim, one eval seam, or
one small route/validation repair.

Root `AGENTS.md` remains authoritative for repository identity, ownership
boundaries, reading order, and validation commands. This card only narrows how
GPT-5.3-Codex-Spark should behave when used as the fast-loop lane.

If `SWARM.md` exists in this directory, treat it as queue or swarm context.
This `AGENTS.md` is the operating policy for Spark work.

## Operating Card

| Field | Route |
| --- | --- |
| role | fast-loop agent lane for small proof-surface changes |
| input | one bounded claim, one eval seam, or one route/validation repair |
| output | done bounded patch or handoff to a slower owner route |
| owner | `.agents/spark/AGENTS.md` for lane posture; proof meaning stays with the target source surface |
| next route | target bundle, mechanic package, generated route, or root `AGENTS.md` |
| tools | root validation, semantic AGENTS validation, nested AGENTS validation, catalog check when generated readers move |
| validation | this card's `Validation` section |

## Read before editing

1. root `AGENTS.md`
2. `DESIGN.AGENTS.md`
3. `.agents/AGENTS.md`
4. `docs/architecture/PROOF_TOPOLOGY.md`
5. `docs/architecture/LEGACY_NAMING.md`
6. the target proof source surface or mechanic package

## Default posture

- Use Spark for short-loop work where a small diff is enough.
- Start with a map: task, files, risks, and validation path.
- Prefer one bounded patch per loop.
- Read the nearest source docs before editing.
- Use the narrowest relevant validation already documented by the repo.
- Report exactly what was and was not checked.
- Escalate instead of widening into a broad architectural rewrite.

## Strongest fit

- focused bundle wording updates
- scorer or fixture cleanup with local scope
- report, index, and selection-surface clarity work
- targeted regression-surface improvements
- metadata and generated-catalog alignment

## Route Boundaries

| Pressure | Route |
| --- | --- |
| scoring-philosophy overhaul | slower root/design or comparison-spine route |
| verdict logic across many bundles | proof-object route plus bundle-local review |
| runner, fixture, and report migration together | proof-infra and owning mechanic part route |
| wording that changes evidence strength | bundle-local `EVAL.md` and `eval.yaml` review |
| proof authority question | Bundle-local `EVAL.md` and `eval.yaml` |
| generated reader change | `generated/AGENTS.md` and the owning builder |

## Validation

Use the narrowest relevant validation already documented by the target surface.
For lane or route edits, run:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
python scripts/validate_nested_agents.py
```

If generated catalogs are touched, run:

```bash
python scripts/build_catalog.py --check
```

## Done signal

A Spark task is done here when:

- the bounded claim is clearer
- verdict boundaries and caveats remain explicit
- dependencies are still visible
- generated surfaces are aligned when touched
- the documented validation path ran or the missing checks were reported

## Local note

Spark should behave like a proof-surface auditor here: narrow the claim, tighten the language, expose the limits.

## Closeout

Always report:

- the restated task and touched scope
- which files or surfaces changed
- whether the change was semantic, structural, or clarity-only
- what validation actually ran
- what still needs a slower model or human review
