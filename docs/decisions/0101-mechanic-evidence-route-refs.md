# Mechanic Evidence Route Refs

- Status: Accepted
- Date: 2026-05-21
- Owner surface: `mechanics/EVIDENCE_CLUSTERS.md`

## Context

The Active Parent Evidence Dimension Ledger made every mechanic parent show
meaning/doctrine, proof pressure, contracts/payloads, builders/readouts,
quest/deferred pressure, owner split and stop-lines, and legacy/provenance.
That was necessary, but still too prose-shaped for a bounded proof refactor.

A parent could satisfy the ledger with broad words while failing to show the
source surface, generated reader, runtime-candidate boundary, sibling
handoff, bundle, test, script, quest, or part route that makes the
cross-root evidence real.

## Options Considered

- Keep the dimension ledger prose-only.
- Require every dimension cell to contain many paths.
- Add a compact route-ref ledger next to the dimension ledger and validate it.

## Decision

`mechanics/EVIDENCE_CLUSTERS.md` now owns an Active Parent Evidence Route Refs
ledger.

Each active parent row must name concrete local route refs. The refs must be
repo-relative, resolve in the current worktree, include an active route under
`mechanics/<parent>/`, and include at least one living non-mechanics route ref,
meaning a non-mechanics route ref that points at current evidence. This
living non-mechanics evidence keeps the evidence map tied to current source
surfaces instead of letting a parent be justified by package-local prose alone.

The validator rejects missing route-ref rows, rows with fewer than three
path-like refs, unresolved local paths, placeholder refs, repo-qualified refs,
rows that cite only mechanic-local routes, and generic root validator refs such
as `scripts/validate_repo.py` or `tests/test_validate_repo.py` standing in for
parent evidence.

Decision notes may still explain why a route was chosen, but a
rationale-only decision ref cannot be the only non-mechanics route evidence for
an active parent. The row must also point at a living source, bundle, generated
readout, quest, workflow/config, root entry, or similarly current local
evidence surface.

## Rationale

The mechanics refactor depends on real cross-root evidence clusters. A compact
route-ref ledger makes that standard auditable without copying each part README
or bundle contract into the evidence map.

The ledger is still a route surface. It does not make generated readers,
runtime candidates, sibling references, or reports stronger than source proof
objects. It only proves that the parent row points at living local evidence.

## Consequences

- Positive: each active parent now has at least one checked route back to
  current local evidence outside its package.
- Positive: stale root paths and invented parent prose have less room to hide.
- Positive: a generic root validator can no longer masquerade as the
  cross-root evidence for a specific parent.
- Positive: a rationale-only decision can no longer masquerade as living
  non-mechanics evidence for a parent.
- Tradeoff: adding or renaming a parent requires updating another compact
  ledger row.

## Boundaries

This decision does not move source proof bundles out of `bundles/`, promote
generated surfaces into proof authority, make runtime candidates verdicts, or
absorb sibling owner truth.

It does not replace part `## Source Surfaces`; part-level refs remain the
local contract for a concrete part.

## Validation

```bash
python -m pytest -q tests/test_validate_repo.py -k mechanic_evidence_route_refs
python scripts/validate_repo.py
```
