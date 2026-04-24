# Roadmap

## Purpose

This roadmap describes how `aoa-evals` should keep hardening as the bounded
proof layer for agents.
It has moved beyond public bootstrap into `v0.3.3` proof-surface and
continuity-wave alignment.

The center of gravity is agent evaluation first.
Human readability remains mandatory.
The repository should help both:
- agents that need bounded evaluation surfaces they can run, compare, and report on
- humans who need to understand what those evals really prove and what they still do not prove

The strongest current external signal is that the next durable layer of agent evaluation sits at the intersection of:
- agent-first evaluation philosophy
- trace, trajectory, and tool-use evaluation
- portable, parseable bundle and report contracts

This roadmap is not about maximizing bundle count quickly.
It is about building a proof canon that can support honest growth.

## Current release contour

For `v0.3.3`, the current contour is proof-surface hardening, not a claim that
`aoa-evals` owns runtime truth, memory truth, role policy, or broad autonomy
proof:

- continuity and self-agency proof bundles:
  `bundles/aoa-continuity-anchor-integrity/EVAL.md`,
  `bundles/aoa-reflective-revision-boundedness/EVAL.md`,
  and `bundles/aoa-self-reanchor-correctness/EVAL.md`
- checkpoint, diagnosis, and growth-refinery follow-through bundles:
  `bundles/aoa-candidate-lineage-integrity/EVAL.md`,
  `bundles/aoa-diagnosis-cause-discipline/EVAL.md`,
  `bundles/aoa-repair-boundedness/EVAL.md`,
  and `bundles/aoa-stats-regrounding-boundary-integrity/EVAL.md`
- current reader and runtime-candidate proof surfaces:
  `generated/eval_catalog.min.json`,
  `generated/eval_capsules.json`,
  `generated/eval_sections.full.json`,
  `generated/runtime_candidate_template_index.min.json`,
  `generated/runtime_candidate_intake.min.json`,
  and `generated/phase_alpha_eval_matrix.min.json`
- proof posture and runtime-artifact bridge docs:
  `docs/PROGRESSION_EVIDENCE_MODEL.md`,
  `docs/SELF_AGENT_CHECKPOINT_EVAL_POSTURE.md`,
  `docs/RECURRENCE_PROOF_PROGRAM.md`,
  `docs/TRACE_EVAL_BRIDGE.md`,
  `docs/EVAL_RESULT_RECEIPT_GUIDE.md`,
  and `docs/RUNTIME_BENCH_PROMOTION_GUIDE.md`

Roadmap drift is an eval-layer risk: if this file falls back to bootstrap-only
language while the repository publishes continuity, checkpoint, diagnosis, and
catalog surfaces, readers may over- or under-read the proof boundary. Keep the
roadmap current while preserving the rule that `aoa-evals` proves only bounded
claims.

## Guiding priorities

Order matters.

This repository should prioritize:
1. bounded proof surfaces for agent behavior
2. portable comparison and regression discipline
3. human-readable score and verdict semantics
4. eval integrity and anti-theater safeguards
5. reusable public bundles over local benchmark spectacle
6. trace-aware workflow evaluation without forcing one exact tool path by default

In practice, this means the repo should prefer a smaller number of strong eval bundles
rather than a fast flood of weak ones.

## Roadmap structure

The roadmap is organized by capability layers rather than by calendar time.
A later layer may begin before an earlier one is fully complete,
but earlier layers should remain the priority until their public shape is stable.

## Research-guided intake lanes

Current external intake should be organized into three main lanes.

### Lane A: agent-first eval philosophy

Priority inputs:
- Anthropic agent-evals methodology
- OpenAI agent-evals and evaluation best-practice guidance
- Inspect core concepts where they reinforce bounded review and scoring discipline

Expected repository outputs:
- stronger vocabulary for task, outcome, grader, scorer, harness, suite, and blind spots
- clearer score and verdict interpretation docs
- clearer workflow-versus-artifact separation

### Lane B: trace, trajectory, and tool-use evaluation

Priority inputs:
- OpenAI trace grading and grader patterns
- Inspect logs and rescoring model
- LangSmith trajectory evaluation ideas
- MLflow trace-aware scoring and tool-correctness ideas

Expected repository outputs:
- workflow bundles that evaluate outcome and path separately where needed
- trajectory-aware review guidance
- log-versus-score separation that remains human-readable

### Lane C: portable bundle and report contracts

Priority inputs:
- OpenAI eval-run and testing-criteria ideas
- Inspect eval-set and scorer separation
- Braintrust remote-eval and baseline-diff ideas
- Langfuse experiment and summary-result object ideas

Expected repository outputs:
- cleaner scorer contracts
- stronger report summary contracts
- more explicit baseline and comparison semantics
- better fixture replacement and portability rules

### Specialized sidecar branch

After the core lanes stabilize, the repository should also draw from:
- Promptfoo for agent red-team and boundary attack patterns
- DeepEval and DeepTeam for selective metric and adversarial ideas
- AWS Agent Evaluation and AgentCore for evaluator hooks and trace normalization concepts

Likely bundle direction from this branch:
- boundary red-team evals that stay distinct from the core workflow-proof bundles

---

## Layer 0: Public bootstrap and repository spine

Goal: create a coherent public skeleton that already teaches the right evaluation discipline.

Includes:
- repository doctrine
- architecture and philosophy docs
- eval rubric and review guide
- portable-boundary guidance
- eval template and starter selection surface
- starter schemas and local validator
- first starter eval bundles

Exit signals:
- a new contributor can understand what an eval bundle is
- the repository can reject malformed bundles locally
- the public docs already discourage benchmark theater and inflated claims
- at least two starter bundles exist and validate cleanly

Current emphasis:
- keep the public shape honest and compact
- prefer clarity over breadth

---

## Layer 1: Agent workflow proof canon

Goal: establish the first canonical cluster of agent-first eval surfaces.

These bundles should focus on how agents behave during bounded work,
not merely on the polish of final artifacts.

This layer should deliberately mix two bundle shapes:
- composite workflow bundles that check whether a bounded workflow still holds together end to end
- diagnostic bundles that isolate one nearby failure surface so regressions are easier to interpret

The repo should name which shape a bundle belongs to before treating nearby bundles as distinct.

Priority starter families:
- bounded change quality:
  composite workflow integrator for non-trivial change tasks; may observe scope drift, fake verification, or reporting drift together, without pretending to isolate the root cause
- approval and authority boundary adherence:
  diagnostic boundary surface for permission, approval, and authority classification; this is about whether the agent is allowed to act, not whether the task itself is underspecified
- verification honesty:
  diagnostic workflow surface for whether claimed verification matches performed verification, skipped checks, and named limits
- scope drift detection:
  diagnostic boundary surface for silent widening, narrowing, or reshaping of the requested work surface
- ambiguity handling:
  diagnostic stress surface for incomplete, conflicting, or underspecified task meaning; this should exclude authority ambiguity already covered by approval-boundary bundles
- trace-to-outcome separation:
  workflow surface that keeps final outcome judgment separate from path judgment when both matter
- tool-trajectory discipline:
  workflow surface for tool-use path quality only when the path itself is part of the bounded claim

Desired outcomes:
- the repo can check whether an agent stayed scoped
- the repo can check whether an agent used real verification rather than symbolic confidence
- the repo can check whether an agent handled ambiguous authority honestly
- the repo can inspect a workflow trace without pretending there is always one exact correct path
- the repo can judge outcome separately from process when that distinction matters
- the repo can check whether a workflow claim is supported without pretending to measure all quality

Exit signals:
- at least 5 strong workflow or boundary bundles exist
- these bundles are clearly distinct and not blurred into one mega-benchmark
- each bundle has bounded interpretation guidance and named blind spots
- public users can tell which bundle to run for which claim

Current public posture:
- the one-run starter tranche now mixes portable composite, diagnostic, and artifact starters with bounded boundary, stress, trace/path, and integrity surfaces
- `aoa-witness-trace-integrity` now opens the first draft witness-facing workflow proof surface without pretending runtime instrumentation is already in place
- the next priority is comparison and regression discipline rather than more one-run starter naming

Important discipline:
- workflow quality should not be collapsed into a single generic score
- bundles should expose different failure modes rather than flatten them
- composite bundles should not masquerade as diagnostic bundles
- diagnostic bundles should state what they intentionally do **not** evaluate so nearby bundles stay distinct

---

## Layer 2: Comparison and regression spine

Goal: make `aoa-evals` useful for repeated agent improvement rather than one-off demos.

This layer turns the repo from proof sketch to proof instrument.

Priority surfaces:
- same-task regression evals
- before-vs-after comparison bundles
- policy-surface comparison bundles
- baseline-mode guidance
- compact summary report contracts
- repeated-run guidance for surfaces where one pass is not enough

Desired outcomes:
- an agent update can be checked against a fixed bounded surface
- regressions become visible even when outputs still look polished
- style changes are less likely to be mistaken for capability growth
- reports remain compact enough for human review and agent consumption

Exit signals:
- at least one stable baseline eval exists
- report summaries have a schema and predictable interpretation contract
- comparative evals can be run without hiding the baseline logic
- readers can tell the difference between improvement, regression, and noisy variation

Current public posture:
- `aoa-regression-same-task` is now the first public `baseline` starter for frozen same-task regression
- `aoa-output-vs-process-gap` remains the draft peer-comparison bridge rather than a baseline-default comparator
- `aoa-longitudinal-growth-snapshot` now has materialized repeated-window fixture, runner, and schema-backed report artifacts while remaining a draft movement surface
- `aoa-eval-integrity-check` should travel as the bounded sidecar whenever public comparison wording changes materially

Important discipline:
- baseline creation should be conservative
- no bundle should be called baseline if repeatability or score semantics are still muddy

---

## Layer 3: Artifact-quality and process-quality separation

Goal: separate polished output quality from underlying workflow discipline.

Many agent systems get over-credited because outputs look good even when process quality is weak.
This layer should make that gap visible.

Current public bridge:
- `aoa-artifact-review-rubric` as the portable artifact-quality anchor
- `aoa-compost-provenance-preservation` as the draft provenance-preserving compost artifact starter
- `aoa-output-vs-process-gap` as the first public artifact-versus-process bridge surface
- first materialized paired proof artifacts across those surfaces plus `aoa-bounded-change-quality` as the portable workflow anchor through a shared fixture family, runner contracts, and schema-backed report examples

Priority surfaces:
- artifact review rubric bundles
- output-vs-process gap evals
- report-quality versus verification-quality distinction
- code diff review bundles that remain bounded and human-checkable

Desired outcomes:
- the repo can tell when an artifact is impressive but process discipline is weak
- the repo can tell when a workflow was disciplined even if the final artifact is only modest
- artifact scoring can be compared against process scoring without pretending they are the same thing

Exit signals:
- at least one artifact eval and one workflow eval are explicitly used together for a bounded claim
- public docs make the separation between artifact quality and process quality obvious
- eval results resist the common trap of rewarding style over substance

Important discipline:
- artifact evals must remain bounded and interpretable
- raw aesthetic or taste-heavy review should not masquerade as objective proof

---

## Layer 4: Fixture and scorer infrastructure

Goal: make bundles more reusable, portable, and auditable.

At this stage the repo should start growing shared infrastructure,
but only after the proof philosophy is already stable.

Priority surfaces:
- shared fixture conventions
- shared scorer helpers
- report schemas and summary builders
- local runner helpers
- fixture replacement contracts for portable bundles
- log and rescore conventions

Desired outcomes:
- bundles can reuse shared parts without becoming opaque
- fixture families become easier to compare and maintain
- scorers can be audited as bounded public logic
- portable bundles can travel without dragging private project assumptions behind them

Exit signals:
- at least one shared scorer is used by more than one bundle
- at least one fixture family is reused across multiple evals
- bundle-local meaning remains readable even when shared infrastructure grows
- infrastructure helpers do not hide the proof contract from human reviewers

Important discipline:
- shared infrastructure should reduce repetition, not bury meaning
- if reuse makes a bundle harder to understand, the abstraction is too expensive

---

## Layer 5: Longitudinal growth surfaces

Goal: make the repository useful for measuring agent development across repeated windows.

This is where `aoa-evals` becomes a true growth organ rather than a collection of bounded checks.

Current public surface:
- `aoa-longitudinal-growth-snapshot` as the draft starter for repeated-window movement on one named workflow surface, now with its first materialized repeated-window proof artifacts

Priority surfaces:
- longitudinal growth snapshot bundles
- repeated-window comparison protocols
- bounded trend summaries
- explicit uncertainty language for movement across time

Desired outcomes:
- the repo can support claims like “this agent improved on this bounded surface”
- growth signals remain modest and evidence-backed
- long-term summaries resist turning into myth-making dashboards

Exit signals:
- at least one longitudinal bundle exists and has interpretation guidance that resists overclaiming
- repeated-window summaries remain understandable to humans
- the repo can distinguish temporary spikes from more stable directional change

Important discipline:
- longitudinal movement should be described with caution
- the repo should prefer bounded growth signals over grand capability narratives

---

## Layer 6: Eval integrity and anti-gaming layer

Goal: make the repository trustworthy even when agents and operators become better at gaming surfaces.

At scale, evals must not only measure agents.
They must also defend themselves.

Current public surface:
- `aoa-eval-integrity-check` as the bounded starter for starter-bundle coherence and public-surface drift review

Priority surfaces:
- eval integrity checks
- score semantics review
- anti-reward-hacking notes
- false-pass detection surfaces
- semantic reviews for nearby bundles that may blur together

Desired outcomes:
- the repo can inspect whether its own bundles still tell the truth coherently
- score inflation and verdict overreach become easier to catch
- public bundles become harder to game accidentally or intentionally

Exit signals:
- at least one eval checks another eval's verdict surface or coherence
- semantic review is used to prevent nearby bundles from collapsing into one vague category
- bundle notes explicitly mention gaming risks where relevant

Important discipline:
- no eval should be treated as permanently trustworthy by default
- proof surfaces should themselves remain review targets

---

## Layer 7: Canonical public proof layer

Goal: establish a small set of default eval bundles that can be recommended by default for bounded claim classes.

This is a maturity layer, not a scale layer.
The repo should reach it slowly.

Priority surfaces:
- canonical workflow evals
- canonical boundary evals
- canonical baseline comparison surfaces
- canonical artifact-vs-process cross-check surfaces

Desired outcomes:
- the repo has a few public defaults that feel earned, not merely declared
- users can choose a default proof surface for a bounded claim class without reading the whole corpus first
- canonical bundles have stronger validation, portability, and interpretation discipline than the rest of the repo

Exit signals:
- the first canonical bundle is promoted with a strong default-use rationale
- canonical promotion reviews are explicit and reviewable
- canonical status remains rare and meaningful

Important discipline:
- canonical should remain a scarce status
- promotion must be evidence-backed, not style-backed

---

## Cross-cutting workstreams

These workstreams matter across all layers.

### A. Agent-readable surfaces

The repo should remain human-readable first,
but it also needs clean surfaces for agent consumption.

Desired direction:
- compact manifests
- predictable report schemas
- deterministic bundle layout
- later generated selection surfaces

Constraint:
- agent-readability must not erase human reviewability

### B. Public safety and sanitization

Every layer must preserve:
- public-safe fixtures
- no secret-bearing traces
- no hidden infrastructure assumptions in public defaults
- honest disclosure when a bundle is still local-shaped

### C. Bundle distinctness

As the repo grows, nearby bundles may blur together.
The repo should actively review whether apparently different evals still have distinct bounded jobs.

### D. Small strong corpus over fast wide corpus

The repository should keep preferring:
- 3 strong bundles over 12 vague ones
- 1 trustworthy baseline over many unstable comparisons
- 1 honest report contract over 5 flashy dashboards

---

## What should happen next

Near-term next moves should use the new docs spine to shape the next agent-first surfaces and support artifacts.

Highest-priority additions:
- keep the newly materialized same-task baseline and repeated-window comparison flows conservative and non-theatrical
- extend the newly materialized artifact/process pairing beyond its first shared fixture family, runner contracts, and schema-backed report slice
- keep `aoa-regression-same-task` conservative as the first public baseline starter rather than promoting other comparison surfaces by association
- keep the repeated-window fixture and report contracts on `aoa-longitudinal-growth-snapshot` aligned with cautious movement wording rather than inflating them into stronger status claims
- field-test the newly materialized witness/compost pilot proof surfaces without inflating them into runtime-instrumentation or canon claims before `abyss-stack` is actually ready
- keep `aoa-scope-drift-detection` conservative as a materialized bounded diagnostic starter rather than promoting it by association
- keep `aoa-ambiguity-handling` conservative as a materialized bounded diagnostic starter rather than promoting it by association
- keep `aoa-approval-boundary-adherence` conservative as a materialized bounded diagnostic starter rather than promoting it by association
- keep `aoa-trace-outcome-separation` conservative as a materialized bounded diagnostic starter rather than promoting it by association
- keep `aoa-tool-trajectory-discipline` conservative as a materialized bounded diagnostic starter rather than promoting it by association
- field-test the newly materialized recurrence-aware proof surfaces without inflating them into broad safety or capability claims, and keep them outside the current starter set while their case families and report artifacts mature
- field-test the newly materialized memo recall, contradiction, and writeback-act pilot surfaces without inflating them into general memory quality, permission policy, canon-promotion claims, future scar proof, retention proof, or live memory-ledger readiness

Next likely cross-surface candidate after the current public starter set:
- `aoa-return-anchor-integrity`, `aoa-long-horizon-depth`, `aoa-memo-recall-integrity`, `aoa-memo-contradiction-integrity`, and `aoa-memo-writeback-act-integrity` as the materialized draft recurrence-and-memo pilot layer

Starter posture remains conservative:
- No additional planned starter bundles are currently named publicly.

Recent repo hardening now in place:
- local dev dependencies in `requirements-dev.txt`
- validator tests under `tests/`
- evidence-path validation for manifest evidence entries
- baseline-readiness validation for baseline-mode bundles
- starter-table parity between `EVAL_INDEX.md` and `EVAL_SELECTION.md`
- starter example-report and integrity-check expectations for current public starters
- status-specific evidence expectations for promotion-shaped statuses
- bounded-status support-note expectations for approve/defer review outcome plus failure-versus-readout distinction
- comparative-summary support-note expectations for comparison-contract clarity
- roadmap parity checks for current public surface references and absence-note sync

Next repository hardening steps:
- keep docs, index, selection, and template aligned to the canonical docs spine
- field-test the materialized memo recall, contradiction, and writeback-act pilots against wider `aoa-memo` guardrail surfaces before naming promotion, permissions, merge bundles, future scar proof, retention proof, or live memory-ledger readiness
- keep distinctness notes ready whenever a newly named starter bundle is introduced so nearby evals do not collapse semantically before they ship

---

## Long-term direction

If this roadmap succeeds, `aoa-evals` should become:
- a public canon of bounded proof surfaces for agents
- a trustworthy regression and comparison layer
- a growth instrument that resists self-deception
- a human-readable and agent-readable proof surface
- a repository where quality claims become harder to fake and easier to check

That is enough.
That is already a strong future.
