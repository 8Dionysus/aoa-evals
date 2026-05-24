# Growth-cycle / Diagnosis Gate Part

## Role

This part owns the support route for cause-hypothesis discipline through
`aoa-diagnosis-cause-discipline`.

It keeps diagnosis under the Growth Cycle mechanic because AoA Growth Cycle
requires diagnosis before repair and separates symptoms from causes. The source
proof bundle stays under `evals/`.

## Thin Support Posture

This is an eval-backed thin support route: payload subdirectories are absent by design.
The source eval package stays under `evals/` because
`evals/workflow/aoa-diagnosis-cause-discipline/` owns the strongest local proof
meaning: claim wording, source notes, example report, and integrity check.

Part-local payload belongs here only when a concrete Growth Cycle support
artifact exists outside the source proof bundle and can name its own owner
split, stop-lines, and validation.

## Source Surfaces

- `evals/workflow/aoa-diagnosis-cause-discipline/EVAL.md`
- `evals/workflow/aoa-diagnosis-cause-discipline/eval.yaml`
- `evals/workflow/aoa-diagnosis-cause-discipline/notes/diagnosis-contract.md`
- `evals/workflow/aoa-diagnosis-cause-discipline/examples/example-report.md`
- `evals/workflow/aoa-diagnosis-cause-discipline/checks/eval-integrity-check.md`

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

`aoa-evals` owns bounded diagnosis-cause discipline proof wording, support
notes, example readout posture, claim limits, and bundle-local interpretation
for `aoa-diagnosis-cause-discipline`. Authority beyond that proof reading
routes through the stronger owner split above.

## Stop-Lines

Boundary routes keep diagnosis-gate pressure with the owner that can act on it:

| Pressure | Owner route |
| --- | --- |
| named cause proven true pressure | source owner diagnosis review plus bundle-local proof evidence |
| repair success pressure | `mechanics/antifragility/parts/repair-proof/` route plus owner repair acceptance |
| owner-fit proof pressure | owner repository acceptance route |
| final object quality proof pressure | owner repository acceptance route |
| broad growth score or universal progression score pressure | `mechanics/rpg/parts/progression-unlocks/` plus `mechanics/comparison-spine/parts/longitudinal-window/` route |
| reviewed closeout acceptance pressure | closeout route plus owner acceptance |
| donor harvest approval pressure | donor harvest route plus target owner acceptance |
| quest promotion pressure | `mechanics/questbook/` route plus owner acceptance |
| memory canon pressure | `aoa-memo` memory route |
| runtime activation or hidden automation pressure | `abyss-stack` runtime route plus `aoa-skills` or `aoa-playbooks` execution/choreography route |
| owner acceptance or owner-local landing pressure | owner repository acceptance route |

`aoa-repair-boundedness` remains under
`mechanics/antifragility/parts/repair-proof/`. Repeated-window movement remains
under `mechanics/comparison-spine/parts/longitudinal-window/`. RPG progression
and unlock proof remains under `mechanics/rpg/parts/progression-unlocks/`.

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
