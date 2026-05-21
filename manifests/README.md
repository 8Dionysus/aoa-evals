# Manifests Route

`manifests/` is a compatibility route card, not an active root manifest payload
district.

No active root manifest payload should live here. Recurrence/component
manifests now live next to the mechanic part whose operation they describe:

- Agon recurrence manifests live under `mechanics/agon/parts/*/manifests/`.
- Recurrence control-plane manifests live under
  `mechanics/recurrence/parts/control-plane-integrity/manifests/`.
- Portable proof beacon manifests live under
  `mechanics/recurrence/parts/portable-proof-beacons/manifests/`.

Future repo-wide manifests may be introduced only when
`docs/PROOF_TOPOLOGY.md` and the relevant decision record explain why no
narrower mechanic, bundle, generated-reader, or quest route owns them.
