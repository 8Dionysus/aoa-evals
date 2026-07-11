# OS Abyss Eval Readiness Dashboard

Generated read-model for OS-wide eval routing. It is navigation and freshness evidence,
not proof acceptance.

## Boundary

This generated read-model routes OS Abyss eval pressure. It is not a verdict, score, baseline, regression, receipt, or central proof acceptance surface.

## Summary

- Generated at: `2026-07-11T07:46:47Z`
- Workspace root: `/srv/AbyssOS`
- Central evals: 39
- Local active ports: 9
- Local invalid ports: 0
- Actionable repo routes: 9
- Runtime candidate exports: 14
- Candidate queue entries: 15
- Candidate packet imports: 5
- Eval Forge archetypes: 18
- Eval Forge candidate hints: 5
- Session-mining reviewed episodes: 20
- Support surfaces: 595 total, 429 eval-relevant
- Eval-relevant surfaces with unresolved manual review: 0
- Unsafe side-effect scripts: 4
- MCP runtime status: `ok`
- Dirty repos: 15

## Research Grounding

| Source | Adopted | Rejected |
| --- | --- | --- |
| OpenAI agent workflow evals | Start debugging agent behavior from traces that expose model calls, tool calls, guardrails, handoffs, routing changes, and regressions before hardening datasets. | Hosted trace grading or eval runs cannot become central OS Abyss proof acceptance. |
| OpenAI evaluation best practices and Evals deprecation boundary | Use objective, representative data, metrics, run/compare loops, human calibration, and continuous eval growth. | Do not couple durable OS Abyss proof control to deprecated hosted Evals platform semantics. |
| Anthropic demystifying evals for AI agents | Model agent evals as task, trials, graders, transcripts, environment outcomes, and a holistic signal stack including manual transcript review. | Do not judge agentic behavior from final text alone when tools or state changes matter. |
| LangSmith trajectory evaluations | Use deterministic trajectory matching when the expected route or tool-call sequence is the claim, and judge-based trajectory evaluation only when the valid path is flexible. | Do not flatten deterministic route-law violations into broad LLM judge prompts. |
| LangChain Agent Evaluation Readiness Checklist | Manually review real traces before infrastructure, separate capability from regression evals, assign owner expertise, and choose run/trace/thread level deliberately. | Do not automate mining before labels, reject taxonomy, owner gates, and error analysis exist. |
| Promptfoo coding-agent eval guidance | Coding agents require trajectory, trace/metadata assertions, cost/latency posture, repeated runs, and disposable workspaces for write-capable tests. | Do not treat a coding agent as a one-shot text completion when file, shell, runtime, and state effects matter. |
| Model Context Protocol security best practices | MCP write-capable tools need explicit safety boundaries, least-privilege scope, consent posture, and validation; access-plane responses should make side effects visible. | Do not let an MCP adapter become proof authority, arbitrary code execution, or a hidden write plane. |
| Model Context Protocol 2025-06-18 specification | Treat tools as potentially arbitrary code and require clear user/tool safety expectations before invocation. | Do not rely on tool descriptions or generated readouts as trusted proof without owner validation. |
| NSA MCP Security Design Considerations | Use secure-by-default implementation rigor, practical validation tools, and deployment-specific threat controls for MCP in high-stakes agentic systems. | Do not widen OS Abyss MCP writes without a new decision, validation route, and explicit proof-owner boundary. |
| Inspect AI | Represent future runnable evals as tasks with datasets, solvers or agents, tools, scorers, logs, and isolation boundaries. | Do not run write-capable eval support without an explicit check, dry-run, or sandbox route. |
| DeepEval agentic metrics | Separate task completion, tool correctness, argument correctness, and judge-based metrics so agent failures can be localized. | Do not use a single score to hide whether reasoning, tool choice, arguments, or state outcome failed. |
| Braintrust systematic evaluation | Keep the data/task/scorer loop, immutable experiments, CI regression checks, production trace scoring, and feedback into datasets. | Do not move OS Abyss proof truth into an external experiment dashboard. |

## Owner Boundaries

| Owner | Owns | Does Not Own |
| --- | --- | --- |
| `aoa-evals` | central proof doctrine, source eval bundles, report/verdict contracts, central adoption gates | live MCP execution, repo-local pressure, unreviewed session evidence, installed skill visibility |
| `repo-local evals/` | local intake, suites, reports, fixtures, and repo pressure evidence | central scoring, proof doctrine, regression baselines, or bundle adoption |
| `aoa-skills` | aoa-eval source skill, trigger wording, prompt/runtime discovery, and skill tests | central eval verdicts or runtime MCP service behavior |
| `abyss-stack` | runnable aoa-evals MCP service and runtime exports | central proof acceptance or local eval-port truth |
| `.aoa` | session evidence, archive freshness, and candidate-only mining references | reviewed truth, eval verdicts, or promotion decisions |

## Repo Readiness

| Repo | State | Severity | Confidence | Freshness | Next Command |
| --- | --- | --- | --- | --- | --- |
| `aoa-skills` | needs_local_design_or_owner_review | high | medium | warning | `python scripts/build_local_eval_port_inventory.py --workspace-root /srv/AbyssOS --json | jq '.repos[] | select(.repo_id == "aoa-skills")'` |
| `connectors/aoa-course-connector` | needs_local_design_or_owner_review | high | medium | warning | `python scripts/build_local_eval_port_inventory.py --workspace-root /srv/AbyssOS --json | jq '.repos[] | select(.repo_id == "connectors/aoa-course-connector")'` |
| `aoa-memo` | needs_local_design_or_owner_review | medium | medium | warning | `python scripts/build_local_eval_port_inventory.py --workspace-root /srv/AbyssOS --json | jq '.repos[] | select(.repo_id == "aoa-memo")'` |
| `aoa-routing` | needs_local_design_or_owner_review | medium | medium | warning | `python scripts/build_local_eval_port_inventory.py --workspace-root /srv/AbyssOS --json | jq '.repos[] | select(.repo_id == "aoa-routing")'` |
| `connectors/aoa-4pda-connector` | needs_local_design_or_owner_review | medium | medium | warning | `python scripts/build_local_eval_port_inventory.py --workspace-root /srv/AbyssOS --json | jq '.repos[] | select(.repo_id == "connectors/aoa-4pda-connector")'` |
| `connectors/aoa-discord-connector` | needs_local_design_or_owner_review | low | medium | warning | `python scripts/build_local_eval_port_inventory.py --workspace-root /srv/AbyssOS --json | jq '.repos[] | select(.repo_id == "connectors/aoa-discord-connector")'` |
| `connectors/aoa-stackoverflow-connector` | needs_local_design_or_owner_review | low | medium | warning | `python scripts/build_local_eval_port_inventory.py --workspace-root /srv/AbyssOS --json | jq '.repos[] | select(.repo_id == "connectors/aoa-stackoverflow-connector")'` |
| `connectors/aoa-telegram-connector` | needs_local_design_or_owner_review | low | medium | warning | `python scripts/build_local_eval_port_inventory.py --workspace-root /srv/AbyssOS --json | jq '.repos[] | select(.repo_id == "connectors/aoa-telegram-connector")'` |
| `connectors/aoa-xda-connector` | needs_local_design_or_owner_review | low | medium | warning | `python scripts/build_local_eval_port_inventory.py --workspace-root /srv/AbyssOS --json | jq '.repos[] | select(.repo_id == "connectors/aoa-xda-connector")'` |

## Candidate Queue

| Candidate | State | Source | Owner | Evidence | Packet | Next Route |
| --- | --- | --- | --- | ---: | --- | --- |
| `local-port:aoa-memo` | needs_owner_review | local_eval_port | aoa-memo | 2 |  | active_intake_select_then_apply_or_design |
| `local-port:aoa-routing` | needs_owner_review | local_eval_port | aoa-routing | 3 |  | active_intake_select_then_apply_or_design |
| `local-port:aoa-skills` | needs_owner_review | local_eval_port | aoa-skills | 6 |  | active_suite_note_review_or_execution_contract_design |
| `local-port:connectors/aoa-4pda-connector` | needs_owner_review | local_eval_port | connectors/aoa-4pda-connector | 2 |  | active_suite_note_review_or_execution_contract_design |
| `local-port:connectors/aoa-course-connector` | needs_owner_review | local_eval_port | connectors/aoa-course-connector | 11 |  | active_suite_note_review_or_execution_contract_design |
| `local-port:connectors/aoa-discord-connector` | needs_owner_review | local_eval_port | connectors/aoa-discord-connector | 1 |  | active_suite_note_review_or_execution_contract_design |
| `local-port:connectors/aoa-stackoverflow-connector` | needs_owner_review | local_eval_port | connectors/aoa-stackoverflow-connector | 1 |  | active_suite_note_review_or_execution_contract_design |
| `local-port:connectors/aoa-telegram-connector` | needs_owner_review | local_eval_port | connectors/aoa-telegram-connector | 1 |  | active_suite_note_review_or_execution_contract_design |
| `local-port:connectors/aoa-xda-connector` | needs_owner_review | local_eval_port | connectors/aoa-xda-connector | 1 |  | active_suite_note_review_or_execution_contract_design |
| `packet:session:aoa-eval-criteria-before-mining` | needs_owner_review | session_episode | aoa-evals | 3 | `mechanics/audit/parts/candidate-readers/packets/session-mining/aoa-eval-criteria-before-mining.eval_candidate.json` | Use this packet to seed a criteria/rubric review before any larger session-mining wave. |
| `packet:session:aoa-eval-goal-shrink-completion-overclaim` | needs_owner_review | session_episode | aoa-evals + aoa-skills | 3 | `mechanics/audit/parts/candidate-readers/packets/session-mining/aoa-eval-goal-shrink-completion-overclaim.eval_candidate.json` | Review the bounded source span against the current guide and decide whether this belongs in a trajectory eval slice or aoa-skills trigger case. |
| `packet:session:aoa-eval-keyword-mining-blindspot` | needs_owner_review | session_episode | aoa-evals + .aoa | 3 | `mechanics/audit/parts/candidate-readers/packets/session-mining/aoa-eval-keyword-mining-blindspot.eval_candidate.json` | Use the manual review gates to design non-keyword pointer signals before any wider session-mining automation. |
| `packet:session:aoa-eval-session-front-door-actionability-gap` | needs_owner_review | session_episode | aoa-evals | 4 | `mechanics/audit/parts/candidate-readers/packets/session-mining/aoa-eval-session-front-door-actionability-gap.eval_candidate.json` | Import real packets into the dashboard queue and expose top candidate routes from session-start output. |
| `packet:session:aoa-eval-working-process-fossilized-as-doctrine` | needs_owner_review | session_episode | aoa-evals + .aoa + aoa-skills | 3 | `mechanics/audit/parts/candidate-readers/packets/session-mining/aoa-eval-working-process-fossilized-as-doctrine.eval_candidate.json` | Decide whether this should become an aoa-skills trigger case, an aoa-evals route-trajectory eval, or a rejected one-off repair note. |
| `runtime-candidates:aoa-evals` | observed | runtime_candidate_export | abyss-stack + aoa-evals | 14 |  | needs_owner_review_before_any_proof_meaning |

## Eval Forge

- Router command: `python mechanics/proof-object/parts/eval-authoring/scripts/eval_forge_route.py --candidate-packet <path> --json`
- Local-port command: `python mechanics/proof-object/parts/eval-authoring/scripts/eval_forge_route.py --local-port-repo <repo_id> --local-port-inventory /tmp/aoa_local_eval_ports.current.json --workspace-root /srv/AbyssOS --json`
- Worksheet command: `python mechanics/proof-object/parts/eval-authoring/scripts/eval_forge_route.py --candidate-packet <path> --write-worksheet <worksheet-path> --json`
- Registry: `mechanics/proof-object/parts/eval-authoring/config/eval-archetypes.json`
- Worksheet schema: `mechanics/proof-object/parts/eval-authoring/schemas/eval-design-worksheet.schema.json`
- Archetype count: 18
- External pattern sources: 12
- Registry valid: True

### Forge Front Door

- operating_path_ref: `mechanics/proof-object/parts/eval-authoring/docs/EVAL_FORGE_OPERATING_PATH.md`
- session_mining_criteria_ref: `mechanics/proof-object/parts/eval-authoring/docs/SESSION_MINING_CRITERIA.md`
- local_port_decision_matrix_ref: `mechanics/proof-object/parts/eval-authoring/docs/LOCAL_PORT_DECISION_MATRIX.md`
- latest_route_review_report_ref: `mechanics/proof-object/parts/eval-authoring/reports/eval-forge/2026-06-26-session-candidate-owner-review.md`
- worksheet_example_ref: `mechanics/proof-object/parts/eval-authoring/examples/aoa_eval_criteria_before_mining.eval_design_worksheet.example.json`
- candidate_packet_schema_ref: `mechanics/audit/parts/candidate-readers/schemas/aoa-eval-candidate-packet.schema.json`
- local_suite_execution_schema_ref: `mechanics/proof-object/parts/eval-authoring/schemas/local-eval-suite-execution.schema.json`
- proof authority: False; promotion allowed: False; refs valid: True
- exact commands:
  - raise the per-session Eval Forge front door: `python scripts/aoa_eval_session_start.py --json`
  - check front-door readiness gates and blockers: `python scripts/check_eval_forge_readiness.py --json`
  - inspect active/skeleton/missing/invalid local eval ports: `python scripts/build_local_eval_port_inventory.py --workspace-root /srv/AbyssOS --json`
  - validate imported candidate packets before review: `python scripts/validate_eval_candidate_packets.py mechanics/audit/parts/candidate-readers/packets`
  - route a session candidate packet through Eval Forge: `python mechanics/proof-object/parts/eval-authoring/scripts/eval_forge_route.py --candidate-packet <path> --json`
  - route one active local eval port through Eval Forge: `python mechanics/proof-object/parts/eval-authoring/scripts/eval_forge_route.py --local-port-repo <repo_id> --local-port-inventory /tmp/aoa_local_eval_ports.current.json --workspace-root /srv/AbyssOS --json`
  - write a non-proof owner-review worksheet only after admission gates: `python mechanics/proof-object/parts/eval-authoring/scripts/eval_forge_route.py --candidate-packet <path> --write-worksheet <worksheet-path> --json`

| Candidate | Decision | Archetype | Owner Route | Promotion |
| --- | --- | --- | --- | --- |
| `packet:session:aoa-eval-criteria-before-mining` | keep | `human-review-rubric` | `domain owner` / `human_review_before_automation` | False |
| `packet:session:aoa-eval-goal-shrink-completion-overclaim` | keep | `trace-trajectory-eval` | `aoa-evals + .aoa candidate evidence` / `trajectory_eval_or_session_candidate` | False |
| `packet:session:aoa-eval-keyword-mining-blindspot` | keep | `aoa-skills-trigger-eval` | `aoa-skills` / `trigger_design_case` | False |
| `packet:session:aoa-eval-session-front-door-actionability-gap` | keep | `abyss-stack-runtime-mcp-smoke` | `abyss-stack` / `runtime_owner_smoke_then_candidate_review` | False |
| `packet:session:aoa-eval-working-process-fossilized-as-doctrine` | keep | `human-review-rubric` | `domain owner` / `human_review_before_automation` | False |

## Trigger Criteria

| Trigger Class | Route | Freshness Gate |
| --- | --- | --- |
| `existing_eval_applicable_before_new_design` | aoa-eval:select_then_apply | central catalog check current enough for route selection |
| `repo_local_eval_pressure_without_central_match` | aoa-eval:local_need_or_design | local port inventory regenerated or inspected in current task |
| `validator_test_script_support_needed` | aoa-eval:apply_existing_validator_or_design_gap | support registry source inventories parse and name owner surfaces |
| `agent_route_miss_or_tool_trajectory_pressure` | aoa-eval:trajectory_slice_or_session_candidate | session refs and repo refs must be current enough to replay route conditions |
| `runtime_candidate_export_needs_review` | aoa-eval:candidate_queue_needs_owner_review | runtime status timestamp and candidate-reader generation state visible |
| `freshness_or_mirror_drift_blocks_eval_route` | aoa-eval:freshness_sentinel_then_route | commit ids, branch names, generated timestamps, and selected roots recorded |
| `session_episode_candidate_for_eval_design` | aoa-eval:session_candidate_only | .aoa maintenance-status or archive freshness readout current |
| `promotion_or_central_adoption_pressure` | aoa-evals owner review, not MCP auto-promotion | central catalog, report index, and owner evidence current |

### Session Mining Gate

- Status: `manual_review_packetized`
- Reason: A bounded 20-episode .aoa manual review was performed; kept items are imported only as schema-valid candidate packets.
- Reviewed episodes: 20
- Packetized candidates: 5
- Report refs: `["mechanics/audit/parts/candidate-readers/reports/session-mining/2026-06-25-aoa-eval-control.manual-review.md"]`
- Boundary: .aoa can supply candidate evidence only; session-mining cannot create reviewed eval truth.

## Support Registry

- Support registry JSON: `generated/eval_support_registry.json`
- Eval-relevant surfaces: 429
- Recommended routes: `{"apply_as_deterministic_eval_support": 466, "candidate_only_eval_support": 11, "component_only_use_owning_validator_or_lane_command": 83, "forbidden_as_eval_apply_until_manual_owner_review": 4, "generated_readmodel_support": 6, "ordinary_owner_route": 8, "run_check_mode_before_eval_support": 17}`
- Semantic classes: `{"deterministic_validator": 463, "generated_parity_check": 32, "ordinary_support": 8, "runtime_candidate_support": 11, "trace_trajectory_eval_support": 14, "unit_contract_property_test": 63, "unsafe_side_effect_script": 4}`
- Review status: `{"candidate_only": 11, "not_eval_relevant": 8, "reviewed_forbidden": 4, "rule_reviewed": 572}`

## Runtime Adoption

- Source skill exists: True
- Installed skill exists: True
- Installed matches source: True
- Installed profile verified: True
- Runtime discovery mentions `aoa-eval`: True
- Trigger harness command: `python -m pytest -q tests/test_aoa_eval_prompt_trigger_harness.py`

## Freshness Sentinel

- Git repos: 21
- Dirty repos: 15
- MCP selected root: `/home/dionysus/src/abyss-stack`
- .aoa freshness status: `failed`

## Phase Coverage

| Phase | Status | Surface |
| ---: | --- | --- |
| 1 | implemented | eval_readiness_dashboard |
| 2 | implemented | eval_support_registry |
| 3 | implemented_read_only_audit | aoa_eval_runtime_adoption |
| 4 | implemented_criteria_and_packet_contract | trigger_criteria + validate_eval_candidate_packets |
| 5 | implemented_runnable_harness | trajectory_eval_slice + run_aoa_eval_route_trajectory_harness.py |
| 6 | implemented_read_only_queue_and_packet_validator | candidate_queue + candidate_packet_contract |
| 7 | implemented_owner_gate_contract | local_to_central_promotion_path |
| 8 | implemented_runnable_sentinel | freshness_sentinel + check_eval_freshness_sentinel.py |
| 9 | implemented_design_forge_router | eval_forge_readiness + eval_forge_route.py |
| 10 | implemented_session_readiness_gate | check_eval_forge_readiness.py + docs/guides/EVAL_FORGE_READINESS_LAYER.md |
