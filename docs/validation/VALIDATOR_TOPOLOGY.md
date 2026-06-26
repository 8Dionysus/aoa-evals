# Validator Topology

Validators in `aoa-evals` are boundary organs for a bounded proof canon. They
protect source proof objects, generated projections, mechanic-local payloads,
release evidence, and advisory compatibility/runtime or agent-behavior
boundaries.

They must not become a historical pile where each proof wave leaves a private
gate that only one script remembers.

## Lanes

| Lane | Posture | Owns | Does not own |
| --- | --- | --- | --- |
| `source-fast` | blocking growth gate | route cards, semantic AGENTS shape, source eval entry/topology, docs/decision topology, root proof boundaries | full generated freshness, release packaging, latest sibling drift |
| `generated` | blocking projection gate | generated catalog, generated report index, runtime-candidate reader parity, and boundary-bridge read-model parity | eval source meaning, sibling truth, runtime policy enforcement |
| `mechanics/part-local` | blocking mechanic-owned gate | mechanic part tests and part-owned builders or validators | root release freeze, public proof interpretation |
| `pinned-sibling` | compatibility-only gate | explicit compatibility proof against clean pinned dependency checkouts when a PR or release makes that claim | `aoa-evals` release identity or latest sibling growth-surface drift |
| `latest-sibling` | advisory moving-sibling canary | local compatibility signal against current sibling repositories | release pass/fail identity |
| `trace/eval` | advisory proof-behavior lane | trace, trajectory, tool-call, outcome, and grader route coverage for future eval harness work | hard runtime execution or model-quality verdicts without a bounded eval bundle |
| `audit` | advisory review lane | evidence sufficiency, route residue, proof limits, receipts, and review/handoff reports | release blocking unless promoted by a decision |
| `release` | blocking release gate | frozen local release sequence through `scripts/release_check.py`, including OS Abyss report-index artifact bundle identity/provenance | ordinary PR growth gating, pinned sibling compatibility, and moving-main canaries |
| `nightly` | moving-main sentinel | source, generated, part-local, and moving-sibling drift evidence | release artifact identity |
| `advisory` | non-blocking boundary inventory | capability/runtime policy, memory/context, inter-agent handoff, observability, and security/adversarial routes | prompt-only guardrails as a security boundary |

## Source/Projection Boundary

Authored source surfaces own meaning:

- `evals/**/EVAL.md` and `evals/**/eval.yaml`
- route cards and proof topology docs
- mechanic parent and part contracts
- decision records for durable rationale

Generated readers, catalogs, runtime-candidate indexes, report indexes, and
boundary-bridge matrices are projections. Generated validators may rebuild
expected payloads from source and compare parity. They do not define what an
eval proves.

The release lane also validates the generated report index as an OS Abyss
artifact bundle through
`scripts/validate_abyss_machine_report_index_bundle.py`. That check proves the
release carrier's ABI/SBOM/SLSA sidecars, release-ready registry latest
selection, consumer `trust-gate` admission, and negative bundle/registry
scenarios against `abyss-machine` policy; it does not promote
`generated/eval_report_index.min.json` above bundle-local proof sources.

`scripts/validate_os_abyss_artifact_trust_plane.py` is the advisory host proof
for the wider OS Abyss artifact trust plane. It reads live `abyss-machine`
requirements, producer profiles, full trust coverage, durable-only trust
coverage, and affected drift read-models to prove scenario coverage,
producer-owner profile coverage, agent-loop command coverage, manual
positive/negative evidence, durable-registry downgrade behavior, and sibling
accepted-lag behavior. The advisory pass may also accept a declared real
blocker only when `abyss-machine` still proves durable latest selection,
fresh source contracts, trust-gate admission, required controls, and explicit
class-specific blocker text; it must not turn a production trust gap into a
release identity shortcut. It is intentionally not part of `release_check.py`,
because it reads live host trust-plane state rather than this repository's
release identity.

Memo-shaped runtime evidence selection packets must carry a
`memory_context_boundary`. The selected-evidence source example owns the
boundary fields; runtime-candidate readers project them so recall,
contradiction, freshness, retention, permission, and writeback pressure stays
visible without turning memory context into proof authority, action
authorization, source truth, or a local memo port.

## Validator Modules

`scripts/validate_repo.py` remains the repo-wide compatibility entrypoint while
the implementation is split by owner route. Current focused modules are:

- `scripts/validators/agon_route_paths.py`
- `scripts/validators/agon_route_tokens.py`
- `scripts/validators/agon_routes.py`
- `scripts/validators/antifragility_route_paths.py`
- `scripts/validators/antifragility_route_tokens.py`
- `scripts/validators/antifragility_routes.py`
- `scripts/validators/audit_route_helpers.py`
- `scripts/validators/audit_route_paths.py`
- `scripts/validators/audit_route_tokens.py`
- `scripts/validators/audit_routes.py`
- `scripts/validators/artifact_hooks.py`
- `scripts/validators/boundary_bridge_canary.py`
- `scripts/validators/boundary_bridge_common.py`
- `scripts/validators/boundary_bridge_routes.py`
- `scripts/validators/boundary_bridge_workflow.py`
- `scripts/validators/checkpoint_route_paths.py`
- `scripts/validators/checkpoint_route_tokens.py`
- `scripts/validators/checkpoint_routes.py`
- `scripts/validators/common.py`
- `scripts/validators/root_context.py`
- `scripts/validators/root_route_tokens.py`
- `scripts/validators/comparison_spine_paths.py`
- `scripts/validators/comparison_spine_tokens.py`
- `scripts/validators/comparison_spine_route_helpers.py`
- `scripts/validators/comparison_spine_routes.py`
- `scripts/validators/decision_index_paths.py`
- `scripts/validators/decision_records.py`
- `scripts/validators/decision_index_renderer.py`
- `scripts/validators/decision_lane_surfaces.py`
- `scripts/validators/decision_index_surfaces.py`
- `scripts/validators/distillation_route_paths.py`
- `scripts/validators/distillation_route_tokens.py`
- `scripts/validators/distillation_routes.py`
- `scripts/validators/docs_routes.py`
- `scripts/validators/docs_topology.py`
- `scripts/validators/eval_bundle_common.py`
- `scripts/validators/eval_entry_cards.py`
- `scripts/validators/eval_starter_surfaces.py`
- `scripts/validators/eval_roadmap_parity.py`
- `scripts/validators/eval_entry_routes.py`
- `scripts/validators/eval_tree_topology.py`
- `scripts/validators/experience_route_paths.py`
- `scripts/validators/experience_route_tokens.py`
- `scripts/validators/experience_routes.py`
- `scripts/validators/generated_eval_capsules.py`
- `scripts/validators/generated_eval_catalogs.py`
- `scripts/validators/generated_eval_comparison_spine.py`
- `scripts/validators/generated_eval_readmodel_common.py`
- `scripts/validators/generated_eval_sections.py`
- `scripts/validators/generated_readouts.py`
- `scripts/validators/generated_route_surfaces.py`
- `scripts/validators/growth_cycle_route_paths.py`
- `scripts/validators/growth_cycle_route_tokens.py`
- `scripts/validators/growth_cycle_routes.py`
- `scripts/validators/active_legacy_parent_wording.py`
- `scripts/validators/mechanic_legacy_archive.py`
- `scripts/validators/mechanic_legacy_common.py`
- `scripts/validators/mechanic_provenance_bridge.py`
- `scripts/validators/mechanic_evidence_dimensions.py`
- `scripts/validators/mechanic_evidence_route_refs.py`
- `scripts/validators/mechanic_parent_allowlist.py`
- `scripts/validators/mechanic_parent_common.py`
- `scripts/validators/mechanic_parent_direction.py`
- `scripts/validators/mechanic_parent_guidance.py`
- `scripts/validators/mechanic_parent_index.py`
- `scripts/validators/mechanic_parent_registry.py`
- `scripts/validators/mechanic_part_contract_common.py`
- `scripts/validators/mechanic_part_contract_index.py`
- `scripts/validators/mechanic_part_payload_inventory.py`
- `scripts/validators/mechanic_part_readme_contract.py`
- `scripts/validators/mechanic_part_role_headings.py`
- `scripts/validators/mechanic_part_source_surfaces.py`
- `scripts/validators/mechanic_part_validation_command_parsing.py`
- `scripts/validators/mechanic_part_validation_command_sources.py`
- `scripts/validators/mechanic_part_validation_command_tokens.py`
- `scripts/validators/mechanic_part_validation_commands.py`
- `scripts/validators/mechanic_part_validation_common.py`
- `scripts/validators/mechanic_parts_index_sync.py`
- `scripts/validators/mechanics.py`
- `scripts/validators/mechanics_common.py`
- `scripts/validators/mechanics_root_districts.py`
- `scripts/validators/mechanics_route_contexts.py`
- `scripts/validators/mechanics_routes.py`
- `scripts/validators/method_growth_route_paths.py`
- `scripts/validators/method_growth_route_tokens.py`
- `scripts/validators/method_growth_routes.py`
- `scripts/validators/observability_readouts.py`
- `scripts/validators/phase_alpha_readouts.py`
- `scripts/validators/phase_alpha_matrix_common.py`
- `scripts/validators/phase_alpha_matrix_projection.py`
- `scripts/validators/phase_alpha_matrix_sibling_compat.py`
- `scripts/validators/proof_infra_common.py`
- `scripts/validators/proof_infra_route_tokens.py`
- `scripts/validators/proof_infra_routes.py`
- `scripts/validators/proof_infra_shared_support.py`
- `scripts/validators/proof_loop_common.py`
- `scripts/validators/proof_loop_local_report.py`
- `scripts/validators/proof_loop_routes.py`
- `scripts/validators/proof_loop_smoke_report.py`
- `scripts/validators/proof_object_route_helpers.py`
- `scripts/validators/proof_object_route_paths.py`
- `scripts/validators/proof_object_route_tokens.py`
- `scripts/validators/proof_object_routes.py`
- `scripts/validators/publication_receipts_common.py`
- `scripts/validators/publication_receipts_intake_artifact.py`
- `scripts/validators/publication_receipts_intake_boundary.py`
- `scripts/validators/publication_receipts_intake_common.py`
- `scripts/validators/publication_receipts_intake_preview.py`
- `scripts/validators/publication_receipts_intake_route.py`
- `scripts/validators/publication_receipts_live.py`
- `scripts/validators/publication_receipts_payload.py`
- `scripts/validators/publication_receipts_route_paths.py`
- `scripts/validators/publication_receipts_route_tokens.py`
- `scripts/validators/publication_receipts_route_helpers.py`
- `scripts/validators/publication_receipts_routes.py`
- `scripts/validators/questbook_context.py`
- `scripts/validators/questbook_io.py`
- `scripts/validators/questbook_obligation_index.py`
- `scripts/validators/questbook_orchestrator_constants.py`
- `scripts/validators/questbook_orchestrator_refs.py`
- `scripts/validators/questbook_projection_parity.py`
- `scripts/validators/questbook_projection_records.py`
- `scripts/validators/questbook_progression.py`
- `scripts/validators/questbook_route_paths.py`
- `scripts/validators/questbook_route_tokens.py`
- `scripts/validators/questbook_routes.py`
- `scripts/validators/questbook_schema_lifecycle.py`
- `scripts/validators/questbook_source_constants.py`
- `scripts/validators/questbook_source_records.py`
- `scripts/validators/recurrence_route_paths.py`
- `scripts/validators/recurrence_route_tokens.py`
- `scripts/validators/recurrence_routes.py`
- `scripts/validators/release_support_refs.py`
- `scripts/validators/release_support_report_checks.py`
- `scripts/validators/release_support_report_commands.py`
- `scripts/validators/release_support_report_constants.py`
- `scripts/validators/release_support_route_tokens.py`
- `scripts/validators/release_support_pr_handoff_report.py`
- `scripts/validators/release_support_readiness_report.py`
- `scripts/validators/release_support_routes.py`
- `scripts/validators/release_support_strategic_closeout_report.py`
- `scripts/validators/report_index.py`
- `scripts/validators/readout_contexts.py`
- `scripts/validators/root_agent_index.py`
- `scripts/validators/root_agent_lanes.py`
- `scripts/validators/root_audit_routes.py`
- `scripts/validators/root_authored_surface_common.py`
- `scripts/validators/root_authored_surface_decision.py`
- `scripts/validators/root_authored_surface_inventory.py`
- `scripts/validators/root_authored_surface_ledger.py`
- `scripts/validators/root_common.py`
- `scripts/validators/root_context.py`
- `scripts/validators/root_route_tokens.py`
- `scripts/validators/root_decision_status.py`
- `scripts/validators/root_design_common.py`
- `scripts/validators/root_design_docs.py`
- `scripts/validators/root_eval_guides.py`
- `scripts/validators/root_frontdoor_guidance.py`
- `scripts/validators/root_guidance_common.py`
- `scripts/validators/root_index_surfaces.py`
- `scripts/validators/root_legacy_bridge_residue.py`
- `scripts/validators/root_legacy_common.py`
- `scripts/validators/root_legacy_external_leakage.py`
- `scripts/validators/root_legacy_naming.py`
- `scripts/validators/root_memory_boundary.py`
- `scripts/validators/root_operations_guidance.py`
- `scripts/validators/root_proof_topology.py`
- `scripts/validators/root_read_model_commands.py`
- `scripts/validators/root_release_guidance.py`
- `scripts/validators/root_route_cards.py`
- `scripts/validators/root_topology.py`
- `scripts/validators/root_validator_surfaces.py`
- `scripts/validators/route_residue_active_mechanics.py`
- `scripts/validators/route_residue_common.py`
- `scripts/validators/route_residue_decisions.py`
- `scripts/validators/route_residue_generated.py`
- `scripts/validators/route_residue_mechanic_payload.py`
- `scripts/validators/route_residue_repo_config.py`
- `scripts/validators/route_residue_root_authored.py`
- `scripts/validators/route_residue_source_bundle.py`
- `scripts/validators/rpg_route_paths.py`
- `scripts/validators/rpg_route_tokens.py`
- `scripts/validators/rpg_routes.py`
- `scripts/validators/runtime_audit_common.py`
- `scripts/validators/runtime_evidence_selection.py`
- `scripts/validators/runtime_integrity_review_common.py`
- `scripts/validators/runtime_integrity_review_docs.py`
- `scripts/validators/runtime_integrity_review_example.py`
- `scripts/validators/runtime_integrity_review_schema.py`
- `scripts/validators/runtime_readouts.py`
- `scripts/validators/runtime_trace_eval_bridge.py`
- `scripts/validators/runtime_candidate_common.py`
- `scripts/validators/runtime_candidate_intake.py`
- `scripts/validators/runtime_candidate_template_index.py`
- `scripts/validators/source_eval_artifact_common.py`
- `scripts/validators/source_eval_comparison.py`
- `scripts/validators/source_eval_common.py`
- `scripts/validators/source_eval_domains.py`
- `scripts/validators/source_eval_evidence.py`
- `scripts/validators/source_eval_fixture_contracts.py`
- `scripts/validators/source_eval_references.py`
- `scripts/validators/source_eval_report_artifacts.py`
- `scripts/validators/source_eval_report_longitudinal.py`
- `scripts/validators/source_eval_report_modes.py`
- `scripts/validators/source_eval_records.py`
- `scripts/validators/source_eval_runner_contracts.py`
- `scripts/validators/source_artifact_process_doctrine.py`
- `scripts/validators/source_comparison_doctrine.py`
- `scripts/validators/source_doctrine_common.py`
- `scripts/validators/source_integrity_taxonomy.py`
- `scripts/validators/source_repeated_window_doctrine.py`
- `scripts/validators/source_eval_collection.py`
- `scripts/validators/titan_canary.py`
- `scripts/validators/titan_route_paths.py`
- `scripts/validators/titan_route_tokens.py`
- `scripts/validators/titan_routes.py`
- `scripts/validators/validation_lane_manifest.py`
- `scripts/validators/validation_script_inventory.py`
- `scripts/validators/validation_test_inventory.py`
- `scripts/validators/validation_topology_common.py`
- `scripts/validators/validation_topology_docs.py`
- `scripts/validators/validation_validator_inventory.py`

Future splits should move another coherent owner surface at a time. Do not
create a second root validator or a broad `validate_everything.py`.

## Agentic AI-OS Boundaries

The proof canon needs visibility for agentic failure surfaces even before every
surface is a hard gate:

- Source/topology validators protect authored source and owner boundaries.
- Projection/generated validators protect rebuild parity and provenance.
- Capability/runtime-policy validators remain route-only until a runtime owner
  exposes enforceable policy; degradation/fallback evidence may be hard-checked
  only as bounded sidecar selection plus trace/eval pairing, not as live health.
- Policy-sensitive trace hooks may hard-check authorization, approval,
  fallback/rollback, and forbidden-claim metadata without granting tool
  permission, runtime owner approval, or cost/time cap proof.
- Trace/eval validators must inspect trajectories, tool calls, environment
  outcome, and grader records, not only final text.
- Memory/context validators must keep reviewed memory as evidence context, not
  hidden authority.
- Inter-agent/handoff validators must keep typed envelopes, delegation, replay,
  and approval routes visible.
- Observability/audit validators must prove enough trace and decision evidence
  exists for review.
- Security/adversarial validators must stay separate from ordinary lint and must
  not rely on prompt-only guardrails.
- Sibling refs in core validation prove syntax, owner route, and claim limits;
  hard target existence belongs to explicit compatibility or canary runs.

## Inventory

Machine-readable validator coverage lives in
[`validator_inventory.json`](validator_inventory.json). It records owner
surface, lane, protected layer, mode, source truth, command coverage, failure
route, and next split posture.

Script-wide coverage lives in [`SCRIPT_TOPOLOGY.md`](SCRIPT_TOPOLOGY.md) and
[`script_inventory.json`](script_inventory.json). Script inventory is
descriptive coverage, not command authority.
