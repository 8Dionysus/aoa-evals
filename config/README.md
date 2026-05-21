# Config Route

`config/` is a compatibility route card, not an active config payload district.

No active root config payload should live here. Mechanic-owned configuration now
lives with the operation that owns it:

- Agon seed and registry inputs live under `mechanics/agon/parts/*/config/`.
- Boundary-bridge sibling canary config lives under
  `mechanics/boundary-bridge/parts/latest-sibling-canary/config/`.

Future repo-wide config may be introduced only when `docs/PROOF_TOPOLOGY.md`
and the relevant decision record explain why no narrower mechanic, bundle, or
generated-reader route owns it.
