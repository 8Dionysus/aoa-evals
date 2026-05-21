from __future__ import annotations

import json
import pathlib
import subprocess
import sys

from jsonschema import Draft202012Validator

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / 'generated/agon_slc_eval_alignment_registry.min.json'
ITEM_KEY = 'eval_alignments'
EXPECTED_COUNT = 8
UNIQUE_KEY_FIELD = 'alignment_id'
REQUIRED_STOP_LINES = ['no_live_verdict_authority', 'no_durable_scar_write', 'no_retention_execution', 'no_rank_or_trust_mutation', 'no_tree_of_sophia_promotion', 'no_kag_promotion', 'no_hidden_scheduler_action', 'no_assistant_contestant_drift', 'no_auto_doctrine_rewrite', 'no_school_as_authority', 'no_lineage_as_canon', 'no_campaign_as_live_arena', 'no_center_takeover_of_owner_truth']
REQUIRED_FORBIDDEN = ['live_verdict_authority', 'durable_scar_write', 'retention_execution', 'rank_mutation', 'trust_mutation', 'tree_of_sophia_promotion', 'kag_promotion', 'hidden_scheduler_action', 'assistant_contestant_drift', 'auto_doctrine_rewrite', 'school_authority', 'lineage_canonization', 'live_campaign_arena']
ENTRY_SCHEMA = ROOT / 'schemas' / 'agon-slc-eval-alignment.schema.json'
REGISTRY_SCHEMA = ROOT / 'schemas' / 'agon-slc-eval-alignment-registry.schema.json'


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding='utf-8'))


def test_wave16_registry_shape():
    reg = load(OUT)
    assert reg['wave'] == 'XVI'
    assert reg['wave_name'] == 'Schools / Lineages / Campaigns'
    assert reg['runtime_posture'] == 'candidate_only'
    assert reg['count'] == EXPECTED_COUNT
    assert len(reg[ITEM_KEY]) == EXPECTED_COUNT
    assert len(reg['digest']) == 64
    keys = set()
    for item in reg[ITEM_KEY]:
        assert item['wave'] == 'XVI'
        assert item['live_protocol'] is False
        assert item['authority_posture'] == 'non_authority'
        assert item['review_status'] == 'candidate_only'
        assert item.get('assistant_contestant_allowed', False) is False
        assert set(REQUIRED_STOP_LINES) <= set(item['stop_lines'])
        assert set(REQUIRED_FORBIDDEN) <= set(item['forbidden_effects'])
        keys.add(item[UNIQUE_KEY_FIELD])
    assert len(keys) == EXPECTED_COUNT


def test_builder_check_and_validator():
    assert subprocess.run([sys.executable, str(ROOT / 'scripts' / 'build_agon_slc_eval_alignment_registry.py'), '--check'], cwd=ROOT).returncode == 0
    assert subprocess.run([sys.executable, str(ROOT / 'scripts' / 'validate_agon_slc_eval_alignment_registry.py')], cwd=ROOT).returncode == 0


def test_schemas_constrain_registry_and_entries():
    entry_schema = load(ENTRY_SCHEMA)
    registry_schema = load(REGISTRY_SCHEMA)
    entry_validator = Draft202012Validator(entry_schema)
    registry_validator = Draft202012Validator(registry_schema)
    reg = load(OUT)

    assert not entry_validator.is_valid({})
    assert not registry_validator.is_valid({})
    registry_validator.validate(reg)
    for item in reg[ITEM_KEY]:
        entry_validator.validate(item)

    bad_item = dict(reg[ITEM_KEY][0])
    bad_item['stop_lines'] = []
    assert not entry_validator.is_valid(bad_item)
    bad_item = dict(reg[ITEM_KEY][0])
    bad_item['live_protocol'] = 'false'
    assert not entry_validator.is_valid(bad_item)
