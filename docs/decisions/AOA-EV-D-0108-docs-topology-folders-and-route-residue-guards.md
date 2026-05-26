# Docs Topology Folders And Route Residue Guards

- Decision ID: AOA-EV-D-0108
- Status: Accepted
- Date: 2026-05-25
- Owner surface: `docs/README.md`, `docs/architecture/`, `docs/guides/`, `docs/operations/`, `docs/architecture/ROUTE_RESIDUE_GUARDS.md`

## Index Metadata

- Original date: 2026-05-25
- Surface classes: root/topology, proof topology, validation guard
- Mechanic parents: none
- Guard families: route residue
- Posture: active rationale

## Context

The first decision-index slice made decision lookup metadata-backed and removed
the largest manual overload from `docs/decisions/README.md`. The next pressure
was the flat `docs/*.md` district itself: authority maps, proof-reading guides,
operations, preserved root reference material, and validation guard detail all
sat beside each other.

That flat layout was cheap for path length but expensive for agents. A reader
had to infer whether a file was an authority map, a guide, an operational
procedure, or a guard contract from a long filename and surrounding prose.

`docs/architecture/PROOF_TOPOLOGY.md` also carried both the authority-class map
and the detailed route-residue guard contract. That made topology heavier than
its main job: classifying the surface and routing to stronger owners.

## Options Considered

- Keep the flat `docs/*.md` district and rely on `docs/README.md` to explain the
  difference.
- Move files into subfolders but leave validation as loose prose.
- Move files into role folders and add a validator-backed docs topology
  contract.

## Decision

`docs/` now keeps only the docs route card, the short route chooser, and owned
subdirectories:

- `docs/architecture/` owns authority and topology surfaces.
- `docs/guides/` owns proof-reading guides.
- `docs/operations/` owns release, quest-integration, closeout/writeback, and
  preserved root-reference docs.
- `docs/decisions/` owns durable rationale and generated lookup indexes.

The detailed route-residue guard contract moves to
`docs/architecture/ROUTE_RESIDUE_GUARDS.md`. `PROOF_TOPOLOGY.md` keeps the
authority-class map and a short guard-family map that links to the contract.

`docs/architecture/topology_contract.yaml` records the expected docs layout,
and `scripts/validators/docs_topology.py` validates the file placement and
route chooser contract through `scripts/validate_repo.py`.

## Rationale

The new shape gives agents a positive route before they read content: authority
map, guide, operation, or rationale. It reduces context cost without deleting
proof law, because the guard details still have an owned contract surface and
validator coverage.

The topology contract keeps the move from becoming a cosmetic folder shuffle.
If a future root docs file appears without an owner folder, validation rejects
it before the docs district becomes flat again.

## Consequences

- Positive: `docs/README.md` is a short route chooser instead of a broad anchor
  catalog.
- Positive: `PROOF_TOPOLOGY.md` focuses on authority classes.
- Positive: route-residue details remain explicit and validator-backed.
- Tradeoff: repo-relative docs paths moved and downstream references had to be
  refreshed.
- Tradeoff: generated/read-model surfaces that carry docs paths must be checked
  when source references move.

## Current Applicability

As of 2026-05-25:

- Still valid: source eval bundles own proof meaning; generated readers remain
  weaker than source surfaces.
- Changed: root docs are classified by folder role instead of flat filename.
- Superseded by: none.

## Boundaries

This decision does not make docs guides stronger than bundle-local `EVAL.md`
and `eval.yaml`.

It does not move mechanic-owned payload docs into root docs. Mechanic payload
guidance stays under the owning mechanic or part.

## Validation

Use the docs topology validator through the root repository validator, plus the
semantic AGENTS check and focused validator tests named in `docs/AGENTS.md`.
