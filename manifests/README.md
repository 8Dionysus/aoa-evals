# Manifests Route

`manifests/` is the root compatibility route card for historical manifest
paths.

## Operating Card

| Field | Route |
| --- | --- |
| role | compatibility route card for root manifest path routing |
| entry | open when an old root manifest path appears or a component manifest needs an owner |
| input | recurrence/component manifest, old manifest reference, lifecycle payload, or proposed repo-wide manifest |
| output | owning mechanic part manifest route or documented repo-wide manifest decision |
| owner | `manifests/AGENTS.md` for route law; owning mechanic part for manifest meaning |
| next route | Agon manifests, recurrence control-plane manifests, portable-proof-beacon manifests, or `docs/PROOF_TOPOLOGY.md` |
| validation | `manifests/AGENTS.md` and the owning mechanic route card |

Active root manifest payloads route next to the mechanic part whose operation
they describe:

- Agon recurrence manifests live under `mechanics/agon/parts/*/manifests/`.
- Recurrence control-plane manifests live under
  `mechanics/recurrence/parts/control-plane-integrity/manifests/`.
- Portable proof beacon manifests live under
  `mechanics/recurrence/parts/portable-proof-beacons/manifests/`.

Future repo-wide manifests may be introduced only when
`docs/PROOF_TOPOLOGY.md` and the relevant decision record explain why no
narrower mechanic, bundle, generated-reader, or quest route owns them.
