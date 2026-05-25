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
| role | read-only MCP contract for proof selection, inspection, expansion, candidate evidence routing, and report skeleton preparation |
| input | proof question, eval name, section key, comparison mode, candidate evidence refs, or runtime template request |
| output | compact source refs, generated reader context, candidate-only evidence shape, or report skeleton |
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

MCP output is always weaker than the source bundle and its manifest.

## MCP Resources

| Resource | Purpose | Stronger owner |
| --- | --- | --- |
| `aoa-evals://catalog` | compact eval catalog with source refs and selection fields | generated catalog and source bundles |
| `aoa-evals://bundle/{name}` | bundle summary, capsule, source refs, and authority boundary | bundle-local `EVAL.md` and `eval.yaml` |
| `aoa-evals://bundle/{name}/sections` | generated section reader for one bundle | bundle-local `EVAL.md` |
| `aoa-evals://comparison-spine` | comparison-mode reader | generated comparison spine and source bundles |
| `aoa-evals://runtime-candidate-templates` | runtime evidence and artifact hook templates | candidate-reader generated indexes and owner review guides |
| `aoa-evals://reports` | generated report index | source reports and bundle-local report contracts |

## MCP Tools

| Tool | Use | Must not do |
| --- | --- | --- |
| `aoa_evals_select(proof_question, filters)` | return matching bounded eval candidates from catalog/read models | decide a verdict or claim applicability as final truth |
| `aoa_evals_inspect(name)` | return compact bundle summary, source refs, capsule, and limits | replace reading the source bundle when interpreting |
| `aoa_evals_expand(name, section_key)` | return generated section content for focused review | treat generated prose as stronger than `EVAL.md` |
| `aoa_evals_comparison(baseline_mode)` | return comparison-spine records filtered by baseline mode | invent comparison results |
| `aoa_evals_runtime_evidence_template(name)` | return candidate evidence or artifact hook templates linked to an eval | promote runtime evidence into accepted proof |
| `aoa_evals_report_skeleton(name, evidence_refs)` | prepare a candidate-only report skeleton and required source refs | publish a receipt, compute a verdict, or mutate repo files |

## MCP Prompts

| Prompt | Route |
| --- | --- |
| `eval-select` | use selection and catalog resources to choose a bounded eval candidate, then inspect the source bundle |
| `eval-review` | inspect bundle sections and review limits before interpreting evidence |
| `evidence-packet` | shape candidate runtime evidence and route it to bundle-local review |
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
`aoa_evals_report_skeleton` may prepare a reviewable outline. Neither accepts
the evidence, decides the verdict, or publishes the result.

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
