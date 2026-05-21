# Fixture Families

## Role

`fixture-families/` owns generic shared fixture-family support for
`aoa-evals`.

It is a part of `proof-infra`, not a parent mechanic. It is not a replacement
for bundle-local `EVAL.md`, bundle-local fixture contracts, comparison
semantics, audit verdicts, memo truth, runtime evidence, or sibling owner
truth.

## Owned Operation

`bundle support need -> public-safe reusable family -> bundle-local fixture contract -> generated proof_artifacts`

The bundle owns the claim. This part owns the reusable family path that lets a
bundle say which public-safe case pressure it uses.

## Source Surfaces

- `mechanics/proof-infra/parts/fixture-families/fixtures/<family>/README.md`
- `bundles/*/fixtures/contract.json`
- `generated/eval_catalog.json`
- `scripts/build_catalog.py`
- `scripts/validate_repo.py`

## Active Families

| Family | Primary source bundle |
| --- | --- |
| `ambiguity-bounded-v1` | `bundles/aoa-ambiguity-handling/` |
| `approval-boundary-bounded-v1` | `bundles/aoa-approval-boundary-adherence/` |
| `local-text-contract-v1` | `bundles/aoa-local-text-contract-fit/` |
| `memo-contradiction-guardrail-v1` | `bundles/aoa-memo-contradiction-integrity/` |
| `memo-writeback-act-guardrail-v1` | `bundles/aoa-memo-writeback-act-integrity/` |
| `ring-application-discipline-v1` | `bundles/aoa-ring-application-discipline/` |
| `scope-drift-bounded-v1` | `bundles/aoa-scope-drift-detection/` |
| `tool-trajectory-bounded-v1` | `bundles/aoa-tool-trajectory-discipline/` |
| `trace-outcome-bounded-v1` | `bundles/aoa-trace-outcome-separation/` |
| `verification-honesty-v1` | `bundles/aoa-verification-honesty/` |
| `witness-trace-v1` | `bundles/aoa-witness-trace-integrity/` |

## Inputs

- a source bundle that needs a reusable public-safe family;
- the family `README.md` under
  `mechanics/proof-infra/parts/fixture-families/fixtures/<family>/`;
- a bundle-local `bundles/<bundle>/fixtures/contract.json` that names this
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

The family path supports the proof object. It does not own:

- the bounded claim;
- the object under evaluation;
- verdict logic;
- report interpretation;
- memo truth;
- runtime or trace acceptance;
- AoA center mechanic meaning;
- sibling owner truth.

If a later evidence pass proves that a family belongs to a narrower active
mechanic, move it with a decision and provenance bridge instead of keeping it
here by habit.

## Stop-Lines

- Do not create a parent mechanic from a family name.
- Do not use this part for domain-owned families already routed through
  `comparison-spine`, `recurrence`, `checkpoint`, `experience`,
  `antifragility`, `method-growth`, `rpg`, `growth-cycle`, or `distillation`.
- Keep former root fixture-family aliases as historical compatibility
  vocabulary.
- Do not weaken bundle-local contracts to preserve an old path.
- Do not treat generated `proof_artifacts` as authority.

## Validation

Payload coverage anchor: `mechanics/proof-infra/parts/fixture-families/`.

Run:

```bash
python scripts/build_catalog.py
python scripts/build_catalog.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```

Run targeted bundle validation for each bundle whose fixture contract points to
this part.
