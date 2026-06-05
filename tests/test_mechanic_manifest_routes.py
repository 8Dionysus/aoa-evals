from __future__ import annotations

import sys
import textwrap
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validators import route_residue_mechanic_payload as route_residue_mechanic_payload_validator


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")


def test_mechanic_manifest_path_globs_reject_unresolved_root_docs_glob(
    tmp_path: Path,
) -> None:
    write_text(
        tmp_path
        / "mechanics"
        / "agon"
        / "parts"
        / "court-prebinding"
        / "manifests"
        / "recurrence"
        / "component.demo.json",
        '{\n  "observation_inputs": [\n    {"path_globs": ["docs/AGON_*.md"]}\n  ]\n}\n',
    )

    issues = route_residue_mechanic_payload_validator.validate_mechanic_manifest_path_glob_routes(tmp_path)

    assert any(
        issue.location
        == "mechanics/agon/parts/court-prebinding/manifests/recurrence/component.demo.json"
        and "unresolved root-authored docs globs" in issue.message
        for issue in issues
    )


def test_mechanic_manifest_route_fields_reject_root_schema_payload(
    tmp_path: Path,
) -> None:
    write_text(
        tmp_path
        / "mechanics"
        / "agon"
        / "parts"
        / "sophian-threshold-alignment"
        / "manifests"
        / "recurrence"
        / "component.demo.json",
        '{\n  "observed_surfaces": [\n    "schemas/agon-sophian-eval-alignment.schema.json"\n  ]\n}\n',
    )

    issues = route_residue_mechanic_payload_validator.validate_mechanic_manifest_path_glob_routes(tmp_path)

    assert any(
        issue.location
        == "mechanics/agon/parts/sophian-threshold-alignment/manifests/recurrence/component.demo.json"
        and "route-card-only root district payload `schemas/agon-sophian-eval-alignment.schema.json`"
        in issue.message
        for issue in issues
    )
