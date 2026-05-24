# Audit Legacy Distillation Log

## 2026-05-20 Mechanics Refactor

Audit work moved from scattered runtime-evidence and artifact-hook surfaces into
the active `mechanics/audit/` parent.

Distilled into active route:

- runtime evidence packet selection lives under
  `mechanics/audit/parts/selected-evidence-packets/`;
- artifact-to-verdict hook support lives under
  `mechanics/audit/parts/artifact-verdict-hooks/`;
- runtime candidate generated readers and builders live under
  `mechanics/audit/parts/candidate-readers/`;
- runtime integrity review support lives under
  `mechanics/audit/parts/integrity-review/`;
- `mechanics/EVIDENCE_CLUSTERS.md` records `runtime-evidence` as an evidence
  class routed to the audit parent.

Still historical:

- `mechanics/runtime-evidence/` as a parent package name;
- root runtime evidence schemas, examples, generated readers, and guide paths;
- any reading where candidate runtime evidence outranks bundle-local review.

Current route:

- new audit proof work starts in the owning active part;
- legacy changes here account for old runtime-evidence placement and lineage.
