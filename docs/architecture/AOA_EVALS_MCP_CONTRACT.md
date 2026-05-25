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

## Operating Card

| Field | Route |
| --- | --- |
| role | read-only MCP contract for proof selection, inspection, expansion, eval-need proposal routing, candidate evidence routing, candidate packet validation, stack runtime candidate export reading, mirror freshness status, and report skeleton preparation |
| input | proof question, eval name, section key, comparison mode, eval-need proposal fields, candidate evidence refs, candidate evidence packet, runtime candidate export id, runtime template request, or freshness/status request |
| output | compact source refs, generated reader context, existing-route matches, candidate-only eval-need proposal context, candidate-only evidence shape, candidate validation result, stack runtime candidate export metadata/detail, mirror freshness status, or report skeleton |
| owner | `aoa-evals` owns this contract and proof authority; `abyss-stack` owns the runnable MCP service implementation |
| next route | source bundle, generated reader builder, runtime-candidate reader, bundle-local review guide, or stack MCP package |
| validation | root `AGENTS.md#verify`, `docs/AGENTS.md#validation`, generated-reader checks, runtime-candidate reader checks, and stack service tests |

## Source Hierarchy

| Layer | Role |
| --- | --- |
| source eval bundle | owns claim, object under evaluation, verdict logic, report contract, blind spots, and interpretation limits |
| generated readers | provide deterministic catalog, capsule, section, comparison, and report lookup |
| runtime-candidate readers | provide candidate evidence and artifact-to-verdict hook shapes that still require bundle-local review |
| `aoa_evals` MCP | exposes compact read-only access to the above surfaces |
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
- Do not compute verdicts.
- Do not publish receipts.
- Do not promote bundles.
- Do not mutate `aoa-evals` source from MCP.
- Do not treat runtime evidence, generated readers, or MCP output as stronger
  than bundle-local `EVAL.md` and `eval.yaml`.
- Do not move proof authority into `abyss-stack`.

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

```bash
scripts/aoa-sync-federation-surfaces --layer aoa-evals
```

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

The service must stay stdio-only until a later decision widens exposure.

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
