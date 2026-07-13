"""Growth-cycle route token constants."""

from __future__ import annotations


GROWTH_CYCLE_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "AoA-aligned",
    "diagnosis pressure",
    "diagnosis-gate",
    "evals/workflow/aoa-diagnosis-cause-discipline/EVAL.md",
    "evals/workflow/aoa-diagnosis-cause-discipline/notes/diagnosis-contract.md",
    "Stronger Owner Split",
    "Stop-Lines",
    "repair proof under `antifragility`",
    "repeated-window movement under",
    "| named cause proven true pressure | source owner diagnosis review plus bundle-local proof evidence |",
    "| repair success from tidy diagnosis pressure | `mechanics/antifragility/parts/repair-proof/` route plus owner repair acceptance |",
    "| repair boundedness, owner fit, or final object quality pressure | repair-proof route plus owner repository acceptance route |",
    "| broad capability growth or universal progression score pressure | `mechanics/rpg/parts/progression-unlocks/` plus `mechanics/comparison-spine/parts/longitudinal-window/` route |",
    "| reviewed closeout acceptance, donor harvest approval, or quest promotion pressure | closeout, donor, questbook, and target owner routes |",
    "| memory canon, runtime activation, hidden automation, or owner-local landing pressure | `aoa-memo`, `abyss-stack`, `aoa-skills` or `aoa-playbooks`, and owner repository routes |",
    "python scripts/validate_repo.py --eval aoa-diagnosis-cause-discipline",
)
GROWTH_CYCLE_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "Growth Cycle diagnosis proof work",
    "mechanics/growth-cycle/PARTS.md",
    "PROVENANCE.md",
    "Keep source proof bundles under `evals/`",
    "Create growth-cycle parts from a recurring proof operation",
    "python scripts/validate_repo.py --eval aoa-diagnosis-cause-discipline",
)
GROWTH_CYCLE_MECHANIC_PARTS_REQUIRED_TOKENS = (
    "diagnosis-gate",
    "Inputs",
    "Outputs",
    "Owner split",
    "Stop-lines",
    "Validation",
    "aoa-diagnosis-cause-discipline",
    "| cause certainty | source owner diagnosis review plus bundle-local proof evidence |",
    "| repair success | `mechanics/antifragility/parts/repair-proof/` route plus owner repair acceptance |",
    "| owner-fit proof or final object quality | owner repository acceptance route |",
    "| broad capability growth or universal progression score | `mechanics/rpg/parts/progression-unlocks/` plus `mechanics/comparison-spine/parts/longitudinal-window/` route |",
    "| reviewed-closeout acceptance, donor harvest approval, or quest promotion | closeout, donor, questbook, and target owner routes |",
    "| memory canon | `aoa-memo` memory route |",
    "| runtime activation or hidden automation | `abyss-stack` runtime route plus `aoa-skills` or `aoa-playbooks` execution/choreography route |",
    "| owner-local landing | owner repository acceptance route |",
)
GROWTH_CYCLE_PARTS_README_REQUIRED_TOKENS = (
    "# Growth-cycle / Parts Route",
    "## Operating Card",
    "| role | lower index for active Growth Cycle proof parts |",
    "## Active Parts",
    "| `diagnosis-gate/` | cause-hypothesis discipline before repair, progression, closeout, quest, memory, runtime, or owner acceptance claims | `diagnosis-gate/README.md` |",
    "## Owner Pressure Routes",
    "| cause certainty | source owner diagnosis review plus bundle-local proof evidence |",
    "| repair success | `mechanics/antifragility/parts/repair-proof/` route plus owner repair acceptance |",
    "| broad capability growth or universal progression score | `mechanics/rpg/parts/progression-unlocks/` plus `mechanics/comparison-spine/parts/longitudinal-window/` route |",
    "| runtime activation or hidden automation | `abyss-stack` runtime route plus `aoa-skills` or `aoa-playbooks` execution/choreography route |",
    "## Part Admission Route",
    "| diagnosis or self-diagnosis evidence needs cause-hypothesis discipline | source bundle and part contract already exist | `diagnosis-gate/README.md` |",
    "mechanics/growth-cycle/parts/AGENTS.md#validation",
)
GROWTH_CYCLE_DIAGNOSIS_GATE_PART_REQUIRED_TOKENS = (
    "Diagnosis Gate Part",
    "eval-backed thin support route",
    "payload subdirectories are absent by design",
    "evals/workflow/aoa-diagnosis-cause-discipline/EVAL.md",
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
    "symptom refs",
    "probable cause hypotheses",
    "aoa-repair-boundedness",
    "mechanics/antifragility/parts/repair-proof/",
    "| named cause proven true pressure | source owner diagnosis review plus bundle-local proof evidence |",
    "| repair success pressure | `mechanics/antifragility/parts/repair-proof/` route plus owner repair acceptance |",
    "| owner-fit proof pressure | owner repository acceptance route |",
    "| final object quality proof pressure | owner repository acceptance route |",
    "| broad growth score or universal progression score pressure | `mechanics/rpg/parts/progression-unlocks/` plus `mechanics/comparison-spine/parts/longitudinal-window/` route |",
    "| reviewed closeout acceptance pressure | closeout route plus owner acceptance |",
    "| donor harvest approval pressure | donor harvest route plus target owner acceptance |",
    "| quest promotion pressure | `mechanics/questbook/` route plus owner acceptance |",
    "| memory canon pressure | `aoa-memo` memory route |",
    "| runtime activation or hidden automation pressure | `abyss-stack` runtime route plus `aoa-skills` or `aoa-playbooks` execution/choreography route |",
    "| owner acceptance or owner-local landing pressure | owner repository acceptance route |",
    "python scripts/validate_repo.py --eval aoa-diagnosis-cause-discipline",
)
GROWTH_CYCLE_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/growth-cycle/",
    "AoA-aligned",
    "diagnosis-gate",
    "aoa-diagnosis-cause-discipline",
    "Source proof bundles stay under `evals/`",
    "aoa-repair-boundedness",
    "aoa-longitudinal-growth-snapshot",
    "No root file movement",
)
GROWTH_CYCLE_DIAGNOSIS_GATE_CONTRACT_DECISION_REQUIRED_TOKENS = (
    "Growth-cycle Diagnosis-gate Contract",
    "mechanics/growth-cycle/parts/diagnosis-gate/README.md",
    "eval-backed thin support route",
    "cause-hypothesis discipline",
    "repair parent",
    "owner-fit proof",
    "broad growth score",
    "donor-harvest approval",
    "quest-promotion",
    "owner-local landing authority",
)
REPAIR_DIAGNOSIS_ROUTE_BOUNDARY_DECISION_REQUIRED_TOKENS = (
    "Repair Diagnosis Route Boundary",
    "mechanics/antifragility/parts/repair-proof/",
    "mechanics/growth-cycle/parts/diagnosis-gate/",
    "aoa-repair-boundedness",
    "aoa-diagnosis-cause-discipline",
    "`repair` remains a wrong parent form",
    "Diagnosis-cause discipline is not an antifragility part",
    "repair proof is not diagnosis proof",
)


__all__ = tuple(
    name
    for name in globals()
    if name.startswith(("GROWTH_CYCLE_", "REPAIR_")) and name.endswith("_TOKENS")
)
