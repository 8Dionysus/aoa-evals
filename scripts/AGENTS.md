# AGENTS.md

## Guidance for `scripts/`

`scripts/` contains repo-wide builders, validators, catalog tools, and
proof-surface helpers.

Mechanic-owned scripts live under the owning part. For example, publication
receipt publishing belongs to `mechanics/publication-receipts/parts/`, and
candidate-reader or sibling-canary builders live under their mechanic parts.

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

Keep scripts deterministic and repo-relative unless an explicit command says otherwise. Avoid hidden network calls, private data, and ambient credentials.

Builder changes must preserve source ownership: bundles, schemas, runners, scorers, and docs own meaning; generated catalogs summarize.

Validator changes must not weaken bounded proof posture. Prefer precise failures over permissive silence.
Pair validator wording changes with focused tests in `tests/test_validate_repo.py`.

Verify with the touched command and normally:

```bash
python scripts/build_catalog.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
