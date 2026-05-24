# AGENTS.md

## Applies to

This card applies to root `scripts/` and repo-wide builder, validator, catalog,
and proof-surface helper scripts.

## Role

`scripts/` contains repo-wide builders, validators, catalog tools, and
proof-surface helpers.

Mechanic-owned scripts live under the owning part. For example, publication
receipt publishing belongs to `mechanics/publication-receipts/parts/`, and
candidate-reader or sibling-canary builders live under their mechanic parts.

## Operating Card

| Field | Route |
| --- | --- |
| role | root builder and validator district |
| input | source eval packages, generated reader inputs, route cards, decision surfaces, mechanics maps, and repo-wide proof contracts |
| output | validation issues, generated readers, catalog projections, or deterministic helper results |
| owner | root `scripts/` for repo-wide tooling; mechanic part for part-owned payload tooling |
| next route | source surface protected by the script, `tests/` regression mesh, or owning mechanic part |
| tools | `validate_repo.py`, catalog builders, semantic/nested AGENTS validators |
| validation | this card's `Verify` section |

## Validator role

`scripts/validate_repo.py` is the root contract mesh for cross-surface topology.
Treat it as a validator surface, not as ordinary glue code.

When adding or moving a validator, name the authority class it protects:
source proof objects, generated/readouts, decisions, route-card-only districts,
root-authored guidance, mechanic parents, mechanic parts, legacy/provenance,
quests, scripts, or tests.

Part-local validators may live under `mechanics/<parent>/parts/<part>/scripts/`
when the owning part owns the payload. Root validators stay here when the check
spans multiple authority classes or protects repository-wide topology.

Keep scripts deterministic and repo-relative unless an explicit command says
otherwise. Public-share pressure routes through explicit command contracts
instead of hidden network calls, private data, or ambient credentials.

Builder changes must preserve source ownership: bundles, schemas, runners, scorers, and docs own meaning; generated catalogs summarize.

The bounded proof posture is protected through precise failures that name the owner
surface, field, and bounded claim being protected.
Pair validator wording changes with focused tests in `tests/test_validate_repo.py`.

## Owner Routes

| Script pressure | Owner route |
| --- | --- |
| repo-wide topology or source-of-truth guard | root `scripts/` plus focused tests in `tests/` |
| mechanic payload script | `mechanics/<parent>/parts/<part>/scripts/` |
| generated reader builder | source surface, builder, generated reader, validator, and tests together |
| cross-repo witness check | bounded proof route with explicit source refs |
| new proof meaning | authored source surface before script logic |

## Verify

Use the touched command first. Common checks:

```bash
python scripts/build_catalog.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
