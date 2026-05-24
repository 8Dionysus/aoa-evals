# Growth Cycle Direction

Growth Cycle in `aoa-evals` should keep diagnosis proof from collapsing into
repair success, progression, harvest, or closeout acceptance by routing those
pressures to their stronger owners.

Use this file for the package's current operating direction: read it after the
parent entry card and before `PARTS.md`, part contracts, source bundles,
decision records, and `PROVENANCE.md`.

## Source-of-truth split

- `README.md`: package entry card and shortest proof-side route.
- `DIRECTION.md`: current operating direction.
- `PARTS.md`: active growth-cycle part map.
- `parts/`: diagnosis-gate support.
- `PROVENANCE.md`: controlled bridge from active route to deferred-stage accounting.
- `legacy/`: archive-local route for deferred-stage accounting after
  `PROVENANCE.md`.
- `evals/`: source proof objects that remain stronger than support parts.

## Current contour

- Keep `diagnosis-gate` as the active part.
- Keep repair proof under `antifragility/repair-proof`.
- Keep repeated-window movement under `comparison-spine/longitudinal-window`.
- Keep RPG progression under `rpg/progression-unlocks`.
- Keep closeout, harvest, quest promotion, and owner-followthrough pressure as
  deferred route work until separate evidence proves a part.

## Growth rule

Add a new growth-cycle part only when the stage is repeatable, has support
payload, and can name what it proves while next-stage pressure routes out. An
eval-backed thin support route is allowed only when the source eval package
stays under `evals/` and the part README explicitly says payload
subdirectories are absent by design.

## Stop-lines

- Repair success pressure routes to `mechanics/antifragility/parts/repair-proof/`
  plus owner repair acceptance.
- Broad capability growth, universal progression, closeout acceptance, donor
  harvest approval, memory canon, and runtime activation pressure route through
  their stronger owner split before eval-side diagnosis proof changes.

## Validation

Use the validation lane in [mechanics/growth-cycle/AGENTS.md](AGENTS.md#validation).
