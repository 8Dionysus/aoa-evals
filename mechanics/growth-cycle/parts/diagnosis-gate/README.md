# Diagnosis Gate Part

## Role

This part owns the support route for cause-hypothesis discipline through
`aoa-diagnosis-cause-discipline`.

It keeps diagnosis under the Growth Cycle mechanic because AoA Growth Cycle
requires diagnosis before repair and separates symptoms from causes. The source
proof bundle stays under `bundles/`.

## Thin Support Posture

This is a bundle-backed thin support route with no part-local payload subdirectories.
The source proof bundle stays under `bundles/` because
`bundles/aoa-diagnosis-cause-discipline/` owns the strongest local proof
meaning: claim wording, source notes, example report, and integrity check.

Do not add empty placeholder payload directories here. Add part-local payload
only when a concrete Growth Cycle support artifact exists outside the source
proof bundle and can name its own owner split, stop-lines, and validation.

## Source Surfaces

- `bundles/aoa-diagnosis-cause-discipline/EVAL.md`
- `bundles/aoa-diagnosis-cause-discipline/eval.yaml`
- `bundles/aoa-diagnosis-cause-discipline/notes/diagnosis-contract.md`
- `bundles/aoa-diagnosis-cause-discipline/examples/example-report.md`
- `bundles/aoa-diagnosis-cause-discipline/checks/eval-integrity-check.md`

## Inputs

- one diagnosis or self-diagnosis artifact;
- symptom refs;
- probable cause hypotheses;
- owner ambiguity notes;
- unknowns and confidence limits;
- one repair or follow-through handoff.

## Outputs

- bounded diagnosis-cause discipline verdict;
- symptom/cause split;
- evidence-limit note;
- unknown and confidence note;
- repair eligibility or proof handoff request;
- owner handoff route when a diagnosis requires local repair, acceptance, or
  follow-through authority.

## Stronger Owner Split

`Agents-of-Abyss` owns Growth Cycle law, stage order, and the center rule that
diagnosis must precede repair when cause is unknown. `aoa-skills` owns
executable diagnosis and repair workflows. `aoa-agents` owns actor health and
role posture. `aoa-sdk` owns checkpoint and closeout control surfaces.
`aoa-memo` owns memory lessons and writeback meaning. `abyss-stack` owns
runtime repair and health plumbing. Owner repositories own local repair,
acceptance, and landing.

`aoa-evals` owns only bounded diagnosis-cause discipline proof wording, support
notes, example readout posture, claim limits, and bundle-local interpretation
for `aoa-diagnosis-cause-discipline`.

## Stop-Lines

This part must not claim:

- the named cause is proven true;
- repair success;
- owner-fit proof;
- final object quality proof;
- broad growth score or universal progression score;
- reviewed closeout acceptance;
- donor harvest approval;
- quest promotion;
- memory canon;
- runtime activation or hidden automation;
- owner acceptance or owner-local landing.

`aoa-repair-boundedness` remains under
`mechanics/antifragility/parts/repair-proof/`. Repeated-window movement remains
under `mechanics/comparison-spine/parts/longitudinal-window/`. RPG progression
and unlock proof remains under `mechanics/rpg/parts/progression-unlocks/`.

## Validation

```bash
python scripts/validate_repo.py --eval aoa-diagnosis-cause-discipline
python scripts/build_catalog.py --check
python scripts/validate_repo.py
```
