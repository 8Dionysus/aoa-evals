#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "agon_ccs_eval_alignment.seed.json"
REGISTRY = ROOT / "generated" / "agon_ccs_eval_alignment_registry.min.json"
REQUIRED_PRECHECKS = {
    "agon.eval.contradiction_status_precheck",
    "agon.eval.closure_legality_precheck",
    "agon.eval.summon_intent_precheck",
}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def fail(message: str) -> int:
    print(message, file=sys.stderr)
    return 1


def validate() -> int:
    seed = load(CONFIG)
    reg = load(REGISTRY)
    if seed.get("live_protocol") is not False:
        return fail("seed live_protocol must be false")
    if seed.get("runtime_effect") != "none":
        return fail("seed runtime_effect must be none")
    if reg.get("live_protocol") is not False:
        return fail("registry live_protocol must be false")
    if reg.get("runtime_effect") != "none":
        return fail("registry runtime_effect must be none")
    if reg.get("alignment_count") != len(seed.get("alignments", [])):
        return fail("alignment_count mismatch")

    prechecks = {alignment["eval_prebinding_id"] for alignment in seed["alignments"]}
    missing_prechecks = sorted(REQUIRED_PRECHECKS - prechecks)
    if missing_prechecks:
        return fail(f"missing CCS prechecks: {missing_prechecks}")

    for alignment in seed["alignments"]:
        alignment_id = alignment["alignment_id"]
        if not alignment["authority"].startswith("precheck_only"):
            return fail(f"{alignment_id} must stay precheck_only")
        if not alignment["center_law_ids"]:
            return fail(f"{alignment_id} must declare center_law_ids")
        if alignment["law_family"] not in {"contradiction", "closure", "summon"}:
            return fail(f"{alignment_id} has invalid law_family")

    stop_lines = set(seed["stop_lines"])
    for required in {"no_live_verdict", "no_closure_grant", "no_live_summon"}:
        if required not in stop_lines:
            return fail(f"missing stop-line {required}")

    return 0


if __name__ == "__main__":
    raise SystemExit(validate() or print("agon CCS eval alignments: ok"))
