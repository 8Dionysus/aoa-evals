# Titan Legacy Distillation Log

## 2026-05-19 Mechanics Refactor

Titan canary work moved from a canary-form parent into the active
`mechanics/titan/` parent.

Distilled into active route:

- former `evals/titan*.yaml` seeds now live under
  `mechanics/titan/parts/seed-boundary/seeds/`;
- former root Titan canary guides now live under `mechanics/titan/parts/seed-boundary/docs/`;
- `mechanics/titan/PARTS.md` names `seed-boundary` as the current part;
- `mechanics/EVIDENCE_CLUSTERS.md` records `titan-canaries` as historical
  canary parent naming routed to `titan`.
- `legacy/raw/evals-titan-seed-placement.md` preserves only the old root
  `evals/` seed holding district as a placement snapshot.

Still historical:

- `evals/` as a Titan seed holding district;
- `docs/TITAN_*` as root guide paths;
- `mechanics/titan-canaries/` as parent package name.

Current route:

- new Titan seed-boundary work starts in `parts/seed-boundary/`;
- legacy changes here account for old seed holding and canary path lineage.
