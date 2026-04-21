from __future__ import annotations
import importlib.util, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]

def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

def test_build_count_and_digest():
    mod = load('builder', 'scripts/build_agon_mechanical_trial_eval_suites.py')
    reg = mod.build()
    assert reg['count'] == 7
    assert reg['digest']
    assert reg['runtime_posture'] in ('candidate_only', 'pre_protocol_candidate_only', 'local_dry_run_candidate_only')

def test_validator_green():
    mod = load('validator', 'scripts/validate_agon_mechanical_trial_eval_suites.py')
    assert mod.main() == 0

def test_validator_rejects_stale_generated_registry(tmp_path):
    validator = load('validator', 'scripts/validate_agon_mechanical_trial_eval_suites.py')
    builder = load('builder', 'scripts/build_agon_mechanical_trial_eval_suites.py')
    stale = builder.build()
    stale['digest'] = '0' * 64
    out = tmp_path / 'agon_mechanical_trial_eval_suite_registry.min.json'
    out.write_text(json.dumps(stale), encoding='utf-8')
    validator.OUT = out
    assert validator.main() == 1
