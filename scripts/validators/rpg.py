"""RPG mechanic route and progression-unlock validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Sequence

from validators.common import ValidationIssue


RPG_MECHANIC_README_NAME = "mechanics/rpg/README.md"
RPG_MECHANIC_AGENTS_NAME = "mechanics/rpg/AGENTS.md"
RPG_MECHANIC_PARTS_NAME = "mechanics/rpg/PARTS.md"
RPG_MECHANIC_PROVENANCE_NAME = "mechanics/rpg/PROVENANCE.md"
RPG_PROGRESS_UNLOCKS_PART_README_NAME = (
    "mechanics/rpg/parts/progression-unlocks/README.md"
)
RPG_MECHANIC_DECISION_NAME = "docs/decisions/AOA-EV-D-0036-rpg-mechanic-package.md"
RPG_PROGRESS_UNLOCKS_CONTRACT_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0067-rpg-progression-unlocks-contract.md"
)
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
    "python scripts/validate_repo.py",
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
    "python -m pytest -q tests/test_mechanic_surface_contracts.py -k rpg_progression_unlocks",
)


@dataclass(frozen=True)
class RpgRouteContext:
    require_tokens: Callable[..., str]
    provenance_tokens: Sequence[str]


def _require(
    context: RpgRouteContext,
    repo_root: Path,
    path_name: str,
    tokens: Sequence[str],
    issues: list[ValidationIssue],
) -> str:
    return context.require_tokens(
        repo_root=repo_root,
        path_name=path_name,
        tokens=tokens,
        issues=issues,
    )


def validate_rpg_route_surfaces(
    repo_root: Path,
    *,
    context: RpgRouteContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    _require(context, repo_root, RPG_MECHANIC_README_NAME, RPG_MECHANIC_REQUIRED_TOKENS, issues)
    _require(context, repo_root, RPG_MECHANIC_AGENTS_NAME, RPG_MECHANIC_AGENTS_REQUIRED_TOKENS, issues)
    _require(context, repo_root, RPG_MECHANIC_PARTS_NAME, RPG_MECHANIC_PARTS_REQUIRED_TOKENS, issues)
    _require(context, repo_root, RPG_PROGRESS_UNLOCKS_PART_README_NAME, RPG_PROGRESS_UNLOCKS_PART_REQUIRED_TOKENS, issues)
    _require(context, repo_root, RPG_MECHANIC_PROVENANCE_NAME, context.provenance_tokens, issues)
    _require(context, repo_root, RPG_MECHANIC_DECISION_NAME, RPG_MECHANIC_DECISION_REQUIRED_TOKENS, issues)
    _require(
        context,
        repo_root,
        RPG_PROGRESS_UNLOCKS_CONTRACT_DECISION_NAME,
        RPG_PROGRESS_UNLOCKS_CONTRACT_DECISION_REQUIRED_TOKENS,
        issues,
    )
    _require(
        context,
        repo_root,
        "docs/decisions/README.md",
        (
            RPG_PROGRESS_UNLOCKS_CONTRACT_DECISION_NAME,
            "RPG Progression-unlocks Contract",
        ),
        issues,
    )
    return issues
