# Experience Legacy Index

| Former root route | Current active route | Reason |
| --- | --- | --- |
| `fixtures/experience-verdict-protocol-integrity-v1/` | `mechanics/experience/parts/protocol-integrity/fixtures/experience-verdict-protocol-integrity-v1/` | active protocol fixture family |
| `tests/test_experience_protocol_integrity.py` | `mechanics/experience/parts/protocol-integrity/tests/test_experience_protocol_integrity.py` | active protocol validation |
| `docs/EXPERIENCE_CERTIFICATION_EVAL_BUNDLES.md` and `docs/ASSISTANT_CERTIFICATION_JUDGE.md` | `mechanics/experience/parts/certification-gate/docs/` | active certification proof support |
| `fixtures/experience-certification-gate-integrity-v1/` | `mechanics/experience/parts/certification-gate/fixtures/experience-certification-gate-integrity-v1/` | active certification fixture family |
| `examples/{canary,certification,deployment,post_release,production_drift,regression,release_certification,rollback,watchtower}*.example.json` | `mechanics/experience/parts/certification-gate/examples/` | active certification and release-gate examples |
| `schemas/{canary,certification,deployment,post_release,production_drift,regression,release_certification,rollback,watchtower}*_v1.json` | `mechanics/experience/parts/certification-gate/schemas/` | active certification and release-gate schemas |
| `tests/test_experience_certification_gate_integrity.py` and `tests/test_experience_wave2_seed_contracts.py` | `mechanics/experience/parts/certification-gate/tests/` | active certification validation |
| `docs/*ADOPTION*.md`, `docs/FEDERATION_HARVEST_EVAL_BUNDLES.md`, `docs/KAG_PROMOTION_VERDICT_MODEL.md`, `docs/OWNER_CONSENT_VERDICT.md`, `docs/PATTERN_LINEAGE_INTEGRITY_BUNDLES.md`, and `docs/TOS_BOUNDARY_VERDICT_MODEL.md` | `mechanics/experience/parts/adoption-federation/docs/` | active adoption and compatibility proof support |
| `fixtures/memo-reviewed-candidate-adoption-guardrail-v1/` | `mechanics/distillation/parts/runtime-candidate-adoption/fixtures/memo-reviewed-candidate-adoption-guardrail-v1/` | former adoption fixture placement, now runtime distillation candidate adoption support |
| `examples/*adoption*.example.json`, `examples/federation_*.example.json`, `examples/kag_promotion_verdict.example.json`, `examples/owner_consent_verdict.example.json`, `examples/pattern_lineage_integrity_verdict.example.json`, `examples/shared_pattern_regression_verdict.example.json`, and `examples/tos_boundary_verdict.example.json` | `mechanics/experience/parts/adoption-federation/examples/` | active adoption and compatibility examples |
| `schemas/*adoption*_v1.json`, `schemas/federation_*_v1.json`, `schemas/kag_promotion_verdict_v1.json`, `schemas/owner_consent_verdict_v1.json`, `schemas/pattern_lineage_integrity_verdict_v1.json`, `schemas/shared_pattern_regression_verdict_v1.json`, and `schemas/tos_boundary_verdict_v1.json` | `mechanics/experience/parts/adoption-federation/schemas/` | active adoption and compatibility schemas |
| `tests/test_experience_wave3_seed_contracts.py` | `mechanics/experience/parts/adoption-federation/tests/test_experience_wave3_seed_contracts.py` | active adoption validation |
| `docs/*GOVERNANCE*.md`, `docs/AUTHORITY_RESOLUTION_VERDICT.md`, `docs/CHARTER_AMENDMENT_EVALS.md`, `docs/CONSTITUTION_RUNTIME_EVAL_BUNDLES.md`, `docs/TOS_DOSSIER_REVIEW_VERDICTS.md`, and `docs/VETO_LEGITIMACY_BUNDLES.md` | `mechanics/experience/parts/governance-runtime-boundary/docs/` | active governance and runtime-boundary support |
| `docs/APPEAL_REVIEW_VERDICT.md`, `docs/STAY_ORDER_ENFORCEMENT_VERDICT.md`, `docs/VOTE_SEAL_INTEGRITY_VERDICT.md`, and `docs/REPLAY_HISTORY_INTEGRITY_VERDICT.md` | `mechanics/experience/parts/governance-runtime-boundary/docs/` | active governance, stay-order, sealed-vote, and replay-history support |
| `examples/{appeal,authority_resolution,charter,governance,runtime_integrity,sealed_vote,tos_dossier,veto}*.example.json` | `mechanics/experience/parts/governance-runtime-boundary/examples/` | active governance and runtime-boundary examples |
| `schemas/{appeal,authority_resolution,charter,governance,runtime_integrity,sealed_vote,tos_dossier,veto}*_v1.json` | `mechanics/experience/parts/governance-runtime-boundary/schemas/` | active governance and runtime-boundary schemas |
| `tests/test_experience_wave4_seed_contracts.py` | `mechanics/experience/parts/governance-runtime-boundary/tests/test_experience_wave4_seed_contracts.py` | active governance validation |
| `docs/BOUNDARY_GUARD_VERDICTS.md`, `docs/GOVERNED_RELEASE_VERDICTS.md`, `docs/HANDOFF_INTEGRITY_VERDICTS.md`, `docs/INSTALLATION_SMOKE_EVALS.md`, `docs/MULTI_OFFICE_RELEASE_TRAIN_EVALS.md`, `docs/OFFICE_SCOPE_FIDELITY_VERDICTS.md`, and `docs/ROLLBACK_DRILL_VERDICTS.md` | `mechanics/experience/parts/office-release-train/docs/` | active office and release-train support |
| `docs/REPLAY_AUDIT_VERDICTS.md` and `docs/SERVICE_MESH_REGRESSION_VERDICTS.md` | `mechanics/experience/parts/office-release-train/docs/` | active replay-audit and service-mesh release-train support |
| `examples/{boundary_guard,governed_release,handoff,installation,multi_office,office,replay,rollback_drill,train_release}*_v1.example.json` | `mechanics/experience/parts/office-release-train/examples/` | active office and release-train examples |
| `schemas/{boundary_guard,governed_release,handoff,installation,multi_office,office,replay,train_release}*_v1.json` | `mechanics/experience/parts/office-release-train/schemas/` | active office and release-train schemas |
| `tests/test_experience_wave5_seed_contracts.py` | `mechanics/experience/parts/office-release-train/tests/test_experience_wave5_seed_contracts.py` | active office and release-train validation |

`rollback_drill_verdict_v1.json` remains part-local under
`certification-gate` because both certification-gate and office-release-train
use that shared rollback verdict contract.
