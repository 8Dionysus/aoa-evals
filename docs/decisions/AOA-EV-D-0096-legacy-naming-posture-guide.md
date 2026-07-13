# Legacy Naming Posture Guide

- Decision ID: AOA-EV-D-0096

## Status

Accepted.

## Index Metadata

- Original date: 2026-05-21
- Surface classes: legacy/provenance
- Mechanic parents: none
- Guard families: legacy and provenance
- Posture: legacy/provenance rationale

## Context

`docs/architecture/LEGACY_NAMING.md` began as a broad map while mechanic packages were still
being discovered. That was useful before every active mechanic had a
`PROVENANCE.md` bridge and local `legacy/` archive.

After the mechanic refactor, keeping archive details in the root legacy naming
file creates a second route into history. It makes `docs/architecture/LEGACY_NAMING.md`
feel like a global archive map beside the real package bridge, even though AoA
mechanics use one controlled bridge from active surfaces into legacy.

## Decision

`docs/architecture/LEGACY_NAMING.md` is now a posture guide, not a global archive map.

It may name:

- posture categories: active, historical, accepted-input,
  generated-projection, candidate-only, or provenance-bridge;
- the active-first lookup rule;
- `PROVENANCE.md` as the only bridge when old placement or source lineage
  matters.

It should not list the concrete old-name inventory, active mechanic parent
allowlist, wrong-parent mapping, or archive internals. Those belong in the
active topology/evidence surfaces or inside the owning `legacy/` archive after
the bridge.

It must not carry archive details. Detailed archive lookup stays inside the
owning `legacy/` archive, reached only after:

`active route -> PROVENANCE.md`

Validator coverage follows the focused legacy-naming posture route in command
authority and the nearest `AGENTS.md`.

## Consequences

Old names remain searchable and routeable, but root docs do not become the
second legacy route.

Package-local `PROVENANCE.md` is the only controlled bridge from active
mechanic surfaces into the legacy archive. The archive can stay detailed
without steering active topology.

Compatibility root route cards such as `schemas/` and `manifests/` follow the
same rule: they may route old root path lineage to the owning mechanic
`PROVENANCE.md`, but they must not list archive-internal index or accounting
surfaces as parallel entrypoints.
