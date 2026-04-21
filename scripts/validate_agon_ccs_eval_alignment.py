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


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate():
    seed = load(CONFIG)
    reg = load(REGISTRY)
    require(seed.get("live_protocol") is False, "seed live_protocol must be false")
    require(seed.get("runtime_effect") == "none", "seed runtime_effect must be none")
    require(
        reg.get("live_protocol") is False, "registry live_protocol must be false"
    )
    require(reg.get("runtime_effect") == "none", "registry runtime_effect must be none")
    require(
        reg.get("alignment_count") == len(seed.get("alignments", [])),
        "alignment_count mismatch",
    )

    prechecks = {alignment["eval_prebinding_id"] for alignment in seed["alignments"]}
    missing_prechecks = sorted(REQUIRED_PRECHECKS - prechecks)
    require(not missing_prechecks, f"missing CCS prechecks: {missing_prechecks}")

    for alignment in seed["alignments"]:
        alignment_id = alignment["alignment_id"]
        require(
            alignment["authority"].startswith("precheck_only"),
            f"{alignment_id} must stay precheck_only",
        )
        require(
            bool(alignment["center_law_ids"]),
            f"{alignment_id} must declare center_law_ids",
        )
        require(
            alignment["law_family"] in {"contradiction", "closure", "summon"},
            f"{alignment_id} has invalid law_family",
        )

    stop_lines = set(seed["stop_lines"])
    for required in {"no_live_verdict", "no_closure_grant", "no_live_summon"}:
        require(required in stop_lines, f"missing stop-line {required}")

    return reg


def main() -> int:
    try:
        validate()
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print("agon CCS eval alignments: ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
