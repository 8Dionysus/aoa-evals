# 0054 Agon Part Contract Guard

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/agon/parts/`

## Context

`agon` is the active parent mechanic. Its current parts already had real source
artifacts, generated registries, schemas, builders, validators, tests, and in
some cases observe-only recurrence bindings.

The weak point was local readability: several part README files only named the
route and validation command. That was too thin for the next growth of Agon
because a future agent could split pressure into a new proof-suffix parent or
mistake a generated registry for verdict authority.

## Decision

Give every active Agon part README an explicit part-level contract:

- `mechanics/agon/parts/court-prebinding/README.md`;
- `mechanics/agon/parts/ccs-alignment/README.md`;
- `mechanics/agon/parts/vds-alignment/README.md`;
- `mechanics/agon/parts/mechanical-trial-suites/README.md`;
- `mechanics/agon/parts/retention-rank-alignment/README.md`;
- `mechanics/agon/parts/epistemic-alignment/README.md`;
- `mechanics/agon/parts/slc-alignment/README.md`;
- `mechanics/agon/parts/kag-alignment/README.md`;
- `mechanics/agon/parts/sophian-threshold-alignment/README.md`.

Each README must expose inputs, outputs, stronger owner split, stop-lines, and
validation. Add validator coverage so those contract headings and part-specific
authority boundaries cannot silently disappear.

## Rationale

This keeps `agon` convex as one parent mechanic: no new Agon parent is created
for court prebinding, CCS, VDS,
mechanical trial suites, retention/rank, epistemic, SLC, KAG, and Sophian
threshold alignment are parts inside Agon, not new parents.

The contract shape also preserves the stronger-owner split. `aoa-evals` owns
candidate proof-alignment and deterministic validation; Agents-of-Abyss, Tree of
Sophia, KAG, stats, memo, runtime, and other sibling owners keep law, canon,
state, verdict, rank, and promotion authority.

## Consequences

- Positive: future Agon work starts from the current part, not from invented
  `*-proof` or `*-canary` parent topology.
- Positive: generated registries remain weaker than seed configs, validators,
  owner truth, and bundle-local review.
- Positive: `python scripts/validate_repo.py` now rejects missing Agon
  part-level contracts.
- Tradeoff: Agon README wording is now deliberately tighter where authority
  boundaries matter.

## Boundaries

This decision does not create a new Agon parent, move Agon quest source records,
run live arena protocol, grant verdict authority, mutate rank or trust, write
scars or memory, execute retention, or promote anything into Tree of Sophia.

It does not transfer Agents-of-Abyss law, Tree of Sophia canon, KAG canon,
runtime truth, stats truth, or memo truth into `aoa-evals`.

## Validation

- `python scripts/validate_repo.py`
- `python -m pytest -q tests/test_validate_repo.py -k 'agon_part_readmes or mechanic_parent_allowlist'`
- part-local Agon builders, validators, and tests before any generated registry
  change
