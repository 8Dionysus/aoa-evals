# Organ Access Central Proof Gate

- Decision ID: AOA-EV-D-0249
- Status: Accepted
- Date: 2026-07-25
- Owner surface: `docs/architecture/AOA_EVALS_MCP_CONTRACT.md`

## Index Metadata

- Original date: 2026-07-25
- Surface classes: proof contract, MCP boundary, admission evidence
- Mechanic parents: proof-object, proof-loop, audit, boundary-bridge
- Guard families: bounded proof, authority boundary, effect denial, rollback
- Posture: active rationale

## Context

OS Abyss is moving from individually wired MCP servers to an owner-bounded
organ access fabric. The current runtime can show packages, processes,
listeners, schemas, and successful calls, but those observations do not prove
owner meaning, grounded freshness, effect isolation, acceptance, or rollback.
A private registry likewise cannot prove its own admission claims.

The proof organ needs one central route for cross-owner access-plane evidence
without becoming the registry, runtime, workflow engine, or acceptance owner.

## Options Considered

- Let each package validator declare its organ admitted.
- Let the SDK registry or `abyss-stack-mcp` aggregate observations into one
  top-level health verdict.
- Define a central, bounded, capability- and policy-plane proof route in
  `aoa-evals`, then require a separate acceptance-owner and control-plane
  receipt before admission changes.

## Decision

Choose the third option.

`aoa-evals` owns central bounded proof for the organ access fabric. The proof
unit is one exact organ capability on one policy plane, source revision,
package/deploy identity, consumer, protocol pair, and observation window.

For a future live pair-specific claim to be admissible, its named source bundle
must explicitly check the applicable surfaces below:

- correct owner and primitive selection;
- argument and owner-specific schema conformance;
- source, package, deploy, process, endpoint, registry, and
  consumer-observed-schema compatibility;
- authority ceiling and owner-specific payload preservation;
- grounded freshness, stale-readable, and stale-blocked behavior;
- deterministic denial and read-to-effect credential isolation;
- prompt, tool, resource, and output injection resistance;
- confused-deputy and cross-tool source-to-sink boundaries;
- context footprint, catalog selection, cold and warm latency, payload limits,
  timeout, concurrency, and cancellation;
- receipt and trace continuity across direct and cross-organ handoffs;
- rollback behavior;
- consumer and model diversity where the claim depends on either.

This decision does not itself provide that live suite. The currently landed
`aoa-organ-access-admission-integrity` bundle validates packet structure,
axis-specific evidence and revision slots, freshness windows, insufficient
evidence, and negative admission inferences only. All other items above remain
requirements for a separately named live bundle rather than current behavior.

Evidence is represented as an independent maturity vector:
`declared`, `owner_reviewed`, `packaged`, `exported`, `deployed`,
`process_alive`, `endpoint_ready`, `registry_indexed`,
`consumer_registered`, `schema_observed`, `call_succeeded`,
`result_grounded`, `freshness_satisfied`, `owner_accepted`,
`cross_organ_proven`, and `rollback_proven`.

Every asserted axis carries timestamp, evidence ref, revision, and expiry or
freshness policy. One axis cannot be inferred from another. A green package
test, process, endpoint, schema list, call, readiness packet, MCP result, or
central eval cannot by itself yield `owner_accepted` or `admitted`.

Proof results are candidate inputs to the named acceptance owner. The
acceptance owner decides durable source, memory, runtime, or external truth.
The SDK control plane may update admission only from an explicit acceptance
receipt. `aoa-evals` does not mutate the private registry, activate a service,
execute a runtime plan, accept memory, apply source changes, or authorize
external effects.

Read, candidate, internal-effect, and external-effect planes require separate
proof. A lower-effect pass cannot support a higher-effect admission.

The current `aoa_evals` MCP read and local-write capabilities remain subject to
the same law. Existing shared loopback authentication is transport evidence,
not effect-isolation proof. Its write-side tools remain candidate/shadow until
separate process and credential contours, denial tests, owner acceptance, and
rollback proof exist.

## Rationale

Keeping proof bounded prevents a convenient status surface from becoming an
authority merger. Independent maturity axes preserve the difference between
installation, reachability, grounded results, acceptance, and recoverability.
The explicit acceptance handoff lets evals remain the proof owner while each
domain owner retains durable truth.

## Consequences

- Owner-local tests remain necessary but are not sufficient for admission.
- The central suite needs cross-repository fixtures and runtime observations
  without importing sibling authority.
- Admission packets must carry evidence and expiry for every claimed axis.
- Effectful planes require negative authorization and rollback scenarios, not
  only successful calls.
- A not-yet-proven organ can remain shadow without weakening the global proof
  gate.

## Current Applicability

As of 2026-07-25:

- Still valid: bundle-local source proof and review remain stronger than
  generated readers and MCP output.
- Changed: organ-access evidence has an executable bounded source packet
  contract and negative-inference suite in
  `evals/boundary/aoa-organ-access-admission-integrity/`.
- Not yet established: live pair-specific owner, runtime, registry, consumer,
  denial, acceptance, cross-organ, and rollback proof.
- Superseded by: none.

## Review Log

### 2026-07-25 - Establish organ-access proof boundary

- Previous assumption: package-local MCP validation and existing candidate
  evidence routes were sufficient navigation.
- New reality: cross-owner admission needs policy-plane proof, independent
  maturity axes, acceptance receipts, and rollback evidence.
- Reason: runtime reachability and registry presence cannot prove authority or
  grounded freshness.
- Source surfaces updated:
  - `docs/architecture/AOA_EVALS_MCP_CONTRACT.md`
  - `docs/architecture/PROOF_TOPOLOGY.md`
  - `evals/boundary/aoa-organ-access-admission-integrity/`
- Validation: use the exact bundle commands recorded in
  `evals/boundary/aoa-organ-access-admission-integrity/runners/contract.json`
  plus the docs, decision-index, and source-fast routes owned by their nearest
  `AGENTS.md` cards.

## Boundaries

Future agents must not infer that `aoa-evals` owns the private registry,
runtime lifecycle, owner payload meaning, durable memory, source acceptance,
or effect authorization. They must not infer higher maturity or effect
authority from a lower axis or policy-plane result.

## Validation

Regenerate decision indexes, run root/docs semantic validation, and execute the
exact scenario and source-bundle argv recorded in
`evals/boundary/aoa-organ-access-admission-integrity/runners/contract.json`
through the command-owning `evals/AGENTS.md` route.

These commands validate the source packet contract, not live organ admission.
Any stronger proof run must carry exact owner, runtime, registry, consumer, and
protocol revisions, preserve the same interpretation limits, and route to the
named acceptance owner.
