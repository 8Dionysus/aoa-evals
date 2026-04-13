---
name: aoa-memo-recall-integrity
category: workflow
status: draft
summary: Checks whether memo recall stays narrow, provenance-visible, and staleness-honest across the first inspect/capsule/expand consumer wave.
object_under_evaluation: integrity of memo recall on explicit inspect/capsule/expand consumer paths
claim_type: bounded
baseline_mode: none
report_format: summary-with-breakdown
technique_dependencies: []
skill_dependencies: []
---

# aoa-memo-recall-integrity

## Intent

Use this eval to check whether the first live memo-recall consumer path stays
honest about what memo can and cannot support.

This draft bundle is a narrow diagnostic workflow eval.

It focuses on three nearby questions only:

- does recall return the smallest relevant surface first?
- does provenance remain visible through compact recall?
- does stale or cooled memory stay visibly non-current?

It is not a general memory-quality bundle.
It is not a contradiction bundle.
It is not a permissions-from-memory bundle.
Its current materialized draft proof flow runs through
`fixtures/memo-recall-guardrail-v1/README.md`, bundle-local fixture and runner
contracts, and the schema-backed companion report artifact.

## Object under evaluation

This eval checks integrity of memo recall on explicit inspect/capsule/expand
consumer paths.

Primary surfaces under evaluation:

- precision of selected recall surfaces
- visibility of provenance-thread and stronger-source posture
- honesty of lifecycle and staleness posture
- consumer restraint when memo grounding is thin

Nearby surfaces intentionally excluded:

- contradiction resolution as its own proof surface
- permission or authority inference from memo fields
- over-promotion of candidate memory into canon posture
- hallucinated merge behavior across separate traces

## Bounded claim

This eval is designed to support a claim like:

under these conditions, a consumer of `aoa-memo` can use the first
inspect/capsule/expand path without turning memo into proof, while keeping
precision, provenance, and staleness posture visible enough for review.

This eval does not support claims such as:

- memo recall is generally solved
- all memo guardrail focuses now have one proof surface
- any recalled surface is true just because it is compact and easy to consume
- downstream consumers can infer authority directly from memo posture fields

## Trigger boundary

Use this eval when:

- a route consumes `aoa-memo` through explicit recall contracts
- the main question is whether memo recall stayed bounded and source-honest
- inspect, capsule, or expand surfaces are part of the real read path
- the narrow concern is recall integrity rather than a broader workflow claim

Do not use this eval when:

- no memo recall surface was consumed
- the main question is contradiction handling or rights policy
- the main question is broad runtime quality rather than memo recall posture
- the case depends on hidden search or ranking behavior outside this pilot

## Inputs

- `repo:aoa-memo/examples/memory_eval_guardrail_pack.example.json`
- `repo:aoa-memo/examples/recall_contract.router.semantic.json`
- `repo:aoa-memo/generated/memory_catalog.min.json`
- `repo:aoa-memo/generated/memory_capsules.json`
- `repo:aoa-memo/generated/memory_sections.full.json`
- `repo:aoa-memo/examples/provenance_thread.kag-lift.example.json`
- `repo:aoa-memo/examples/claim.superseded.example.json`
- `repo:aoa-memo/examples/claim.retracted.example.json`

## Fixtures and case surface

A strong starter case surface should include:

- one precision case where inspect should beat broad full expansion
- one provenance case where a claim or bridge must still walk back to its
  provenance thread
- one staleness case where lifecycle and trust posture must stay visible during
  recall
- one consumer note showing that stronger-source routing is lifted when memo
  grounding is too weak

Fixtures should avoid:

- hidden semantic search or ranking behavior
- cases that rely on private runtime evidence not present in the memo contract
- broad contradiction suites that belong to a later guardrail wave
- permission or authority cases that are really owned by `aoa-agents`

The current materialized shared family is
`fixtures/memo-recall-guardrail-v1/README.md`.
When the machine-readable proof surface is in use, local replacements should
preserve the same five memo-recall pressures through the bounded replacement
rule in `fixtures/contract.json`.

## Scoring or verdict logic

This eval prefers a summary-with-breakdown verdict.

Suggested verdict classes:

- `supports bounded claim`
- `mixed support`
- `does not support bounded claim`

Suggested breakdown axes:

- `precision_fit`
- `provenance_visibility`
- `staleness_honesty`

Per-case review should ask:

- did recall return the smallest relevant surface before full expansion?
- could the reviewer still see provenance-thread or stronger-source posture?
- did stale, superseded, or retracted memory remain visibly non-current?
- did the consumer escalate to a stronger source instead of pretending memo was
  enough?

### Approve signals

Signals toward `supports bounded claim`:

- inspect beats broad expansion when the smaller surface is enough
- capsule use stays compact rather than pretending to be proof
- provenance-thread or stronger-source posture stays visible
- stale or withdrawn memory is marked as such during recall
- memo insufficiency leads to stronger-source routing rather than confident
  invention

### Degrade signals

Signals toward `mixed support` or `does not support bounded claim`:

- full expansion is treated as the default read even when inspect is enough
- provenance-thread linkage disappears in compact recall
- stale or withdrawn memory is presented as equally current
- the consumer infers truth rather than escalating when memo grounding is thin

## Baseline or comparison mode

This bundle uses `none`.

It is the first narrow diagnostic memo-recall pilot.

A later stronger form may compare:

- two recall-contract revisions on the same cases
- two consumer paths over the same memo surfaces
- the first pilot triad against a later wider guardrail wave

Without a baseline, this bundle supports only modest claims about the current
memo-recall pilot surface.

## Execution contract

A careful run should:

1. select cases from the first memo guardrail pack
2. keep the read path explicit as inspect, capsule, expand, or stronger-source
   escalation
3. review precision, provenance, and staleness separately before any top-line
   read
4. publish a summary-with-breakdown artifact with explicit interpretation
   limits

Execution expectations:

- do not invent semantic search or hidden ranking behavior
- do not treat compact memo surfaces as proof artifacts
- do not widen the bundle into contradiction, permission, or merge diagnostics
- do not collapse stronger-source routing into memo success
- when shipping a machine-readable report, validate it against
  `reports/summary.schema.json`
- keep the shared case-family contract in
  `fixtures/memo-recall-guardrail-v1/README.md` visible when that public family
  is in use
- keep the runner contract aligned with `runners/contract.json` so read path,
  provenance posture, lifecycle honesty, and stronger-source escalation do not
  collapse into one top-line memo success story

## Outputs

The eval should produce:

- one bundle-level verdict
- one breakdown across the three pilot axes
- one note on the strongest memo-recall success
- one note on the strongest memo-recall risk
- one explicit interpretation boundary
- an optional schema-backed companion report artifact at
  `reports/example-report.json`

## Failure modes

This eval can fail as an instrument when:

- cases are really about contradiction handling rather than recall integrity
- the reviewer mistakes compactness for authority
- hidden runtime search behavior is smuggled into the memo reading
- stronger-source escalation is judged as failure instead of honesty

## Blind spots

This eval does not prove:

- contradiction handling quality
- permission leakage resistance
- over-promotion discipline
- hallucinated merge resistance
- pre-Agon scar or retention readiness
- live Agon memory ledger behavior
- general runtime quality outside the memo recall path

Likely false-pass path:

- the consumer stays tidy on one compact case, but the broader guardrail program
  would still fail on contradiction or promotion posture.

Likely misleading-result path:

- the route escalates honestly to a stronger source, and the result looks
  weaker even though the memo reading stayed truthful.

## Interpretation guidance

Treat a positive result as support for one bounded claim:
the current memo consumer can read the first inspect/capsule/expand path
without hiding precision, provenance, or staleness posture.

Do not treat a positive result as:

- proof that memo recall is generally authoritative
- proof that all memo guardrail risks are now covered
- proof that downstream routing or runtime behavior is fully solved

A mixed or negative result is still valuable because it can reveal:

- over-expansion
- provenance loss
- stale-memory overclaim
- false confidence when memo grounding is weak

## Verification

- confirm the bounded claim is explicit
- confirm the case surface stays anchored to the memo guardrail pack
- confirm the three breakdown axes remain visible
- confirm the output does not imply stronger proof than the pilot supports
- confirm blind spots remain explicit
- confirm the machine-readable report contract keeps read path, provenance, and
  staleness posture visible enough for review
- confirm fixture and runner contracts preserve the same memo-recall question
  under bounded local replacement

## Technique traceability

This pilot currently uses no explicit upstream technique dependency.

## Skill traceability

This pilot currently uses no explicit upstream skill dependency.

## Adaptation points

Project overlays may add:

- local memo recall case packs
- consumer-specific inspect/capsule/expand traces
- local stronger-source escalation notes
- later comparison dossiers once the pilot grows beyond the first triad
- local fixture replacements allowed by `fixtures/contract.json`
- local runner wrappers that still validate against `reports/summary.schema.json`
