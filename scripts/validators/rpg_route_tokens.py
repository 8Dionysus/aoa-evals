"""RPG route token constants."""

from __future__ import annotations


RPG_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "AoA-aligned",
    "progression or unlock pressure",
    "progression-unlocks",
    "mechanics/rpg/parts/progression-unlocks/docs/PROGRESSION_EVIDENCE_MODEL.md",
    "mechanics/rpg/parts/progression-unlocks/docs/UNLOCK_PROOF_BRIDGE.md",
    "mechanics/rpg/parts/progression-unlocks/schemas/progression_evidence.schema.json",
    "mechanics/rpg/parts/progression-unlocks/generated/unlock_proof_cards.min.example.json",
    "Stronger Owner Split",
    "Stop-Lines",
    "| universal agent score or broad capability growth | `mechanics/rpg/parts/progression-unlocks/` can hold bounded evidence; broad growth reading routes through `mechanics/comparison-spine/parts/longitudinal-window/` and owner review |",
    "| runtime equip state, activation, reward logic, or penalties | `abyss-stack` runtime route after owner gates and proof review |",
    "python scripts/validate_repo.py",
)
RPG_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "RPG proof work",
    "mechanics/rpg/PARTS.md",
    "PROVENANCE.md",
    "progression evidence",
    "unlock proof",
    "Create RPG parts from a recurring proof operation",
    "python scripts/validate_repo.py",
)
RPG_MECHANIC_PARTS_REQUIRED_TOKENS = (
    "progression-unlocks",
    "Inputs",
    "Outputs",
    "Owner split",
    "Stop-lines",
    "Validation",
    "growth-cycle",
    "| universal score, automatic rank, or broad capability growth | bounded progression evidence plus comparison/growth owner review |",
    "| generated-card authority | source support plus generated-reader route before citation |",
)
RPG_PROGRESS_UNLOCKS_PART_REQUIRED_TOKENS = (
    "Progression Unlocks Part",
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
    "mechanics/rpg/parts/progression-unlocks/docs/PROGRESSION_EVIDENCE_MODEL.md",
    "mechanics/rpg/parts/progression-unlocks/docs/UNLOCK_PROOF_BRIDGE.md",
    "mechanics/rpg/parts/progression-unlocks/schemas/progression_evidence.schema.json",
    "mechanics/rpg/parts/progression-unlocks/generated/unlock_proof_cards.min.example.json",
    "progression evidence",
    "unlock proof",
    "| quest completion or quest acceptance | quest source owner and questbook lifecycle route with proof refs |",
    "| universal rank, one global score, automatic rank assignment, or broad capability growth | bounded progression evidence plus `mechanics/comparison-spine/parts/longitudinal-window/` and owner review |",
    "| runtime equip state, runtime activation, reward logic, or penalties | `abyss-stack` runtime route after owner gates |",
    "| growth-cycle diagnosis, repair, harvest, closeout, or longitudinal movement | `mechanics/growth-cycle/`, `mechanics/antifragility/`, closeout, and comparison owner routes |",
    "| generated-card authority | generated support source, schema/example review, and bundle-local proof citation route |",
    "python scripts/build_catalog.py --check",
)
RPG_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/rpg/",
    "AoA-aligned",
    "progression-unlocks",
    "docs/PROGRESSION_EVIDENCE_MODEL.md",
    "docs/UNLOCK_PROOF_BRIDGE.md",
    "Quest source records stay under",
    "growth-cycle",
    "pressure-to-owner route map",
    "runtime equip",
)
RPG_PROGRESS_UNLOCKS_CONTRACT_DECISION_REQUIRED_TOKENS = (
    "RPG Progression-unlocks Contract",
    "mechanics/rpg/parts/progression-unlocks/README.md",
    "`## Stronger Owner Split`",
    "`## Stop-Lines`",
    "pressure-to-owner route map",
    "quest source owner and questbook lifecycle route",
    "runtime route after owner gates",
    "generated unlock cards remain",
    "Diagnosis, repair, harvest, closeout, and longitudinal movement",
)


__all__ = tuple(
    name for name in globals() if name.startswith("RPG_") and name.endswith("_TOKENS")
)
