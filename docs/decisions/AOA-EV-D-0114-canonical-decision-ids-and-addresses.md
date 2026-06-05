# Canonical Decision IDs and Addresses

- Decision ID: AOA-EV-D-0114
- Status: Accepted
- Date: 2026-05-26
- Owner surface: `docs/decisions/`

## Index Metadata

- Original date: 2026-05-26
- Surface classes: root/topology, generated/readout, validation guard
- Mechanic parents: none
- Guard families: decision index/read-model
- Posture: accepted canonical cleanup

## Context

`aoa-evals` already moved the heavy decision crosswalks out of
`docs/decisions/README.md` and into generated lookup indexes. That made the
lane agent-operable, but the active source paths still used short numbered
filenames such as `0001-root-design-spine.md`.

After the `aoa-memo` decision-lane cleanup, the remaining weakness is visible:
short numbered paths sort well inside the directory, but outside that local
context they do not carry owner, organ, or decision-class identity.

For OS Abyss, decision filenames are part of the operational map. A distant
agent should be able to see `AOA-EV-D-####` in a path, search hit, generated
index, or review note and know it is an `aoa-evals` decision record without
reconstructing that from surrounding directory context.

## Options Considered

- Keep short numbered paths and rely on `docs/decisions/` context.
- Add `Decision ID` inside each note but leave filenames short.
- Use full canonical decision IDs as both the in-file handle and the filename
  prefix, then regenerate lookup indexes from source metadata.

## Decision

Use full canonical IDs for `aoa-evals` decision records:

`AOA-EV-D-####`

Each decision note must include `- Decision ID: AOA-EV-D-####`, and the
filename prefix must match the decision ID exactly:

`docs/decisions/AOA-EV-D-####-short-slug.md`

Each decision note also owns an `## Index Metadata` block with `Original date`,
surface classes, mechanic parents, guard families, and posture. Generated
lookup indexes derive from that metadata, including a date index:

- `by-number.md`
- `by-date.md`
- `by-surface.md`
- `by-mechanic.md`
- `by-validation-guard.md`

Previous short numbered paths are retired. They remain recoverable through git
history, PRs, and release notes, not through compatibility stubs or generated
path maps.

## Rationale

This mirrors the mature `aoa-memo` decision-lane principle without importing
memory-specific fields into `aoa-evals`.

The canonical ID gives every decision a stable handle. Matching filenames make
that handle visible in ordinary file listings, search results, cross-repo refs,
and generated read models. The generated indexes keep lookup cheap while
preserving decision notes as the rationale authority.

Avoiding a compatibility map keeps the active lane small. Compatibility maps
are useful during staged migrations, but here the old paths were short local
addresses and all active repository refs can move in one bounded slice.

## Consequences

- Positive: decision records are now self-identifying outside local directory
  context.
- Positive: date lookup is generated from source metadata instead of inferred
  from path shape or chronology.
- Positive: future agents can search `AOA-EV-D-####` as a stable decision
  handle.
- Tradeoff: existing short-path refs outside git history must be updated to the
  canonical paths.
- Follow-up: future decision notes must use the canonical ID template before
  generated index parity can pass.

## Current Applicability

As of 2026-05-26:

- Still valid: decision notes explain why; source surfaces keep current proof
  authority.
- Changed: active decision source paths use full canonical ID filename prefixes.
- Superseded by: none.

## Review Log

### 2026-05-26 - Initial canonical-address landing

- Previous assumption: short numbered filenames were sufficient because
  generated indexes provided lookup.
- New reality: OS Abyss routeability benefits when the path itself carries
  owner, organ, and decision class.
- Reason: this makes decision refs easier to route from search, MCP packets,
  generated indexes, reviews, and cross-repo notes.
- Source surfaces updated: `docs/decisions/`, generated decision indexes,
  `docs/decisions/indexes/index_contract.yaml`, and the decision-index
  validator layer later split by AOA-EV-D-0218.
- Validation: `python scripts/generate_decision_indexes.py --check`,
  focused tests for decision indexes, and semantic AGENTS validation.

## Boundaries

This decision does not make generated indexes decision authority.

It does not add memory-object metadata to `aoa-evals`; memory-specific classes
remain an `aoa-memo` concern.

It does not preserve old short numbered paths as active compatibility routes.

It does not change the bounded proof meaning of any eval bundle, report,
receipt, runtime candidate, or sibling reference.

## Validation

- `scripts/validators/decision_records.py` enforces canonical ID filename
  prefixes, in-file decision IDs, and original dates.
- `scripts/validators/decision_index_surfaces.py` enforces generated index
  parity.
- `docs/decisions/indexes/index_contract.yaml` names the active path policy.
- Generated decision indexes route back to `AOA-EV-D-####-*.md` source notes.
