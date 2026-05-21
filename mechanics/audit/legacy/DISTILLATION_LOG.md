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
- `mechanics/EVIDENCE_CLUSTERS.md` records why `runtime-evidence` is not a
  parent mechanic.

Still historical:

- `mechanics/runtime-evidence/` as a parent package name;
- root runtime evidence schemas, examples, generated readers, and guide paths;
- any reading where candidate runtime evidence outranks bundle-local review.

Do not create new audit work in legacy. Distill into the owning active part
first.
