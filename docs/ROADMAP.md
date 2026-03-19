# Roadmap

## Purpose

This roadmap describes how `aoa-evals` should grow from a strong public bootstrap into a trustworthy proof layer for agents.

The center of gravity is agent evaluation first.
Human readability remains mandatory.
The repository should help both:
- agents that need bounded evaluation surfaces they can run, compare, and report on
- humans who need to understand what those evals really prove and what they still do not prove

This roadmap is not about maximizing bundle count quickly.
It is about building a proof canon that can support honest growth.

## Guiding priorities

Order matters.

This repository should prioritize:
1. bounded proof surfaces for agent behavior
2. portable comparison and regression discipline
3. human-readable score and verdict semantics
4. eval integrity and anti-theater safeguards
5. reusable public bundles over local benchmark spectacle

In practice, this means the repo should prefer a smaller number of strong eval bundles
rather than a fast flood of weak ones.

## Roadmap structure

The roadmap is organized by capability layers rather than by calendar time.
A later layer may begin before an earlier one is fully complete,
but earlier layers should remain the priority until their public shape is stable.

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

Priority starter families:
- bounded change quality
- approval and authority boundary adherence
- verification honesty
- scope drift detection
- ambiguity handling

Desired outcomes:
- the repo can check whether an agent stayed scoped
- the repo can check whether an agent used real verification rather than symbolic confidence
- the repo can check whether an agent handled ambiguous authority honestly
- the repo can check whether a workflow claim is supported without pretending to measure all quality

Exit signals:
- at least 5 strong workflow or boundary bundles exist
- these bundles are clearly distinct and not blurred into one mega-benchmark
- each bundle has bounded interpretation guidance and named blind spots
- public users can tell which bundle to run for which claim

Important discipline:
- workflow quality should not be collapsed into a single generic score
- bundles should expose different failure modes rather than flatten them

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

Important discipline:
- baseline creation should be conservative
- no bundle should be called baseline if repeatability or score semantics are still muddy

---

## Layer 3: Artifact-quality and process-quality separation

Goal: separate polished output quality from underlying workflow discipline.

Many agent systems get over-credited because outputs look good even when process quality is weak.
This layer should make that gap visible.

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

Near-term next moves should focus on agent-first surfaces and repository coherence.

Highest-priority additions:
- `aoa-verification-honesty`
- `aoa-regression-same-task`
- `aoa-ambiguity-handling`
- `aoa-scope-drift-detection`
- `requirements-dev.txt`
- missing guidance docs linked from `docs/README.md`
- support artifacts for the starter bundles so local validation becomes meaningful rather than structural only

Next repository hardening steps:
- add tests for the validator
- add stronger manifest-to-index parity checks
- add support-artifact requirements per bundle maturity level
- add compact report examples for starter bundles

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
