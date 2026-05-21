# Growth-cycle / Part Index

`mechanics/growth-cycle/parts/` contains the active parts of the eval-side
Growth Cycle proof operation.

The mechanic owns the route:

`diagnosis pressure -> cause-hypothesis proof question -> bundle-local diagnosis review -> repair eligibility or owner handoff`

## Parts

| Part | Role | Active surfaces |
| --- | --- | --- |
| `diagnosis-gate` | Maintains cause-hypothesis discipline before repair without turning symptoms, owner ambiguity, or later cleanup into cause proof. | `mechanics/growth-cycle/parts/diagnosis-gate/README.md` |

## Part Contract

The active source proof bundle is `aoa-diagnosis-cause-discipline`.

Inputs are diagnosis or self-diagnosis artifacts, symptom refs, probable cause
hypotheses, owner ambiguity notes, explicit unknowns, confidence limits, and
repair or follow-through handoff language.

Outputs are bounded diagnosis-cause discipline verdicts, symptom/cause splits,
evidence-limit notes, unknown and confidence notes, repair eligibility, proof
handoff requests, and owner handoff routes.

Owner split stays explicit: `Agents-of-Abyss` owns Growth Cycle law, stage
order, and stop-lines; `aoa-skills` owns executable diagnosis and repair
workflows; `aoa-agents` owns actor health and role posture; `aoa-sdk` owns
checkpoint and closeout control surfaces; target owner repositories own local
repair acceptance; `aoa-evals` owns proof wording, verdict logic, support
notes, example readout posture, and claim limits.

Stop-lines forbid cause certainty, repair success, owner-fit proof, final
object quality, broad capability growth, universal progression scores,
reviewed-closeout acceptance, donor harvest approval, quest promotion, memory
canon, runtime activation, hidden automation, and owner-local landing.

Validation is the affected bundle validation, generated catalog check, root
repository validation, semantic agent validation, and the growth-cycle mechanic
route checks in `scripts/validate_repo.py`.

## Deferred Part Families

`repair-cycle` remains deferred as a Growth Cycle part because current bounded
repair proof is actively routed through
`mechanics/antifragility/parts/repair-proof/`.

`progression-lift` remains deferred as a Growth Cycle part because current RPG
progression and unlock proof routes through
`mechanics/rpg/parts/progression-unlocks/`, while repeated-window movement
routes through `mechanics/comparison-spine/parts/longitudinal-window/`.

`reviewed-closeout-chain`, `donor-harvest`, `quest-promotion`, and
`owner-followthrough` remain deferred because current local evidence is quest,
ingress, or owner-pressure context rather than an active eval-side proof
operation with its own part-local contract.
