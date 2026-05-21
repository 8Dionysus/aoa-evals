# Release Support Legacy Distillation Log

## 2026-05-20 Mechanics Refactor

Release support work moved from proof-release wording and root report/test
paths into the active `mechanics/release-support/` parent.

Distilled into active route:

- readiness-audit artifacts live under
  `mechanics/release-support/parts/readiness-audit/`;
- strategic-closeout artifacts live under
  `mechanics/release-support/parts/strategic-closeout/`;
- PR handoff artifacts live under
  `mechanics/release-support/parts/pr-handoff/`;
- `mechanics/EVIDENCE_CLUSTERS.md` records why `proof-release` is not a parent
  mechanic.

Still historical:

- `mechanics/proof-release/` as a parent package name;
- root release-support report paths under `reports/`;
- proof-release decision and report naming vocabulary.

Do not create new release-support work in legacy. Distill into the owning
active part first.
