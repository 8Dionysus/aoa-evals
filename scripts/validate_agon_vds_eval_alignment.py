from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "generated" / "agon_vds_eval_alignment_registry.min.json"


def fail(message: str) -> int:
    print(message, file=sys.stderr)
    return 1


def validate():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if data.get("registry_id") != "agon.vds_eval_alignment.registry.v1":
        return fail("wrong registry_id")
    if data.get("wave") != "XI":
        return fail("wave must be XI")
    if data.get("live_protocol") is not False:
        return fail("live_protocol must be false")
    if data.get("runtime_effect") != "none":
        return fail("runtime_effect must be none")

    alignments = data.get("alignments", [])
    if data.get("alignment_count") != len(alignments):
        return fail("alignment_count mismatch")

    for item in alignments:
        alignment_id = item.get("alignment_id", "<missing>")
        if not item.get("must_not_emit"):
            return fail(f"{alignment_id} missing must_not_emit")
        if item.get("may_emit") is None:
            return fail(f"{alignment_id} missing may_emit")

    stop_lines = set(data.get("stop_lines", []))
    for required in {"no_live_verdict", "no_closure_grant"}:
        if required not in stop_lines:
            return fail(f"missing stop-line {required}")

    return data


if __name__ == "__main__":
    result = validate()
    if isinstance(result, int):
        raise SystemExit(result)
    print(f"validated {result['alignment_count']} VDS eval alignments")
