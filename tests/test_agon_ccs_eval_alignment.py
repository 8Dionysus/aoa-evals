import importlib.util
from pathlib import Path

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
