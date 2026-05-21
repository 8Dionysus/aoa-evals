# AGENTS.md

## Guidance for `scripts/`

`scripts/` contains repo-wide builders, validators, catalog tools, and
proof-surface helpers.

Mechanic-owned scripts live under the owning part. For example, publication
receipt publishing belongs to `mechanics/publication-receipts/parts/`, and
candidate-reader or sibling-canary builders live under their mechanic parts.

Keep scripts deterministic and repo-relative unless an explicit command says otherwise. Avoid hidden network calls, private data, and ambient credentials.

Builder changes must preserve source ownership: bundles, schemas, runners, scorers, and docs own meaning; generated catalogs summarize.

Validator changes must not weaken bounded proof posture. Prefer precise failures over permissive silence.

Verify with the touched command and normally:

```bash
python scripts/build_catalog.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
