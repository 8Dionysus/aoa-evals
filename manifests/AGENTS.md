# AGENTS.md

## Role

`manifests/` is a route-card-only compatibility route card for root manifest
paths.

Active root manifest payloads route with the mechanic part whose lifecycle they
describe:

- Agon recurrence manifests live under `mechanics/agon/parts/*/manifests/`.
- Recurrence control-plane manifests live under
  `mechanics/recurrence/parts/control-plane-integrity/manifests/`.
- Portable proof beacon manifests live under
  `mechanics/recurrence/parts/portable-proof-beacons/manifests/`.

## Rules

Root recurrence manifest aliases route through the owning mechanic
`PROVENANCE.md`; the owning legacy archive explains itself after that bridge.

Manifest edits are topology edits. Pair them with the owning mechanic docs,
decision record, and validation that explains why the component belongs to that
part.

## Validation

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
