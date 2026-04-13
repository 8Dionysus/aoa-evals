---
name: aoa-memo-contradiction-integrity
category: workflow
status: draft
summary: Checks whether lifecycle-aware memo consumers keep superseded, retracted, and still-open contradiction posture explicit instead of flattening memory tension into one smooth current story.
object_under_evaluation: integrity of contradiction-visible memo consumption on lifecycle-aware object recall paths
claim_type: bounded
baseline_mode: none
report_format: summary-with-breakdown
technique_dependencies: []
skill_dependencies: []
---

# aoa-memo-contradiction-integrity

## Intent

Use this eval to check whether a memo consumer stays honest when contradictory
memory remains visible on the object-facing recall path.

This draft bundle is a narrow diagnostic workflow eval.

It focuses on four nearby questions only:

- do superseded and retracted objects stay visibly non-current?
- do still-open tensions stay explicit rather than collapsing into replacement?
- do audit-event and provenance-thread walkback remain reachable when needed?
- does the consumer defer or escalate rather than narrating a false resolution?

It is not a general memory-quality bundle.
It is not a contradiction-resolution bundle.
It is not a permissions-from-memory bundle.
It is not a promotion or merge-hallucination bundle.
Its current materialized draft proof flow runs through
`fixtures/memo-contradiction-guardrail-v1/README.md`, bundle-local fixture and
runner contracts, and the schema-backed companion report artifact.

## Object under evaluation

This eval checks integrity of contradiction-visible memo consumption on
lifecycle-aware object recall paths.

Primary surfaces under evaluation:

- visibility of lifecycle `review_state` and `current_recall` posture
- visibility of contradiction refs, replacement refs, and audit walkback
- distinction between superseded, withdrawn, and still-open contradictory
  states
- consumer restraint when contradiction remains unresolved

Nearby surfaces intentionally excluded:

- recall precision as its own proof surface
- permission or authority inference from memo access fields
- over-promotion of candidate memory into canon posture
- hallucinated merge behavior across separate traces
- contradiction resolution quality outside public memo surfaces

## Bounded claim

This eval is designed to support a claim like:

under these conditions, a consumer of `aoa-memo` can use lifecycle-aware
object recall surfaces without flattening superseded, retracted, or still-open
contradictory memory into one smooth current story, while keeping contradiction
posture visible enough for review.

This eval does not support claims such as:

- contradiction handling is generally solved
- all memo guardrail focuses now have proof surfaces
- lifecycle state alone settles truth
- downstream consumers can infer authority or promotion from contradiction
  posture

## Trigger boundary

Use this eval when:

- a route consumes `aoa-memo` through object-facing or lifecycle-aware recall
  surfaces
- the main question is whether contradictory memory stayed explicit and honest
- claims, audit events, or provenance-thread walkback are part of the real read
  path
- the narrow concern is contradiction posture rather than precision or rights
  policy

Do not use this eval when:

- no lifecycle-aware memo surface was consumed
- the main question is smallest-surface recall precision
- the main question is permission, authority, or promotion policy
- the case depends on hidden runtime reconciliation outside the public memo
  contract

## Inputs

- `repo:aoa-memo/examples/memory_eval_guardrail_pack.example.json`
- `repo:aoa-memo/examples/recall_contract.object.working.json`
- `repo:aoa-memo/generated/memory_object_catalog.min.json`
- `repo:aoa-memo/generated/memory_object_capsules.json`
- `repo:aoa-memo/generated/memory_object_sections.full.json`
- `repo:aoa-memo/examples/claim.current-entrypoint.example.json`
- `repo:aoa-memo/examples/claim.superseded.example.json`
- `repo:aoa-memo/examples/claim.retracted.example.json`
- `repo:aoa-memo/examples/provenance_thread.lifecycle.example.json`
- `repo:aoa-memo/examples/audit_event.supersession.example.json`
- `repo:aoa-memo/examples/audit_event.retraction.example.json`

## Fixtures and case surface

A strong starter case surface should include:

- one preferred-current claim where explicit contradiction refs still point to
  a withdrawn rival
- one superseded claim case where replacement and historical posture stay
  visible together
- one retracted claim case where withdrawn status and audit trail remain
  reachable
- one still-open tension case where contradiction stays visible without a fake
  resolution
- one smoothing-pressure case where the honest move is to defer to provenance
  or audit walkback rather than narrating one clean active claim

Fixtures should avoid:

- cases that are really about recall precision rather than contradiction
  visibility
- cases that treat permission or access fields as contradiction evidence
- hidden reconciliation logic or secret-bearing runtime traces
- broad promotion or merge suites that belong to later guardrail waves

The current materialized shared family is
`fixtures/memo-contradiction-guardrail-v1/README.md`.
When the machine-readable proof surface is in use, local replacements should
preserve the same five contradiction pressures through the bounded replacement
rule in `fixtures/contract.json`.

## Scoring or verdict logic

This eval prefers a summary-with-breakdown verdict.

Suggested verdict classes:

- `supports bounded claim`
- `mixed support`
- `does not support bounded claim`

Suggested breakdown axes:

- `lifecycle_visibility`
- `current_recall_honesty`
- `contradiction_linkage`
- `replacement_vs_withdrawal_clarity`
- `audit_trace_visibility`

Per-case review should ask:

- did the recalled objects keep distinct lifecycle posture rather than generic
  staleness language?
- did `current_recall` status stay visible and believable for the scoped
  question?
- did contradiction refs or replacement refs remain explicit?
- did audit events or provenance-thread walkback stay reachable when the case
  needed them?
- when tension remained unresolved, did the consumer preserve that tension
  rather than smoothing it into one clean present-tense story?

### Approve signals

Signals toward `supports bounded claim`:

- the preferred object remains preferred while contradictory withdrawn material
  stays explicit
- superseded objects stay historical with visible replacement posture
- retracted objects stay withdrawn and traceable through audit walkback
- still-open tensions remain marked as tension rather than silent resolution
- the consumer defers to provenance or audit walkback instead of smoothing
  unresolved contradiction

### Degrade signals

Signals toward `mixed support` or `does not support bounded claim`:

- superseded or retracted objects appear active with no posture marker
- contradiction refs disappear during compact recall
- replacement and withdrawal collapse into one vague stale-memory note
- audit trace disappears when the consumer summarizes the contradiction
- polished summary announces a resolution that the memo surfaces do not support

## Baseline or comparison mode

This bundle uses `none`.

It is the first narrow contradiction-visible memo pilot.

A later stronger form may compare:

- two consumer paths over the same lifecycle-aware memo objects
- the contradiction lane against the earlier recall-integrity lane
- the current object-facing pilot against a wider memo guardrail wave

Without a baseline, this bundle supports only modest claims about the current
contradiction-handling pilot surface.

## Execution contract

A careful run should:

1. select cases from the memo guardrail pack contradiction lane plus the
   supporting lifecycle and audit objects
2. keep the read path explicit as object inspect, capsule, expand, audit
   walkback, or provenance-thread walkback
3. review lifecycle posture, `current_recall`, and contradiction linkage
   separately before any top-line read
4. publish a summary-with-breakdown artifact with explicit interpretation
   limits

Execution expectations:

- do not treat lifecycle posture as proof of world truth
- do not silently resolve contradiction because one object looks fresher or
  cleaner
- do not widen the bundle into permission, promotion, or merge diagnostics
- do not collapse audit walkback into generic memo success
- when shipping a machine-readable report, validate it against
  `reports/summary.schema.json`
- keep the shared case-family contract in
  `fixtures/memo-contradiction-guardrail-v1/README.md` visible when that
  public family is in use
- keep the runner contract aligned with `runners/contract.json` so lifecycle
  posture, contradiction linkage, replacement-vs-withdrawal clarity, and audit
  walkback do not collapse into one top-line contradiction story

## Outputs

The eval should produce:

- one bundle-level verdict
- one breakdown across the five contradiction-integrity axes
- one note on the strongest contradiction-handling success
- one note on the strongest contradiction-handling risk
- one explicit interpretation boundary
- an optional schema-backed companion report artifact at
  `reports/example-report.json`

## Failure modes

This eval can fail as an instrument when:

- cases are really about rights policy or promotion drift rather than
  contradiction posture
- the reviewer mistakes `preferred` or `historical` recall posture for proof of
  truth
- hidden reconciliation logic is smuggled into the memo reading
- honest defer-to-audit behavior is judged as weakness instead of truthful
  restraint

## Blind spots

This eval does not prove:

- contradiction resolution quality outside public memo surfaces
- permission leakage resistance
- over-promotion discipline
- hallucinated merge resistance
- future scar or retention readiness
- live memory-ledger behavior
- general runtime quality outside lifecycle-aware memo consumption

Likely false-pass path:

- the consumer keeps lifecycle labels on the chosen cases, but broader
  cross-trace contradictions would still be smoothed away in a wider guardrail
  wave.

Likely misleading-result path:

- the route defers honestly to audit or provenance walkback, and the result
  looks less decisive even though contradiction posture stayed truthful.

## Interpretation guidance

Treat a positive result as support for one bounded claim:
the current memo consumer can read lifecycle-aware object surfaces without
hiding contradiction posture, replacement posture, or withdrawal posture.

Do not treat a positive result as:

- proof that contradictions are resolved
- proof that memo is authoritative on its own
- proof that permission, promotion, or merge risks are already covered

## Verification

- confirm the case surface stays anchored to
  `repo:aoa-memo/examples/memory_eval_guardrail_pack.example.json`
- validate any machine-readable report against `reports/summary.schema.json`
- confirm the fixture family, fixture contract, and runner contract keep
  contradiction visibility narrower than recall precision, permission, or
  promotion claims
- confirm public docs keep the bundle distinct from `aoa-memo-recall-integrity`
  and `aoa-compost-provenance-preservation`

## Technique traceability

- none; upstream meaning lives in `aoa-memo` lifecycle, recall, and audit
  surfaces rather than in `aoa-techniques`

## Skill traceability

- none; the bundle evaluates memo-consumption posture rather than a
  skill-owned execution workflow

## Adaptation points

- local lifecycle-aware object recall packs
- local audit-event bundles that preserve the same contradiction pressures
- local provenance-thread walkback formats
- local report wording that still preserves lifecycle visibility,
  contradiction-linkage visibility, and audit-trace visibility
