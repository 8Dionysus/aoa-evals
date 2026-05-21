# Growth Cycle Direction

Growth Cycle in `aoa-evals` should keep diagnosis proof from collapsing into
repair success, progression, harvest, or closeout acceptance.

This file owns the current operating direction only. It does not replace the
entry card, part map, part contracts, source bundles, decisions, or provenance
bridge.

## Source-of-truth split

- `README.md`: package entry card and shortest proof-side route.
- `DIRECTION.md`: current operating direction.
- `PARTS.md`: active growth-cycle part map.
- `parts/`: diagnosis-gate support.
- `PROVENANCE.md`: controlled bridge from active route to deferred-stage accounting.
- `legacy/`: lineage only; not a generic growth backlog.
- `bundles/`: source proof objects that remain stronger than support parts.

## Current contour

- Keep `diagnosis-gate` as the active part.
- Keep repair proof under `antifragility/repair-proof`.
- Keep repeated-window movement under `comparison-spine/longitudinal-window`.
- Keep RPG progression under `rpg/progression-unlocks`.
- Keep closeout, harvest, quest promotion, and owner-followthrough pressure as
  deferred route work until separate evidence proves a part.

## Growth rule

Add a new growth-cycle part only when the stage is repeatable, has support
payload, and can name what it proves without claiming the next stage. A
bundle-backed thin support route is allowed only when the source proof bundle
stays under `bundles/` and the part README explicitly says there are no
part-local payload subdirectories yet.

## Stop-lines

- Do not claim repair success from diagnosis proof.
- Do not claim broad capability growth, universal progression, closeout
  acceptance, donor harvest approval, memory canon, or runtime activation.

## Validation

Use the validation lane in [mechanics/growth-cycle/AGENTS.md](AGENTS.md#validation).
