# Decision Records Index

This directory is the durable decision surface for `aoa-evals`.

Use it for meaningful choices about bounded proof topology, root surfaces,
agent-facing guidance, proof-object contracts, quest posture, mechanics, legacy,
validation, runtime-candidate intake, receipt posture, or sibling reference
compatibility.

Ordinary edit summaries, generated output, release notes, runtime logs, private
evidence, and one-off planning thoughts route to their owning surfaces instead.

## Operating Card

| Field | Route |
| --- | --- |
| role | durable decision rationale index |
| entry | use when a structural, topology, validation, public-contract, legacy, runtime-candidate, sibling-reference, or agent-route change needs recoverable rationale |
| input | changed source surface, owner boundary, rejected option, validation guard, or cross-surface route pressure |
| output | numbered decision note, index row, surface-class lookup, mechanic-parent lookup, and validation-guard lookup |
| owner | `docs/decisions/AGENTS.md` for lane law; this README for the agent-facing index; numbered decisions for the rationale |
| next route | source surface first, then local route card, `docs/PROOF_TOPOLOGY.md`, `mechanics/EVIDENCE_CLUSTERS.md`, or the affected generated/runtime/sibling owner |
| validation | [docs/decisions/AGENTS.md#validation](AGENTS.md#validation) and the owning route card for the changed surface |

## Authority

Decision notes explain why a route was chosen.

They are weaker than the source surface they describe:

- source eval package meaning stays in `evals/**/EVAL.md` and `eval.yaml`;
- system form stays in `DESIGN.md`;
- agent-facing shape stays in `DESIGN.AGENTS.md` and nearest `AGENTS.md` cards;
- technical proof model stays in `docs/ARCHITECTURE.md`;
- evaluation posture stays in `docs/EVAL_PHILOSOPHY.md`;
- generated readers stay derived from their builders;
- runtime candidates and receipts stay below eval-package-local review;
- sibling repositories keep their own stronger truth.

## Index Shape

This README is the agent-facing index for decision rationale.

Use it in both directions:

- top down: repo route -> authority class -> operation -> mechanic parent -> part -> validation guard -> decision rationale;
- bottom up: changed source surface -> local route card or part index -> validator guard -> decision rationale -> stronger owner surface.

The chronological list preserves stable lookup by number. The crosswalks below
make the same decisions findable by surface class, mechanic parent, and guard
family without promoting decisions above the source surfaces they describe.

## Current Decisions

| No. | Decision | Path | Primary index tags | Posture |
| --- | --- | --- | --- | --- |
| 0001 | [Root Design Spine](0001-root-design-spine.md) | `docs/decisions/0001-root-design-spine.md` | root/topology | active rationale |
| 0002 | [Proof Object Authority Contract](0002-proof-object-authority-contract.md) | `docs/decisions/0002-proof-object-authority-contract.md` | proof topology | active rationale |
| 0003 | [Sibling Proof Reference Compatibility](0003-sibling-proof-reference-compatibility.md) | `docs/decisions/0003-sibling-proof-reference-compatibility.md` | boundary/runtime/sibling | active rationale |
| 0004 | [Questbook Topology](0004-questbook-topology.md) | `docs/decisions/0004-questbook-topology.md` | root/topology, quest/lane | active rationale |
| 0005 | [Proof Topology Map](0005-proof-topology-map.md) | `docs/decisions/0005-proof-topology-map.md` | root/topology | active rationale |
| 0006 | [Questbook Mechanic Package](0006-questbook-mechanic-package.md) | `docs/decisions/0006-questbook-mechanic-package.md` | mechanic package, quest/lane | active rationale |
| 0007 | [Audit Mechanic Package](0007-audit-mechanic-package.md) | `docs/decisions/0007-audit-mechanic-package.md` | mechanic package, boundary/runtime/sibling | active rationale |
| 0008 | [Boundary Bridge Mechanic Package](0008-boundary-bridge-mechanic-package.md) | `docs/decisions/0008-boundary-bridge-mechanic-package.md` | mechanic package, boundary/runtime/sibling | active rationale |
| 0009 | [Legacy Naming Containment](0009-legacy-naming-containment.md) | `docs/decisions/0009-legacy-naming-containment.md` | legacy/provenance | legacy/provenance rationale |
| 0010 | [Proof Object Mechanic Package](0010-proof-object-mechanic-package.md) | `docs/decisions/0010-proof-object-mechanic-package.md` | mechanic package | active rationale |
| 0011 | [Comparison Spine Mechanic Package](0011-comparison-spine-mechanic-package.md) | `docs/decisions/0011-comparison-spine-mechanic-package.md` | mechanic package | active rationale |
| 0012 | [Proof Infra Mechanic Package](0012-proof-infra-mechanic-package.md) | `docs/decisions/0012-proof-infra-mechanic-package.md` | mechanic package | active rationale |
| 0013 | [Publication Receipts Mechanic Package](0013-publication-receipts-mechanic-package.md) | `docs/decisions/0013-publication-receipts-mechanic-package.md` | mechanic package, report/release/receipt | report/release/receipt rationale |
| 0014 | [Release Support Mechanic Package](0014-release-support-mechanic-package.md) | `docs/decisions/0014-release-support-mechanic-package.md` | mechanic package, report/release/receipt | report/release/receipt rationale |
| 0015 | [Titan Mechanic Package](0015-titan-mechanic-package.md) | `docs/decisions/0015-titan-mechanic-package.md` | mechanic package, boundary/runtime/sibling | active rationale |
| 0016 | [Agon Mechanic Package](0016-agon-mechanic-package.md) | `docs/decisions/0016-agon-mechanic-package.md` | mechanic package, boundary/runtime/sibling | active rationale |
| 0017 | [Spark Agent Lane Placement](0017-spark-agent-lane-placement.md) | `docs/decisions/0017-spark-agent-lane-placement.md` | proof topology | active rationale |
| 0018 | [Quest Lane-State Source Layout](0018-quest-lane-state-source-layout.md) | `docs/decisions/0018-quest-lane-state-source-layout.md` | quest/lane | active rationale |
| 0019 | [Proof Loop Mechanic Package](0019-proof-loop-mechanic-package.md) | `docs/decisions/0019-proof-loop-mechanic-package.md` | mechanic package | active rationale |
| 0020 | [Proof Loop Local Smoke Report](0020-proof-loop-local-smoke-report.md) | `docs/decisions/0020-proof-loop-local-smoke-report.md` | report/release/receipt | report/release/receipt rationale |
| 0021 | [Quest Lifecycle Contract](0021-quest-lifecycle-contract.md) | `docs/decisions/0021-quest-lifecycle-contract.md` | quest/lane | active rationale |
| 0022 | [Proof Loop Bundle-Local Report](0022-proof-loop-bundle-local-report.md) | `docs/decisions/0022-proof-loop-bundle-local-report.md` | report/release/receipt | report/release/receipt rationale |
| 0023 | [Eval Report Index Reader](0023-eval-report-index-reader.md) | `docs/decisions/0023-eval-report-index-reader.md` | report/release/receipt, generated/readout | generated/readout rationale |
| 0024 | [Receipt Intake Dry Review](0024-receipt-intake-dry-review.md) | `docs/decisions/0024-receipt-intake-dry-review.md` | report/release/receipt | report/release/receipt rationale |
| 0025 | [Release Support Readiness Audit](0025-release-support-readiness-audit.md) | `docs/decisions/0025-release-support-readiness-audit.md` | report/release/receipt, boundary/runtime/sibling | report/release/receipt rationale |
| 0026 | [Strategic Closeout Audit](0026-strategic-closeout-audit.md) | `docs/decisions/0026-strategic-closeout-audit.md` | report/release/receipt, boundary/runtime/sibling | report/release/receipt rationale |
| 0027 | [Release Prep PR Handoff](0027-release-prep-pr-handoff.md) | `docs/decisions/0027-release-prep-pr-handoff.md` | report/release/receipt | report/release/receipt rationale |
| 0028 | [Repo Validation aoa-memo Pin Refresh](0028-repo-validation-aoa-memo-pin-refresh.md) | `docs/decisions/0028-repo-validation-aoa-memo-pin-refresh.md` | proof topology | active rationale |
| 0029 | [Comparison Spine Report Parts](0029-comparison-spine-report-parts.md) | `docs/decisions/0029-comparison-spine-report-parts.md` | mechanic part, report/release/receipt | report/release/receipt rationale |
| 0030 | [Proof Loop Route-Smoke Part](0030-proof-loop-route-smoke-part.md) | `docs/decisions/0030-proof-loop-route-smoke-part.md` | mechanic part | active rationale |
| 0031 | [Recurrence Mechanic Package](0031-recurrence-mechanic-package.md) | `docs/decisions/0031-recurrence-mechanic-package.md` | mechanic package | active rationale |
| 0032 | [Checkpoint Mechanic Package](0032-checkpoint-mechanic-package.md) | `docs/decisions/0032-checkpoint-mechanic-package.md` | mechanic package | active rationale |
| 0033 | [Experience Mechanic Package](0033-experience-mechanic-package.md) | `docs/decisions/0033-experience-mechanic-package.md` | mechanic package | active rationale |
| 0034 | [Antifragility Mechanic Package](0034-antifragility-mechanic-package.md) | `docs/decisions/0034-antifragility-mechanic-package.md` | mechanic package | active rationale |
| 0035 | [Method-growth Mechanic Package](0035-method-growth-mechanic-package.md) | `docs/decisions/0035-method-growth-mechanic-package.md` | mechanic package | active rationale |
| 0036 | [RPG Mechanic Package](0036-rpg-mechanic-package.md) | `docs/decisions/0036-rpg-mechanic-package.md` | mechanic package | active rationale |
| 0037 | [Growth-cycle Mechanic Package](0037-growth-cycle-mechanic-package.md) | `docs/decisions/0037-growth-cycle-mechanic-package.md` | mechanic package | active rationale |
| 0038 | [Distillation Mechanic Package](0038-distillation-mechanic-package.md) | `docs/decisions/0038-distillation-mechanic-package.md` | mechanic package | active rationale |
| 0039 | [Recurrence Support Parts Expansion](0039-recurrence-support-parts-expansion.md) | `docs/decisions/0039-recurrence-support-parts-expansion.md` | mechanic part | active rationale |
| 0040 | [Comparison Spine Fixture Parts](0040-comparison-spine-fixture-parts.md) | `docs/decisions/0040-comparison-spine-fixture-parts.md` | mechanic part | active rationale |
| 0041 | [Proof Infra Fixture Families](0041-proof-infra-fixture-families.md) | `docs/decisions/0041-proof-infra-fixture-families.md` | mechanic part | active rationale |
| 0042 | [Recurrence Portable Proof Beacons Part](0042-recurrence-portable-proof-beacons-part.md) | `docs/decisions/0042-recurrence-portable-proof-beacons-part.md` | mechanic part | active rationale |
| 0043 | [Experience Verdict Residue Parts](0043-experience-verdict-residue-parts.md) | `docs/decisions/0043-experience-verdict-residue-parts.md` | mechanic part | active rationale |
| 0044 | [Boundary Bridge Orchestrator Proof Anchors](0044-boundary-bridge-orchestrator-proof-anchors.md) | `docs/decisions/0044-boundary-bridge-orchestrator-proof-anchors.md` | boundary/runtime/sibling | active rationale |
| 0045 | [Closeout Writeback Ingress Boundary](0045-closeout-writeback-ingress-boundary.md) | `docs/decisions/0045-closeout-writeback-ingress-boundary.md` | report/release/receipt | report/release/receipt rationale |
| 0046 | [Boundary Bridge Phase Alpha Eval Matrix](0046-boundary-bridge-phase-alpha-eval-matrix.md) | `docs/decisions/0046-boundary-bridge-phase-alpha-eval-matrix.md` | generated/readout, boundary/runtime/sibling | generated/readout rationale |
| 0047 | [Questbook Schema Parts](0047-questbook-schema-parts.md) | `docs/decisions/0047-questbook-schema-parts.md` | mechanic part, quest/lane | active rationale |
| 0048 | [Proof Object Contract Parts](0048-proof-object-contract-parts.md) | `docs/decisions/0048-proof-object-contract-parts.md` | mechanic part | active rationale |
| 0049 | [Proof Infra Reportable Contracts](0049-proof-infra-reportable-contracts.md) | `docs/decisions/0049-proof-infra-reportable-contracts.md` | report/release/receipt | report/release/receipt rationale |
| 0050 | [Part-local Test Placement](0050-part-local-test-placement.md) | `docs/decisions/0050-part-local-test-placement.md` | mechanic part | active rationale |
| 0051 | [Root Route-card Guard](0051-root-route-card-guard.md) | `docs/decisions/0051-root-route-card-guard.md` | validation guard, root/topology | active guard rationale |
| 0052 | [Mechanic Parent Allowlist](0052-mechanic-parent-allowlist.md) | `docs/decisions/0052-mechanic-parent-allowlist.md` | validation guard | active guard rationale |
| 0053 | [Audit Part Contract Guard](0053-audit-part-contract-guard.md) | `docs/decisions/0053-audit-part-contract-guard.md` | mechanic part, validation guard, boundary/runtime/sibling | active guard rationale |
| 0054 | [Agon Part Contract Guard](0054-agon-part-contract-guard.md) | `docs/decisions/0054-agon-part-contract-guard.md` | mechanic part, validation guard, boundary/runtime/sibling | active guard rationale |
| 0055 | [Titan Seed-boundary Contract](0055-titan-seed-boundary-contract.md) | `docs/decisions/0055-titan-seed-boundary-contract.md` | boundary/runtime/sibling | active rationale |
| 0056 | [Boundary Bridge Part Contract Guard](0056-boundary-bridge-part-contract-guard.md) | `docs/decisions/0056-boundary-bridge-part-contract-guard.md` | mechanic part, validation guard, boundary/runtime/sibling | active guard rationale |
| 0057 | [Publication Receipts Part Contract Guard](0057-publication-receipts-part-contract-guard.md) | `docs/decisions/0057-publication-receipts-part-contract-guard.md` | mechanic part, validation guard, report/release/receipt | report/release/receipt rationale |
| 0058 | [Release Support Part Contract Guard](0058-release-support-part-contract-guard.md) | `docs/decisions/0058-release-support-part-contract-guard.md` | mechanic part, validation guard, report/release/receipt | report/release/receipt rationale |
| 0059 | [Comparison Spine Part Contract Guard](0059-comparison-spine-part-contract-guard.md) | `docs/decisions/0059-comparison-spine-part-contract-guard.md` | mechanic part, validation guard | active guard rationale |
| 0060 | [Proof Loop Route-Smoke Contract](0060-proof-loop-route-smoke-contract.md) | `docs/decisions/0060-proof-loop-route-smoke-contract.md` | proof topology | active rationale |
| 0061 | [Antifragility Part Contract Guard](0061-antifragility-part-contract-guard.md) | `docs/decisions/0061-antifragility-part-contract-guard.md` | mechanic part, validation guard | active guard rationale |
| 0062 | [Checkpoint Part Contract Guard](0062-checkpoint-part-contract-guard.md) | `docs/decisions/0062-checkpoint-part-contract-guard.md` | mechanic part, validation guard | active guard rationale |
| 0063 | [Experience Part Contract Guard](0063-experience-part-contract-guard.md) | `docs/decisions/0063-experience-part-contract-guard.md` | mechanic part, validation guard | active guard rationale |
| 0064 | [Distillation Part Contract Guard](0064-distillation-part-contract-guard.md) | `docs/decisions/0064-distillation-part-contract-guard.md` | mechanic part, validation guard | active guard rationale |
| 0065 | [Growth-cycle Diagnosis-gate Contract](0065-growth-cycle-diagnosis-gate-contract.md) | `docs/decisions/0065-growth-cycle-diagnosis-gate-contract.md` | proof topology | active rationale |
| 0066 | [Recurrence Control-plane Contract](0066-recurrence-control-plane-contract.md) | `docs/decisions/0066-recurrence-control-plane-contract.md` | proof topology | active rationale |
| 0067 | [RPG Progression-unlocks Contract](0067-rpg-progression-unlocks-contract.md) | `docs/decisions/0067-rpg-progression-unlocks-contract.md` | proof topology | active rationale |
| 0068 | [Method-growth Part Owner-split Contract](0068-method-growth-part-owner-split-contract.md) | `docs/decisions/0068-method-growth-part-owner-split-contract.md` | mechanic part | active rationale |
| 0069 | [Proof-object Part Owner-split Contract](0069-proof-object-part-owner-split-contract.md) | `docs/decisions/0069-proof-object-part-owner-split-contract.md` | mechanic part | active rationale |
| 0070 | [Questbook Part Owner-split Contract](0070-questbook-part-owner-split-contract.md) | `docs/decisions/0070-questbook-part-owner-split-contract.md` | mechanic part, quest/lane | active rationale |
| 0071 | [Mechanic Legacy Archive Boundary](0071-mechanic-legacy-skeleton-contract.md) | `docs/decisions/0071-mechanic-legacy-skeleton-contract.md` | legacy/provenance | legacy/provenance rationale |
| 0072 | [Mechanic Parent Class Contract](0072-mechanic-parent-class-contract.md) | `docs/decisions/0072-mechanic-parent-class-contract.md` | proof topology | active rationale |
| 0073 | [Generated Route Residue Guard](0073-generated-route-residue-guard.md) | `docs/decisions/0073-generated-route-residue-guard.md` | validation guard, generated/readout | generated/readout rationale |
| 0074 | [Mechanic Part README Contract](0074-mechanic-part-readme-contract.md) | `docs/decisions/0074-mechanic-part-readme-contract.md` | mechanic part | active rationale |
| 0075 | [Mechanic Provenance Entry Contract](0075-mechanic-provenance-entry-contract.md) | `docs/decisions/0075-mechanic-provenance-entry-contract.md` | legacy/provenance | legacy/provenance rationale |
| 0076 | [Active Mechanic Route Residue Guard](0076-active-mechanic-route-residue-guard.md) | `docs/decisions/0076-active-mechanic-route-residue-guard.md` | validation guard | active guard rationale |
| 0077 | [Root Authored Route Residue Guard](0077-root-authored-route-residue-guard.md) | `docs/decisions/0077-root-authored-route-residue-guard.md` | validation guard, root/topology | active guard rationale |
| 0078 | [Decision Route Residue Guard](0078-decision-route-residue-guard.md) | `docs/decisions/0078-decision-route-residue-guard.md` | validation guard | active guard rationale |
| 0079 | [Repo Config Route Residue Guard](0079-repo-config-route-residue-guard.md) | `docs/decisions/0079-repo-config-route-residue-guard.md` | validation guard | active guard rationale |
| 0080 | [Source Bundle Route Residue Guard](0080-source-bundle-route-residue-guard.md) | `docs/decisions/0080-source-bundle-route-residue-guard.md` | validation guard | active guard rationale |
| 0081 | [Mechanic Payload Route Residue Guard](0081-mechanic-payload-route-residue-guard.md) | `docs/decisions/0081-mechanic-payload-route-residue-guard.md` | mechanic part, validation guard | active guard rationale |
| 0082 | [Mechanic Parent Direction Contract](0082-mechanic-parent-direction-contract.md) | `docs/decisions/0082-mechanic-parent-direction-contract.md` | proof topology | active rationale |
| 0083 | [Mechanic Evidence Dimension Ledger](0083-mechanic-evidence-dimension-ledger.md) | `docs/decisions/0083-mechanic-evidence-dimension-ledger.md` | root/topology | active rationale |
| 0084 | [Mechanic Root-district Reconnaissance](0084-mechanic-root-district-reconnaissance.md) | `docs/decisions/0084-mechanic-root-district-reconnaissance.md` | root/topology | active rationale; source tree routed by 0104 |
| 0085 | [Root-authored Surface Classification](0085-root-authored-surface-classification.md) | `docs/decisions/0085-root-authored-surface-classification.md` | root/topology | active rationale |
| 0086 | [Mechanic Part Payload Inventory](0086-mechanic-part-payload-inventory.md) | `docs/decisions/0086-mechanic-part-payload-inventory.md` | mechanic part | active rationale |
| 0087 | [Mechanic Part Validation Command Reachability](0087-mechanic-part-validation-command-reachability.md) | `docs/decisions/0087-mechanic-part-validation-command-reachability.md` | mechanic part, validation guard | active guard rationale |
| 0088 | [Mechanic PARTS Index Synchronization](0088-mechanic-parts-index-synchronization.md) | `docs/decisions/0088-mechanic-parts-index-synchronization.md` | mechanic part, validation guard | active guard rationale |
| 0089 | [Mechanic Legacy Single Bridge](0089-mechanic-legacy-single-bridge.md) | `docs/decisions/0089-mechanic-legacy-single-bridge.md` | legacy/provenance, boundary/runtime/sibling | legacy/provenance rationale |
| 0090 | [Mechanic Provenance Bridge Posture](0090-mechanic-provenance-bridge-posture.md) | `docs/decisions/0090-mechanic-provenance-bridge-posture.md` | legacy/provenance, boundary/runtime/sibling | legacy/provenance rationale |
| 0091 | [Legacy Naming Single-Bridge Language](0091-legacy-naming-single-bridge-language.md) | `docs/decisions/0091-legacy-naming-single-bridge-language.md` | legacy/provenance, boundary/runtime/sibling | legacy/provenance rationale |
| 0092 | [Active Legacy Parent Wording Boundary](0092-active-legacy-parent-wording-boundary.md) | `docs/decisions/0092-active-legacy-parent-wording-boundary.md` | legacy/provenance | legacy/provenance rationale |
| 0093 | [Architecture Proof Model Contract](0093-architecture-proof-model-contract.md) | `docs/decisions/0093-architecture-proof-model-contract.md` | root/topology | active rationale |
| 0094 | [Mechanic Part Source Surface Reference Guard](0094-mechanic-part-source-surface-reference-guard.md) | `docs/decisions/0094-mechanic-part-source-surface-reference-guard.md` | mechanic part | active rationale |
| 0095 | [Mechanic Part Source Surfaces Section Contract](0095-mechanic-part-source-surfaces-section-contract.md) | `docs/decisions/0095-mechanic-part-source-surfaces-section-contract.md` | mechanic part | active rationale |
| 0096 | [Legacy Naming Posture Guide](0096-legacy-naming-posture-guide.md) | `docs/decisions/0096-legacy-naming-posture-guide.md` | legacy/provenance | legacy/provenance rationale |
| 0097 | [Mechanic Parent Guidance Boundary](0097-mechanic-parent-guidance-boundary.md) | `docs/decisions/0097-mechanic-parent-guidance-boundary.md` | proof topology | active rationale |
| 0098 | [Agon Quest-note Provenance Route](0098-agon-quest-note-provenance-route.md) | `docs/decisions/0098-agon-quest-note-provenance-route.md` | legacy/provenance, quest/lane, boundary/runtime/sibling | legacy/provenance rationale |
| 0099 | [Repair Diagnosis Route Boundary](0099-repair-diagnosis-route-boundary.md) | `docs/decisions/0099-repair-diagnosis-route-boundary.md` | proof topology | active rationale |
| 0100 | [Active Mechanics Topology Wording](0100-active-mechanics-topology-wording.md) | `docs/decisions/0100-active-mechanics-topology-wording.md` | root/topology | active rationale |
| 0101 | [Mechanic Evidence Route Refs](0101-mechanic-evidence-route-refs.md) | `docs/decisions/0101-mechanic-evidence-route-refs.md` | root/topology | active rationale |
| 0102 | [Mechanic Part Validation Command Ownership](0102-mechanic-part-validation-command-ownership.md) | `docs/decisions/0102-mechanic-part-validation-command-ownership.md` | mechanic part, validation guard | active guard rationale |
| 0103 | [Agent Index Chain Surface](0103-agent-index-chain-surface.md) | `docs/decisions/0103-agent-index-chain-surface.md` | root/topology | active rationale |
| 0104 | [Source Eval Tree Topology](0104-source-eval-tree-topology.md) | `docs/decisions/0104-source-eval-tree-topology.md` | proof topology, root/topology | active rationale |
| 0105 | [Proof-object Eval Part Names](0105-proof-object-eval-part-names.md) | `docs/decisions/0105-proof-object-eval-part-names.md` | proof topology, mechanic part | active rationale |
| 0106 | [Memory Consumer Proof Boundary](0106-memory-consumer-proof-boundary.md) | `docs/decisions/0106-memory-consumer-proof-boundary.md` | proof topology, boundary/runtime/sibling | active rationale |

## Index By Surface Class

### Root / Topology

- [0001 Root Design Spine](0001-root-design-spine.md) (`docs/decisions/0001-root-design-spine.md`)
- [0004 Questbook Topology](0004-questbook-topology.md) (`docs/decisions/0004-questbook-topology.md`)
- [0005 Proof Topology Map](0005-proof-topology-map.md) (`docs/decisions/0005-proof-topology-map.md`)
- [0051 Root Route-card Guard](0051-root-route-card-guard.md) (`docs/decisions/0051-root-route-card-guard.md`)
- [0077 Root Authored Route Residue Guard](0077-root-authored-route-residue-guard.md) (`docs/decisions/0077-root-authored-route-residue-guard.md`)
- [0083 Mechanic Evidence Dimension Ledger](0083-mechanic-evidence-dimension-ledger.md) (`docs/decisions/0083-mechanic-evidence-dimension-ledger.md`)
- [0084 Mechanic Root-district Reconnaissance](0084-mechanic-root-district-reconnaissance.md) (`docs/decisions/0084-mechanic-root-district-reconnaissance.md`)
- [0085 Root-authored Surface Classification](0085-root-authored-surface-classification.md) (`docs/decisions/0085-root-authored-surface-classification.md`)
- [0093 Architecture Proof Model Contract](0093-architecture-proof-model-contract.md) (`docs/decisions/0093-architecture-proof-model-contract.md`)
- [0100 Active Mechanics Topology Wording](0100-active-mechanics-topology-wording.md) (`docs/decisions/0100-active-mechanics-topology-wording.md`)
- [0101 Mechanic Evidence Route Refs](0101-mechanic-evidence-route-refs.md) (`docs/decisions/0101-mechanic-evidence-route-refs.md`)
- [0103 Agent Index Chain Surface](0103-agent-index-chain-surface.md) (`docs/decisions/0103-agent-index-chain-surface.md`)
- [0104 Source Eval Tree Topology](0104-source-eval-tree-topology.md) (`docs/decisions/0104-source-eval-tree-topology.md`)

### Proof Topology

- [0002 Proof Object Authority Contract](0002-proof-object-authority-contract.md) (`docs/decisions/0002-proof-object-authority-contract.md`)
- [0017 Spark Agent Lane Placement](0017-spark-agent-lane-placement.md) (`docs/decisions/0017-spark-agent-lane-placement.md`)
- [0028 Repo Validation aoa-memo Pin Refresh](0028-repo-validation-aoa-memo-pin-refresh.md) (`docs/decisions/0028-repo-validation-aoa-memo-pin-refresh.md`)
- [0060 Proof Loop Route-Smoke Contract](0060-proof-loop-route-smoke-contract.md) (`docs/decisions/0060-proof-loop-route-smoke-contract.md`)
- [0065 Growth-cycle Diagnosis-gate Contract](0065-growth-cycle-diagnosis-gate-contract.md) (`docs/decisions/0065-growth-cycle-diagnosis-gate-contract.md`)
- [0066 Recurrence Control-plane Contract](0066-recurrence-control-plane-contract.md) (`docs/decisions/0066-recurrence-control-plane-contract.md`)
- [0067 RPG Progression-unlocks Contract](0067-rpg-progression-unlocks-contract.md) (`docs/decisions/0067-rpg-progression-unlocks-contract.md`)
- [0072 Mechanic Parent Class Contract](0072-mechanic-parent-class-contract.md) (`docs/decisions/0072-mechanic-parent-class-contract.md`)
- [0082 Mechanic Parent Direction Contract](0082-mechanic-parent-direction-contract.md) (`docs/decisions/0082-mechanic-parent-direction-contract.md`)
- [0097 Mechanic Parent Guidance Boundary](0097-mechanic-parent-guidance-boundary.md) (`docs/decisions/0097-mechanic-parent-guidance-boundary.md`)
- [0099 Repair Diagnosis Route Boundary](0099-repair-diagnosis-route-boundary.md) (`docs/decisions/0099-repair-diagnosis-route-boundary.md`)
- [0104 Source Eval Tree Topology](0104-source-eval-tree-topology.md) (`docs/decisions/0104-source-eval-tree-topology.md`)
- [0105 Proof-object Eval Part Names](0105-proof-object-eval-part-names.md) (`docs/decisions/0105-proof-object-eval-part-names.md`)
- [0106 Memory Consumer Proof Boundary](0106-memory-consumer-proof-boundary.md) (`docs/decisions/0106-memory-consumer-proof-boundary.md`)

### Mechanic Package

- [0006 Questbook Mechanic Package](0006-questbook-mechanic-package.md) (`docs/decisions/0006-questbook-mechanic-package.md`)
- [0007 Audit Mechanic Package](0007-audit-mechanic-package.md) (`docs/decisions/0007-audit-mechanic-package.md`)
- [0008 Boundary Bridge Mechanic Package](0008-boundary-bridge-mechanic-package.md) (`docs/decisions/0008-boundary-bridge-mechanic-package.md`)
- [0010 Proof Object Mechanic Package](0010-proof-object-mechanic-package.md) (`docs/decisions/0010-proof-object-mechanic-package.md`)
- [0011 Comparison Spine Mechanic Package](0011-comparison-spine-mechanic-package.md) (`docs/decisions/0011-comparison-spine-mechanic-package.md`)
- [0012 Proof Infra Mechanic Package](0012-proof-infra-mechanic-package.md) (`docs/decisions/0012-proof-infra-mechanic-package.md`)
- [0013 Publication Receipts Mechanic Package](0013-publication-receipts-mechanic-package.md) (`docs/decisions/0013-publication-receipts-mechanic-package.md`)
- [0014 Release Support Mechanic Package](0014-release-support-mechanic-package.md) (`docs/decisions/0014-release-support-mechanic-package.md`)
- [0015 Titan Mechanic Package](0015-titan-mechanic-package.md) (`docs/decisions/0015-titan-mechanic-package.md`)
- [0016 Agon Mechanic Package](0016-agon-mechanic-package.md) (`docs/decisions/0016-agon-mechanic-package.md`)
- [0019 Proof Loop Mechanic Package](0019-proof-loop-mechanic-package.md) (`docs/decisions/0019-proof-loop-mechanic-package.md`)
- [0031 Recurrence Mechanic Package](0031-recurrence-mechanic-package.md) (`docs/decisions/0031-recurrence-mechanic-package.md`)
- [0032 Checkpoint Mechanic Package](0032-checkpoint-mechanic-package.md) (`docs/decisions/0032-checkpoint-mechanic-package.md`)
- [0033 Experience Mechanic Package](0033-experience-mechanic-package.md) (`docs/decisions/0033-experience-mechanic-package.md`)
- [0034 Antifragility Mechanic Package](0034-antifragility-mechanic-package.md) (`docs/decisions/0034-antifragility-mechanic-package.md`)
- [0035 Method-growth Mechanic Package](0035-method-growth-mechanic-package.md) (`docs/decisions/0035-method-growth-mechanic-package.md`)
- [0036 RPG Mechanic Package](0036-rpg-mechanic-package.md) (`docs/decisions/0036-rpg-mechanic-package.md`)
- [0037 Growth-cycle Mechanic Package](0037-growth-cycle-mechanic-package.md) (`docs/decisions/0037-growth-cycle-mechanic-package.md`)
- [0038 Distillation Mechanic Package](0038-distillation-mechanic-package.md) (`docs/decisions/0038-distillation-mechanic-package.md`)

### Mechanic Part

- [0029 Comparison Spine Report Parts](0029-comparison-spine-report-parts.md) (`docs/decisions/0029-comparison-spine-report-parts.md`)
- [0030 Proof Loop Route-Smoke Part](0030-proof-loop-route-smoke-part.md) (`docs/decisions/0030-proof-loop-route-smoke-part.md`)
- [0039 Recurrence Support Parts Expansion](0039-recurrence-support-parts-expansion.md) (`docs/decisions/0039-recurrence-support-parts-expansion.md`)
- [0040 Comparison Spine Fixture Parts](0040-comparison-spine-fixture-parts.md) (`docs/decisions/0040-comparison-spine-fixture-parts.md`)
- [0041 Proof Infra Fixture Families](0041-proof-infra-fixture-families.md) (`docs/decisions/0041-proof-infra-fixture-families.md`)
- [0042 Recurrence Portable Proof Beacons Part](0042-recurrence-portable-proof-beacons-part.md) (`docs/decisions/0042-recurrence-portable-proof-beacons-part.md`)
- [0043 Experience Verdict Residue Parts](0043-experience-verdict-residue-parts.md) (`docs/decisions/0043-experience-verdict-residue-parts.md`)
- [0047 Questbook Schema Parts](0047-questbook-schema-parts.md) (`docs/decisions/0047-questbook-schema-parts.md`)
- [0048 Proof Object Contract Parts](0048-proof-object-contract-parts.md) (`docs/decisions/0048-proof-object-contract-parts.md`)
- [0050 Part-local Test Placement](0050-part-local-test-placement.md) (`docs/decisions/0050-part-local-test-placement.md`)
- [0053 Audit Part Contract Guard](0053-audit-part-contract-guard.md) (`docs/decisions/0053-audit-part-contract-guard.md`)
- [0054 Agon Part Contract Guard](0054-agon-part-contract-guard.md) (`docs/decisions/0054-agon-part-contract-guard.md`)
- [0056 Boundary Bridge Part Contract Guard](0056-boundary-bridge-part-contract-guard.md) (`docs/decisions/0056-boundary-bridge-part-contract-guard.md`)
- [0057 Publication Receipts Part Contract Guard](0057-publication-receipts-part-contract-guard.md) (`docs/decisions/0057-publication-receipts-part-contract-guard.md`)
- [0058 Release Support Part Contract Guard](0058-release-support-part-contract-guard.md) (`docs/decisions/0058-release-support-part-contract-guard.md`)
- [0059 Comparison Spine Part Contract Guard](0059-comparison-spine-part-contract-guard.md) (`docs/decisions/0059-comparison-spine-part-contract-guard.md`)
- [0061 Antifragility Part Contract Guard](0061-antifragility-part-contract-guard.md) (`docs/decisions/0061-antifragility-part-contract-guard.md`)
- [0062 Checkpoint Part Contract Guard](0062-checkpoint-part-contract-guard.md) (`docs/decisions/0062-checkpoint-part-contract-guard.md`)
- [0063 Experience Part Contract Guard](0063-experience-part-contract-guard.md) (`docs/decisions/0063-experience-part-contract-guard.md`)
- [0064 Distillation Part Contract Guard](0064-distillation-part-contract-guard.md) (`docs/decisions/0064-distillation-part-contract-guard.md`)
- [0068 Method-growth Part Owner-split Contract](0068-method-growth-part-owner-split-contract.md) (`docs/decisions/0068-method-growth-part-owner-split-contract.md`)
- [0069 Proof-object Part Owner-split Contract](0069-proof-object-part-owner-split-contract.md) (`docs/decisions/0069-proof-object-part-owner-split-contract.md`)
- [0070 Questbook Part Owner-split Contract](0070-questbook-part-owner-split-contract.md) (`docs/decisions/0070-questbook-part-owner-split-contract.md`)
- [0074 Mechanic Part README Contract](0074-mechanic-part-readme-contract.md) (`docs/decisions/0074-mechanic-part-readme-contract.md`)
- [0081 Mechanic Payload Route Residue Guard](0081-mechanic-payload-route-residue-guard.md) (`docs/decisions/0081-mechanic-payload-route-residue-guard.md`)
- [0086 Mechanic Part Payload Inventory](0086-mechanic-part-payload-inventory.md) (`docs/decisions/0086-mechanic-part-payload-inventory.md`)
- [0087 Mechanic Part Validation Command Reachability](0087-mechanic-part-validation-command-reachability.md) (`docs/decisions/0087-mechanic-part-validation-command-reachability.md`)
- [0088 Mechanic PARTS Index Synchronization](0088-mechanic-parts-index-synchronization.md) (`docs/decisions/0088-mechanic-parts-index-synchronization.md`)
- [0094 Mechanic Part Source Surface Reference Guard](0094-mechanic-part-source-surface-reference-guard.md) (`docs/decisions/0094-mechanic-part-source-surface-reference-guard.md`)
- [0095 Mechanic Part Source Surfaces Section Contract](0095-mechanic-part-source-surfaces-section-contract.md) (`docs/decisions/0095-mechanic-part-source-surfaces-section-contract.md`)
- [0102 Mechanic Part Validation Command Ownership](0102-mechanic-part-validation-command-ownership.md) (`docs/decisions/0102-mechanic-part-validation-command-ownership.md`)

### Validation Guard

- [0051 Root Route-card Guard](0051-root-route-card-guard.md) (`docs/decisions/0051-root-route-card-guard.md`)
- [0052 Mechanic Parent Allowlist](0052-mechanic-parent-allowlist.md) (`docs/decisions/0052-mechanic-parent-allowlist.md`)
- [0053 Audit Part Contract Guard](0053-audit-part-contract-guard.md) (`docs/decisions/0053-audit-part-contract-guard.md`)
- [0054 Agon Part Contract Guard](0054-agon-part-contract-guard.md) (`docs/decisions/0054-agon-part-contract-guard.md`)
- [0056 Boundary Bridge Part Contract Guard](0056-boundary-bridge-part-contract-guard.md) (`docs/decisions/0056-boundary-bridge-part-contract-guard.md`)
- [0057 Publication Receipts Part Contract Guard](0057-publication-receipts-part-contract-guard.md) (`docs/decisions/0057-publication-receipts-part-contract-guard.md`)
- [0058 Release Support Part Contract Guard](0058-release-support-part-contract-guard.md) (`docs/decisions/0058-release-support-part-contract-guard.md`)
- [0059 Comparison Spine Part Contract Guard](0059-comparison-spine-part-contract-guard.md) (`docs/decisions/0059-comparison-spine-part-contract-guard.md`)
- [0061 Antifragility Part Contract Guard](0061-antifragility-part-contract-guard.md) (`docs/decisions/0061-antifragility-part-contract-guard.md`)
- [0062 Checkpoint Part Contract Guard](0062-checkpoint-part-contract-guard.md) (`docs/decisions/0062-checkpoint-part-contract-guard.md`)
- [0063 Experience Part Contract Guard](0063-experience-part-contract-guard.md) (`docs/decisions/0063-experience-part-contract-guard.md`)
- [0064 Distillation Part Contract Guard](0064-distillation-part-contract-guard.md) (`docs/decisions/0064-distillation-part-contract-guard.md`)
- [0073 Generated Route Residue Guard](0073-generated-route-residue-guard.md) (`docs/decisions/0073-generated-route-residue-guard.md`)
- [0076 Active Mechanic Route Residue Guard](0076-active-mechanic-route-residue-guard.md) (`docs/decisions/0076-active-mechanic-route-residue-guard.md`)
- [0077 Root Authored Route Residue Guard](0077-root-authored-route-residue-guard.md) (`docs/decisions/0077-root-authored-route-residue-guard.md`)
- [0078 Decision Route Residue Guard](0078-decision-route-residue-guard.md) (`docs/decisions/0078-decision-route-residue-guard.md`)
- [0079 Repo Config Route Residue Guard](0079-repo-config-route-residue-guard.md) (`docs/decisions/0079-repo-config-route-residue-guard.md`)
- [0080 Source Bundle Route Residue Guard](0080-source-bundle-route-residue-guard.md) (`docs/decisions/0080-source-bundle-route-residue-guard.md`)
- [0081 Mechanic Payload Route Residue Guard](0081-mechanic-payload-route-residue-guard.md) (`docs/decisions/0081-mechanic-payload-route-residue-guard.md`)
- [0087 Mechanic Part Validation Command Reachability](0087-mechanic-part-validation-command-reachability.md) (`docs/decisions/0087-mechanic-part-validation-command-reachability.md`)
- [0088 Mechanic PARTS Index Synchronization](0088-mechanic-parts-index-synchronization.md) (`docs/decisions/0088-mechanic-parts-index-synchronization.md`)
- [0102 Mechanic Part Validation Command Ownership](0102-mechanic-part-validation-command-ownership.md) (`docs/decisions/0102-mechanic-part-validation-command-ownership.md`)

### Legacy / Provenance

- [0009 Legacy Naming Containment](0009-legacy-naming-containment.md) (`docs/decisions/0009-legacy-naming-containment.md`)
- [0071 Mechanic Legacy Archive Boundary](0071-mechanic-legacy-skeleton-contract.md) (`docs/decisions/0071-mechanic-legacy-skeleton-contract.md`)
- [0075 Mechanic Provenance Entry Contract](0075-mechanic-provenance-entry-contract.md) (`docs/decisions/0075-mechanic-provenance-entry-contract.md`)
- [0089 Mechanic Legacy Single Bridge](0089-mechanic-legacy-single-bridge.md) (`docs/decisions/0089-mechanic-legacy-single-bridge.md`)
- [0090 Mechanic Provenance Bridge Posture](0090-mechanic-provenance-bridge-posture.md) (`docs/decisions/0090-mechanic-provenance-bridge-posture.md`)
- [0091 Legacy Naming Single-Bridge Language](0091-legacy-naming-single-bridge-language.md) (`docs/decisions/0091-legacy-naming-single-bridge-language.md`)
- [0092 Active Legacy Parent Wording Boundary](0092-active-legacy-parent-wording-boundary.md) (`docs/decisions/0092-active-legacy-parent-wording-boundary.md`)
- [0096 Legacy Naming Posture Guide](0096-legacy-naming-posture-guide.md) (`docs/decisions/0096-legacy-naming-posture-guide.md`)
- [0098 Agon Quest-note Provenance Route](0098-agon-quest-note-provenance-route.md) (`docs/decisions/0098-agon-quest-note-provenance-route.md`)

### Generated / Readout

- [0023 Eval Report Index Reader](0023-eval-report-index-reader.md) (`docs/decisions/0023-eval-report-index-reader.md`)
- [0046 Boundary Bridge Phase Alpha Eval Matrix](0046-boundary-bridge-phase-alpha-eval-matrix.md) (`docs/decisions/0046-boundary-bridge-phase-alpha-eval-matrix.md`)
- [0073 Generated Route Residue Guard](0073-generated-route-residue-guard.md) (`docs/decisions/0073-generated-route-residue-guard.md`)

### Report / Release / Receipt

- [0013 Publication Receipts Mechanic Package](0013-publication-receipts-mechanic-package.md) (`docs/decisions/0013-publication-receipts-mechanic-package.md`)
- [0014 Release Support Mechanic Package](0014-release-support-mechanic-package.md) (`docs/decisions/0014-release-support-mechanic-package.md`)
- [0020 Proof Loop Local Smoke Report](0020-proof-loop-local-smoke-report.md) (`docs/decisions/0020-proof-loop-local-smoke-report.md`)
- [0022 Proof Loop Bundle-Local Report](0022-proof-loop-bundle-local-report.md) (`docs/decisions/0022-proof-loop-bundle-local-report.md`)
- [0023 Eval Report Index Reader](0023-eval-report-index-reader.md) (`docs/decisions/0023-eval-report-index-reader.md`)
- [0024 Receipt Intake Dry Review](0024-receipt-intake-dry-review.md) (`docs/decisions/0024-receipt-intake-dry-review.md`)
- [0025 Release Support Readiness Audit](0025-release-support-readiness-audit.md) (`docs/decisions/0025-release-support-readiness-audit.md`)
- [0026 Strategic Closeout Audit](0026-strategic-closeout-audit.md) (`docs/decisions/0026-strategic-closeout-audit.md`)
- [0027 Release Prep PR Handoff](0027-release-prep-pr-handoff.md) (`docs/decisions/0027-release-prep-pr-handoff.md`)
- [0029 Comparison Spine Report Parts](0029-comparison-spine-report-parts.md) (`docs/decisions/0029-comparison-spine-report-parts.md`)
- [0045 Closeout Writeback Ingress Boundary](0045-closeout-writeback-ingress-boundary.md) (`docs/decisions/0045-closeout-writeback-ingress-boundary.md`)
- [0049 Proof Infra Reportable Contracts](0049-proof-infra-reportable-contracts.md) (`docs/decisions/0049-proof-infra-reportable-contracts.md`)
- [0057 Publication Receipts Part Contract Guard](0057-publication-receipts-part-contract-guard.md) (`docs/decisions/0057-publication-receipts-part-contract-guard.md`)
- [0058 Release Support Part Contract Guard](0058-release-support-part-contract-guard.md) (`docs/decisions/0058-release-support-part-contract-guard.md`)

### Quest / Lane

- [0004 Questbook Topology](0004-questbook-topology.md) (`docs/decisions/0004-questbook-topology.md`)
- [0006 Questbook Mechanic Package](0006-questbook-mechanic-package.md) (`docs/decisions/0006-questbook-mechanic-package.md`)
- [0018 Quest Lane-State Source Layout](0018-quest-lane-state-source-layout.md) (`docs/decisions/0018-quest-lane-state-source-layout.md`)
- [0021 Quest Lifecycle Contract](0021-quest-lifecycle-contract.md) (`docs/decisions/0021-quest-lifecycle-contract.md`)
- [0047 Questbook Schema Parts](0047-questbook-schema-parts.md) (`docs/decisions/0047-questbook-schema-parts.md`)
- [0070 Questbook Part Owner-split Contract](0070-questbook-part-owner-split-contract.md) (`docs/decisions/0070-questbook-part-owner-split-contract.md`)
- [0098 Agon Quest-note Provenance Route](0098-agon-quest-note-provenance-route.md) (`docs/decisions/0098-agon-quest-note-provenance-route.md`)

### Boundary / Runtime / Sibling

- [0003 Sibling Proof Reference Compatibility](0003-sibling-proof-reference-compatibility.md) (`docs/decisions/0003-sibling-proof-reference-compatibility.md`)
- [0007 Audit Mechanic Package](0007-audit-mechanic-package.md) (`docs/decisions/0007-audit-mechanic-package.md`)
- [0008 Boundary Bridge Mechanic Package](0008-boundary-bridge-mechanic-package.md) (`docs/decisions/0008-boundary-bridge-mechanic-package.md`)
- [0015 Titan Mechanic Package](0015-titan-mechanic-package.md) (`docs/decisions/0015-titan-mechanic-package.md`)
- [0016 Agon Mechanic Package](0016-agon-mechanic-package.md) (`docs/decisions/0016-agon-mechanic-package.md`)
- [0025 Release Support Readiness Audit](0025-release-support-readiness-audit.md) (`docs/decisions/0025-release-support-readiness-audit.md`)
- [0026 Strategic Closeout Audit](0026-strategic-closeout-audit.md) (`docs/decisions/0026-strategic-closeout-audit.md`)
- [0044 Boundary Bridge Orchestrator Proof Anchors](0044-boundary-bridge-orchestrator-proof-anchors.md) (`docs/decisions/0044-boundary-bridge-orchestrator-proof-anchors.md`)
- [0046 Boundary Bridge Phase Alpha Eval Matrix](0046-boundary-bridge-phase-alpha-eval-matrix.md) (`docs/decisions/0046-boundary-bridge-phase-alpha-eval-matrix.md`)
- [0053 Audit Part Contract Guard](0053-audit-part-contract-guard.md) (`docs/decisions/0053-audit-part-contract-guard.md`)
- [0054 Agon Part Contract Guard](0054-agon-part-contract-guard.md) (`docs/decisions/0054-agon-part-contract-guard.md`)
- [0055 Titan Seed-boundary Contract](0055-titan-seed-boundary-contract.md) (`docs/decisions/0055-titan-seed-boundary-contract.md`)
- [0056 Boundary Bridge Part Contract Guard](0056-boundary-bridge-part-contract-guard.md) (`docs/decisions/0056-boundary-bridge-part-contract-guard.md`)
- [0089 Mechanic Legacy Single Bridge](0089-mechanic-legacy-single-bridge.md) (`docs/decisions/0089-mechanic-legacy-single-bridge.md`)
- [0090 Mechanic Provenance Bridge Posture](0090-mechanic-provenance-bridge-posture.md) (`docs/decisions/0090-mechanic-provenance-bridge-posture.md`)
- [0091 Legacy Naming Single-Bridge Language](0091-legacy-naming-single-bridge-language.md) (`docs/decisions/0091-legacy-naming-single-bridge-language.md`)
- [0098 Agon Quest-note Provenance Route](0098-agon-quest-note-provenance-route.md) (`docs/decisions/0098-agon-quest-note-provenance-route.md`)
- [0106 Memory Consumer Proof Boundary](0106-memory-consumer-proof-boundary.md) (`docs/decisions/0106-memory-consumer-proof-boundary.md`)

## Index By Mechanic Parent

### `proof-object`

- [0002 Proof Object Authority Contract](0002-proof-object-authority-contract.md) (`docs/decisions/0002-proof-object-authority-contract.md`)
- [0010 Proof Object Mechanic Package](0010-proof-object-mechanic-package.md) (`docs/decisions/0010-proof-object-mechanic-package.md`)
- [0048 Proof Object Contract Parts](0048-proof-object-contract-parts.md) (`docs/decisions/0048-proof-object-contract-parts.md`)
- [0069 Proof-object Part Owner-split Contract](0069-proof-object-part-owner-split-contract.md) (`docs/decisions/0069-proof-object-part-owner-split-contract.md`)
- [0105 Proof-object Eval Part Names](0105-proof-object-eval-part-names.md) (`docs/decisions/0105-proof-object-eval-part-names.md`)

### `proof-loop`

- [0019 Proof Loop Mechanic Package](0019-proof-loop-mechanic-package.md) (`docs/decisions/0019-proof-loop-mechanic-package.md`)
- [0020 Proof Loop Local Smoke Report](0020-proof-loop-local-smoke-report.md) (`docs/decisions/0020-proof-loop-local-smoke-report.md`)
- [0022 Proof Loop Bundle-Local Report](0022-proof-loop-bundle-local-report.md) (`docs/decisions/0022-proof-loop-bundle-local-report.md`)
- [0030 Proof Loop Route-Smoke Part](0030-proof-loop-route-smoke-part.md) (`docs/decisions/0030-proof-loop-route-smoke-part.md`)
- [0060 Proof Loop Route-Smoke Contract](0060-proof-loop-route-smoke-contract.md) (`docs/decisions/0060-proof-loop-route-smoke-contract.md`)

### `comparison-spine`

- [0011 Comparison Spine Mechanic Package](0011-comparison-spine-mechanic-package.md) (`docs/decisions/0011-comparison-spine-mechanic-package.md`)
- [0029 Comparison Spine Report Parts](0029-comparison-spine-report-parts.md) (`docs/decisions/0029-comparison-spine-report-parts.md`)
- [0040 Comparison Spine Fixture Parts](0040-comparison-spine-fixture-parts.md) (`docs/decisions/0040-comparison-spine-fixture-parts.md`)
- [0059 Comparison Spine Part Contract Guard](0059-comparison-spine-part-contract-guard.md) (`docs/decisions/0059-comparison-spine-part-contract-guard.md`)

### `proof-infra`

- [0012 Proof Infra Mechanic Package](0012-proof-infra-mechanic-package.md) (`docs/decisions/0012-proof-infra-mechanic-package.md`)
- [0041 Proof Infra Fixture Families](0041-proof-infra-fixture-families.md) (`docs/decisions/0041-proof-infra-fixture-families.md`)
- [0049 Proof Infra Reportable Contracts](0049-proof-infra-reportable-contracts.md) (`docs/decisions/0049-proof-infra-reportable-contracts.md`)

### `publication-receipts`

- [0013 Publication Receipts Mechanic Package](0013-publication-receipts-mechanic-package.md) (`docs/decisions/0013-publication-receipts-mechanic-package.md`)
- [0057 Publication Receipts Part Contract Guard](0057-publication-receipts-part-contract-guard.md) (`docs/decisions/0057-publication-receipts-part-contract-guard.md`)

### `release-support`

- [0014 Release Support Mechanic Package](0014-release-support-mechanic-package.md) (`docs/decisions/0014-release-support-mechanic-package.md`)
- [0025 Release Support Readiness Audit](0025-release-support-readiness-audit.md) (`docs/decisions/0025-release-support-readiness-audit.md`)
- [0058 Release Support Part Contract Guard](0058-release-support-part-contract-guard.md) (`docs/decisions/0058-release-support-part-contract-guard.md`)

### `titan`

- [0015 Titan Mechanic Package](0015-titan-mechanic-package.md) (`docs/decisions/0015-titan-mechanic-package.md`)
- [0055 Titan Seed-boundary Contract](0055-titan-seed-boundary-contract.md) (`docs/decisions/0055-titan-seed-boundary-contract.md`)

### `agon`

- [0016 Agon Mechanic Package](0016-agon-mechanic-package.md) (`docs/decisions/0016-agon-mechanic-package.md`)
- [0054 Agon Part Contract Guard](0054-agon-part-contract-guard.md) (`docs/decisions/0054-agon-part-contract-guard.md`)
- [0098 Agon Quest-note Provenance Route](0098-agon-quest-note-provenance-route.md) (`docs/decisions/0098-agon-quest-note-provenance-route.md`)

### `recurrence`

- [0031 Recurrence Mechanic Package](0031-recurrence-mechanic-package.md) (`docs/decisions/0031-recurrence-mechanic-package.md`)
- [0039 Recurrence Support Parts Expansion](0039-recurrence-support-parts-expansion.md) (`docs/decisions/0039-recurrence-support-parts-expansion.md`)
- [0042 Recurrence Portable Proof Beacons Part](0042-recurrence-portable-proof-beacons-part.md) (`docs/decisions/0042-recurrence-portable-proof-beacons-part.md`)
- [0066 Recurrence Control-plane Contract](0066-recurrence-control-plane-contract.md) (`docs/decisions/0066-recurrence-control-plane-contract.md`)

### `checkpoint`

- [0032 Checkpoint Mechanic Package](0032-checkpoint-mechanic-package.md) (`docs/decisions/0032-checkpoint-mechanic-package.md`)
- [0062 Checkpoint Part Contract Guard](0062-checkpoint-part-contract-guard.md) (`docs/decisions/0062-checkpoint-part-contract-guard.md`)

### `experience`

- [0033 Experience Mechanic Package](0033-experience-mechanic-package.md) (`docs/decisions/0033-experience-mechanic-package.md`)
- [0043 Experience Verdict Residue Parts](0043-experience-verdict-residue-parts.md) (`docs/decisions/0043-experience-verdict-residue-parts.md`)
- [0063 Experience Part Contract Guard](0063-experience-part-contract-guard.md) (`docs/decisions/0063-experience-part-contract-guard.md`)

### `antifragility`

- [0034 Antifragility Mechanic Package](0034-antifragility-mechanic-package.md) (`docs/decisions/0034-antifragility-mechanic-package.md`)
- [0061 Antifragility Part Contract Guard](0061-antifragility-part-contract-guard.md) (`docs/decisions/0061-antifragility-part-contract-guard.md`)

### `method-growth`

- [0035 Method-growth Mechanic Package](0035-method-growth-mechanic-package.md) (`docs/decisions/0035-method-growth-mechanic-package.md`)
- [0068 Method-growth Part Owner-split Contract](0068-method-growth-part-owner-split-contract.md) (`docs/decisions/0068-method-growth-part-owner-split-contract.md`)

### `rpg`

- [0036 RPG Mechanic Package](0036-rpg-mechanic-package.md) (`docs/decisions/0036-rpg-mechanic-package.md`)
- [0067 RPG Progression-unlocks Contract](0067-rpg-progression-unlocks-contract.md) (`docs/decisions/0067-rpg-progression-unlocks-contract.md`)

### `growth-cycle`

- [0037 Growth-cycle Mechanic Package](0037-growth-cycle-mechanic-package.md) (`docs/decisions/0037-growth-cycle-mechanic-package.md`)
- [0065 Growth-cycle Diagnosis-gate Contract](0065-growth-cycle-diagnosis-gate-contract.md) (`docs/decisions/0065-growth-cycle-diagnosis-gate-contract.md`)

### `distillation`

- [0038 Distillation Mechanic Package](0038-distillation-mechanic-package.md) (`docs/decisions/0038-distillation-mechanic-package.md`)
- [0064 Distillation Part Contract Guard](0064-distillation-part-contract-guard.md) (`docs/decisions/0064-distillation-part-contract-guard.md`)

### `questbook`

- [0004 Questbook Topology](0004-questbook-topology.md) (`docs/decisions/0004-questbook-topology.md`)
- [0006 Questbook Mechanic Package](0006-questbook-mechanic-package.md) (`docs/decisions/0006-questbook-mechanic-package.md`)
- [0047 Questbook Schema Parts](0047-questbook-schema-parts.md) (`docs/decisions/0047-questbook-schema-parts.md`)
- [0070 Questbook Part Owner-split Contract](0070-questbook-part-owner-split-contract.md) (`docs/decisions/0070-questbook-part-owner-split-contract.md`)

### `audit`

- [0007 Audit Mechanic Package](0007-audit-mechanic-package.md) (`docs/decisions/0007-audit-mechanic-package.md`)
- [0025 Release Support Readiness Audit](0025-release-support-readiness-audit.md) (`docs/decisions/0025-release-support-readiness-audit.md`)
- [0026 Strategic Closeout Audit](0026-strategic-closeout-audit.md) (`docs/decisions/0026-strategic-closeout-audit.md`)
- [0053 Audit Part Contract Guard](0053-audit-part-contract-guard.md) (`docs/decisions/0053-audit-part-contract-guard.md`)

### `boundary-bridge`

- [0008 Boundary Bridge Mechanic Package](0008-boundary-bridge-mechanic-package.md) (`docs/decisions/0008-boundary-bridge-mechanic-package.md`)
- [0044 Boundary Bridge Orchestrator Proof Anchors](0044-boundary-bridge-orchestrator-proof-anchors.md) (`docs/decisions/0044-boundary-bridge-orchestrator-proof-anchors.md`)
- [0046 Boundary Bridge Phase Alpha Eval Matrix](0046-boundary-bridge-phase-alpha-eval-matrix.md) (`docs/decisions/0046-boundary-bridge-phase-alpha-eval-matrix.md`)
- [0056 Boundary Bridge Part Contract Guard](0056-boundary-bridge-part-contract-guard.md) (`docs/decisions/0056-boundary-bridge-part-contract-guard.md`)

### Cross-parent mechanic decisions

- [0052 Mechanic Parent Allowlist](0052-mechanic-parent-allowlist.md) (`docs/decisions/0052-mechanic-parent-allowlist.md`)
- [0071 Mechanic Legacy Archive Boundary](0071-mechanic-legacy-skeleton-contract.md) (`docs/decisions/0071-mechanic-legacy-skeleton-contract.md`)
- [0072 Mechanic Parent Class Contract](0072-mechanic-parent-class-contract.md) (`docs/decisions/0072-mechanic-parent-class-contract.md`)
- [0074 Mechanic Part README Contract](0074-mechanic-part-readme-contract.md) (`docs/decisions/0074-mechanic-part-readme-contract.md`)
- [0075 Mechanic Provenance Entry Contract](0075-mechanic-provenance-entry-contract.md) (`docs/decisions/0075-mechanic-provenance-entry-contract.md`)
- [0076 Active Mechanic Route Residue Guard](0076-active-mechanic-route-residue-guard.md) (`docs/decisions/0076-active-mechanic-route-residue-guard.md`)
- [0081 Mechanic Payload Route Residue Guard](0081-mechanic-payload-route-residue-guard.md) (`docs/decisions/0081-mechanic-payload-route-residue-guard.md`)
- [0082 Mechanic Parent Direction Contract](0082-mechanic-parent-direction-contract.md) (`docs/decisions/0082-mechanic-parent-direction-contract.md`)
- [0083 Mechanic Evidence Dimension Ledger](0083-mechanic-evidence-dimension-ledger.md) (`docs/decisions/0083-mechanic-evidence-dimension-ledger.md`)
- [0084 Mechanic Root-district Reconnaissance](0084-mechanic-root-district-reconnaissance.md) (`docs/decisions/0084-mechanic-root-district-reconnaissance.md`)
- [0086 Mechanic Part Payload Inventory](0086-mechanic-part-payload-inventory.md) (`docs/decisions/0086-mechanic-part-payload-inventory.md`)
- [0087 Mechanic Part Validation Command Reachability](0087-mechanic-part-validation-command-reachability.md) (`docs/decisions/0087-mechanic-part-validation-command-reachability.md`)
- [0088 Mechanic PARTS Index Synchronization](0088-mechanic-parts-index-synchronization.md) (`docs/decisions/0088-mechanic-parts-index-synchronization.md`)
- [0089 Mechanic Legacy Single Bridge](0089-mechanic-legacy-single-bridge.md) (`docs/decisions/0089-mechanic-legacy-single-bridge.md`)
- [0090 Mechanic Provenance Bridge Posture](0090-mechanic-provenance-bridge-posture.md) (`docs/decisions/0090-mechanic-provenance-bridge-posture.md`)
- [0094 Mechanic Part Source Surface Reference Guard](0094-mechanic-part-source-surface-reference-guard.md) (`docs/decisions/0094-mechanic-part-source-surface-reference-guard.md`)
- [0095 Mechanic Part Source Surfaces Section Contract](0095-mechanic-part-source-surfaces-section-contract.md) (`docs/decisions/0095-mechanic-part-source-surfaces-section-contract.md`)
- [0097 Mechanic Parent Guidance Boundary](0097-mechanic-parent-guidance-boundary.md) (`docs/decisions/0097-mechanic-parent-guidance-boundary.md`)
- [0100 Active Mechanics Topology Wording](0100-active-mechanics-topology-wording.md) (`docs/decisions/0100-active-mechanics-topology-wording.md`)
- [0101 Mechanic Evidence Route Refs](0101-mechanic-evidence-route-refs.md) (`docs/decisions/0101-mechanic-evidence-route-refs.md`)
- [0102 Mechanic Part Validation Command Ownership](0102-mechanic-part-validation-command-ownership.md) (`docs/decisions/0102-mechanic-part-validation-command-ownership.md`)

## Index By Validation Guard Family

### Route residue guards

- [0073 Generated Route Residue Guard](0073-generated-route-residue-guard.md) (`docs/decisions/0073-generated-route-residue-guard.md`)
- [0076 Active Mechanic Route Residue Guard](0076-active-mechanic-route-residue-guard.md) (`docs/decisions/0076-active-mechanic-route-residue-guard.md`)
- [0077 Root Authored Route Residue Guard](0077-root-authored-route-residue-guard.md) (`docs/decisions/0077-root-authored-route-residue-guard.md`)
- [0078 Decision Route Residue Guard](0078-decision-route-residue-guard.md) (`docs/decisions/0078-decision-route-residue-guard.md`)
- [0079 Repo Config Route Residue Guard](0079-repo-config-route-residue-guard.md) (`docs/decisions/0079-repo-config-route-residue-guard.md`)
- [0080 Source Bundle Route Residue Guard](0080-source-bundle-route-residue-guard.md) (`docs/decisions/0080-source-bundle-route-residue-guard.md`)
- [0081 Mechanic Payload Route Residue Guard](0081-mechanic-payload-route-residue-guard.md) (`docs/decisions/0081-mechanic-payload-route-residue-guard.md`)

### Parent and package guards

- [0052 Mechanic Parent Allowlist](0052-mechanic-parent-allowlist.md) (`docs/decisions/0052-mechanic-parent-allowlist.md`)
- [0072 Mechanic Parent Class Contract](0072-mechanic-parent-class-contract.md) (`docs/decisions/0072-mechanic-parent-class-contract.md`)
- [0082 Mechanic Parent Direction Contract](0082-mechanic-parent-direction-contract.md) (`docs/decisions/0082-mechanic-parent-direction-contract.md`)
- [0083 Mechanic Evidence Dimension Ledger](0083-mechanic-evidence-dimension-ledger.md) (`docs/decisions/0083-mechanic-evidence-dimension-ledger.md`)
- [0097 Mechanic Parent Guidance Boundary](0097-mechanic-parent-guidance-boundary.md) (`docs/decisions/0097-mechanic-parent-guidance-boundary.md`)
- [0101 Mechanic Evidence Route Refs](0101-mechanic-evidence-route-refs.md) (`docs/decisions/0101-mechanic-evidence-route-refs.md`)

### Part and payload guards

- [0029 Comparison Spine Report Parts](0029-comparison-spine-report-parts.md) (`docs/decisions/0029-comparison-spine-report-parts.md`)
- [0030 Proof Loop Route-Smoke Part](0030-proof-loop-route-smoke-part.md) (`docs/decisions/0030-proof-loop-route-smoke-part.md`)
- [0039 Recurrence Support Parts Expansion](0039-recurrence-support-parts-expansion.md) (`docs/decisions/0039-recurrence-support-parts-expansion.md`)
- [0040 Comparison Spine Fixture Parts](0040-comparison-spine-fixture-parts.md) (`docs/decisions/0040-comparison-spine-fixture-parts.md`)
- [0042 Recurrence Portable Proof Beacons Part](0042-recurrence-portable-proof-beacons-part.md) (`docs/decisions/0042-recurrence-portable-proof-beacons-part.md`)
- [0043 Experience Verdict Residue Parts](0043-experience-verdict-residue-parts.md) (`docs/decisions/0043-experience-verdict-residue-parts.md`)
- [0047 Questbook Schema Parts](0047-questbook-schema-parts.md) (`docs/decisions/0047-questbook-schema-parts.md`)
- [0048 Proof Object Contract Parts](0048-proof-object-contract-parts.md) (`docs/decisions/0048-proof-object-contract-parts.md`)
- [0053 Audit Part Contract Guard](0053-audit-part-contract-guard.md) (`docs/decisions/0053-audit-part-contract-guard.md`)
- [0054 Agon Part Contract Guard](0054-agon-part-contract-guard.md) (`docs/decisions/0054-agon-part-contract-guard.md`)
- [0056 Boundary Bridge Part Contract Guard](0056-boundary-bridge-part-contract-guard.md) (`docs/decisions/0056-boundary-bridge-part-contract-guard.md`)
- [0057 Publication Receipts Part Contract Guard](0057-publication-receipts-part-contract-guard.md) (`docs/decisions/0057-publication-receipts-part-contract-guard.md`)
- [0058 Release Support Part Contract Guard](0058-release-support-part-contract-guard.md) (`docs/decisions/0058-release-support-part-contract-guard.md`)
- [0059 Comparison Spine Part Contract Guard](0059-comparison-spine-part-contract-guard.md) (`docs/decisions/0059-comparison-spine-part-contract-guard.md`)
- [0061 Antifragility Part Contract Guard](0061-antifragility-part-contract-guard.md) (`docs/decisions/0061-antifragility-part-contract-guard.md`)
- [0062 Checkpoint Part Contract Guard](0062-checkpoint-part-contract-guard.md) (`docs/decisions/0062-checkpoint-part-contract-guard.md`)
- [0063 Experience Part Contract Guard](0063-experience-part-contract-guard.md) (`docs/decisions/0063-experience-part-contract-guard.md`)
- [0064 Distillation Part Contract Guard](0064-distillation-part-contract-guard.md) (`docs/decisions/0064-distillation-part-contract-guard.md`)
- [0068 Method-growth Part Owner-split Contract](0068-method-growth-part-owner-split-contract.md) (`docs/decisions/0068-method-growth-part-owner-split-contract.md`)
- [0069 Proof-object Part Owner-split Contract](0069-proof-object-part-owner-split-contract.md) (`docs/decisions/0069-proof-object-part-owner-split-contract.md`)
- [0070 Questbook Part Owner-split Contract](0070-questbook-part-owner-split-contract.md) (`docs/decisions/0070-questbook-part-owner-split-contract.md`)
- [0074 Mechanic Part README Contract](0074-mechanic-part-readme-contract.md) (`docs/decisions/0074-mechanic-part-readme-contract.md`)
- [0081 Mechanic Payload Route Residue Guard](0081-mechanic-payload-route-residue-guard.md) (`docs/decisions/0081-mechanic-payload-route-residue-guard.md`)
- [0086 Mechanic Part Payload Inventory](0086-mechanic-part-payload-inventory.md) (`docs/decisions/0086-mechanic-part-payload-inventory.md`)
- [0087 Mechanic Part Validation Command Reachability](0087-mechanic-part-validation-command-reachability.md) (`docs/decisions/0087-mechanic-part-validation-command-reachability.md`)
- [0088 Mechanic PARTS Index Synchronization](0088-mechanic-parts-index-synchronization.md) (`docs/decisions/0088-mechanic-parts-index-synchronization.md`)
- [0094 Mechanic Part Source Surface Reference Guard](0094-mechanic-part-source-surface-reference-guard.md) (`docs/decisions/0094-mechanic-part-source-surface-reference-guard.md`)
- [0095 Mechanic Part Source Surfaces Section Contract](0095-mechanic-part-source-surfaces-section-contract.md) (`docs/decisions/0095-mechanic-part-source-surfaces-section-contract.md`)
- [0102 Mechanic Part Validation Command Ownership](0102-mechanic-part-validation-command-ownership.md) (`docs/decisions/0102-mechanic-part-validation-command-ownership.md`)
- [0105 Proof-object Eval Part Names](0105-proof-object-eval-part-names.md) (`docs/decisions/0105-proof-object-eval-part-names.md`)

### Legacy and provenance guards

- [0009 Legacy Naming Containment](0009-legacy-naming-containment.md) (`docs/decisions/0009-legacy-naming-containment.md`)
- [0071 Mechanic Legacy Archive Boundary](0071-mechanic-legacy-skeleton-contract.md) (`docs/decisions/0071-mechanic-legacy-skeleton-contract.md`)
- [0075 Mechanic Provenance Entry Contract](0075-mechanic-provenance-entry-contract.md) (`docs/decisions/0075-mechanic-provenance-entry-contract.md`)
- [0089 Mechanic Legacy Single Bridge](0089-mechanic-legacy-single-bridge.md) (`docs/decisions/0089-mechanic-legacy-single-bridge.md`)
- [0090 Mechanic Provenance Bridge Posture](0090-mechanic-provenance-bridge-posture.md) (`docs/decisions/0090-mechanic-provenance-bridge-posture.md`)
- [0091 Legacy Naming Single-Bridge Language](0091-legacy-naming-single-bridge-language.md) (`docs/decisions/0091-legacy-naming-single-bridge-language.md`)
- [0092 Active Legacy Parent Wording Boundary](0092-active-legacy-parent-wording-boundary.md) (`docs/decisions/0092-active-legacy-parent-wording-boundary.md`)
- [0096 Legacy Naming Posture Guide](0096-legacy-naming-posture-guide.md) (`docs/decisions/0096-legacy-naming-posture-guide.md`)
- [0098 Agon Quest-note Provenance Route](0098-agon-quest-note-provenance-route.md) (`docs/decisions/0098-agon-quest-note-provenance-route.md`)

### Generated, report, receipt, and runtime guards

- [0013 Publication Receipts Mechanic Package](0013-publication-receipts-mechanic-package.md) (`docs/decisions/0013-publication-receipts-mechanic-package.md`)
- [0014 Release Support Mechanic Package](0014-release-support-mechanic-package.md) (`docs/decisions/0014-release-support-mechanic-package.md`)
- [0020 Proof Loop Local Smoke Report](0020-proof-loop-local-smoke-report.md) (`docs/decisions/0020-proof-loop-local-smoke-report.md`)
- [0022 Proof Loop Bundle-Local Report](0022-proof-loop-bundle-local-report.md) (`docs/decisions/0022-proof-loop-bundle-local-report.md`)
- [0023 Eval Report Index Reader](0023-eval-report-index-reader.md) (`docs/decisions/0023-eval-report-index-reader.md`)
- [0024 Receipt Intake Dry Review](0024-receipt-intake-dry-review.md) (`docs/decisions/0024-receipt-intake-dry-review.md`)
- [0025 Release Support Readiness Audit](0025-release-support-readiness-audit.md) (`docs/decisions/0025-release-support-readiness-audit.md`)
- [0026 Strategic Closeout Audit](0026-strategic-closeout-audit.md) (`docs/decisions/0026-strategic-closeout-audit.md`)
- [0027 Release Prep PR Handoff](0027-release-prep-pr-handoff.md) (`docs/decisions/0027-release-prep-pr-handoff.md`)
- [0029 Comparison Spine Report Parts](0029-comparison-spine-report-parts.md) (`docs/decisions/0029-comparison-spine-report-parts.md`)
- [0045 Closeout Writeback Ingress Boundary](0045-closeout-writeback-ingress-boundary.md) (`docs/decisions/0045-closeout-writeback-ingress-boundary.md`)
- [0046 Boundary Bridge Phase Alpha Eval Matrix](0046-boundary-bridge-phase-alpha-eval-matrix.md) (`docs/decisions/0046-boundary-bridge-phase-alpha-eval-matrix.md`)
- [0049 Proof Infra Reportable Contracts](0049-proof-infra-reportable-contracts.md) (`docs/decisions/0049-proof-infra-reportable-contracts.md`)
- [0057 Publication Receipts Part Contract Guard](0057-publication-receipts-part-contract-guard.md) (`docs/decisions/0057-publication-receipts-part-contract-guard.md`)
- [0058 Release Support Part Contract Guard](0058-release-support-part-contract-guard.md) (`docs/decisions/0058-release-support-part-contract-guard.md`)
- [0073 Generated Route Residue Guard](0073-generated-route-residue-guard.md) (`docs/decisions/0073-generated-route-residue-guard.md`)

### Sibling and boundary guards

- [0003 Sibling Proof Reference Compatibility](0003-sibling-proof-reference-compatibility.md) (`docs/decisions/0003-sibling-proof-reference-compatibility.md`)
- [0008 Boundary Bridge Mechanic Package](0008-boundary-bridge-mechanic-package.md) (`docs/decisions/0008-boundary-bridge-mechanic-package.md`)
- [0044 Boundary Bridge Orchestrator Proof Anchors](0044-boundary-bridge-orchestrator-proof-anchors.md) (`docs/decisions/0044-boundary-bridge-orchestrator-proof-anchors.md`)
- [0045 Closeout Writeback Ingress Boundary](0045-closeout-writeback-ingress-boundary.md) (`docs/decisions/0045-closeout-writeback-ingress-boundary.md`)
- [0046 Boundary Bridge Phase Alpha Eval Matrix](0046-boundary-bridge-phase-alpha-eval-matrix.md) (`docs/decisions/0046-boundary-bridge-phase-alpha-eval-matrix.md`)
- [0055 Titan Seed-boundary Contract](0055-titan-seed-boundary-contract.md) (`docs/decisions/0055-titan-seed-boundary-contract.md`)
- [0056 Boundary Bridge Part Contract Guard](0056-boundary-bridge-part-contract-guard.md) (`docs/decisions/0056-boundary-bridge-part-contract-guard.md`)
- [0068 Method-growth Part Owner-split Contract](0068-method-growth-part-owner-split-contract.md) (`docs/decisions/0068-method-growth-part-owner-split-contract.md`)
- [0069 Proof-object Part Owner-split Contract](0069-proof-object-part-owner-split-contract.md) (`docs/decisions/0069-proof-object-part-owner-split-contract.md`)
- [0070 Questbook Part Owner-split Contract](0070-questbook-part-owner-split-contract.md) (`docs/decisions/0070-questbook-part-owner-split-contract.md`)
- [0071 Mechanic Legacy Archive Boundary](0071-mechanic-legacy-skeleton-contract.md) (`docs/decisions/0071-mechanic-legacy-skeleton-contract.md`)
- [0089 Mechanic Legacy Single Bridge](0089-mechanic-legacy-single-bridge.md) (`docs/decisions/0089-mechanic-legacy-single-bridge.md`)
- [0090 Mechanic Provenance Bridge Posture](0090-mechanic-provenance-bridge-posture.md) (`docs/decisions/0090-mechanic-provenance-bridge-posture.md`)
- [0091 Legacy Naming Single-Bridge Language](0091-legacy-naming-single-bridge-language.md) (`docs/decisions/0091-legacy-naming-single-bridge-language.md`)
- [0092 Active Legacy Parent Wording Boundary](0092-active-legacy-parent-wording-boundary.md) (`docs/decisions/0092-active-legacy-parent-wording-boundary.md`)
- [0097 Mechanic Parent Guidance Boundary](0097-mechanic-parent-guidance-boundary.md) (`docs/decisions/0097-mechanic-parent-guidance-boundary.md`)
- [0099 Repair Diagnosis Route Boundary](0099-repair-diagnosis-route-boundary.md) (`docs/decisions/0099-repair-diagnosis-route-boundary.md`)

## Queued Decision Topics

These topics are known but should become decision notes only when they constrain
a concrete near-term change:

- Future maintained agent lanes beyond Spark.
- Stricter quest lifecycle transition rules after a real state movement needs
  them.
- Further proof-loop examples or checklists only after another reviewed local
  run needs them.
- A real eval-result receipt publication only after the dry-reviewed intake
  route from
  `mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json` needs a live owner
  append.
- Further PR movement after the release-prep PR handoff only through current git
  and GitHub state; do not read
  `mechanics/release-support/parts/pr-handoff/reports/release-prep-pr-handoff-v1.json` as live PR status after branch or PR
  creation.
- Goal completion only after `mechanics/release-support/parts/strategic-closeout/reports/strategic-closeout-audit-v1.json` is
  reread against the landed diff, GitHub `Repo Validation` is observed, and the
  owner-visible final closeout says the goal is actually complete.
- Future pinned sibling checkout refreshes only after the failing public CI lane
  is compared against current sibling truth and the local proof-reference map.

## Naming

Use monotonically increasing four-digit numbers:

`0016-short-decision-slug.md`

Prefer short titles that name the route, not the whole debate.

## Template

Start from [TEMPLATE.md](TEMPLATE.md) for new decisions. Keep notes concise, but
include enough context, alternatives, consequences, and validation for a future
agent to avoid repeating the same mistake.
