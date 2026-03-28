---
name: aoa-long-horizon-depth
category: workflow
status: draft
summary: Checks whether a checkpoint-based long-horizon inquiry can relaunch with its axis, contradictions, and canon-vs-memory boundaries still legible.
object_under_evaluation: restart fidelity of checkpoint-based long-horizon inquiry routes
claim_type: bounded
baseline_mode: none
report_format: summary-with-breakdown
technique_dependencies: []
skill_dependencies: []
---

# aoa-long-horizon-depth

## Intent

Use this eval to check whether a long-horizon inquiry route can stop and relaunch without faking continuity.

This draft bundle is a `diagnostic` workflow eval.
It focuses on one nearby question:
did the checkpoint pack preserve enough axis, contradiction posture, and delta separation for a bounded relaunch?

It is not a general depth eval.
It is not a judgment of philosophical quality by itself.
Its current materialized draft proof flow runs through
`fixtures/long-horizon-restart-v1/README.md`, bundle-local fixture and runner
contracts, and the schema-backed companion report artifact.

## Object under evaluation

This eval checks restart fidelity of checkpoint-based long-horizon inquiry routes.

Primary surfaces under evaluation:
- checkpoint completeness
- axis retention after relaunch
- contradiction preservation
- separation of `memory_delta` and `canon_delta`
- resistance to false continuity

Nearby surfaces intentionally excluded:
- final truth of the inquiry outcome
- rhetorical sophistication of the synthesis
- runtime instrumentation depth in `abyss-stack`
- general artifact polish outside the checkpoint route

## Bounded claim

This eval is designed to support a claim like:

under these conditions, a checkpoint-based long-horizon inquiry route can relaunch with its active axis, open contradictions, and memo-versus-canon boundaries still reviewably intact.

This eval does **not** support claims such as:
- the inquiry reached the right final answer
- the route is generally intelligent
- the runtime stack has complete long-horizon instrumentation
- every long-horizon question now supports the same restart fidelity

## Trigger boundary

Use this eval when:
- the route spans more than one bounded pass
- a checkpoint pack is the intended relaunch surface
- contradictions and deltas need to survive a pause honestly
- the main question is restart fidelity rather than final answer quality

Do not use this eval when:
- the route ends in one bounded pass and never needs relaunch
- no checkpoint artifact exists to inspect
- the main question is witness-trace reviewability rather than restart fidelity
- the route depends on hidden private context unavailable to public reviewers

## Inputs

- one `inquiry_checkpoint` artifact
- one prior-pass evidence pack
- one relaunch or simulated relaunch readout
- contradiction notes or contradiction map
- the bounded restart contract for the route

## Fixtures and case surface

A strong starter case surface should include:
- one architectural inquiry with an explicit checkpoint pack
- one pass where contradictions remain open across relaunch
- one pass where `memory_delta` and `canon_delta` are both present
- one pass where a restart could easily drift into summary theater if the checkpoint were weak

Fixtures should avoid:
- one-pass tasks with no real restart need
- checkpoints that are only polished summaries with no explicit evidence refs
- cases where the next pass still depends on the full raw history
- routes whose continuity depends on private notes outside the bundle

The current materialized shared family is
`fixtures/long-horizon-restart-v1/README.md`.
When the machine-readable proof surface is in use, local replacements should
preserve the same five checkpoint-and-relaunch pressures through the bounded
replacement rule in `fixtures/contract.json`.

## Scoring or verdict logic

This eval prefers a summary-with-breakdown verdict.

Suggested verdict classes:
- `supports bounded claim`
- `mixed support`
- `does not support bounded claim`

Suggested breakdown axes:
- `checkpoint_completeness`
- `axis_retention`
- `contradiction_preservation`
- `delta_separation`
- `false_continuity_resistance`

Per-case review should ask:
- does the checkpoint name the objective, current thesis, open questions, and next tests clearly enough to relaunch?
- does the relaunch keep the same active axis rather than inventing a cleaner one?
- do contradictions survive as contradictions?
- do `memory_delta` and `canon_delta` remain distinct?
- does the relaunch rely on the checkpoint pack rather than on hidden raw continuity?

### Approve signals

Signals toward `supports bounded claim`:
- the checkpoint pack is complete enough for bounded relaunch
- the relaunch preserves the active axis without inflation
- contradictions remain visible and reviewable
- delta separation stays explicit
- the relaunch does not silently depend on the full prior transcript

### Degrade signals

Signals toward `mixed support` or `does not support bounded claim`:
- the checkpoint omits current axis, open questions, or next tests
- relaunch invents new continuity not supported by the pack
- contradictions disappear for smoothness
- `memory_delta` and `canon_delta` collapse into one summary blur
- the route needs hidden raw history to make sense again

## Baseline or comparison mode

This bundle uses `none`.

It is a standalone bounded proof surface for restart fidelity.
A later stronger form may compare:
- repeated relaunches on the same inquiry line
- different checkpoint shapes on the same long-horizon route
- before-vs-after checkpoint contract revisions

Without a baseline, this bundle supports only modest claims about the current restart surface on the chosen cases.

## Execution contract

A careful run should:
1. choose a long-horizon route with a real checkpoint pack
2. inspect the checkpoint, contradiction notes, and delta artifacts together
3. inspect the relaunch readout or simulated relaunch prompt surface
4. judge whether the checkpoint alone is strong enough to preserve the axis honestly
5. publish a summary-with-breakdown artifact with an explicit interpretation boundary

Execution expectations:
- do not grade final answer quality as if it were restart fidelity
- do not assume full raw history is allowed during relaunch
- do not reward smooth prose if contradiction posture disappeared
- do not treat `memory_delta` and `canon_delta` as interchangeable
- when shipping a machine-readable report, validate it against
  `reports/summary.schema.json`
- keep the shared case-family contract in
  `fixtures/long-horizon-restart-v1/README.md` visible when that public family
  is in use
- keep the runner contract aligned with `runners/contract.json` so checkpoint
  completeness, axis retention, contradiction posture, delta separation, and
  false-continuity pressure do not collapse into one top-line readout

## Outputs

The eval should produce:
- one bundle-level verdict
- one breakdown across the restart-fidelity axes
- one note on the strongest restart-support signal
- one note on the strongest restart-risk gap
- one explicit interpretation boundary
- an optional schema-backed companion report artifact at
  `reports/example-report.json`

## Failure modes

This eval can fail as an instrument when:
- the checkpoint is judged by prose smoothness instead of relaunch usefulness
- the relaunch secretly relies on raw history the reviewer cannot see
- contradictions are treated as noise to clean up
- canon and memory deltas are merged for convenience
- the chosen cases never really stress restart fidelity

## Blind spots

This eval does not prove:
- final inquiry correctness
- philosophical depth by itself
- runtime trace completeness
- long-term stability across every inquiry family
- that one good restart implies general long-horizon competence

Likely false-pass path:
- a checkpoint looks tidy and complete, but the next pass still needed hidden transcript continuity.

Likely misleading-result path:
- a route gets a mixed result because the inquiry is genuinely open-ended, even though the checkpoint preserved that openness honestly.

Nearby claim classes that should use a different bundle instead:
- witness-trace reviewability should use `aoa-witness-trace-integrity`
- repeated-window movement should use `aoa-longitudinal-growth-snapshot`
- same-task regression should use `aoa-regression-same-task`

## Interpretation guidance

Treat a positive result as support for one bounded claim:
the checkpoint-based route can relaunch without losing its axis dishonestly.

Do not treat a positive result as:
- proof that the inquiry reached the right conclusion
- proof of broad long-horizon capability
- proof that runtime instrumentation is solved
- proof that every future relaunch will be equally strong

A mixed or negative result is still valuable because it can reveal:
- thin checkpoint packs
- erased contradictions
- hidden dependence on raw history
- blurred canon-versus-memory boundaries

## Verification

- confirm the bounded claim is explicit
- confirm the checkpoint artifact is real and inspectable
- confirm scoring logic stays on restart fidelity rather than final-answer quality
- confirm blind spots are named
- confirm the output does not imply stronger claims than the bundle supports
- confirm manifest evidence is explicit and resolves publicly
- confirm the machine-readable report contract keeps checkpoint completeness,
  delta separation, and false-continuity pressure visible enough for review
- confirm fixture and runner contracts preserve the same checkpoint-and-relaunch
  question under bounded local replacement

## Technique traceability

This bundle currently uses no explicit upstream technique dependency.

## Skill traceability

This bundle currently uses no explicit upstream skill dependency.

## Adaptation points

Project overlays may add:
- local checkpoint schemas
- local relaunch harnesses
- local contradiction-map formats
- local report sinks
- local fixture replacements allowed by `fixtures/contract.json`
- local runner wrappers that still validate against `reports/summary.schema.json`

When they do, the bounded claim should remain restart fidelity rather than final-answer quality.
