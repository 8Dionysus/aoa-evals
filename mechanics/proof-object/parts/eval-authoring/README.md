# Proof Object / Eval Authoring Part

## Role

This part owns the starter authoring scaffold for source eval packages.

Proof bundle, doctrine essay, generated reader, and example report meaning
route to their owning source surfaces.

## Owned Operation

`origin proof pressure -> existing-route check -> forge archetype route -> design worksheet -> starter scaffold -> bounded source proof object`

## Source Surfaces

- `mechanics/proof-object/parts/eval-authoring/docs/EVAL_BIRTH_PROTOCOL.md`
- `mechanics/proof-object/parts/eval-authoring/docs/EVAL_FORGE_OPERATING_PATH.md`
- `mechanics/proof-object/parts/eval-authoring/docs/SESSION_MINING_CRITERIA.md`
- `mechanics/proof-object/parts/eval-authoring/docs/LOCAL_PORT_DECISION_MATRIX.md`
- `mechanics/proof-object/parts/eval-authoring/schemas/eval-need.schema.json`
- `mechanics/proof-object/parts/eval-authoring/schemas/eval-archetype-registry.schema.json`
- `mechanics/proof-object/parts/eval-authoring/schemas/eval-design-worksheet.schema.json`
- `mechanics/proof-object/parts/eval-authoring/schemas/local-eval-suite-execution.schema.json`
- `mechanics/proof-object/parts/eval-authoring/config/eval-archetypes.json`
- `mechanics/proof-object/parts/eval-authoring/config/external-pattern-grounding.json`
- `mechanics/proof-object/parts/eval-authoring/examples/eval_need.example.json`
- `mechanics/proof-object/parts/eval-authoring/examples/eval_design_worksheet.example.json`
- `mechanics/proof-object/parts/eval-authoring/examples/aoa_eval_criteria_before_mining.eval_design_worksheet.example.json`
- `mechanics/proof-object/parts/eval-authoring/scripts/eval_forge_route.py`
- `mechanics/proof-object/parts/eval-authoring/scripts/prepare_eval_case.py`
- `mechanics/proof-object/parts/eval-authoring/scripts/scaffold_eval_bundle.py`
- `mechanics/proof-object/parts/eval-authoring/templates/EVAL.template.md`
- `evals/**/EVAL.md`
- `evals/**/eval.yaml`
- `mechanics/proof-object/parts/eval-contracts/`

## Inputs

- a bounded proof question;
- an existing eval route check against current generated catalog surfaces;
- object under evaluation;
- claim type and baseline posture;
- expected evidence, fixtures, runners, reports, and blind spots.

## Outputs

- a route-first eval need packet;
- an Eval Forge route with candidate admission gates, archetype ranking, owner
  route, scaffold posture, and worksheet payload;
- an Eval Forge operating path, manual-mining criteria, reject taxonomy, and
  local-port decision matrix for future agent sessions;
- part-local route-review reports under
  `mechanics/proof-object/parts/eval-authoring/reports/eval-forge/`;
- a case-preparation kit with schema validation, existing-match review, and
  scaffold commands plus the forge route;
- an existing eval route, candidate-evidence route, quest route, or explicit
  new-draft posture;
- a new or reshaped `EVAL.md` scaffold;
- frontmatter aligned with the eval source contract;
- explicit comparison and report contract placeholders when applicable.
- an inspect-only local suite execution route whose state is
  `absent`/`invalid`/`stale`/`ready`; `.suite.md` alone is never runnable.
  `ready` means source-contract-ready only and requires canonical Git/PORT
  owner identity plus typed `python_pytest` argv.

## Stronger Owner Split

`evals/**/EVAL.md` and `evals/**/eval.yaml` own the actual source proof
claim, object under evaluation, status, evidence posture, verdict logic,
blind spots, and manifest metadata.

`docs/architecture/ARCHITECTURE.md`, `docs/guides/EVAL_PHILOSOPHY.md`, review guides, comparison
guides, score guides, and verdict guides own repo-level proof vocabulary.
The template borrows that vocabulary for a starter shape. When it reads as
doctrine or accepted proof meaning, route back to the source package and proof
guides.

`mechanics/proof-object/parts/eval-contracts/` owns schema-backed contract
checks. Generated catalogs, capsules, sections, reports, receipts, runtime
candidates, and sibling refs stay weaker than source eval packages.

`aoa-evals` owns only the bounded authoring scaffold in this part: a
route-first form that helps a future eval package expose source truth without
hiding limits or bypassing existing proof surfaces.

Eval Forge is the design router before source authoring. It can choose an
archetype, explain missing evidence, and write an `eval_design_worksheet_v1`
only when requested. It cannot create central bundles, accept proof, score
evidence, mint baselines, promote candidate packets, or mutate repo-local
`evals/` ports. It also cannot execute local suite `runner.argv`; only the
selected repo owner or `aoa-eval-apply` may invoke an exact validated argv when
the sidecar state is `ready`, JIT revalidation succeeds, and environment plus
execution-receipt capture is arranged. Ready does not prove a pinned or
reproducible runtime.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| template reads as active proof meaning | route proof meaning to `evals/**/EVAL.md`, `evals/**/eval.yaml`, and repo proof guides |
| placeholder text reads as evidence | route to real evidence entries, fixtures, reports, or examples |
| proof pressure fits an existing eval | return the existing source bundle route instead of creating a parallel bundle |
| proof pressure is recurring but not authoring-ready | route through `QUESTBOOK.md` and source quest records |
| candidate pressure is concrete but not source-authoring-ready | run `python mechanics/proof-object/parts/eval-authoring/scripts/eval_forge_route.py --candidate-packet <path> --json` and keep the result as design guidance only |
| a new case needs quick collection before authoring | run `python mechanics/proof-object/parts/eval-authoring/scripts/prepare_eval_case.py --json`; write only an `eval_need_v1` proposal until review |
| runtime or trace artifact is the input | route through audit selected-evidence packets and candidate readers before bundle-local review |
| `.suite.md` is present without a ready sidecar | keep it as design pressure; validate or repair `local_eval_suite_execution_v1` before owner/apply |
| inventory, Forge, readiness, dashboard, session-start, promotion review, generated readers, or MCP would execute a local suite | stop; these surfaces are inspect-only |
| comparison posture hides in prose | carry it in frontmatter, `eval.yaml`, and comparison guidance |
| source eval package movement appears | keep source eval packages under `evals/` |
| generated readers, reports, receipts, runtime candidates, or sibling refs outrank source eval packages | return to source eval packages and bundle-local review |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
