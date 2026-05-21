#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/agon_retention_rank_eval_alignment.seed.json"
OUTPUT = ROOT / "generated/agon_retention_rank_eval_alignment_registry.min.json"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_registry():
    seed = load_json(CONFIG)
    return {
        "registry_id": seed["registry_id"],
        "wave": seed["wave"],
        "status": seed.get("status", "seeded"),
        "live_protocol": seed["live_protocol"],
        "runtime_effect": seed["runtime_effect"],
        "entry_count": len(seed["entries"]),
        "entries": sorted(seed["entries"], key=lambda item: item["id"]),
        "stop_lines": seed.get("stop_lines", []),
        "source_config": "config/agon_retention_rank_eval_alignment.seed.json",
        "generated_note": "Generated from seed config. Review before integration into release checks."
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    registry = build_registry()
    text = json.dumps(registry, ensure_ascii=False, separators=(",", ":"), sort_keys=True) + "\n"
    if args.check:
        if not OUTPUT.exists():
            raise SystemExit(f"missing generated registry: {OUTPUT}")
        current = OUTPUT.read_text(encoding="utf-8")
        if current != text:
            raise SystemExit(f"generated registry drift: {OUTPUT}")
        print(f"ok: {OUTPUT.relative_to(ROOT)}")
        return 0
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
