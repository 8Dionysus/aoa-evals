from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[5]
PUBLISHER_PATH = (
    REPO_ROOT
    / "mechanics"
    / "publication-receipts"
    / "parts"
    / "live-publisher"
    / "scripts"
    / "publish_live_receipts.py"
)
EXAMPLE_RECEIPT_PATH = (
    REPO_ROOT
    / "mechanics"
    / "publication-receipts"
    / "parts"
    / "receipt-payload"
    / "examples"
    / "eval_result_receipt.example.json"
)


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load module from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


publish_live_receipts = load_module(PUBLISHER_PATH)


def test_publish_live_receipts_accepts_example_and_skips_duplicate_event_ids(tmp_path: Path) -> None:
    receipts = publish_live_receipts.load_receipts([EXAMPLE_RECEIPT_PATH, EXAMPLE_RECEIPT_PATH])
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
    payload = json.loads(EXAMPLE_RECEIPT_PATH.read_text(encoding="utf-8"))
    del payload["payload"]["interpretation_bound"]
    bad_path = tmp_path / "bad-receipt.json"
    bad_path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(publish_live_receipts.ReceiptPublishError, match="interpretation_bound"):
        publish_live_receipts.load_receipts([bad_path])


@pytest.mark.parametrize("observed_at", ["2026-05-17", "2026-05-17T12:00:00"])
def test_publish_live_receipts_rejects_non_rfc3339_datetimes(
    tmp_path: Path, observed_at: str
) -> None:
    payload = json.loads(EXAMPLE_RECEIPT_PATH.read_text(encoding="utf-8"))
    payload["observed_at"] = observed_at
    bad_path = tmp_path / "bad-receipt.json"
    bad_path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(publish_live_receipts.ReceiptPublishError, match="date-time"):
        publish_live_receipts.load_receipts([bad_path])


@pytest.mark.parametrize("observed_at", ["2026-05-17t12:00:00z", "2026-05-17t12:00:00Z"])
def test_publish_live_receipts_accepts_lowercase_rfc3339_designators(
    tmp_path: Path, observed_at: str
) -> None:
    payload = json.loads(EXAMPLE_RECEIPT_PATH.read_text(encoding="utf-8"))
    payload["observed_at"] = observed_at
    input_path = tmp_path / "receipt.json"
    input_path.write_text(json.dumps(payload), encoding="utf-8")

    receipts = publish_live_receipts.load_receipts([input_path])

    assert receipts[0]["observed_at"] == observed_at


def test_publish_live_receipts_rejects_malformed_jsonl_line(tmp_path: Path) -> None:
    malformed_path = tmp_path / "bad-receipts.jsonl"
    malformed_path.write_text("{\n", encoding="utf-8")

    with pytest.raises(publish_live_receipts.ReceiptPublishError, match="invalid JSON"):
        publish_live_receipts.load_receipts([malformed_path])
