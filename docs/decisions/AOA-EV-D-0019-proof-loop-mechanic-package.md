# Proof Loop Mechanic Package

- Decision ID: AOA-EV-D-0019
- Status: Accepted
- Date: 2026-05-19
- Owner surface: `mechanics/proof-loop/`

## Index Metadata

- Original date: 2026-05-19
- Surface classes: mechanic package
- Mechanic parents: proof-loop
- Guard families: none
- Posture: active rationale

## Context

The strategic plan names Phase 8 as the active proof loop:

`pick proof question -> inspect source bundle -> expand fixture/report contract -> select candidate evidence -> review against bundle -> publish bounded report -> emit optional receipt`

Earlier slices created the topology needed for this route: proof-object,
proof-infra, audit, boundary-bridge, publication-receipts,
questbook, generated readers, decisions, and route cards. The loop is now
real enough to route locally, but still easy to misread as a new proof
authority above those packages.

## Options Considered

- Leave the loop only in `DESIGN.md` and `ROADMAP.md`.
- Add a broad guide under `docs/` that narrates the loop.
- Add `mechanics/proof-loop/` as the operation route that coordinates existing
  mechanics without owning their source truth.

## Decision

Create `mechanics/proof-loop/` with `README.md` and `AGENTS.md`.

The package owns the route shape for one local proof loop. It does not own
bundle meaning, support contracts, runtime evidence, sibling-owner truth,
review outcomes, reports, or receipts. Those remain with their existing
owner routes.

In short: it does not own bundle meaning.

## Rationale

The loop is a repeatable proof-layer operation, not just documentation prose.
It needs a nearby route card so a low-context agent can follow the whole local
path without connecting `aoa-evals` to live runtime, hidden dispatch, or
sibling authority.

A package is the smallest durable home because the loop coordinates several
existing mechanics. A plain docs guide would be easier to ignore; a generated
surface would be too weak to own route semantics.

## Consequences

- Positive: Phase 8 becomes locally followable from `aoa-evals`.
- Positive: each loop step points to its stronger owner package.
- Tradeoff: there is one more package, so validators must keep it from becoming
  a decorative or sovereign meta-layer.
- Follow-up: future usability work can add examples or checklists only when
  they preserve the same owner split.

## Boundaries

This decision does not create runtime dispatch, live scheduling, benchmark
ranking, global trust scoring, autonomous-self proof, or hidden proof
acceptance.

It does not move `evals/`, generated readers, runtime candidate readers,
reports, receipts, sibling refs, or quest source records.

It does not allow receipts, generated readers, candidate evidence, or sibling
refs to outrank bundle-local review.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
