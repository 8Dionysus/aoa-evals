from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "bundles" / "aoa-experience-certification-gate-integrity"


def _load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    start = text.index("---\n") + 4
    end = text.index("\n---\n", start)
    import yaml

    return yaml.safe_load(text[start:end])


def _load_yaml(path: Path) -> object:
    import yaml

    return yaml.safe_load(path.read_text(encoding="utf-8"))


def test_certification_gate_integrity_example_validates() -> None:
    schema = _load_json(BUNDLE / "reports" / "summary.schema.json")
    report = _load_json(BUNDLE / "reports" / "example-report.json")
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(report)


def test_certification_gate_integrity_eval_metadata_matches() -> None:
    meta = _load_yaml(BUNDLE / "eval.yaml")
    frontmatter = _load_frontmatter(BUNDLE / "EVAL.md")

    assert meta["name"] == frontmatter["name"]
    assert meta["category"] == frontmatter["category"]
    assert meta["status"] == frontmatter["status"]
    assert meta["object_under_evaluation"] == frontmatter["object_under_evaluation"]


def test_certification_gate_integrity_does_not_certify() -> None:
    report = _load_json(BUNDLE / "reports" / "example-report.json")
    assert isinstance(report, dict)
    assert report["authority_ceiling"] == "bounded_eval_not_certification"
    assert report["verdict"] != "certified"
