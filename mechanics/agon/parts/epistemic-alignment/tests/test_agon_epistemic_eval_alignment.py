from __future__ import annotations
import json, pathlib, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]

def test_generated_registry_shape():
    reg = json.loads((ROOT / 'generated/agon_epistemic_eval_alignment_registry.min.json').read_text(encoding='utf-8'))
    assert reg['wave'] == 'XV'
    assert reg['runtime_posture'] in ('candidate_only', 'pre_protocol_candidate_only')
    assert reg['count'] == 8
    assert len(reg['alignments']) == 8
    for item in reg['alignments']:
        assert item['live_protocol'] is False
        assert 'auto_doctrine_rewrite' in item.get('forbidden_effects', [])

def test_builder_check_and_validator():
    assert subprocess.run([sys.executable, str(ROOT / 'scripts/build_agon_epistemic_eval_alignment_registry.py'), '--check'], cwd=ROOT).returncode == 0
    assert subprocess.run([sys.executable, str(ROOT / 'scripts/validate_agon_epistemic_eval_alignment.py')], cwd=ROOT).returncode == 0
