from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "generated" / "agon_vds_eval_alignment_registry.min.json"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate():
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    require(data.get("registry_id") == "agon.vds_eval_alignment.registry.v1", "wrong registry_id")
    require(data.get("wave") == "XI", "wave must be XI")
    require(data.get("live_protocol") is False, "live_protocol must be false")
    require(data.get("runtime_effect") == "none", "runtime_effect must be none")

    alignments = data.get("alignments", [])
    require(len(alignments) >= 5, "alignment_count must remain >= 5")
    require(data.get("alignment_count") == len(alignments), "alignment_count mismatch")

    for item in alignments:
        alignment_id = item.get("alignment_id", "<missing>")
        require(bool(item.get("must_not_emit")), f"{alignment_id} missing must_not_emit")
        require(item.get("may_emit") is not None, f"{alignment_id} missing may_emit")

    stop_lines = set(data.get("stop_lines", []))
    for required in {"no_live_verdict", "no_closure_grant"}:
        require(required in stop_lines, f"missing stop-line {required}")

    return data


def main() -> int:
    try:
        result = validate()
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"validated {result['alignment_count']} VDS eval alignments")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
