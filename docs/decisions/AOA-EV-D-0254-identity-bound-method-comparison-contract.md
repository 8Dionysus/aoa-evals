# Identity-Bound Method Comparison Uses a Draft Fixed-Baseline ABI

- Decision ID: AOA-EV-D-0254
- Status: Accepted
- Date: 2026-08-22
- Owner surface: `evals/comparison/fixed-baseline/aoa-identity-bound-method-comparison`

## Index Metadata

- Original date: 2026-08-22
- Surface classes: comparison contract, eval bundle, runner admission
- Mechanic parents: comparison-spine, proof-infra
- Guard families: identity parity, evidence class, claim boundary
- Posture: active rationale

## Context

The identity-bound real-session method-comparison direction reached only a
`partial_fit`: no matched real pairs were available, provisional episodes did
not provide reviewed parity, and cache, resource, and first-failure evidence
were not consistently observable. The existing runtime-latency bundle could
not lawfully absorb the missing apply ABI without changing its claim.

The owner needed a durable design surface that makes the identity tuple,
selection/apply fields, method pluralism, and non-observed states explicit
before future execution.

## Options Considered

- Option A: extend `aoa-runtime-latency-tradeoff` with real-session method IDs
  and retry/failure/resource admission.
- Option B: use the `peer-compare` part and represent each method as a peer
  surface.
- Option C: add a draft fixed-baseline bundle and paired readout whose
  baseline is the named legacy serial method while method IDs remain
  bundle-local observation routes.

## Decision

Choose Option C. Add
`aoa-identity-bound-method-comparison` under the existing fixed-baseline part
with a schema-backed `exact_fit` apply packet, a deterministic non-executing
runner, a manual case trace, and an explicit unmatched design report.

The bundle requires exact equality for the nine identity fields, known cache
and resource posture for an observed pair, explicit source digest and
environment identity, reviewed or controlled rows, and distinct metric state
semantics. Synthetic and controlled values remain accounting-only.

## Rationale

Option A would make the existing runtime tradeoff bundle imply a broader
real-session and method-effect claim. Option B would require existing eval
names as peer surfaces and would misrepresent method IDs as independent proof
bundles. The fixed-baseline route keeps one declared reference method while
allowing the new bundle to own its ABI and claim limit.

The runner is intentionally non-executing so that an apply command remains a
typed owner contract rather than a hidden runtime side effect. Generated
readers and the comparison-spine dossier remain derived/support surfaces.

## Consequences

- Positive: future owner-local applies have a complete identity/parity gate;
  unmatched, unknown, null, excluded, unobservable, and synthetic states stay
  visible.
- Tradeoff: the draft cannot answer a winner or effect question and needs a
  fresh reviewed cohort before any matched observation is meaningful.
- Follow-up: use owner-local apply only after the full packet is populated and
  separately review any live/runtime or central-proof route.

## Current Applicability

As of 2026-08-22:

- Still valid: source bundle meaning owns the bounded claim; generated readers
  and comparison readouts do not outrank it.
- Changed: a new draft bundle and fixed-baseline readout now hold the
  identity-bound comparison ABI.
- Superseded by: none.

## Review Log

### 2026-08-22 - Establish identity-bound comparison route

- Previous assumption: the nearest runtime tradeoff bundle could carry the
  method comparison pressure.
- New reality: the supplied evaluator direction lacked a complete identity,
  parity, and apply contract and had zero matched real pairs.
- Reason: preserve the bounded claim and make future selection/apply complete
  before method-effect interpretation.
- Source surfaces updated:
  - new bundle-local source, fixture, runner, report, and manual-case paths;
  - fixed-baseline comparison-spine readout and index route;
  - this decision note.
- Validation: bundle tests, schema checks, source validators, generated
  catalog/readers, and repository validation are required before landing.

## Boundaries

This decision does not admit a real-session cohort, issue a speedup or causal
effect, select a universal method winner, establish runtime health, authorize
deployment, create central proof, or accept the Goal. A green validator,
generated reader, PR, or wake receipt cannot replace those claims.

The `aoa-runtime-latency-tradeoff` anchor is a routing neighbor only; its
measurements and semantics are not imported into this bundle. Sibling
repositories, canonical dirty worktrees, runtime state, and human acceptance
remain outside this owner lane.

## Validation

The bundle-local test and schema route, `validate_repo.py`,
`validate_semantic_agents.py`, generated catalog/report/comparison checks, and
the source decision index generator cover this route. A successful validation
proves source and contract consistency only; it does not establish live
identity-bound evidence.
