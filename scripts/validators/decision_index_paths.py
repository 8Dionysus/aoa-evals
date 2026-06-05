"""Decision-lane path constants for source records and generated indexes."""

from __future__ import annotations

import re
from pathlib import Path


DECISIONS_DIR = Path("docs/decisions")
INDEXES_DIR = DECISIONS_DIR / "indexes"
INDEX_CONTRACT_PATH = INDEXES_DIR / "index_contract.yaml"
GENERATED_INDEX_PATHS = (
    INDEXES_DIR / "README.md",
    INDEXES_DIR / "by-number.md",
    INDEXES_DIR / "by-date.md",
    INDEXES_DIR / "by-surface.md",
    INDEXES_DIR / "by-mechanic.md",
    INDEXES_DIR / "by-validation-guard.md",
)
DECISION_ROOT_FILENAMES = {"AGENTS.md", "README.md", "TEMPLATE.md"}
FULL_ID_FILENAME_RE = re.compile(r"^(AOA-EV-D-(\d{4}))-.+\.md$")


__all__ = (
    "DECISION_ROOT_FILENAMES",
    "DECISIONS_DIR",
    "FULL_ID_FILENAME_RE",
    "GENERATED_INDEX_PATHS",
    "INDEXES_DIR",
    "INDEX_CONTRACT_PATH",
)
