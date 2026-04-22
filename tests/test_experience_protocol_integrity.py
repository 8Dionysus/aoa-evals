from __future__ import annotations

import json
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
BUNDLE = ROOT / "bundles" / "aoa-experience-protocol-integrity"


def _load_json(relative_path: Path) -> object:
    return json.loads(relative_path.read_text(encoding="utf-8"))


def _load_frontmatter(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    start = text.index("---\n") + 4
    end = text.index("\n---\n", start)
    import yaml

    return yaml.safe_load(text[start:end])


def _load_yaml(relative_path: Path) -> object:
    import yaml

    return yaml.safe_load(relative_path.read_text(encoding="utf-8"))


def test_experience_protocol_integrity_example_validates() -> None:
    schema = _load_json(BUNDLE / "reports" / "summary.schema.json")
    report = _load_json(BUNDLE / "reports" / "example-report.json")
    Draft202012Validator.check_schema(schema)
    Draft202012Validator(schema).validate(report)


def test_experience_protocol_integrity_eval_metadata_matches() -> None:
    meta = _load_yaml(BUNDLE / "eval.yaml")
    frontmatter = _load_frontmatter(BUNDLE / "EVAL.md")

    assert meta["name"] == frontmatter["name"]
    assert meta["category"] == frontmatter["category"]
    assert meta["status"] == frontmatter["status"]
    assert meta["object_under_evaluation"] == frontmatter["object_under_evaluation"]
