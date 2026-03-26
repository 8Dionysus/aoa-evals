# Spark lane for aoa-evals

This file only governs work started from `Spark/`.

The root `AGENTS.md` remains authoritative for repository identity, ownership boundaries, reading order, and validation commands. This local file only narrows how GPT-5.3-Codex-Spark should behave when used as the fast-loop lane.

If `SWARM.md` exists in this directory, treat it as queue / swarm context. This `AGENTS.md` is the operating policy for Spark work.

## Default Spark posture

- Use Spark for short-loop work where a small diff is enough.
- Start with a map: task, files, risks, and validation path.
- Prefer one bounded patch per loop.
- Read the nearest source docs before editing.
- Use the narrowest relevant validation already documented by the repo.
- Report exactly what was and was not checked.
- Escalate instead of widening into a broad architectural rewrite.

## Spark is strongest here for

- focused bundle wording updates
- scorer or fixture cleanup with local scope
- report, index, and selection-surface clarity work
- targeted regression-surface improvements
- metadata and generated-catalog alignment

## Do not widen Spark here into

- scoring-philosophy overhaul
- broad verdict-logic rewrites across many bundles
- runner, fixture, and report migration all at once
- polished wording that makes the claim stronger than the evidence

## Local done signal

A Spark task is done here when:

- the bounded claim is clearer
- verdict boundaries and caveats remain explicit
- dependencies are still visible
- generated surfaces are aligned when touched
- the documented validation path ran or the missing checks were reported

## Local note

Spark should behave like a proof-surface auditor here: narrow the claim, tighten the language, expose the limits.

## Reporting contract

Always report:

- the restated task and touched scope
- which files or surfaces changed
- whether the change was semantic, structural, or clarity-only
- what validation actually ran
- what still needs a slower model or human review
