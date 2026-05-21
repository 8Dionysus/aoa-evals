# Growth-cycle Mechanic

## Entry Route

Start with this README for role and owned operation. Then read [DIRECTION.md](DIRECTION.md) for current operating direction, [PARTS.md](PARTS.md) for active parts, and [PROVENANCE.md](PROVENANCE.md) only for legacy or former placement.

## Owned Operation

`mechanics/growth-cycle/` owns the eval-side Growth Cycle diagnosis proof
operation:

`diagnosis pressure -> cause-hypothesis proof question -> bundle-local diagnosis review -> repair eligibility or owner handoff`

This package is AoA-aligned. It keeps the parent name `growth-cycle` because
the operation materializes the center Growth Cycle mechanic on the proof side.
The first active part is `diagnosis-gate`; repair, harvest, closeout, and
progression-lift pressure remain routed to their current owners until separate
evidence proves another active part.

Route guard: repair proof under `antifragility`; repeated-window movement under
`comparison-spine`; RPG progression under `rpg`.

## Active Source Surfaces

- `bundles/aoa-diagnosis-cause-discipline/EVAL.md`
- `bundles/aoa-diagnosis-cause-discipline/eval.yaml`
- `bundles/aoa-diagnosis-cause-discipline/notes/diagnosis-contract.md`
- `bundles/aoa-diagnosis-cause-discipline/examples/example-report.md`
- `bundles/aoa-diagnosis-cause-discipline/checks/eval-integrity-check.md`
- `mechanics/growth-cycle/parts/diagnosis-gate/README.md`

## Boundary And Deferred Context

- `mechanics/method-growth/PARTS.md`
- `mechanics/antifragility/parts/repair-proof/README.md`
- `mechanics/comparison-spine/parts/longitudinal-window/README.md`
- `docs/REPEATED_WINDOW_DISCIPLINE_GUIDE.md`
- `docs/REVIEWED_CLOSEOUT_WRITEBACK_PROOF_INGRESS.md`
- `quests/harvest/captured/AOA-EV-Q-0004.yaml`
- `quests/closeout/captured/AOA-EV-Q-0010.yaml`
- `quests/closeout/captured/AOA-EV-Q-0013.yaml`

These context surfaces explain why nearby stages stay deferred or route to
other parents. They are not active Growth Cycle parts by themselves.

## Parts

See [PARTS.md](PARTS.md).

The active part is `diagnosis-gate`. It owns cause-hypothesis discipline before
repair. It does not own repair success, owner-fit routing, longitudinal growth,
reviewed closeout promotion, donor harvest, quest promotion, memory canon, or
runtime repair.

## Inputs

- diagnosis or self-diagnosis artifact;
- symptom refs and probable cause hypotheses;
- owner ambiguity notes, explicit unknowns, and confidence limits;
- repair or follow-through handoff language;
- nearby deferred pressure from closeout, harvest, repair, or progression only
  as context, not as active growth-cycle verdict authority.

## Outputs

- bounded diagnosis-cause discipline verdict;
- symptom and cause split;
- evidence-limit and unknown notes;
- repair eligibility or proof handoff request;
- owner handoff route;
- no repair success proof, final object quality proof, universal growth score,
  owner acceptance, quest promotion, or memory canon.

## Stronger Owner Split

`Agents-of-Abyss` owns Growth Cycle law, stage order, stop-lines, and the
center rule that diagnosis must precede repair when cause is not yet known.

`aoa-skills` owns executable diagnosis and repair workflows. `aoa-agents` owns
actor health and role posture. `aoa-sdk` owns checkpoint and closeout control
surfaces. `aoa-playbooks` owns recurring cycle choreography. `aoa-memo` owns
memory lessons and writeback meaning. `aoa-stats` owns derived movement
visibility. `abyss-stack` owns runtime repair and health plumbing.

`aoa-evals` owns bounded proof wording, verdict logic, support notes, example
readout posture, claim limits, and validation for diagnosis-cause discipline.

## Stop-Lines

Do not use this package to claim:

- the named cause is proven true;
- repair worked because the diagnosis was tidy;
- repair boundedness, owner fit, or final object quality;
- broad capability growth or a universal progression score;
- reviewed closeout acceptance, donor harvest approval, or quest promotion;
- memory canon, runtime activation, hidden automation, or owner-local landing.

## Deferred Stages

- `repair-cycle`: current bounded repair proof routes through
  `mechanics/antifragility/parts/repair-proof/`.
- `progression-lift`: current progression and unlock proof routes through
  `mechanics/rpg/parts/progression-unlocks/`; repeated-window movement routes
  through `mechanics/comparison-spine/parts/longitudinal-window/`.
- `reviewed-closeout-chain` and `donor-harvest`: current local evidence is
  quest pressure and ingress context, not an active growth-cycle part.
- `quest-promotion` and `owner-followthrough`: route through questbook and
  target owner repositories until a concrete eval-side proof operation exists.

## Legacy

Use [PROVENANCE.md](PROVENANCE.md) only when auditing why diagnosis-cause
discipline was split out of method-growth, why repair remained under
antifragility, or why closeout, harvest, and longitudinal movement stayed
deferred. New Growth Cycle proof work starts from this README, [PARTS.md](PARTS.md),
and the active part.

## Validation

```bash
python scripts/validate_repo.py --eval aoa-diagnosis-cause-discipline
python scripts/build_catalog.py --check
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
```
