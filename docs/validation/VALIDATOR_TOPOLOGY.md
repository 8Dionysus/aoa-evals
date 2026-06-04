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
| `generated` | blocking projection gate | generated catalog, generated report index, runtime-candidate reader parity, and boundary-bridge read-model parity | eval source meaning, sibling truth, runtime policy |
| `mechanics/part-local` | blocking mechanic-owned gate | mechanic part tests and part-owned builders or validators | root release freeze, public proof interpretation |
| `pinned-sibling` | compatibility-only gate | explicit compatibility proof against clean pinned dependency checkouts when a PR or release makes that claim | `aoa-evals` release identity or latest sibling growth-surface drift |
| `latest-sibling` | advisory moving-sibling canary | local compatibility signal against current sibling repositories | release pass/fail identity |
| `trace/eval` | advisory proof-behavior lane | trace, trajectory, tool-call, outcome, and grader route coverage for future eval harness work | hard runtime execution or model-quality verdicts without a bounded eval bundle |
| `audit` | advisory review lane | evidence sufficiency, route residue, proof limits, receipts, and review/handoff reports | release blocking unless promoted by a decision |
| `release` | blocking release gate | frozen local release sequence through `scripts/release_check.py` | ordinary PR growth gating, pinned sibling compatibility, and moving-main canaries |
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

## Validator Modules

`scripts/validate_repo.py` remains the repo-wide compatibility entrypoint while
the implementation is split by owner route. Current focused modules are:

- `scripts/validators/agon.py`
- `scripts/validators/antifragility.py`
- `scripts/validators/audit.py`
- `scripts/validators/artifact_hooks.py`
- `scripts/validators/boundary_bridge.py`
- `scripts/validators/checkpoint.py`
- `scripts/validators/common.py`
- `scripts/validators/root_context.py`
- `scripts/validators/comparison_spine.py`
- `scripts/validators/distillation.py`
- `scripts/validators/docs_decisions.py`
- `scripts/validators/docs_routes.py`
- `scripts/validators/docs_topology.py`
- `scripts/validators/eval_bundles.py`
- `scripts/validators/evidence_readouts.py`
- `scripts/validators/experience.py`
- `scripts/validators/generated_parity.py`
- `scripts/validators/growth_cycle.py`
- `scripts/validators/mechanic_legacy.py`
- `scripts/validators/mechanic_parents.py`
- `scripts/validators/mechanic_parts.py`
- `scripts/validators/mechanics.py`
- `scripts/validators/mechanics_routes.py`
- `scripts/validators/method_growth.py`
- `scripts/validators/phase_alpha_matrix.py`
- `scripts/validators/proof_infra.py`
- `scripts/validators/proof_loop.py`
- `scripts/validators/proof_object.py`
- `scripts/validators/publication_receipts.py`
- `scripts/validators/questbook.py`
- `scripts/validators/recurrence.py`
- `scripts/validators/release_support.py`
- `scripts/validators/report_index.py`
- `scripts/validators/root_authority.py`
- `scripts/validators/root_guidance.py`
- `scripts/validators/root_route_cards.py`
- `scripts/validators/root_topology.py`
- `scripts/validators/route_residue.py`
- `scripts/validators/rpg.py`
- `scripts/validators/runtime_audit.py`
- `scripts/validators/runtime_candidates.py`
- `scripts/validators/source_eval_domains.py`
- `scripts/validators/source_doctrine.py`
- `scripts/validators/source_eval_contracts.py`
- `scripts/validators/titan.py`
- `scripts/validators/validation_topology.py`

Future splits should move another coherent owner surface at a time. Do not
create a second root validator or a broad `validate_everything.py`.

## Agentic AI-OS Boundaries

The proof canon needs visibility for agentic failure surfaces even before every
surface is a hard gate:

- Source/topology validators protect authored source and owner boundaries.
- Projection/generated validators protect rebuild parity and provenance.
- Capability/runtime-policy validators remain route-only until a runtime owner
  exposes enforceable policy.
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
