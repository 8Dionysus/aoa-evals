from __future__ import annotations
import importlib.util, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def load(p):
    spec=importlib.util.spec_from_file_location(p.stem,p); m=importlib.util.module_from_spec(spec); assert spec.loader; spec.loader.exec_module(m); return m
def test_registry_build_clean():
    r=subprocess.run([sys.executable,str(ROOT/'scripts'/'build_agon_vds_eval_alignment_registry.py'),'--check'],cwd=ROOT,text=True,capture_output=True)
    assert r.returncode==0, r.stdout+r.stderr
def test_registry_validates():
    d=load(ROOT/'scripts'/'validate_agon_vds_eval_alignment.py').validate()
    assert d['alignment_count']>=5
