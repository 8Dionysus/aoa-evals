# Release Support Legacy Index

| Former or overloaded source | Current active route | Posture |
| --- | --- | --- |
| `mechanics/proof-release/` | `mechanics/release-support/` | rejected parent naming: release-support is the AoA-aligned mechanic |
| `docs/decisions/0014-proof-release-mechanic-package.md` | `docs/decisions/AOA-EV-D-0014-release-support-mechanic-package.md` | former decision path vocabulary |
| `docs/decisions/0025-proof-release-readiness-audit.md` | `docs/decisions/AOA-EV-D-0025-release-support-readiness-audit.md` | former decision path vocabulary |
| `reports/proof-release-readiness-audit-v1.json` | `mechanics/release-support/parts/readiness-audit/reports/release-support-readiness-audit-v1.json` | former root report path and old report name |
| `reports/strategic-closeout-audit-v1.json` | `mechanics/release-support/parts/strategic-closeout/reports/strategic-closeout-audit-v1.json` | former root report path |
| `reports/release-prep-pr-handoff-v1.json` | `mechanics/release-support/parts/pr-handoff/reports/release-prep-pr-handoff-v1.json` | former root report path |
| `tests/test_proof_release_readiness_audit.py` | `mechanics/release-support/parts/readiness-audit/tests/test_release_support_readiness_audit.py` | former root test path and old test name |
| `tests/test_strategic_closeout_audit.py` | `mechanics/release-support/parts/strategic-closeout/tests/test_strategic_closeout_audit.py` | former root test path |
| `tests/test_release_prep_pr_handoff.py` | `mechanics/release-support/parts/pr-handoff/tests/test_release_prep_pr_handoff.py` | former root test path |

## Boundary

Former root paths are provenance only. Current release-support contracts should
cite the active part-local paths and keep release artifacts weaker than
bundle-local proof meaning.
