---
name: aoa-memo-reviewed-candidate-adoption-integrity
category: workflow
status: draft
summary: Checks whether reviewed distillation candidates can reach adopted memo visibility, live receipt visibility, and recall surfaces without flattening candidate posture into settled truth.
object_under_evaluation: integrity of reviewed-candidate adoption on runtime-to-memo distillation paths
claim_type: bounded
baseline_mode: none
report_format: summary-with-breakdown
technique_dependencies: []
skill_dependencies: []
---

# aoa-memo-reviewed-candidate-adoption-integrity

## Intent

Use this eval to check whether the next memo gap after the base writeback-act
pilot is actually solved on the current public surfaces.

This draft bundle is a narrow diagnostic workflow eval.

It focuses on five nearby questions only:

- do runtime writeback mappings stay explicit for
  `distillation_claim_candidate`,
  `distillation_pattern_candidate`, and
  `distillation_bridge_candidate`?
- does reviewed adoption remain visible instead of collapsing into one vague
  memo object?
- does live receipt publication actually exist for the adopted candidate path?
- does candidate posture stay honest instead of being flattened into settled
  truth?
- do object-facing recall surfaces keep the adopted candidate inspectable
  downstream?

It is not a general memory-quality bundle.
It is not a contradiction bundle.
It is not a confirmed-decision writeback-act bundle.
It is not a promotion-readiness bundle.
It is not a permissions-from-memory bundle.
Its current materialized draft proof flow runs through
`fixtures/memo-reviewed-candidate-adoption-guardrail-v1/README.md`,
bundle-local fixture and runner contracts, and the schema-backed companion
report artifacts.

## Object under evaluation

This eval checks integrity of reviewed-candidate adoption on runtime-to-memo
distillation paths.

Primary surfaces under evaluation:

- runtime writeback target, intake, and governance alignment for reviewed
  candidate mappings
- reviewed-to-adopted linkage for claim, pattern, and bridge candidate paths
- live receipt visibility for adopted candidate paths
- candidate-posture honesty on object-facing recall surfaces
- recall-path inspectability after candidate adoption

Nearby surfaces intentionally excluded:

- confirmed memo-surviving-event writeback acts
- contradiction handling as its own proof surface
- final promotion from candidate posture into settled doctrine or lifted graph
  truth
- future scar or retention readiness
- generic live memory-ledger behavior

## Bounded claim

This eval is designed to support a claim like:

under these conditions, a reviewed distillation candidate can move from runtime
candidate mapping through reviewed memo adoption into live receipt visibility
and object-facing recall without silently upgrading candidate posture into
settled truth.

This eval does not support claims such as:

- reviewed-candidate promotion is generally solved
- all claim, pattern, and bridge adoption paths are already complete
- candidate visibility on recall surfaces is the same thing as live receipt
  completeness
- bridge-ready or KAG-facing exports imply final bridge promotion
- generic memory automation readiness

## Trigger boundary

Use this eval when:

- the main question is reviewed-candidate adoption rather than confirmed
  decision writeback
- a route names distillation claim, pattern, or bridge candidates explicitly
- reviewed adoption, live receipt visibility, and recall surfaces all matter to
  the claim being made
- the honest question is whether the current public path works end to end or
  still has a real memo gap

Do not use this eval when:

- no candidate-facing memo object exists yet
- the main question is contradiction handling or recall precision
- the main question is final promotion into settled doctrine or downstream graph
  truth
- the case depends on hidden runtime stores or private receipt logs

## Inputs

- `repo:aoa-memo/examples/checkpoint_to_memory_contract.example.json`
- `repo:aoa-memo/generated/runtime_writeback_targets.min.json`
- `repo:aoa-memo/generated/runtime_writeback_intake.min.json`
- `repo:aoa-memo/generated/runtime_writeback_governance.min.json`
- `repo:aoa-memo/generated/phase_alpha_writeback_map.min.json`
- `repo:aoa-memo/examples/claim.phase-alpha-runtime-history-later-infra-track.example.json`
- `repo:aoa-memo/examples/pattern.phase-alpha-remediation-recurrence.example.json`
- `repo:aoa-memo/examples/bridge.kag-lift.example.json`
- `repo:aoa-memo/generated/memory_object_catalog.min.json`
- `repo:aoa-memo/generated/memory_object_capsules.json`
- `repo:aoa-memo/generated/memory_object_sections.full.json`
- `repo:aoa-memo/.aoa/live_receipts/memo-writeback-receipts.jsonl`
- `repo:aoa-memo/tests/fixtures/memo_writeback_receipts.example.jsonl`
- `repo:aoa-memo/scripts/publish_live_receipts.py`

## Fixtures and case surface

A strong starter case surface should include:

- one claim candidate case where runtime writeback mapping, reviewed adoption,
  and recall visibility all exist on the same bounded path
- one pattern candidate case where the real adoption pressure can be tested
  honestly rather than narrated from adjacent recurrence evidence
- one bridge candidate case where candidate-only posture remains visible and is
  not mistaken for final lift
- one receipt-gap case where adoption looks plausible but live publication is
  still missing or asymmetric

Fixtures should avoid:

- hidden runtime stores as the only evidence of candidate adoption
- cases that are really about contradiction handling or recall precision
- treating KAG export presence as proof of bridge promotion
- generic growth stories wider than the current reviewed-candidate adoption
  path

The current materialized shared family is
`fixtures/memo-reviewed-candidate-adoption-guardrail-v1/README.md`.
When the machine-readable proof surface is in use, local replacements should
preserve the same reviewed-candidate adoption pressures through the bounded
replacement rule in `fixtures/contract.json`.

## Scoring or verdict logic

This eval prefers a summary-with-breakdown verdict.

Suggested verdict classes:

- `supports bounded claim`
- `mixed support`
- `does not support bounded claim`

Suggested breakdown axes:

- `target_mapping_integrity`
- `review_to_adoption_alignment`
- `receipt_visibility`
- `candidate_posture_honesty`
- `recall_surface_alignment`

Per-case review should ask:

- do runtime mapping surfaces still name the reviewed-candidate target kind
  explicitly?
- is the adopted memo object actually linked to reviewed evidence rather than
  merely coexisting nearby?
- does a live receipt exist and point back to the adopted object and review
  anchor?
- does candidate posture remain visible instead of being over-read as settled
  truth?
- can a downstream reader inspect the adopted candidate through object-facing
  recall surfaces without losing lifecycle posture?

### Approve signals

Signals toward `supports bounded claim`:

- reviewed-candidate mappings remain explicit for claim, pattern, and bridge
- the adopted memo object preserves reviewed evidence refs and candidate posture
- a live receipt points back to the adopted object and review anchor
- recall surfaces expose the same object with lifecycle and provenance posture
  intact
- the path stays weaker than promotion or generic live-ledger claims

### Degrade signals

Signals toward `mixed support` or `does not support bounded claim`:

- target mapping exists, but the adopted object cannot be tied to a real
  reviewed candidate path
- a candidate object is visible, but no live receipt publishes it
- bridge or pattern visibility is mistaken for completed reviewed adoption
- recall surfaces smooth over `proposed`, `candidate`, or open-risk posture
- one successful claim leg is over-read as proof that the whole triad is ready

## Baseline or comparison mode

This bundle uses `none`.

It is the first narrow reviewed-candidate adoption pilot.

A later stronger form may compare:

- one claim, pattern, and bridge family before and after live receipt hardening
- reviewed-candidate adoption against confirmed memo-surviving-event writeback
- candidate-only recall visibility against later owner-confirmed adoption

Without a baseline, this bundle supports only modest claims about the current
reviewed-candidate adoption path.

## Execution contract

A careful run should:

1. select one bounded claim, pattern, and bridge candidate family from current
   public memo surfaces
2. review runtime mapping, reviewed adoption, receipt visibility,
   candidate-posture honesty, and recall alignment separately before any
   top-line read
3. keep live receipt evidence weaker than the adopted memo object and reviewed
   anchors
4. publish a summary-with-breakdown artifact with explicit interpretation
   limits

Execution expectations:

- do not treat object visibility alone as receipt-complete adoption
- do not widen the bundle into contradiction, promotion, or graph-lift proof
- do not rely on hidden runtime traces when public reviewed anchors exist
- when shipping a machine-readable report, validate it against
  `reports/summary.schema.json`
- keep the shared case-family contract in
  `fixtures/memo-reviewed-candidate-adoption-guardrail-v1/README.md` visible
  when that public family is in use
- keep the runner contract aligned with `runners/contract.json` so mapping,
  review, receipt, candidate posture, and recall alignment do not collapse into
  one vague readiness story

## Outputs

The eval should produce:

- one bundle-level verdict
- one breakdown across the five adoption axes
- one note on the strongest adoption signal
- one note on the strongest adoption risk
- one explicit interpretation boundary
- an optional schema-backed companion report artifact at
  `reports/example-report.json`

## Failure modes

This eval can fail as an instrument when:

- candidate visibility is mistaken for final promotion
- the reviewer treats one stronger claim leg as proof that pattern and bridge
  legs are equally ready
- hidden runtime context is smuggled in to repair missing receipt evidence
- bridge export posture is mistaken for reviewed writeback completion

## Blind spots

This eval does not prove:

- contradiction handling quality
- confirmed memo-surviving-event writeback quality
- final promotion discipline
- future scar or retention readiness
- live memory-ledger behavior
- general runtime quality outside the reviewed-candidate adoption path

Likely false-pass path:

- one reviewed claim object looks healthy while pattern or bridge adoption still
  lacks live receipt coverage or reviewed-writeback evidence.

Likely misleading-result path:

- candidate posture remains honestly `proposed`, which can look weak even when
  the recall surface is correctly preserving bounded adoption.

## Interpretation guidance

Treat a positive result as support for one bounded claim:
the current public seam can keep one reviewed-candidate adoption path
inspectable from runtime mapping through memo recall without silently upgrading
candidate posture into settled truth.

Do not treat a positive result as:

- proof that reviewed-candidate promotion is ready
- proof that all three distillation target kinds have equal support
- proof of KAG-lift readiness
- proof of generic live writeback readiness

## Verification

- review at least one claim, pattern, and bridge candidate family
- confirm mapping, receipt visibility, and recall posture stay distinct
- confirm the report names current asymmetry instead of smoothing it away
- confirm claim limits remain explicit in the report

## Technique traceability

- none currently declared

## Skill traceability

- none currently declared

## Adaptation points

- add a real reviewed-candidate live receipt family once claim, pattern, and
  bridge publication is grounded on owner-local evidence
- compare reviewed-candidate adoption against the already-landed confirmed
  writeback-act lane once the receipt gap is materially tighter
