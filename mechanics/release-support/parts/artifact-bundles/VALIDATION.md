# Release Support / Artifact Bundles Validation

Executable validation commands for this part live in
[the parent validation card](../VALIDATION.md).

Use the `artifact-bundles` child validation block there. This file is the
part-local validation route marker so the README can remain a contract map.


Source anchor: `mechanics/release-support/parts/artifact-bundles`.

## Commands

```bash
python scripts/validate_abyss_machine_report_index_bundle.py
python scripts/validate_repo.py
python scripts/release_check.py
```
