"""Release-support report verification command constants."""

from __future__ import annotations

LEGACY_NAMING_SINGLE_BRIDGE_LANGUAGE_COMMAND = (
    "python -m pytest -q tests/test_root_surface_roles.py -k legacy_naming_single_bridge_language"
)
ACTIVE_LEGACY_PARENT_WORDING_COMMAND = (
    "python -m pytest -q tests/test_mechanic_legacy_archive_routes.py -k active_legacy_parent_wording"
)
ACTIVE_MECHANIC_ROUTE_RESIDUE_COMMAND = (
    "python -m pytest -q tests/test_route_residue.py -k active_mechanic_route_residue"
)
ROOT_AUTHORED_ROUTE_RESIDUE_COMMAND = (
    "python -m pytest -q tests/test_route_residue.py -k root_authored_route_residue"
)
DECISION_ROUTE_RESIDUE_COMMAND = (
    "python -m pytest -q tests/test_route_residue.py -k decision_route_residue"
)
REPO_CONFIG_ROUTE_RESIDUE_COMMAND = (
    "python -m pytest -q tests/test_route_residue.py -k repo_config_route_residue"
)
SOURCE_BUNDLE_ROUTE_RESIDUE_COMMAND = (
    "python -m pytest -q tests/test_route_residue.py -k source_bundle_route_residue"
)
MECHANIC_PAYLOAD_ROUTE_RESIDUE_COMMAND = (
    "python -m pytest -q tests/test_route_residue.py -k mechanic_payload_route_residue"
)
MECHANIC_PART_PAYLOAD_INVENTORY_COMMAND = (
    "python -m pytest -q tests/test_mechanic_part_contracts.py -k mechanic_part_payload_inventory"
)
MECHANIC_PART_VALIDATION_COMMAND_COMMAND = (
    "python -m pytest -q tests/test_mechanic_part_validation_commands.py -k mechanic_part_validation_command"
)
MECHANIC_PARTS_INDEX_SYNC_COMMAND = (
    "python -m pytest -q tests/test_mechanic_parts_index.py -k mechanic_parts_index_sync"
)
MECHANIC_LEGACY_SINGLE_BRIDGE_COMMAND = (
    "python -m pytest -q tests/test_mechanic_legacy_bridge.py -k mechanic_legacy_single_bridge"
)
MECHANIC_PROVENANCE_BRIDGE_POSTURE_COMMAND = (
    "python -m pytest -q tests/test_mechanic_legacy_bridge.py -k mechanic_provenance_bridge_posture"
)
MECHANIC_PARENT_DIRECTION_COMMAND = (
    "python -m pytest -q tests/test_mechanic_parent_direction.py -k mechanic_parent_direction"
)
MECHANIC_EVIDENCE_DIMENSION_LEDGER_COMMAND = (
    "python -m pytest -q tests/test_mechanic_evidence_ledger.py -k mechanic_evidence_dimension"
)
MECHANIC_ROOT_DISTRICT_RECON_COMMAND = (
    "python -m pytest -q tests/test_mechanic_root_district_recon.py -k mechanic_root_district_recon"
)
ROOT_AUTHORED_SURFACE_CLASSIFICATION_COMMAND = "python -m pytest -q tests/test_mechanics_topology.py"


__all__ = tuple(name for name in globals() if name.endswith("_COMMAND"))
