# Proof Loop Legacy Distillation Log

## 2026-05-20 Mechanics Refactor

Proof-loop route-smoke work moved from root report placement into the active
`mechanics/proof-loop/` parent.

Distilled into active route:

- route-smoke report placement lives under
  `mechanics/proof-loop/parts/route-smoke/`;
- the first route-smoke report now lives at
  `mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md`;
- `docs/decisions/AOA-EV-D-0030-proof-loop-route-smoke-part.md` records why root
  `reports/` placement was too broad for the route-smoke artifact.

Still historical:

- `reports/proof-loop-local-route-smoke-v1.md` as the old root report path;
- root `reports/` as the placement for proof-loop route-smoke artifacts with a
  narrower mechanic owner.

Current route:

- new proof-loop route-smoke work starts in the owning active part;
- legacy changes here account for old root report placement.
