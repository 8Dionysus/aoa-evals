# Owner-Authored MCP Capability Profiles

- Decision ID: AOA-EV-D-0252
- Status: Accepted
- Date: 2026-08-01
- Owner surface: `docs/architecture/AOA_EVALS_MCP_CONTRACT.md`

## Index Metadata

- Original date: 2026-08-01
- Surface classes: MCP access plane, proof contract, capability declaration
- Mechanic parents: proof-object, boundary-bridge
- Guard families: bounded proof, authority boundary, candidate isolation, context economy
- Posture: active rationale

## Context

The historical `aoa_evals` MCP catalog combines discovery, generated readers,
runtime-candidate navigation, local-port inspection, and gated local-port
writes. That complete surface remains useful for portable compatibility, but
it is too broad to serve as one admitted organ capability. OS Abyss needs an
owner-authored declaration that separates proof discovery, request pressure,
and access to already issued bounded results without turning the MCP adapter or
the private registry into proof authority.

## Options Considered

- Admit the historical read and candidate catalogs as two coarse capabilities.
- Let `abyss-stack` or `aoa-sdk` derive narrower catalogs from implementation
  names without an `aoa-evals` owner source.
- Declare three exact owner capabilities and require the stack runtime to bind
  its exposed primitives to that declaration.

## Decision

Choose the third option.

`aoa-evals` declares `eval-discovery-read`, `eval-request-prepare`, and
`proof-result-read` in a schema-backed owner manifest. Discovery uses the read
process and `evals-read` credential. Request preparation uses the candidate
process and `evals-candidate` credential but produces only a non-persistent
typed request candidate. Proof-result access uses the read process and may
return only an already issued, indexed bundle-local report.

Proof issuance remains an owner-local eval and review operation. MCP does not
run the eval, compute the verdict, publish the report, accept evidence, issue a
receipt, or infer proof from a successful read. `abyss-stack` owns runtime
binding and `aoa-sdk` owns admission mechanics; neither owns the meaning of the
three capabilities.

## Rationale

The split gives consumers the smallest useful catalog for each task, makes
request pressure visibly candidate-only, and provides a precise read route for
an existing result without confusing report retrieval with proof production.
Keeping the manifest in the proof owner repository prevents runtime or control
plane code from silently widening the proof surface.

## Consequences

- Positive: capability admission can compare an exact owner declaration to an
  exact runtime catalog.
- Positive: discovery and proof-result reads no longer require loading the
  historical complete catalog.
- Tradeoff: the stack adapter must maintain an explicit binding and reject
  owner/runtime drift.
- Follow-up: deployment and admission remain blocked until the owner and stack
  changes land and a separately reviewed runtime contour proves the exact
  catalog, credential, freshness, result grounding, and rollback axes.

## Current Applicability

As of 2026-08-01:

- Still valid: AOA-EV-D-0110 keeps proof meaning in `aoa-evals` and the runnable
  adapter in `abyss-stack`.
- Changed: the historical complete catalog is now a compatibility surface, not
  the preferred admission unit.
- Superseded by: none.

## Review Log

### 2026-08-01 - Establish the three owner capability profiles

- Previous assumption: read and candidate process families were sufficiently
  narrow units for consumer exposure.
- New reality: admission and context economy need exact task-specific catalogs,
  while proof result retrieval needs a visible non-issuance boundary.
- Reason: a successful tool call or readable report cannot become proof,
  acceptance, or admission by association.
- Source surfaces updated:
  - `docs/architecture/AOA_EVALS_MCP_CONTRACT.md`
  - `docs/architecture/aoa_evals_mcp_capabilities.v1.json`
  - `docs/architecture/aoa_evals_mcp_capabilities.schema.json`
- Validation: schema validation, owner repository validation, decision-index
  parity, and stack adapter tests.

## Boundaries

Future agents must not infer that `proof-result-read` issues proof, that
`eval-request-prepare` persists or approves a request, or that any capability
declaration is itself admitted. They must not let discovery expand candidate
write roots or let a read/candidate credential authorize an effect.

## Validation

Validate the manifest against its schema, run the owner repository validation
and decision-index checks, and run the stack package tests that bind exact tool
and resource catalogs to the owner manifest. Live admission still requires
separate owner, runtime, consumer, freshness, proof, acceptance, and rollback
evidence.
