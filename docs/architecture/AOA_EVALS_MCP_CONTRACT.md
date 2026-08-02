# AoA Evals MCP Contract

## Role

This contract defines the first `aoa_evals` MCP access plane for OS Abyss.

`aoa_evals` helps an agent choose and inspect bounded proof surfaces without
loading the whole repository into prompt context. It is an access plane over
`aoa-evals`; it is not proof authority.

The proof authority remains:

- bundle-local `evals/**/EVAL.md` and `eval.yaml` for bounded claim meaning;
- generated readers under `generated/` for compact navigation only;
- runtime-candidate readers under
  `mechanics/audit/parts/candidate-readers/generated/` for candidate shapes;
- bundle-local review and report contracts for final interpretation.

The access plane also exposes evidence needed by the organ-access proof route,
but it does not admit an organ. A registry entry, runnable process, observed
schema, successful call, candidate packet, or green command remains weaker
than the bounded source eval and reviewed acceptance route.

## Organ Access Proof Boundary

The current central source proof is capability- and policy-plane-specific. It
validates the packet unit, named owners, exact revision-slot bindings,
independent maturity evidence, observation and expiry windows, honest
insufficient-evidence posture, and the prohibition on acceptance, admission,
or higher-effect inference. It does not collapse those fields into general
health.

This source route does not test a live primitive or arguments, process or
credential denial, context footprint, latency, cancellation, injection
resistance, receipt continuity, cross-organ handoff, or rollback. Any claim on
those surfaces requires a separate named live proof bundle and validation
route; none is supplied by this source contract.

The proof packet carries a maturity vector with independent evidence for:

```text
declared
owner_reviewed
packaged
exported
deployed
process_alive
endpoint_ready
registry_indexed
consumer_registered
schema_observed
call_succeeded
result_grounded
freshness_satisfied
owner_accepted
cross_organ_proven
rollback_proven
```

Each asserted axis requires an observation timestamp, owner-qualified evidence
reference, revision, and expiry or freshness policy. No axis is inferred from
another. In particular, `endpoint_ready` does not imply `result_grounded`, and
a central eval result does not imply `owner_accepted`.

Admission remains a control-plane and acceptance-owner action after proof.
`aoa-evals` emits a bounded proof result and its limits; it does not mutate the
private registry, start a service, accept memory, apply source changes, or
authorize effects.

Read, candidate, internal-effect, and external-effect planes are evaluated
separately. A read-plane pass is not evidence for an effect plane. Tests must
not claim effect isolation until a named live suite shows that a read
credential is denied at higher-effect processes. Candidate output cannot
become durable truth without the named acceptance owner.

## Current Source-Backed Organ-Access Route

The bounded source contract and negative-inference suite live in
[`aoa-organ-access-admission-integrity`](../../evals/boundary/aoa-organ-access-admission-integrity/EVAL.md).
Its packet schema is
[`organ-access-proof-packet.schema.json`](../../evals/boundary/aoa-organ-access-admission-integrity/schemas/organ-access-proof-packet.schema.json).

The exact checked-in scenario, packet-validation, and bundle-validation argv
are recorded in the bundle's
[`runners/contract.json`](../../evals/boundary/aoa-organ-access-admission-integrity/runners/contract.json)
and governed by `evals/AGENTS.md#validation`.

This route makes the public packet shape and its forbidden inferences
executable. It does **not** collect or authenticate live owner, runtime,
registry, consumer, denial, freshness, cross-organ, or rollback observations.
A green source suite cannot admit an organ, accept owner meaning, prove a live
protocol pair, or change a registry. Live pair-specific proof remains a
separate evidence and acceptance route.

## Owner-Authored Organ Capabilities

The exact agent-facing capability source is
[`aoa_evals_mcp_capabilities.v1.json`](aoa_evals_mcp_capabilities.v1.json),
validated by
[`aoa_evals_mcp_capabilities.schema.json`](aoa_evals_mcp_capabilities.schema.json).
It defines three non-overlapping capability profiles:

| Capability | Policy and credential | Authority ceiling |
| --- | --- | --- |
| `eval-discovery-read` | read / `evals-read` | select and inspect bounded eval source routes only |
| `eval-request-prepare` | candidate / `evals-candidate` | prepare one non-persistent typed `eval_need_v1` request candidate |
| `proof-result-read` | read / `evals-read` | read one already issued bundle-local report without issuing, accepting, or strengthening its verdict |

The source manifest is a capability declaration, not an admission record.
`abyss-stack` binds the runnable catalogs to it; `aoa-sdk` may use it as one
input to discovery and admission; neither may change proof meaning. Managed
consumers should request one exact profile rather than loading the historical
complete catalog. The portable complete catalog remains a compatibility
surface until the profiled contours are landed, deployed, and admitted.

`proof-result-read` is deliberately separate from proof issuance. The MCP
adapter resolves an indexed source report and returns its exact source refs,
content identity, owner revision, and bundle-local payload. It does not run an
eval, compute a verdict, publish a report or receipt, or infer acceptance from
the report's presence. The source report and bundle remain stronger than the
MCP projection.

## Operating Card

| Field | Route |
| --- | --- |
| role | MCP contract for proof selection, inspection, expansion, eval-need proposal routing, local eval-port federation, gated local-port file writes, candidate evidence routing, candidate packet validation, stack runtime candidate export reading, mirror freshness status, and report skeleton preparation |
| input | proof question, eval name, section key, comparison mode, eval-need proposal fields, candidate evidence refs, candidate evidence packet, runtime candidate export id, runtime template request, or freshness/status request |
| output | compact source refs, generated reader context, existing-route matches, candidate-only eval-need proposal context, candidate-only evidence shape, candidate validation result, stack runtime candidate export metadata/detail, mirror freshness status, local suite execution state, or report skeleton |
| owner | `aoa-evals` owns this contract and proof authority; `abyss-stack` owns the runnable MCP service implementation |
| next route | source bundle, generated reader builder, runtime-candidate reader, bundle-local review guide, or stack MCP package |
| validation | root `AGENTS.md#verify`, `docs/AGENTS.md#validation`, generated-reader checks, runtime-candidate reader checks, and stack service tests |

## Source Hierarchy

| Layer | Role |
| --- | --- |
| source eval bundle | owns claim, object under evaluation, verdict logic, report contract, blind spots, and interpretation limits |
| generated readers | provide deterministic catalog, capsule, section, comparison, and report lookup |
| runtime-candidate readers | provide candidate evidence and artifact-to-verdict hook shapes that still require bundle-local review |
| `aoa_evals` MCP | exposes compact proof/candidate read access and narrow gated sibling-local eval-port writes |
| `abyss-stack` service | runs the stdio MCP server and resolves source or approved mirror paths |
| `abyss-stack` runtime export lane | owns private `Logs/eval-exports/` candidate records |

MCP output is always weaker than the source bundle and its manifest.

## MCP Resources

| Resource | Purpose | Stronger owner |
| --- | --- | --- |
| `aoa-evals://catalog` | compact eval catalog with source refs and selection fields | generated catalog and source bundles |
| `aoa-evals://bundle/{name}` | bundle summary, capsule, source refs, and authority boundary | bundle-local `EVAL.md` and `eval.yaml` |
| `aoa-evals://bundle/{name}/sections` | generated section reader for one bundle | bundle-local `EVAL.md` |
| `aoa-evals://comparison-spine` | comparison-mode reader | generated comparison spine and source bundles |
| `aoa-evals://runtime-candidate-templates` | runtime evidence and artifact hook templates | candidate-reader generated indexes and owner review guides |
| `aoa-evals://runtime-status` | source and approved-mirror freshness, required reader presence, and catalog/template counts | source checkout, generated builders, and stack federation sync wrapper |
| `aoa-evals://runtime-evidence/schema` | public-safe candidate packet schema refs and validation boundary | selected-evidence and artifact-hook schemas |
| `aoa-evals://runtime-candidate-exports` | stack-owned private candidate export metadata and validation summaries | governed execution candidate-export lane |
| `aoa-evals://runtime-candidate-export/{record_id}` | one stack-owned private candidate export without nested payload by default | governed execution candidate-export lane and bundle-local review |
| `aoa-evals://reports` | generated report index | source reports and bundle-local report contracts |
| `aoa-evals://proof-result/{report_id}` | one already issued indexed source report with content identity and owner revision | source report, source bundle, manifest, and report contract |
| `aoa-evals://local-ports` | workspace local eval-port registry with validation summaries and advisory route recommendations | sibling `evals/PORT.yaml` files, `aoa-evals` local-port validator, and local-port inventory read-model |
| `aoa-evals://local-port/{repo}` | one repo-local eval port summary, pressure counts, validator issues, and advisory route key | sibling repo-local `evals/` port |
| `aoa-evals://local-port/{repo}/intake` | local `eval_need_v1` intake packets | sibling repo-local `evals/intake/` |
| `aoa-evals://local-port/{repo}/suites` | local suite notes plus inspect-only `absent`/`invalid`/`stale`/`ready` execution-sidecar metadata | sibling repo-local `evals/suites/` and central sidecar validator |
| `aoa-evals://local-port/{repo}/reports` | local report notes | sibling repo-local `evals/reports/` |

## MCP Tools

| Tool | Use | Must not do |
| --- | --- | --- |
| `aoa_evals_select(proof_question, filters)` | return matching bounded eval candidates from catalog/read models | decide a verdict or claim applicability as final truth |
| `aoa_evals_find_or_propose(proof_question, proposal)` | return likely existing eval routes and a candidate `eval_need_v1` proposal context for repo-local authoring | create a source bundle, approve a proposal, or bypass the route-first scaffold helper |
| `aoa_evals_inspect(name)` | return compact bundle summary, source refs, capsule, and limits | replace reading the source bundle when interpreting |
| `aoa_evals_expand(name, section_key)` | return generated section content for focused review | treat generated prose as stronger than `EVAL.md` |
| `aoa_evals_comparison(baseline_mode)` | return comparison-spine records filtered by baseline mode | invent comparison results |
| `aoa_evals_runtime_evidence_template(name)` | return candidate evidence or artifact hook templates linked to an eval | promote runtime evidence into accepted proof |
| `aoa_evals_runtime_status()` | report selected root kind, source/mirror freshness, required reader presence, and next refresh route | refresh mirrors, mutate source, or claim freshness when provenance is missing |
| `aoa_evals_validate_evidence_candidate(packet)` | validate a runtime evidence selection or artifact hook candidate against public-safe schema and known template/eval refs | ingest, persist, accept, score, or turn the packet into a verdict |
| `aoa_evals_runtime_candidate_exports(limit)` | list stack-owned private runtime candidate exports with validation summaries | include nested private payloads, accept evidence, or publish results |
| `aoa_evals_read_runtime_candidate_export(record_id, include_payload)` | read one stack-owned private candidate export for review routing | treat readability or schema validity as proof acceptance |
| `aoa_evals_report_skeleton(name, evidence_refs)` | prepare a candidate-only report skeleton and required source refs | publish a receipt, compute a verdict, or mutate repo files |
| `aoa_evals_prepare_request_candidate(proof_question, proposal)` | prepare a non-persistent typed `eval_need_v1` request candidate on the candidate contour | persist intake, approve a request, create a bundle, run an eval, or issue proof |
| `aoa_evals_read_proof_result(report_id)` | read one already issued indexed source report with exact source and revision refs | compute, strengthen, accept, publish, or replace the source verdict |
| `aoa_evals_local_ports(status, include_skeleton)` | list repo-local eval ports, validation summaries, pressure counts, and advisory route recommendations | treat local pressure as accepted proof |
| `aoa_evals_local_port(repo)` | inspect one repo-local eval port, counts, validator issues, owner boundary, and advisory route key | override the sibling repo's local route card |
| `aoa_evals_find_or_propose_local(repo, proof_question, proposal)` | shape a local `eval_need_v1` packet and target route for a sibling port | write source, approve proposal, or skip existing-route review |
| `aoa_evals_write_local_intake(repo, packet, file_slug, apply, replace_existing)` | dry-run or write one local intake packet under `repo/evals/intake/` | write central bundles, overwrite silently, accept proof, or bypass validation |
| `aoa_evals_write_local_suite_note(repo, suite_slug, title, summary, body_markdown, refs, apply, replace_existing)` | dry-run or write one local suite note under `repo/evals/suites/` | define scoring truth, final verdicts, or regression authority |
| `aoa_evals_write_local_report_note(repo, report_slug, title, summary, body_markdown, refs, apply, replace_existing)` | dry-run or write one local report note under `repo/evals/reports/` | publish receipts, compute verdicts, or claim central report authority |

## MCP Prompts

| Prompt | Route |
| --- | --- |
| `eval-select` | use selection and catalog resources to choose a bounded eval candidate, then inspect the source bundle |
| `eval-find-or-propose` | search existing routes first, then shape a candidate `eval_need_v1` packet for repo-local authoring only when needed |
| `eval-review` | inspect bundle sections and review limits before interpreting evidence |
| `evidence-packet` | shape and validate candidate runtime evidence, then route it to bundle-local review |
| `report-skeleton` | prepare a report skeleton that keeps verdict and receipt publication out of MCP |

## Stop Lines

- Do not run general evals.
- Do not invoke local suite `runner.argv`; only the selected repo owner or
  `aoa-eval-apply` may invoke an exact validated argv after state is `ready`
  and a just-in-time revalidation succeeds; that route captures environment
  metadata and an execution receipt.
- Do not compute verdicts.
- Do not issue proof through MCP; reading an existing report is not proof issuance.
- Do not publish receipts.
- Do not promote bundles.
- Do not mutate `aoa-evals` source from MCP.
- Do not create central `aoa-evals/evals/**` source bundles from MCP.
- Do not write outside a sibling repo-local `evals/` port.
- Do not treat runtime evidence, generated readers, or MCP output as stronger
  than bundle-local `EVAL.md` and `eval.yaml`.
- Do not move proof authority into `abyss-stack`.
- Do not mutate the private organ registry or treat a central proof result as
  admission or owner acceptance.
- Do not infer a higher maturity axis, policy plane, or effect authority from a
  lower one.

## Runtime Evidence Posture

Runtime, trace, machine, and stack artifacts enter as candidates:

```text
runtime or machine artifact -> candidate evidence shape -> bundle-local review -> bounded report -> optional receipt
```

`aoa_evals_runtime_evidence_template` may help choose the candidate shape.
`aoa_evals_validate_evidence_candidate` may check that a proposed packet is
schema-shaped and linked to known candidate templates, source refs, or evals.
`aoa_evals_report_skeleton` may prepare a reviewable outline. Neither accepts
the evidence, decides the verdict, or publishes the result.

Candidate validation is still pre-ingestion. A valid packet means only:

- the packet shape matches a public-safe candidate schema;
- referenced eval/template names are known enough for review routing;
- required review posture fields are present;
- provenance refs are visible enough for the next owner to inspect.

It does not mean evidence has been reviewed, accepted, scored, compared, or
published.

Stack-owned runtime exports live below `abyss-stack/Logs/eval-exports/`.
`aoa_evals_runtime_candidate_exports` may list compact metadata and validation
summaries. `aoa_evals_read_runtime_candidate_export` may read one export and,
when explicitly requested, include its nested private candidate payload. Both
surfaces remain read-only. They do not create a review queue inside
`aoa-evals`, mark evidence accepted, or produce a report/verdict.

## Eval Need Proposal Posture

Eval growth starts as a route question, not as a source write:

```text
proof question -> existing eval search -> candidate evidence or quest route -> eval_need_v1 proposal -> repo-local scaffold helper
```

`aoa_evals_find_or_propose` may return:

- likely existing eval matches from generated readers;
- route notes that tell the agent which owner should be inspected next;
- a candidate `eval_need_v1` proposal context shaped for
  `mechanics/proof-object/parts/eval-authoring/schemas/eval-need.schema.json`;
- stack runtime candidate export refs when the proposal is really evidence
  routing rather than new source authoring.

The result is advisory. It is not proof, proposal approval, duplicate-fit
truth, source mutation permission, or bundle creation. New source bundles still
go through the repo-local scaffold helper and its `--allow-new`/`--write`
gates after review.

## Local Eval-Port Federation And Writes

Sibling repositories may expose `evals/` local ports using
`local_eval_port_v1`. These ports preserve repo-local pressure, fixtures,
suites, reports, and intake packets below central proof authority.

`aoa_evals` may federate those ports across the workspace. It may list ports,
inspect one port, read local intake/suite/report files, and validate local
port shape against `scripts/validate_local_eval_port.py` semantics.

Where the workspace inventory read-model is available, the local-port registry
should be backed by `scripts/build_local_eval_port_inventory.py` or equivalent
semantics. Registry entries may expose status, pressure counts, central-name
overlap, validation issues, and a route key such as
`active_intake_select_then_apply_or_design` or `invalid_active_repair`.

The current producer/consumer shape for that inventory is locked in
`docs/architecture/local_eval_port_inventory.contract.v2.json`. The v1 file
remains a compatibility input. During rollout the stack MCP consumer must
dual-read both contract/inventory schema versions. V1 entries map suite
execution to `absent` and must never infer runnable from `suite_notes`, an
injected `suite_execution.ready`, or an old runnable route key. Consumers
normalize v1/unknown input before routing; v2 exposes the explicit suite
execution state and aggregate priority.

The route key is advisory. It helps the agent pick `aoa-eval-select`,
`aoa-eval-apply`, `aoa-eval-design`, local repair, or no mutation. It is not
proposal approval, evidence acceptance, proof scoring, regression truth, or a
central adoption decision.

Write-side MCP is intentionally narrow:

- default behavior is dry-run (`apply=false`);
- `apply=true` may write only `evals/intake/*.eval_need.json`,
  `evals/suites/*.suite.md`, and `evals/reports/*.report.md` in the selected
  sibling repo;
- when a skeleton port receives its first valid local pressure file, MCP may
  move `evals/PORT.yaml` from `status: skeleton` to `status: active` in the
  same operation;
- overwrite requires an explicit `replace_existing=true` flag in the stack
  implementation and contract.

These writes are authoring convenience, not proof acceptance. They do not
approve proposals, accept evidence, compute results, publish receipts, define
scoring, declare regression state, or promote local bundles into `aoa-evals`.
Central source bundle creation remains a separate `aoa-evals` source-authoring
route.

The AOA-EV-D-0241 write allowlist does not include
`evals/suites/*.suite.json`. MCP may read validated sidecar metadata but must
not create or replace a sidecar, refresh tracked-source hashes, or execute its
runner. Widening that surface requires a separate decision.

## Local Suite Execution Read Boundary

`local_eval_suite_execution_v1` is a source contract owned by `aoa-evals` and
stored in the sibling repo beside its `.suite.md` note. MCP may expose:

- aggregate state `absent`, `invalid`, `stale`, or `ready`, with priority
  `invalid > stale > ready > absent`;
- sidecar ref, suite id, entrypoint ref, exact argv/cwd, timeout, accepted exit
  codes, canonical owner identity, source-contract readiness scope, required
  JIT/environment/receipt posture, and stale/validation diagnostics;
- fixed `execution_allowed: false`, `proof_authority: false`, and
  `promotion_allowed: false` on the MCP projection.

Readability, schema validity, or `ready` state is not an instruction to run.
`ready` means only `source-contract-ready`; it does not prove a pinned
interpreter, dependency environment, or reproducible runtime. It only makes
the owner/apply route discoverable. That stronger route must JIT-revalidate the
sidecar and tracked hashes immediately before execution and capture environment
metadata plus an execution receipt. MCP does none of those writes or execution
steps.

`entrypoint_ref` is repo-relative source identity; the final argv token is its
path relative to `runner.cwd` and must resolve to that exact file. MCP exposes
the validated pair but does not recompute it into an execution request.

## Refresh and Mirror Discipline

`aoa_evals` may read either the source checkout or an approved runtime mirror.
The mirror is a read cache, not proof authority.

The runtime status surface reports:

- selected root and root kind;
- source and approved mirror paths when discoverable;
- required generated reader and candidate-reader presence;
- catalog and candidate-template counts;
- stack-owned runtime candidate export count;
- source git commit when the selected root is a checkout;
- mirror manifest or freshness gaps when the mirror lacks provenance.

The refresh route remains stack-owned:

Use the stack-owned federation sync wrapper for the `aoa-evals` layer; its CLI
and execution contract remain with `abyss-stack`.

If mirror provenance is missing or stale, agents must refresh through the stack
federation sync wrapper or read the source checkout directly. They must not
edit the mirror as source truth.

## Implementation Boundary

The runnable server belongs in `abyss-stack` under
`mcp/services/aoa-evals-mcp/` because MCP services are runtime access planes.

The service may read:

- source checkout `aoa-evals`;
- generated readers from that checkout;
- an approved runtime mirror when explicitly configured.

Portable execution remains stdio-first. Managed Streamable HTTP may be used
only on loopback with separate read/candidate credentials and exact
capability-profile catalogs. Transport reachability and bearer authentication
remain runtime observations, not proof, admission, or effect authorization.

## Validation

For this contract surface, use the docs route:

- `docs/AGENTS.md#validation`
- root `AGENTS.md#verify`

For generated reader parity, use the generated/catalog checks named in root
`AGENTS.md#verify`.

For runtime-candidate reader parity, use the candidate-reader checks named in
root `AGENTS.md#verify`.

For the runnable service, use the `abyss-stack` package-local validation in
`mcp/services/aoa-evals-mcp/AGENTS.md`.
