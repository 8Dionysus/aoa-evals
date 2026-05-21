# Owner Landing Part

## Role

This part owns the support route for bounded method-growth owner landing proof
through `aoa-owner-fit-routing-quality`.

It keeps the shared owner-fit fixture family under the Method-growth mechanic
because AoA method-growth routes reviewed candidates toward owner-local
acceptance, landing, pruning, or handoff. The source proof bundle stays under
`bundles/`.

## Source Surfaces

- `bundles/aoa-owner-fit-routing-quality/EVAL.md`
- `bundles/aoa-owner-fit-routing-quality/eval.yaml`
- `bundles/aoa-owner-fit-routing-quality/fixtures/contract.json`
- `bundles/aoa-owner-fit-routing-quality/runners/contract.json`
- `bundles/aoa-owner-fit-routing-quality/reports/summary.schema.json`
- `bundles/aoa-owner-fit-routing-quality/reports/example-report.json`
- `mechanics/method-growth/parts/owner-landing/fixtures/owner-fit-routing-v1/README.md`

## Inputs

- one reviewed growth-refinery candidate;
- one chosen `owner_hypothesis`;
- one chosen `owner_shape`;
- one rejected `nearest_wrong_target`;
- bounded evidence for derivative-repo exclusion.

## Outputs

- bounded owner-fit routing verdict;
- owner-fit note per reviewed candidate;
- nearest-wrong-target note;
- derivative-drift warning when routing tries to turn `aoa-routing` or
  `aoa-kag` into first-authoring homes;
- owner handoff route when the candidate needs local acceptance.

## Stronger Owner Split

`Agents-of-Abyss` owns Method-growth law, owner-landing grammar, pruning
discipline, and the center rule that owner fit is a route question before it is
an owner-local truth.

Final owner repositories own landed object truth, owner-local acceptance,
activation, quality, and future maintenance. `aoa-skills`, `aoa-techniques`,
`aoa-playbooks`, `aoa-memo`, and `Dionysus` own their local skill, technique,
method, memory, and seed truths. `aoa-routing` and `aoa-kag` stay derivative
unless their owner routes explicitly land meaning.

`aoa-evals` owns only bounded owner-fit proof wording, nearest-wrong-target
visibility, derivative-repo exclusion evidence, fixture/report contracts, and
claim limits for `aoa-owner-fit-routing-quality`.

## Stop-Lines

This part must not claim:

- final owner-object quality;
- owner-local acceptance, activation, or future maintenance;
- permanent routing from one owner-fit read;
- derivative first-authoring for `aoa-routing` or `aoa-kag`;
- skill, technique, playbook, memory, seed, or stats truth;
- proof that lineage coherence implies owner fit;
- one universal growth score.

This part is an owner-landing proof route, not final object proof. A clean
owner-fit read does not prove the object is good, permanently routed, accepted
by the owner, or ready for derivative first-authoring.

## Validation

```bash
python scripts/validate_repo.py --eval aoa-owner-fit-routing-quality
python scripts/build_catalog.py --check
python scripts/validate_repo.py
```
