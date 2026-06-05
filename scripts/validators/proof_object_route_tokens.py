"""Proof-object route token constants."""

from __future__ import annotations


MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS = (
    "`PROVENANCE.md` is the active-to-archive bridge for this mechanic.",
    "Use active surfaces first:",
    "DIRECTION.md",
    "PARTS.md",
    "parts/",
    "legacy archive",
    "legacy/README.md",
    "owns its own details",
    "archive details stay in the legacy archive",
)
PROOF_OBJECT_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "evals/**/EVAL.md",
    "evals/**/eval.yaml",
    "mechanics/proof-object/PARTS.md",
    "mechanics/proof-object/PROVENANCE.md",
    "mechanics/proof-object/parts/eval-authoring/templates/EVAL.template.md",
    "mechanics/proof-object/parts/eval-contracts/schemas/eval-frontmatter.schema.json",
    "mechanics/proof-object/parts/eval-contracts/schemas/eval-manifest.schema.json",
    "generated/eval_catalog.min.json",
    "generated/eval_capsules.json",
    "generated/eval_sections.full.json",
    "proof-object completeness review",
    "bundle-local review",
    "Source eval packages stay under `evals/`",
    "python scripts/build_catalog.py --check",
    "AGENTS.md#validation",
)
PROOF_OBJECT_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "source proof objects",
    "evals/**/EVAL.md",
    "evals/**/eval.yaml",
    "mechanics/proof-object/PARTS.md",
    "mechanics/proof-object/PROVENANCE.md",
    "EVAL.md and eval.yaml",
    "eval-local support artifacts",
    "python scripts/build_catalog.py --check",
)
PROOF_OBJECT_MECHANIC_PARTS_REQUIRED_TOKENS = (
    "eval-authoring",
    "eval-contracts",
    "mechanics/proof-object/parts/eval-authoring/templates/EVAL.template.md",
    "mechanics/proof-object/parts/eval-contracts/schemas/eval-frontmatter.schema.json",
    "mechanics/proof-object/parts/eval-contracts/schemas/eval-manifest.schema.json",
    "Source eval packages stay under `evals/`",
    "AGENTS.md#validation",
)
PROOF_OBJECT_PARTS_README_REQUIRED_TOKENS = (
    "## Operating Card",
    "lower index for proof-object authoring and contract support parts",
    "source eval bundle for proof meaning",
    "source `evals/**/EVAL.md` and `evals/**/eval.yaml`",
    "## Part Admission Route",
    "`eval-authoring/`",
    "`eval-contracts/`",
    "stronger-owner split",
    "mechanics/proof-object/AGENTS.md#validation",
    "generated-reader check",
    "generated-reader freshness checks",
)
PROOF_OBJECT_PARTS_README_FORBIDDEN_TOKENS = (
    "They do not own source eval meaning and do not replace generated readers",
)
PROOF_OBJECT_EVAL_AUTHORING_PART_REQUIRED_TOKENS = (
    "Eval Authoring",
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "mechanics/proof-object/parts/eval-authoring/templates/EVAL.template.md",
    "evals/**/EVAL.md",
    "evals/**/eval.yaml",
    "actual source proof",
    "template",
    "doctrine or accepted proof meaning",
    "sibling refs outrank source eval packages",
    "python scripts/build_catalog.py --check",
)
PROOF_OBJECT_EVAL_CONTRACTS_PART_REQUIRED_TOKENS = (
    "Eval Contracts",
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "mechanics/proof-object/parts/eval-contracts/schemas/eval-frontmatter.schema.json",
    "mechanics/proof-object/parts/eval-contracts/schemas/eval-manifest.schema.json",
    "evals/**/EVAL.md",
    "evals/**/eval.yaml",
    "schema-backed contract validation",
    "claim invention",
    "schema acceptance reads as eval-local review",
    "python scripts/build_catalog.py --check",
)
PROOF_OBJECT_MECHANIC_PROVENANCE_REQUIRED_TOKENS = MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
PROOF_OBJECT_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/proof-object/",
    "evals/**/EVAL.md",
    "evals/**/eval.yaml",
    "proof-object completeness review",
    "does not move `evals/`",
    "generated readers",
    "bundle-local review",
)
PROOF_OBJECT_CONTRACT_PART_DECISION_REQUIRED_TOKENS = (
    "mechanics/proof-object/parts/eval-authoring/templates/EVAL.template.md",
    "mechanics/proof-object/parts/eval-contracts/schemas/",
    "source bundles stay under `evals/`",
    "generated readers stay",
    "python scripts/validate_repo.py",
)
PROOF_OBJECT_PART_OWNER_SPLIT_DECISION_REQUIRED_TOKENS = (
    "Proof-object Part Owner-split Contract",
    "mechanics/proof-object/parts/eval-authoring/README.md",
    "mechanics/proof-object/parts/eval-contracts/README.md",
    "`## Stronger Owner Split`",
    "source proof object remains",
    "Source proof bundle meaning stays under `evals/`",
    "generated readers, reports, receipts, runtime candidates, sibling refs, quests",
    "Schema acceptance may prove metadata shape",
    "python -m pytest -q tests/test_mechanic_surface_contracts.py -k proof_object_part_owner_split",
)
PROOF_OBJECT_EVAL_PART_NAMES_DECISION_REQUIRED_TOKENS = (
    "Proof-object Eval Part Names",
    "bundle-authoring",
    "eval-authoring",
    "bundle-contracts",
    "eval-contracts",
    "active directory topology",
    "source eval packages into mechanics",
    "python scripts/validate_repo.py",
)


__all__ = tuple(name for name in globals() if name.endswith("_TOKENS"))
