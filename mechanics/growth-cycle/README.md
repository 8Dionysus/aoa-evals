# Growth-cycle Mechanic

## Entry Route

Start with this README for role and owned operation. Then read [DIRECTION.md](DIRECTION.md) for current operating direction, [PARTS.md](PARTS.md) for active parts, and [PROVENANCE.md](PROVENANCE.md) as the active-to-archive bridge for legacy or former-placement lookup.

## Role

`mechanics/growth-cycle/` routes bounded diagnosis proof before repair,
progression, harvest, closeout, or owner-followthrough claims.

It receives growth-cycle pressure when symptom refs, probable cause
hypotheses, unknowns, confidence limits, and handoff language need an
eval-side diagnosis route.

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

- `evals/workflow/aoa-diagnosis-cause-discipline/EVAL.md`
- `evals/workflow/aoa-diagnosis-cause-discipline/eval.yaml`
- `evals/workflow/aoa-diagnosis-cause-discipline/notes/diagnosis-contract.md`
- `evals/workflow/aoa-diagnosis-cause-discipline/examples/example-report.md`
- `evals/workflow/aoa-diagnosis-cause-discipline/checks/eval-integrity-check.md`
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
other parents. Active Growth Cycle topology still starts from `diagnosis-gate`.

## Parts

See [PARTS.md](PARTS.md).

The active part is `diagnosis-gate`. It owns cause-hypothesis discipline before
repair. Repair success, owner-fit routing, longitudinal growth, reviewed
closeout promotion, donor harvest, quest promotion, memory canon, and runtime
repair pressure route to the stronger owners below.

## Inputs

- diagnosis or self-diagnosis artifact;
- symptom refs and probable cause hypotheses;
- owner ambiguity notes, explicit unknowns, and confidence limits;
- repair or follow-through handoff language;
- nearby deferred pressure from closeout, harvest, repair, or progression as
  context; verdict authority routes through the owning proof or owner surface.

## Outputs

- bounded diagnosis-cause discipline verdict;
- symptom and cause split;
- evidence-limit and unknown notes;
- repair eligibility or proof handoff request;
- owner handoff route;
- owner handoff routes for repair success, final object quality, universal
  growth score, owner acceptance, quest promotion, or memory-canon pressure.

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

Boundary routes keep Growth Cycle diagnosis pressure with the owner that can
act on it:

| Pressure | Owner route |
| --- | --- |
| named cause proven true pressure | source owner diagnosis review plus bundle-local proof evidence |
| repair success from tidy diagnosis pressure | `mechanics/antifragility/parts/repair-proof/` route plus owner repair acceptance |
| repair boundedness, owner fit, or final object quality pressure | repair-proof route plus owner repository acceptance route |
| broad capability growth or universal progression score pressure | `mechanics/rpg/parts/progression-unlocks/` plus `mechanics/comparison-spine/parts/longitudinal-window/` route |
| reviewed closeout acceptance, donor harvest approval, or quest promotion pressure | closeout, donor, questbook, and target owner routes |
| memory canon, runtime activation, hidden automation, or owner-local landing pressure | `aoa-memo`, `abyss-stack`, `aoa-skills` or `aoa-playbooks`, and owner repository routes |

## Deferred Stages

- `repair-cycle`: current bounded repair proof routes through
  `mechanics/antifragility/parts/repair-proof/`.
- `progression-lift`: current progression and unlock proof routes through
  `mechanics/rpg/parts/progression-unlocks/`; repeated-window movement routes
  through `mechanics/comparison-spine/parts/longitudinal-window/`.
- `reviewed-closeout-chain` and `donor-harvest`: current local evidence routes
  as quest pressure and ingress context.
- `quest-promotion` and `owner-followthrough`: route through questbook and
  target owner repositories until a concrete eval-side proof operation exists.

## Legacy

Use [PROVENANCE.md](PROVENANCE.md) as the active-to-archive bridge when auditing why diagnosis-cause
discipline was split out of method-growth, why repair remained under
antifragility, or why closeout, harvest, and longitudinal movement stayed
deferred. New Growth Cycle proof work starts from this README, [PARTS.md](PARTS.md),
and the active part.

## Validation

Use [AGENTS](AGENTS.md#validation) for executable validation commands. This
README names the mechanic role, routes, and boundaries; the nearest route card
owns command execution.

When generated or source-support surfaces change, follow the same AGENTS
validation lane before closeout.

## Next Route

Use this mechanic before changing diagnosis-gate support, diagnosis-cause
discipline, or deferred-stage context that affects the diagnosis proof route.

For repair proof, start with `mechanics/antifragility/parts/repair-proof/`.
For progression or unlock proof, start with
`mechanics/rpg/parts/progression-unlocks/`. For longitudinal movement, start
with `mechanics/comparison-spine/parts/longitudinal-window/`.
