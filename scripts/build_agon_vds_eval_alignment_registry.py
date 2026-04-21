from __future__ import annotations
import argparse,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CONFIG=ROOT/'config'/'agon_vds_eval_alignment.seed.json'
OUTPUT=ROOT/'generated'/'agon_vds_eval_alignment_registry.min.json'
def compact(o): return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n'
def build_registry():
    s=json.loads(CONFIG.read_text(encoding='utf-8'))
    return {'registry_id':s['registry_id'],'version':s['version'],'wave':s['wave'],'status':s['status'],'live_protocol':False,'runtime_effect':'none','alignment_count':len(s['alignments']),'alignments':s['alignments'],'stop_lines':s['stop_lines']}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--check',action='store_true'); args=ap.parse_args(); txt=compact(build_registry())
    if args.check:
        assert OUTPUT.exists(), f'missing {OUTPUT}'
        assert OUTPUT.read_text(encoding='utf-8')==txt, 'generated agon_vds_eval_alignment_registry.min.json is stale'
        print('agon_vds_eval_alignment_registry.min.json is up to date'); return 0
    OUTPUT.parent.mkdir(parents=True,exist_ok=True); OUTPUT.write_text(txt,encoding='utf-8'); print(f'wrote {OUTPUT}'); return 0
if __name__=='__main__': raise SystemExit(main())
