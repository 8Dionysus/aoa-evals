# SDK Routing Reference Succession

- Decision ID: AOA-EV-D-0250
- Status: Accepted
- Date: 2026-07-27
- Owner surface: `mechanics/boundary-bridge/parts/compatibility-map/docs/SIBLING_PROOF_REFS.md`

## Index Metadata

- Original date: 2026-07-27
- Surface classes: boundary/runtime/sibling, CI compatibility, proof reference
- Mechanic parents: boundary-bridge, antifragility, audit
- Guard families: sibling and boundary, owner succession, consumer-zero
- Posture: active rationale

## Context

`aoa-sdk` became the canonical routing producer while preserving
`aoa-routing` as a compatibility namespace and predecessor provenance source.
`aoa-evals` still checked out the predecessor in its latest-sibling canary and
used predecessor paths for current stress-recovery and runtime-integrity proof
inputs.

That made a retired producer checkout operationally necessary for current
proof-reference validation. Removing every `repo:aoa-routing/...` string,
however, would also erase honest references from historical decisions and
accepted provenance.

## Options Considered

- Continue checking out `aoa-routing` and resolving both current and historical
  references against it.
- Rewrite every predecessor-qualified reference as an `aoa-sdk` reference,
  including historical provenance.
- Route current proof inputs and strict sibling checks to `aoa-sdk`, while
  preserving `aoa-routing` as a syntax-checked, reference-only provenance
  namespace.

## Decision

Choose the third option.

Current route hints, reentry contracts, routing consumer contracts, and
strict latest-sibling compatibility checks route to `aoa-sdk`.
`aoa-routing` is removed from the canary checkout matrix and active root map.

Historical `repo:aoa-routing/...` references remain parseable as
reference-only provenance. They do not require a predecessor checkout and do
not pass through current path-existence or anchor validation. New current
proof inputs must not use that exception.

## Rationale

This removes an obsolete runtime dependency without rewriting history.
`aoa-sdk` current paths receive the strong checkout-backed compatibility check,
while predecessor-qualified material stays visibly weaker and cannot be
mistaken for current producer truth.

The split also preserves the existing sibling-reference law: `aoa-evals`
decides whether a reference may support local bounded review, while the sibling
repository retains meaning and acceptance authority.

## Consequences

- Positive: the latest-sibling workflow no longer pays for an `aoa-routing`
  checkout, and current routing refs are verified against their canonical
  producer.
- Tradeoff: historical predecessor refs receive syntax and provenance review,
  not current path-existence proof.
- Follow-up: consumer-zero evidence should scan current proof inputs
  independently from preserved historical refs before any compatibility-exit
  or archive proposal.

## Current Applicability

As of 2026-07-27:

- Still valid: repo-qualified sibling refs remain inputs below proof authority
  and sibling-owner acceptance.
- Changed: current routing refs and canary coverage route to `aoa-sdk`;
  `aoa-routing` is reference-only provenance.
- Superseded by: none.

## Review Log

### 2026-07-27 - Adopt SDK routing references

- Previous assumption: `aoa-routing` remained a current sibling producer that
  strict compatibility needed to check out.
- New reality: `aoa-sdk` owns the canonical routing producer and current
  consumer contracts.
- Reason: retaining the predecessor checkout adds cost and permits current
  proof refs to drift from their owner.
- Source surfaces updated:
  - `mechanics/boundary-bridge/parts/compatibility-map/docs/SIBLING_PROOF_REFS.md`
  - `mechanics/boundary-bridge/parts/latest-sibling-canary/config/sibling_canary_matrix.json`
  - `scripts/validators/root_context.py`
  - current stress-recovery and runtime-integrity reference examples
- Validation: use focused reference-parser and part tests, the latest-sibling
  canary against explicit sibling roots, root validation, and the repository
  release gate.

## Boundaries

This decision does not transfer eval verdict, runtime, or sibling source
authority into `aoa-sdk`. It does not make historical predecessor paths current
or path-verified. It does not authorize archive, deletion, compatibility-window
exit, or rollback retirement for `aoa-routing`.

## Validation

Regenerate and check decision indexes. Validate the stress-recovery,
artifact-hook, integrity-review, sibling-canary, source-fast, and full
repository surfaces with `AOA_SDK_ROOT` set to the admitted SDK source
checkout. Confirm separately that the active repository no longer requires
`AOA_ROUTING_ROOT` or an `aoa-routing` checkout.
