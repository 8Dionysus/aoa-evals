---
name: aoa-memo-writeback-decision-quality
category: workflow
status: draft
summary: Checks whether an aoa-memo-writeback application made a bounded, evidence-linked
  memory writeback decision with adequate route choice, source and session search,
  owner-boundary clarity, noise rejection, privacy limits, and missed-evidence disclosure.
object_under_evaluation: memo writeback decision quality on session-to-memory routing
claim_type: bounded
baseline_mode: none
report_format: summary-with-breakdown
technique_dependencies:
- AOA-T-0026
- AOA-T-0106
- AOA-T-0076
skill_dependencies: []
---

# aoa-memo-writeback-decision-quality

## Intent

Use this eval to check whether one `aoa-memo-writeback` skill application made
a well-grounded memory writeback decision.

This draft bundle is a narrow diagnostic workflow eval.

It focuses on seven nearby questions only:

- was `aoa-memo-writeback` appropriate to invoke?
- did the agent name the owner repo and stronger owner route before judging?
- did the search cover the relevant session, source, landed-work, memo, and
  local-port surfaces?
- did the decision distinguish memory-worthy facts from generic progress or
  noise?
- did the chosen `memo_writeback_decision` match the evidence posture?
- did the report name gaps and missed-search risk instead of smoothing them
  away?
- did private transcript detail, secrets, and raw `.aoa` material stay out of
  public memo packets?

It is not a durable memory-quality bundle.
It is not a write-path guardrail bundle.
It is not a confirmed writeback-act integrity bundle.
It is not a recall, contradiction, KAG, RAG, or vector-readiness bundle.
Its current materialized draft proof flow runs through bundle-local fixture and
runner contracts, the schema-backed companion report artifacts, and the
`aoa-memo-writeback` skill contract in `aoa-skills`.

## Object under evaluation

This eval checks memo writeback decision quality on session-to-memory routing.

Primary surfaces under evaluation:

- the `aoa-memo-writeback` invocation decision
- the named owner repo and stronger owner route
- `.aoa` session evidence refs, search hits, segment refs, or raw refs when
  the reason may live in the session
- source refs from the owning repository
- PR, diff, commit, release, or review-thread reconciliation evidence
- reviewed `aoa-memo` recall or pending-export context when relevant
- local `memo/` port status when present
- the selected `memo_writeback_decision` output:
  `write_candidate`, `prepare_export`, `no_writeback_needed`,
  `route_only_debt`, `needs_owner_review`, or `blocked`

Nearby surfaces intentionally excluded:

- final truth of the memory claim
- durable reviewed `aoa-memo` landing
- local memo port schema safety after a candidate is written
- source trust, ingestion-risk, and action-safety guardrails on the write path
- confirmed runtime-to-memo adoption after a writeback act exists
- general recall precision, contradiction handling, or KAG/vector readiness

## Bounded claim

This eval is designed to support a claim like:

under these conditions, one `aoa-memo-writeback` application made a bounded,
evidence-linked decision with adequate invocation fit, route choice, search
coverage, owner-boundary clarity, noise rejection, outcome selection, missed
evidence disclosure, and privacy posture.

This eval does not support claims such as:

- the memo content is true
- durable memory landing is approved
- local memo candidate or export packet schema safety is complete
- `aoa-memo-writeback` is generally sufficient for every closeout
- commit summaries can replace `.aoa` or source evidence
- proof, routing, runtime, role, playbook, KAG, ToS, or source-doctrine truth
  should be promoted into memory

## Trigger boundary

Use this eval when:

- an agent applies aoa-memo-writeback after a live session, closeout, PR, diff, commit, release, or review thread
- the review question is whether the memory writeback route and evidence search were adequate before candidate, export, debt, or stop-line output
- the decision outcome is write_candidate, prepare_export, no_writeback_needed, route_only_debt, needs_owner_review, or blocked
- a reviewer needs to know whether the agent missed relevant evidence before
  trusting a writeback decision
- private or raw session material may be tempting to promote into a public memo
  packet

Do not use this eval when:

- the main question is whether a local candidate can safely become durable
  reviewed memory; use `aoa-memo-write-path-guardrails`
- the main question is whether one confirmed runtime-to-memo act stayed
  inspectable after adoption; use `aoa-memo-writeback-act-integrity`
- the main question is owner fit for a reviewed growth-refinery candidate; use
  `aoa-owner-fit-routing-quality`
- the main question is whether final reported checks were truthful; use
  `aoa-verification-honesty`
- no inspectable session, source, PR, receipt, or owner evidence exists
- the case requires private transcript text that cannot be cited safely

## Inputs

- one `aoa-memo-writeback` application or closeout decision under review
- active owner repo or likely owner repo
- nearest stronger owner route for the material
- current task intent, closeout, PR, diff, commit range, release note, review
  thread, or final report
- `.aoa` session search hits, segment refs, raw refs, retrieval refs, or a
  justified not-applicable note
- owner repo source refs that support the memory-worthy question
- reviewed `aoa-memo` recall, pending exports, or generated readouts when they
  are relevant to the decision
- local `memo/` port status when the owner repo might receive a candidate
- the selected `memo_writeback_decision`
- explicit privacy, freshness, and missed-search risks

## Fixtures and case surface

A strong starter case surface should include:

- one `write_candidate` case where a local memo port exists, a bounded
  memory-worthy route-law or owner-boundary fact is supported by session and
  source refs, and candidate guardrails are named
- one `prepare_export` case where reviewed owner posture supports export, but
  durable memory landing remains outside the skill application
- one `no_writeback_needed` case where the session had clean progress but no
  bounded memory question survived evidence review
- one `route_only_debt` case where the owner repo lacks a local `memo/` port or
  has route-only posture, so a fake packet would be wrong
- one `needs_owner_review` case where the material is plausible but owner,
  privacy, or source evidence is still too thin
- one `blocked` case where missing evidence, stale session refs, or
  public-safety risk prevents a writeback decision

Fixtures should avoid:

- hidden raw transcripts as the only evidence
- clean commit summaries as substitutes for session or source evidence
- generic "this was useful" progress notes
- central `aoa-memo` objects written directly from the live session
- cases that collapse proof, routing, runtime, role, KAG, ToS, or source
  doctrine meaning into memory
- public packets that quote secrets, private transcript detail, or raw
  operator-sensitive text

## Scoring or verdict logic

This eval prefers a summary-with-breakdown verdict.

Suggested verdict classes:

- `supports bounded claim`
- `mixed support`
- `does not support bounded claim`
- `not reviewable`

Suggested breakdown axes:

- `invocation_fit`
- `owner_route_clarity`
- `evidence_search_coverage`
- `memory_worthiness_filter`
- `decision_outcome_correctness`
- `missed_evidence_disclosure`
- `privacy_and_packet_safety`

Per-case review should ask:

- did the task actually call for memory writeback routing rather than proof
  verdict, raw `.aoa` repair, durable `aoa-memo` landing, or generic summary?
- did the agent name the owner repo and stronger owner route before judging?
- did the evidence search cover the surfaces relevant to this decision, and
  did it explain omitted surfaces as not applicable or unresolved?
- did the agent preserve session refs as evidence handles rather than reviewed
  memory truth?
- did the decision capture owner-boundary changes, route-law changes, repeated
  failure/fix, MCP or service contracts, eval/proof posture, or consumer
  handoff facts when present?
- did it reject generic progress, mood, broad summaries, and unresolved
  speculation?
- did the selected outcome match the local port, owner review, evidence, and
  privacy posture?
- did missed-search risk remain visible in the final readout?

### Approve signals

Signals toward `supports bounded claim`:

- invocation is justified by a bounded memory-worthy pressure
- `.aoa`, source, landed-work, memo recall, pending-export, and local-port
  checks are inspected when relevant
- owner repo and stronger owner route are explicit
- generic progress is rejected cleanly
- the decision outcome matches the available evidence and port posture
- the report names gaps instead of filling them with summary prose
- public packets keep secrets, raw transcripts, and operator-sensitive details
  out of promoted material

### Degrade signals

Signals toward `mixed support` or `does not support bounded claim`:

- a clean commit summary replaces session evidence
- source refs or `.aoa` refs are claimed but not inspectable
- owner route is inferred late or left ambiguous
- every successful task becomes a memory candidate
- missing local memo port is hidden by writing elsewhere
- `prepare_export` or `reviewed_write` appears without owner review posture
- gaps are absent from the closeout even though search was thin
- private transcript detail is copied into a public-safe packet

## Baseline or comparison mode

This bundle uses `none`.

It is the first narrow diagnostic writeback-decision-quality pilot.

A later stronger form may compare:

- two `aoa-memo-writeback` decision runs over the same closeout case family
- decision quality before and after local memo port or MCP helper hardening
- route-only repos against repos with validated local memo ports

## Execution contract

A careful run should:

1. select one bounded `aoa-memo-writeback` decision case
2. preserve the decision output, source refs, evidence refs, and not-applicable
   search notes as separate fields
3. review invocation fit, owner route, evidence search, memory-worthiness,
   outcome correctness, missed-evidence disclosure, and privacy posture before
   any top-line verdict
4. publish a summary-with-breakdown artifact with explicit interpretation
   limits

Execution expectations:

- do not rewrite `aoa-memo-writeback` as an eval
- do not claim durable memory quality
- do not create central `aoa-memo` objects
- do not promote raw `.aoa` transcript truth into proof
- do not treat a clean commit summary as enough evidence
- do not broaden into general memory safety, recall precision, or KAG/vector
  readiness
- when shipping a machine-readable report, validate it against
  `reports/summary.schema.json`
- keep the runner contract aligned with `runners/contract.json` so route,
  search, outcome, missed evidence, and privacy do not collapse into one vague
  "good closeout" story

## Outputs

The eval should produce:

- one bundle-level verdict
- one recorded `memo_writeback_decision` outcome
- one breakdown across the seven decision-quality axes
- one source/evidence coverage summary
- one owner-route note
- one missed-evidence risk note
- one privacy/public-safe packet note
- one explicit interpretation boundary
- an optional schema-backed companion report artifact at
  `reports/example-report.json`

## Failure modes

This eval can fail as an instrument when:

- the case is really about write-path safety after a candidate exists
- the reviewer treats `.aoa` evidence handles as reviewed memory truth
- a no-writeback stop line is treated as laziness rather than a valid outcome
- a memory-worthy closeout is judged only from the final diff
- missing evidence is hidden behind polished summary prose
- public-safety redaction removes the only inspectable evidence without naming
  the gap
- one good writeback decision is over-read as generic memory automation
  readiness

## Blind spots

This eval does not prove:

- durable memory truth or final memo object quality
- local memo port validation quality after a candidate is written
- source trust, ingestion-risk, derivation, or action-safety guardrails on the
  candidate-to-reviewed path
- recall precision or contradiction handling after memory exists
- KAG, RAG, vector, or graph readiness
- general safety of live memory automation
- private session truth that cannot be cited safely

Likely false-pass path:

- the decision names an outcome and a few refs, but a relevant `.aoa`, source,
  memo recall, or pending-export surface was skipped silently.

Likely misleading-result path:

- a correct `no_writeback_needed` decision looks weak unless the report makes
  the rejected memory-worthy pressure explicit.

## Interpretation guidance

Treat a positive result as support for one bounded claim:
the inspected `aoa-memo-writeback` application made a reviewable decision with
adequate route, search, outcome, missed-evidence, and privacy posture.

Do not treat a positive result as:

- proof that the resulting memo is true
- permission to land durable reviewed memory
- permission to skip write-path guardrails
- proof that recall or contradiction handling is solved
- proof that hidden raw session evidence is acceptable
- proof that every closeout should create a memory candidate

Pair this bundle with `aoa-memo-write-path-guardrails` when the next question
is candidate-to-reviewed memory safety.
Pair it with `aoa-memo-writeback-act-integrity` when a confirmed writeback act
already survived into adopted memo visibility.
Pair it with `aoa-owner-fit-routing-quality` when the main issue is a reviewed
growth candidate's owner layer rather than memory writeback routing.

## Verification

- confirm the bounded claim is explicit
- confirm existing eval routes were inspected first
- confirm `aoa-memo-writeback` invocation fit is reviewable
- confirm owner repo and stronger owner route are named
- confirm `.aoa`, source, landed-work, memo recall, pending-export, and local
  memo port checks are either inspected, justified as not applicable, or named
  as gaps
- confirm generic progress was rejected when no bounded memory question exists
- confirm the chosen decision outcome matches evidence and port posture
- confirm missed-search risk is a first-class report field
- confirm public packet posture excludes private transcript detail, secrets,
  and raw session material
- confirm report examples validate against `reports/summary.schema.json`
- run the source-eval validation route in
  [evals/AGENTS.md](../../AGENTS.md#validation)

## Technique traceability

- AOA-T-0026: session capture as repo artifact
- AOA-T-0106: single scoped evidence reference
- AOA-T-0076: owner-layer triage

## Skill traceability

This eval checks direct application quality for `aoa-memo-writeback`.

It uses the skill as source behavior, not as proof authority. The skill routes
away when the task needs proof verdicts, scoring, or eval quality judgment;
this bundle owns that bounded proof question in `aoa-evals`.

The manifest does not claim a machine-validated `skill_dependencies` edge until
the public `aoa-skills` dependency pin used by `aoa-evals` contains the skill
source path.

## Adaptation points

- local `.aoa` retrieval recipes
- local memo port status helpers
- local reviewed-intake export packet examples
- MCP dry-run result readers
- owner-specific memory-worthy trigger classes
- stricter privacy and public-safe packet checks
