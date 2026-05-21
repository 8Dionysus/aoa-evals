from __future__ import annotations
import json, pathlib, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
GENERATED = ROOT / 'generated/agon_sophian_eval_alignment_registry.min.json'
SCRIPT = ROOT / 'scripts/build_agon_sophian_eval_alignment_registry.py'
EXPECTED_COUNT = 7
ITEM_KEY = 'sophian_eval_alignments'

def test_generated_registry_shape():
    reg = json.loads(GENERATED.read_text(encoding='utf-8'))
    assert reg['wave'] == 'XVIII'
    assert reg['count'] == EXPECTED_COUNT
    assert len(reg[ITEM_KEY]) == EXPECTED_COUNT
    assert all(item.get('live_protocol') is False for item in reg[ITEM_KEY])
    assert all(item.get('review_status') == 'candidate_only' for item in reg[ITEM_KEY])

def test_builder_check():
    result = subprocess.run([sys.executable, str(SCRIPT), '--check'], cwd=str(ROOT), text=True, capture_output=True)
    assert result.returncode == 0, result.stderr
