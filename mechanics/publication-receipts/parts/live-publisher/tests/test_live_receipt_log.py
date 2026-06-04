from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[5]
SCRIPTS_DIR = REPO_ROOT / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from validators import publication_receipts as publication_receipts_validator

EXAMPLE_RECEIPT_PATH = (
    REPO_ROOT
    / "mechanics"
    / "publication-receipts"
    / "parts"
    / "receipt-payload"
    / "examples"
    / "eval_result_receipt.example.json"
)


def load_example_receipt() -> dict:
    return json.loads(EXAMPLE_RECEIPT_PATH.read_text(encoding="utf-8"))


def write_receipt_log(repo_root: Path, entries: list[dict]) -> None:
    log_path = repo_root / ".aoa" / "live_receipts" / "eval-result-receipts.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(
        "\n".join(json.dumps(entry) for entry in entries) + "\n",
        encoding="utf-8",
    )


def validate_live_receipt_log(repo_root: Path):
    return publication_receipts_validator.validate_live_receipt_log(
        repo_root,
        fallback_repo_root=REPO_ROOT,
        repo_ref_roots={"aoa-evals": REPO_ROOT},
        strict_sibling_compat=False,
    )


def test_validate_live_receipt_log_accepts_example_entry(tmp_path: Path) -> None:
    write_receipt_log(tmp_path, [load_example_receipt()])

    assert validate_live_receipt_log(tmp_path) == []


def test_validate_live_receipt_log_flags_duplicate_ids_and_missing_primary_refs(tmp_path: Path) -> None:
    first = load_example_receipt()
    second = load_example_receipt()
    second["evidence_refs"] = [
        {
            "kind": "bundle_report",
            "ref": second["payload"]["report_ref"],
        },
        {
            "kind": "bundle_contract",
            "ref": second["payload"]["bundle_ref"],
            "role": "verdict-meaning",
        },
    ]
    write_receipt_log(tmp_path, [first, second])

    issues = validate_live_receipt_log(tmp_path)
    messages = [issue.message for issue in issues]

    assert any("duplicate event_id 'evr-bcq-2026-04-05-001'" in message for message in messages)
    assert any("must include one primary evidence ref" in message for message in messages)


@pytest.mark.parametrize(
    "observed_at",
    [
        "not-a-date-time",
        "2026-05-17",
        "2026-05-17 12:00:00",
        "2026-05-17T12:00:00",
    ],
)
def test_validate_live_receipt_log_enforces_datetime_format(
    tmp_path: Path,
    observed_at: str,
) -> None:
    receipt = load_example_receipt()
    receipt["observed_at"] = observed_at
    write_receipt_log(tmp_path, [receipt])

    issues = validate_live_receipt_log(tmp_path)

    assert any("date-time" in issue.message for issue in issues)


@pytest.mark.parametrize(
    "observed_at",
    ["2026-05-17t12:00:00z", "2026-05-17t12:00:00Z"],
)
def test_validate_live_receipt_log_accepts_lowercase_rfc3339_designators(
    tmp_path: Path,
    observed_at: str,
) -> None:
    receipt = load_example_receipt()
    receipt["observed_at"] = observed_at
    write_receipt_log(tmp_path, [receipt])

    issues = validate_live_receipt_log(tmp_path)

    assert not any("date-time" in issue.message for issue in issues)
