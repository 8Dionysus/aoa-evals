from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[1]


def load_module(script_name: str):
    path = REPO_ROOT / "scripts" / script_name
    spec = importlib.util.spec_from_file_location(script_name.replace(".py", ""), path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


publish_live_receipts = load_module("publish_live_receipts.py")


def test_publish_live_receipts_accepts_example_and_skips_duplicate_event_ids(tmp_path: Path) -> None:
    example_path = REPO_ROOT / "examples" / "eval_result_receipt.example.json"
    receipts = publish_live_receipts.load_receipts([example_path, example_path])
    log_path = tmp_path / "eval-result-receipts.jsonl"

    appended, skipped = publish_live_receipts.append_new_receipts(
        log_path=log_path,
        receipts=receipts,
    )

    assert appended == 1
    assert skipped == 1
    logged = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert [entry["event_id"] for entry in logged] == ["evr-bcq-2026-04-05-001"]


def test_publish_live_receipts_rejects_schema_invalid_payload(tmp_path: Path) -> None:
    example_path = REPO_ROOT / "examples" / "eval_result_receipt.example.json"
    payload = json.loads(example_path.read_text(encoding="utf-8"))
    del payload["payload"]["interpretation_bound"]
    bad_path = tmp_path / "bad-receipt.json"
    bad_path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(publish_live_receipts.ReceiptPublishError, match="interpretation_bound"):
        publish_live_receipts.load_receipts([bad_path])


def test_publish_live_receipts_rejects_malformed_jsonl_line(tmp_path: Path) -> None:
    malformed_path = tmp_path / "bad-receipts.jsonl"
    malformed_path.write_text("{\n", encoding="utf-8")

    with pytest.raises(publish_live_receipts.ReceiptPublishError, match="invalid JSON"):
        publish_live_receipts.load_receipts([malformed_path])
