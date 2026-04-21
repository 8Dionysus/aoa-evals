from __future__ import annotations
import json, pathlib, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]

def test_wave17_registry_shape():
    reg = json.loads((ROOT / 'generated/agon_kag_eval_alignment_registry.min.json').read_text(encoding='utf-8'))
    assert reg['wave'] == 'XVII'
    assert reg['count'] == 7
    assert len(reg['eval_alignments']) == 7
    for item in reg['eval_alignments']:
        assert item['live_protocol'] is False
        assert 'no_kag_as_canon' in item.get('stop_lines', [])
        assert 'single_event_promotion' in item.get('forbidden_effects', [])
        assert item.get('canonical_status') not in ('canon', 'canonical', 'tree_of_sophia_canon')

def test_builder_check_and_validator():
    assert subprocess.run([sys.executable, str(ROOT / 'scripts/build_agon_kag_eval_alignment_registry.py'), '--check'], cwd=ROOT).returncode == 0
    assert subprocess.run([sys.executable, str(ROOT / 'scripts/validate_agon_kag_eval_alignment_registry.py')], cwd=ROOT).returncode == 0
