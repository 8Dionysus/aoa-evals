# AGENTS.md

## Guidance for `manifests/`

`manifests/` is a compatibility route card, not an active manifest payload
district.

No active root manifest payload should live here. Recurrence manifests now live
with the mechanic part whose lifecycle they describe, such as
`mechanics/agon/parts/*/manifests/`,
`mechanics/recurrence/parts/control-plane-integrity/manifests/`, and
`mechanics/recurrence/parts/portable-proof-beacons/manifests/`.

Do not recreate root recurrence manifest aliases to make old paths convenient.
Route old root path lineage through the owning mechanic `PROVENANCE.md`; the
owning legacy archive explains itself after that bridge.

Manifest edits are topology edits. Pair them with the owning mechanic docs,
decision record, and validation that explains why the component belongs to that
part.

Verify with:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
