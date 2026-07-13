# AoA Evals MCP Access Plane Contract

- Decision ID: AOA-EV-D-0110
- Status: Accepted
- Date: 2026-05-25
- Owner surface: `docs/architecture/AOA_EVALS_MCP_CONTRACT.md`

## Index Metadata

- Original date: 2026-05-25
- Surface classes: root/topology, generated/readout, validation guard, boundary/runtime/sibling
- Mechanic parents: audit, boundary-bridge, cross-parent
- Guard families: generated/report/receipt/runtime, sibling and boundary, decision index/read-model
- Posture: active rationale

## Context

`aoa-evals` already owns the bounded proof canon, generated proof readers, and
runtime-candidate posture. OS Abyss also needs agents to use those surfaces
without flattening the whole repository into prompt context.

The pressure is not to create a general eval runner. The pressure is to give
Codex and OS Abyss a small `aoa_evals` access plane that can answer which eval
applies, what a bundle claims, what evidence shape is required, and which
candidate runtime evidence template fits.

## Options Considered

- Keep `aoa-evals` repo-only: simple, but agents keep loading broad docs and
  generated readers by hand.
- Let `abyss-stack` define the eval MCP surface: runnable, but it would move
  proof-contract authority into the runtime owner.
- Define the MCP contract in `aoa-evals`, then let `abyss-stack` implement the
  runnable stdio service as an access-plane adapter.

## Decision

Choose the third option.

`aoa-evals` defines the `aoa_evals` MCP contract as an authority surface for
resources, tools, prompts, owner split, non-goals, validation route, and
candidate-only runtime evidence posture.

`abyss-stack` implements the runnable service under
`mcp/services/aoa-evals-mcp/` because MCP services are runtime access planes.
The stack service reads source/generated `aoa-evals` surfaces or an approved
runtime mirror, but it does not own proof meaning.

## Rationale

This route keeps the proof organ convex. Source bundles still own claims,
generated readers stay deterministic companions, runtime evidence stays
candidate-only, and MCP becomes a compact route into those surfaces instead of
a new proof layer.

It also matches the existing stack topology: `abyss-stack` owns MCP service
packages, while sibling repositories keep the meaning the service exposes.

## Consequences

- Positive: agents can select, inspect, expand, and shape evidence packets
  through a compact MCP surface.
- Positive: the service can be wired into the Codex plane as `aoa_evals`
  without making `8Dionysus` or `abyss-stack` proof authority.
- Tradeoff: two repositories must stay aligned: contract in `aoa-evals`,
  implementation in `abyss-stack`.
- Follow-up: later exposure beyond stdio, verdict computation, receipt
  publication, or source mutation requires a new decision.

## Current Applicability

As of 2026-05-25:

- Still valid: `aoa-evals` owns proof authority and the MCP contract.
- Changed: the Codex plane may now route to `aoa_evals` after stack service
  implementation and renderer-based wiring.
- Superseded by: none.

## Review Log

### 2026-05-25 - Initial access-plane contract

- Previous assumption: agents read `aoa-evals` directly from repo surfaces.
- New reality: OS Abyss needs a stable MCP route that keeps prompt context
  compact and proof authority local to `aoa-evals`.
- Reason: MCP should expose bounded proof selection and inspection without
  becoming an eval runner or verdict engine.
- Source surfaces updated:
  - `docs/architecture/AOA_EVALS_MCP_CONTRACT.md`
  - `docs/architecture/PROOF_TOPOLOGY.md`
  - `docs/architecture/AGENT_INDEX.md`
  - `docs/README.md`
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

## Boundaries

Future agents must not infer that `aoa_evals` may run general evals, compute
verdicts, publish receipts, promote bundles, mutate source files, or treat
generated/runtime/MCP output as stronger than bundle-local `EVAL.md` and
`eval.yaml`.

Future agents must not infer that `abyss-stack` owns proof meaning because it
owns the runnable MCP package.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
