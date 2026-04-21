import json
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


def _load_script(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_ccs_eval_alignment_registry_is_current():
    builder = _load_script(ROOT / 'scripts' / 'build_agon_ccs_eval_alignment_registry.py')
    seed = builder.load_json(ROOT / 'config' / 'agon_ccs_eval_alignment.seed.json')
    assert builder.load_json(ROOT / 'generated' / 'agon_ccs_eval_alignment_registry.min.json') == builder.build(seed)


def test_ccs_eval_alignment_validates():
    validator = _load_script(ROOT / 'scripts' / 'validate_agon_ccs_eval_alignment.py')
    validator.validate()


def test_ccs_eval_alignment_validate_raises_on_invalid_stop_line(tmp_path: Path):
    validator = _load_script(ROOT / "scripts" / "validate_agon_ccs_eval_alignment.py")
    seed = json.loads((ROOT / "config" / "agon_ccs_eval_alignment.seed.json").read_text(encoding="utf-8"))
    registry = json.loads((ROOT / "generated" / "agon_ccs_eval_alignment_registry.min.json").read_text(encoding="utf-8"))
    seed["stop_lines"] = [
        item for item in seed["stop_lines"] if item != "no_live_verdict"
    ]

    seed_path = tmp_path / "agon_ccs_eval_alignment.seed.json"
    registry_path = tmp_path / "agon_ccs_eval_alignment_registry.min.json"
    seed_path.write_text(json.dumps(seed), encoding="utf-8")
    registry_path.write_text(json.dumps(registry), encoding="utf-8")
    validator.CONFIG = seed_path
    validator.REGISTRY = registry_path

    with pytest.raises(ValueError, match="missing stop-line no_live_verdict"):
        validator.validate()
