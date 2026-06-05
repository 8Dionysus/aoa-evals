"""Mechanic part validation-command token constants."""

from __future__ import annotations


MECHANIC_PART_VALIDATION_COMMAND_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0087-mechanic-part-validation-command-reachability.md"
)
MECHANIC_PART_VALIDATION_COMMAND_OWNERSHIP_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0102-mechanic-part-validation-command-ownership.md"
)
MECHANIC_PART_VALIDATION_COMMAND_COMMAND = (
    "python -m pytest -q tests/test_mechanic_part_validation_commands.py -k mechanic_part_validation_command"
)
MECHANIC_PART_VALIDATION_COMMAND_DECISION_REQUIRED_TOKENS = (
    "Mechanic Part Validation Command Reachability",
    "`## Validation`",
    "`mechanics/<parent>/parts/<part>/README.md`",
    "python command",
    "reachable path",
    "payload coverage anchor",
    "naked route-wide command",
    "stale validation path",
    "Current Applicability",
    "Review Log",
    "Previous assumption",
    "New reality",
    "Source surfaces updated",
    "mechanics/AGENTS.md#validation",
    "focused mechanic part validation-command guard",
)
MECHANIC_PART_VALIDATION_COMMAND_OWNERSHIP_DECISION_REQUIRED_TOKENS = (
    "Mechanic Part Validation Command Ownership",
    "`mechanics/<parent>/parts/<part>/README.md`",
    "`mechanics/<parent>/parts/<part>/VALIDATION.md`",
    "`mechanics/<parent>/parts/AGENTS.md`",
    "mechanic index surfaces",
    "centralized child validation",
    "python command",
    "payload coverage anchor",
    "stale validation path",
    "Current Applicability",
    "Review Log",
    "validation route",
    "README files remain contract maps",
    "nearest `AGENTS.md`",
)


__all__ = (
    "MECHANIC_PART_VALIDATION_COMMAND_COMMAND",
    "MECHANIC_PART_VALIDATION_COMMAND_DECISION_NAME",
    "MECHANIC_PART_VALIDATION_COMMAND_DECISION_REQUIRED_TOKENS",
    "MECHANIC_PART_VALIDATION_COMMAND_OWNERSHIP_DECISION_NAME",
    "MECHANIC_PART_VALIDATION_COMMAND_OWNERSHIP_DECISION_REQUIRED_TOKENS",
)
