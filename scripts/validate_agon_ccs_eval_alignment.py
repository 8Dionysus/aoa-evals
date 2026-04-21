#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / 'config' / 'agon_ccs_eval_alignment.seed.json'
REGISTRY = ROOT / 'generated' / 'agon_ccs_eval_alignment_registry.min.json'
REQUIRED_PRECHECKS = {
    'agon.eval.contradiction_status_precheck',
    'agon.eval.closure_legality_precheck',
    'agon.eval.summon_intent_precheck',
}


def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))


def validate() -> None:
    seed = load(CONFIG)
    reg = load(REGISTRY)
    assert seed['live_protocol'] is False
    assert seed['runtime_effect'] == 'none'
    assert reg['live_protocol'] is False
    assert reg['runtime_effect'] == 'none'
    assert reg['alignment_count'] == len(seed['alignments'])
    prechecks = {a['eval_prebinding_id'] for a in seed['alignments']}
    assert REQUIRED_PRECHECKS <= prechecks, f'missing CCS prechecks: {sorted(REQUIRED_PRECHECKS - prechecks)}'
    for a in seed['alignments']:
        assert a['authority'].startswith('precheck_only'), a['alignment_id']
        assert a['center_law_ids'], a['alignment_id']
        assert a['law_family'] in {'contradiction', 'closure', 'summon'}, a['alignment_id']
    stop_text = json.dumps(seed['stop_lines'])
    assert 'no_live_verdict' in stop_text
    assert 'no_closure_grant' in stop_text
    assert 'no_live_summon' in stop_text


if __name__ == '__main__':
    validate()
    print('agon CCS eval alignments: ok')
