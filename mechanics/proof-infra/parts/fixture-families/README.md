# Proof Infra / Fixture Families Part

## Role

`fixture-families/` owns generic shared fixture-family support for
`aoa-evals`.

It routes reusable public-safe case pressure from a source bundle to a
part-local family path while the bundle and any narrower mechanic keep stronger
proof meaning.

## Owned Operation

`bundle support need -> public-safe reusable family -> bundle-local fixture contract -> generated proof_artifacts`

The bundle owns the claim. This part owns the reusable family path that lets a
bundle say which public-safe case pressure it uses.

## Source Surfaces

- `mechanics/proof-infra/parts/fixture-families/fixtures/<family>/README.md`
- `evals/**/fixtures/contract.json`
- `generated/eval_catalog.json`
- `scripts/build_catalog.py`
- `scripts/validate_repo.py`

## Active Families

| Family | Primary source bundle |
| --- | --- |
| `ambiguity-bounded-v1` | `evals/stress/aoa-ambiguity-handling/` |
| `approval-boundary-bounded-v1` | `evals/boundary/aoa-approval-boundary-adherence/` |
| `local-text-contract-v1` | `evals/boundary/aoa-local-text-contract-fit/` |
| `memo-contradiction-guardrail-v1` | `evals/workflow/aoa-memo-contradiction-integrity/` |
| `memo-write-path-guardrail-v1` | `evals/boundary/aoa-memo-write-path-guardrails/` |
| `memo-writeback-act-guardrail-v1` | `evals/workflow/aoa-memo-writeback-act-integrity/` |
| `memo-writeback-decision-quality-v1` | `evals/workflow/aoa-memo-writeback-decision-quality/` |
| `ring-application-discipline-v1` | `evals/workflow/aoa-ring-application-discipline/` |
| `scope-drift-bounded-v1` | `evals/boundary/aoa-scope-drift-detection/` |
| `tool-trajectory-bounded-v1` | `evals/workflow/aoa-tool-trajectory-discipline/` |
| `trace-outcome-bounded-v1` | `evals/workflow/aoa-trace-outcome-separation/` |
| `verification-honesty-v1` | `evals/workflow/aoa-verification-honesty/` |
| `witness-trace-v1` | `evals/workflow/aoa-witness-trace-integrity/` |

## Inputs

- a source bundle that needs a reusable public-safe family;
- the family `README.md` under
  `mechanics/proof-infra/parts/fixture-families/fixtures/<family>/`;
- a bundle-local `evals/<family>/<eval>/fixtures/contract.json` that names this
  family through `shared_fixture_family_path`;
- optional bundle-local runner, report schema, example, or reviewed report
  surfaces.

## Outputs

- an explicit `shared_fixture_family_path` under
  `mechanics/proof-infra/parts/fixture-families/fixtures/<family>/README.md`;
- generated catalog `proof_artifacts` derived from bundle-local contracts;
- updated public route text in bundle docs, selection/index surfaces, and
  proof-loop or audit bridges that cite these families.

## Stronger Owner Split

The family path supports the proof object. Stronger meaning routes through:

| Meaning pressure | Stronger route |
| --- | --- |
| bounded claim and object under evaluation | bundle-local `EVAL.md` and `eval.yaml` |
| verdict logic and report interpretation | bundle-local report contracts and reviewed reports |
| comparison, audit, recurrence, checkpoint, experience, antifragility, method-growth, RPG, growth-cycle, or distillation semantics | the owning active mechanic part |
| memo, runtime, trace, AoA center, or sibling-owner truth | the stronger owner repository or intake route named by the bundle/mechanic |

If a later evidence pass proves that a family belongs to a narrower active
mechanic, move it with a decision and provenance bridge instead of keeping it
here by habit.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| Family-name parent pressure | `mechanics/EVIDENCE_CLUSTERS.md` before any parent proposal; this part stays reusable support. |
| Domain-owned family pressure | `comparison-spine`, `recurrence`, `checkpoint`, `experience`, `antifragility`, `method-growth`, `rpg`, `growth-cycle`, or `distillation`, whichever owns the operation. |
| Former root fixture-family alias pressure | `PROVENANCE.md` and `legacy/` as compatibility vocabulary. |
| Bundle-local contract drift | the bundle-local fixture contract and source claim. |
| Generated `proof_artifacts` pressure | source contracts plus `scripts/build_catalog.py --check`; generated readers stay derived. |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
