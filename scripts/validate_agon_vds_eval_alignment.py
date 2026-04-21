from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REGISTRY=ROOT/'generated'/'agon_vds_eval_alignment_registry.min.json'
def validate():
    d=json.loads(REGISTRY.read_text(encoding='utf-8'))
    assert d['registry_id']=='agon.vds_eval_alignment.registry.v1'
    assert d['wave']=='XI' and d['live_protocol'] is False and d['runtime_effect']=='none'
    assert d['alignment_count']>=5
    ids=[]
    for item in d['alignments']:
        assert item.get('must_not_emit')
        assert item.get('may_emit') is not None

    assert 'no_live_verdict' in d['stop_lines']
    assert 'no_closure_grant' in d['stop_lines']
    return d
if __name__=='__main__':
    d=validate(); print('validated {count} VDS eval alignments'.format(count=d['alignment_count']))
