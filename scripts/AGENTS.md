# AGENTS.md

## Guidance for `scripts/`

`scripts/` contains builders, validators, publishers, catalog tools, and proof-surface helpers.

Keep scripts deterministic and repo-relative unless an explicit command says otherwise. Avoid hidden network calls, private data, and ambient credentials.

Builder changes must preserve source ownership: bundles, schemas, runners, scorers, and docs own meaning; generated catalogs summarize.

Validator changes must not weaken bounded proof posture. Prefer precise failures over permissive silence.

Verify with the touched command and normally:

```bash
python scripts/build_catalog.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
