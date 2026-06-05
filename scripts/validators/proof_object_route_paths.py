"""Proof-object route path constants."""

from __future__ import annotations


PROOF_OBJECT_MECHANIC_README_NAME = "mechanics/proof-object/README.md"
PROOF_OBJECT_MECHANIC_AGENTS_NAME = "mechanics/proof-object/AGENTS.md"
PROOF_OBJECT_MECHANIC_PARTS_NAME = "mechanics/proof-object/PARTS.md"
PROOF_OBJECT_MECHANIC_PROVENANCE_NAME = "mechanics/proof-object/PROVENANCE.md"
PROOF_OBJECT_PARTS_README_NAME = "mechanics/proof-object/parts/README.md"
PROOF_OBJECT_EVAL_AUTHORING_PART_README_NAME = (
    "mechanics/proof-object/parts/eval-authoring/README.md"
)
PROOF_OBJECT_EVAL_CONTRACTS_PART_README_NAME = (
    "mechanics/proof-object/parts/eval-contracts/README.md"
)
PROOF_OBJECT_MECHANIC_DECISION_NAME = "docs/decisions/AOA-EV-D-0010-proof-object-mechanic-package.md"
PROOF_OBJECT_CONTRACT_PART_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0048-proof-object-contract-parts.md"
)
PROOF_OBJECT_PART_OWNER_SPLIT_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0069-proof-object-part-owner-split-contract.md"
)
PROOF_OBJECT_EVAL_PART_NAMES_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0105-proof-object-eval-part-names.md"
)


__all__ = tuple(name for name in globals() if name.startswith("PROOF_OBJECT_"))
