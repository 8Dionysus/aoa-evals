from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def load(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader
    spec.loader.exec_module(module)
    return module


def test_registry_build_clean():
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "build_agon_vds_eval_alignment_registry.py"), "--check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_registry_validates():
    data = load(ROOT / "scripts" / "validate_agon_vds_eval_alignment.py").validate()
    assert data["alignment_count"] >= 5


def test_registry_validate_rejects_too_few_alignments(tmp_path: Path):
    validator = load(ROOT / "scripts" / "validate_agon_vds_eval_alignment.py")
    data = json.loads(
        (ROOT / "generated" / "agon_vds_eval_alignment_registry.min.json").read_text(
            encoding="utf-8"
        )
    )
    data["alignments"] = data["alignments"][:4]
    data["alignment_count"] = 4

    registry_path = tmp_path / "agon_vds_eval_alignment_registry.min.json"
    registry_path.write_text(json.dumps(data), encoding="utf-8")
    validator.REGISTRY = registry_path

    with pytest.raises(ValueError, match="alignment_count must remain >= 5"):
        validator.validate()
