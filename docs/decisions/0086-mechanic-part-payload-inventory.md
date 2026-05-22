# Mechanic Part Payload Inventory

- Status: Accepted
- Date: 2026-05-20
- Owner surface: `mechanics/README.md`

## Context

The mechanics refactor now routes active work through
`mechanics/<parent>/parts/<part>/` directories. Parent `PARTS.md` files and
part README contracts already make each concrete part visible, but there was
still a smaller topology gap: a part could gain a payload subdirectory while
its part README stayed silent.

That gap matters because payload directories such as `fixtures/`, `schemas/`,
`manifests/`, `scripts/`, `tests/`, `reports/`, or `generated/` are not neutral
storage. They are the active proof material that makes a mechanic part real.
If they are invisible from the part README, future edits can hide residue,
empty scaffolding, or owner drift behind a plausible part name.

## Options Considered

- Let parent `PARTS.md` be the only route into part contents.
- Require a generic source-surface section but do not compare it with the file
  tree.
- Add a validator-backed payload inventory contract for each concrete part.

## Decision

Each concrete `mechanics/<parent>/parts/<part>/README.md` must route every
actual payload subdirectory that exists under that part.

`scripts/validate_repo.py` rejects:

- an unexpected payload class under a mechanic part;
- an empty payload subdirectory under a mechanic part;
- an unexpected part-root file beside `README.md` or `AGENTS.md`;
- a payload subdirectory that exists on disk but is not named by the part
  README.
- a part with no payload subdirectories unless the README declares a
  eval-backed thin support route where the source eval package stays under
  `evals/`.

Allowed payload classes are intentionally generic proof-support classes:
`config`, `docs`, `examples`, `fixtures`, `generated`, `manifests`, `reports`,
`runners`, `schemas`, `scorers`, `scripts`, `seeds`, `templates`, and `tests`.

## Rationale

This keeps the part as the smallest honest operation boundary. A parent may own
the broad mechanic, but the part README must expose the concrete proof material
that makes the part operable.

The only acceptable no-payload shape is not an empty future slot. It is a
eval-backed thin support route: the part routes a real source eval package
that deliberately stays under `evals/` because bundle-local proof meaning is
stronger than mechanics support. That posture must be visible in the part
README.

The contract also prevents two opposite errors: hiding real files below a part
without a route, and preserving empty payload folders as future "maybe" space.
Both would make the mechanics atlas look more complete than it is.

## Consequences

- Positive: part-local payloads become visible from the part route card.
- Positive: empty scaffolding and unknown payload names are rejected early.
- Positive: future part growth has a small, repeatable topology guard.
- Tradeoff: adding a new payload directory now requires updating the part
  README in the same slice.

## Boundaries

This decision does not create new parent mechanics and does not make payload
classes active by themselves.

It does not move source proof bundles out of `evals/`, does not promote
generated readers into authority, and does not let a part-local payload outrank
the stronger owner named by the part contract.

## Validation

### Superseded Original Route

- ~~python -m pytest -q tests/test_validate_repo.py -k mechanic_part_payload_inventory~~
- ~~python scripts/validate_repo.py~~

### 2026-05-21 Update

Validation routes through
[mechanics/AGENTS.md#validation](../../mechanics/AGENTS.md#validation).
Use the focused mechanic part payload-inventory guard there when changing this
decision, part README payload routing, or part payload topology validators.
