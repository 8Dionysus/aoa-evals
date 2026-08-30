"""Regression tests for the bounded code-observation refactor contract."""

import copy
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RUNNER = (
    ROOT
    / "evals/capability/aoa-code-observation-refactor-integrity/runners/run_scenarios.py"
)
EXAMPLE = (
    ROOT
    / "evals/capability/aoa-code-observation-refactor-integrity/fixtures/observation-report.example.json"
)
sys.path.insert(0, str(RUNNER.parent))
import run_scenarios as runner  # noqa: E402
import provider_agreement  # noqa: E402
import adjacent_provider_evidence  # noqa: E402
import provider_execution  # noqa: E402


AGREEMENT_SOURCE = b"export function render(): string { return 'fixture'; }\n"


def run_runner(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(RUNNER), *arguments],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def _agreement_envelope(provider_id: str, facts: list[str]) -> dict[str, object]:
    observations: list[dict[str, object]] = []
    for index, fact in enumerate(facts):
        kind, label = fact.split(":", 1)
        observations.append(
            {
                "capability_class": "code-structure",
                "observation_kind": "symbol" if kind == "definition" else "relation",
                "observation_id": f"{provider_id}:{index}",
                "semantic_key": f"typescript:{kind}:{label}",
                "subject": {
                    "label": label,
                    "qualified_name": label,
                    "symbol_id": f"typescript:{label}",
                    "symbol_kind": "function",
                },
                "occurrence": {
                    "start_line": 1,
                    "start_column": 1,
                    "end_line": 1,
                    "end_column": 6,
                },
                "confidence": {"evidence_class": "observed", "value": 1},
                "relation": None
                if kind == "definition"
                else {"kind": kind, "target_name": label},
            }
        )
    return {
        "schema_version": "aoa-code-observation-v1",
        "provider": {
            "id": provider_id,
            "version": "1.0.0",
            "config_digest": "0" * 64,
            "lane": {"id": provider_id, "status": "supplied_unadmitted"},
        },
        "source": {
            "repo": "fixture",
            "path": "src/render.ts",
            "source_epoch": "sha256:"
            + hashlib.sha256(AGREEMENT_SOURCE).hexdigest(),
            "content_digest": hashlib.sha256(AGREEMENT_SOURCE).hexdigest(),
            "language": "typescript",
        },
        "parse_status": "parsed",
        "observations": observations,
        "qualification": {"machine_admission": {"state": "not_admitted"}},
    }


def test_typescript_provider_agreement_requires_shared_source_and_facts(
    tmp_path: Path,
) -> None:
    facts = ["definition:render"]
    payload = {
        "schema_version": "aoa_code_observation_provider_agreement_v1",
        "observed_at": "2026-08-29T00:00:00Z",
        "required_facts": facts,
        "claim_boundary": provider_agreement.CLAIM_BOUNDARY,
        "envelopes": [
            _agreement_envelope(provider_id, facts)
            for provider_id in ("tree-sitter", "scip", "lsp")
        ],
    }
    source_path = tmp_path / "src" / "render.ts"
    source_path.parent.mkdir(parents=True)
    source_path.write_bytes(AGREEMENT_SOURCE)
    path = tmp_path / "agreement.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    result = provider_agreement.validate(path)
    assert result["issues"] == []
    assert result["verdict"] == "supports bounded cross-provider agreement"

    payload["envelopes"][2]["provider"]["lane"]["id"] = "tree-sitter"
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert "provider_lane_identity_mismatch:lsp" in provider_agreement.validate(
        path
    )["issues"]
    payload["envelopes"][2]["provider"]["lane"]["id"] = "lsp"

    payload["envelopes"][0]["observations"][0]["occurrence"]["start_line"] = True
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert "invalid_normalized_observation:tree-sitter:0:occurrence" in (
        provider_agreement.validate(path)["issues"]
    )
    payload["envelopes"][0]["observations"][0]["occurrence"]["start_line"] = 1

    payload["envelopes"][0]["observations"][0]["occurrence"]["start_line"] = 999
    payload["envelopes"][0]["observations"][0]["occurrence"]["end_line"] = 999
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert (
        "invalid_normalized_observation:tree-sitter:0:occurrence_source_bounds"
        in provider_agreement.validate(path)["issues"]
    )
    payload["envelopes"][0]["observations"][0]["occurrence"]["start_line"] = 1
    payload["envelopes"][0]["observations"][0]["occurrence"]["end_line"] = 1

    for envelope in payload["envelopes"]:
        envelope["source"]["source_epoch"] = "sha256:" + ("f" * 64)
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert "source_epoch_content_mismatch" in provider_agreement.validate(path)[
        "issues"
    ]
    expected_source_epoch = "sha256:" + hashlib.sha256(AGREEMENT_SOURCE).hexdigest()
    for envelope in payload["envelopes"]:
        envelope["source"]["source_epoch"] = expected_source_epoch

    payload["envelopes"][2]["source"]["source_epoch"] = "git:other"
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert "source_identity_mismatch" in provider_agreement.validate(path)["issues"]


def test_provider_agreement_rejects_duplicate_normalized_observations(
    tmp_path: Path,
) -> None:
    facts = ["definition:render"]
    payload = {
        "schema_version": "aoa_code_observation_provider_agreement_v1",
        "observed_at": "2026-08-29T00:00:00Z",
        "required_facts": facts,
        "claim_boundary": provider_agreement.CLAIM_BOUNDARY,
        "envelopes": [
            _agreement_envelope(provider_id, facts)
            for provider_id in ("tree-sitter", "scip", "lsp")
        ],
    }
    source_path = tmp_path / "src" / "render.ts"
    source_path.parent.mkdir(parents=True)
    source_path.write_bytes(AGREEMENT_SOURCE)
    path = tmp_path / "duplicate-agreement.json"

    duplicate_id_payload = copy.deepcopy(payload)
    duplicate_id_payload["envelopes"][0]["observations"].append(
        copy.deepcopy(duplicate_id_payload["envelopes"][0]["observations"][0])
    )
    path.write_text(json.dumps(duplicate_id_payload), encoding="utf-8")
    duplicate_id_issues = provider_agreement.validate(path)["issues"]
    assert "duplicate_observation_id:tree-sitter:tree-sitter:0" in duplicate_id_issues

    duplicate_occurrence_payload = copy.deepcopy(payload)
    duplicate_observation = copy.deepcopy(
        duplicate_occurrence_payload["envelopes"][0]["observations"][0]
    )
    duplicate_observation["observation_id"] = "tree-sitter:distinct"
    duplicate_occurrence_payload["envelopes"][0]["observations"].append(
        duplicate_observation
    )
    path.write_text(json.dumps(duplicate_occurrence_payload), encoding="utf-8")
    duplicate_occurrence_issues = provider_agreement.validate(path)["issues"]
    assert (
        "duplicate_semantic_occurrence:tree-sitter:typescript:definition:render"
        in duplicate_occurrence_issues
    )


def test_provider_agreement_rejects_conflicting_normalized_fact_identity(
    tmp_path: Path,
) -> None:
    facts = ["definition:render"]
    payload = {
        "schema_version": "aoa_code_observation_provider_agreement_v1",
        "observed_at": "2026-08-29T00:00:00Z",
        "required_facts": facts,
        "claim_boundary": provider_agreement.CLAIM_BOUNDARY,
        "envelopes": [
            _agreement_envelope(provider_id, facts)
            for provider_id in ("tree-sitter", "scip", "lsp")
        ],
    }
    source_path = tmp_path / "src" / "render.ts"
    source_path.parent.mkdir(parents=True)
    source_path.write_bytes(AGREEMENT_SOURCE)
    path = tmp_path / "conflicting-agreement.json"

    mutations = (
        lambda observation: observation.__setitem__(
            "semantic_key", "typescript:definition:other"
        ),
        lambda observation: observation["subject"].__setitem__(
            "qualified_name", "other.render"
        ),
        lambda observation: observation["subject"].__setitem__(
            "symbol_kind", "class"
        ),
        lambda observation: observation["occurrence"].__setitem__(
            "end_column", 7
        ),
    )
    for index, mutate in enumerate(mutations):
        candidate = copy.deepcopy(payload)
        mutate(candidate["envelopes"][1]["observations"][0])
        path.write_text(json.dumps(candidate), encoding="utf-8")
        issues = provider_agreement.validate(path)["issues"]
        assert "fact_normalized_identity_mismatch:definition:render" in issues, index


def test_provider_agreement_rejects_claim_boundary_drift(tmp_path: Path) -> None:
    facts = ["definition:render"]
    payload = {
        "schema_version": "aoa_code_observation_provider_agreement_v1",
        "observed_at": "2026-08-29T00:00:00Z",
        "required_facts": facts,
        "claim_boundary": "This envelope proves provider correctness and admission.",
        "envelopes": [
            _agreement_envelope(provider_id, facts)
            for provider_id in ("tree-sitter", "scip", "lsp")
        ],
    }
    path = tmp_path / "agreement-boundary-drift.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    source_path = tmp_path / "src" / "render.ts"
    source_path.parent.mkdir(parents=True)
    source_path.write_bytes(AGREEMENT_SOURCE)

    result = provider_agreement.validate(path)

    assert any("claim_boundary" in issue for issue in result["issues"])
    assert result["verdict"] == "does not support bounded cross-provider agreement"


def test_provider_agreement_rejects_source_digest_drift(tmp_path: Path) -> None:
    facts = ["definition:render"]
    payload = {
        "schema_version": "aoa_code_observation_provider_agreement_v1",
        "observed_at": "2026-08-29T00:00:00Z",
        "required_facts": facts,
        "claim_boundary": provider_agreement.CLAIM_BOUNDARY,
        "envelopes": [
            _agreement_envelope(provider_id, facts)
            for provider_id in ("tree-sitter", "scip", "lsp")
        ],
    }
    source_path = tmp_path / "src" / "render.ts"
    source_path.parent.mkdir(parents=True)
    source_path.write_bytes(AGREEMENT_SOURCE + b"// drift\n")
    path = tmp_path / "agreement-source-drift.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    result = provider_agreement.validate(path)

    assert "source_content_digest_mismatch" in result["issues"]


def test_adjacent_provider_evidence_requires_all_unadmitted_classes(
    tmp_path: Path,
) -> None:
    source_epoch = "commit:" + "a" * 40
    source_repo = "fixture"
    source_path = "fixture.py"
    source_contents = b"def fixture():\n    return 1\n"
    source_digest = "sha256:" + hashlib.sha256(source_contents).hexdigest()
    config_digest = "sha256:" + "0" * 64
    specs = {
        "static_security": ("semgrep", "static-security"),
        "software_components": ("syft", "software-components"),
        "artifact_provenance": ("in-toto", "artifact-provenance"),
        "document_structure": ("markitdown", "document-structure"),
    }
    batches = {}
    observation_specs = {
        "static_security": ("security_finding", "sarif:"),
        "software_components": ("software_component", "component:"),
        "artifact_provenance": ("artifact_subject", "provenance:"),
        "document_structure": ("heading", "document:"),
    }
    for key, (provider_id, capability) in specs.items():
        symbol_kind, semantic_prefix = observation_specs[key]
        semantic_key = {
            "static_security": "sarif:0:0:fixture",
            "software_components": "component:0:fixture@1.0.0",
            "artifact_provenance": "provenance:subject:0:fixture",
            "document_structure": (
                "document:0:heading:"
                + hashlib.sha256(b"fixture").hexdigest()[:16]
            ),
        }[key]
        qualified_name = {
            "software_components": "fixture@1.0.0",
            "document_structure": "fixture#0",
        }.get(key, "fixture")
        batches[key] = {
            "schema_version": "aoa-code-observation-v1",
            "capability_class": capability,
            "provider": {
                "id": provider_id,
                "version": "1.0.0",
                "config_digest": config_digest,
                "lane": {"id": provider_id, "status": "supplied_unadmitted"},
            },
            "currentness": {
                "provider": {
                    "id": provider_id,
                    "version": "1.0.0",
                    "config_digest": config_digest,
                }
            },
            "provenance": {
                "extractor_ref": f"fixture:{provider_id}@1.0.0#{config_digest}",
                "parser_ref": f"{provider_id}@1.0.0#{config_digest}",
                "source_refs": [
                    {
                        "repo": source_repo,
                        "path": source_path,
                        "role": "primary_source",
                        "content_digest": source_digest,
                    }
                ],
            },
            "source": {
                "repo": source_repo,
                "path": source_path,
                "source_epoch": source_epoch,
                "content_digest": source_digest,
            },
            "parse_status": "parsed",
            "observations": [
                {
                    "capability_class": capability,
                    "observation_kind": "symbol",
                    "observation_id": f"{provider_id}:0",
                    "semantic_key": semantic_key,
                    "subject": {
                        "label": "fixture",
                        "qualified_name": qualified_name,
                        "symbol_id": semantic_prefix + "fixture",
                        "symbol_kind": symbol_kind,
                    },
                    "occurrence": {
                        "start_line": 1,
                        "start_column": 1,
                        "end_line": 1,
                        "end_column": 1,
                    },
                    "confidence": {"evidence_class": "observed", "value": 1},
                    "relation": None,
                }
            ],
            "qualification": {"machine_admission": {"state": "not_admitted"}},
        }
    payload = {
        "schema": "abyssos_adjacent_provider_evidence_v1",
        "goal_id": "fixture",
        "observed_at": "2026-08-29T00:00:00Z",
        "source_epoch": source_epoch,
        "artifact": {
            "sha256": source_digest,
            "subject_digest": "sha256:" + "2" * 64,
            "signature_status": "missing",
            "admission_status": "not_admitted",
        },
        "providers": {
            provider_id: {"version": "1.0.0", "runtime_posture": "candidate_unadmitted"}
            for provider_id, _capability in specs.values()
        },
        "raw_evidence": {
            "sarif": {"path": "sarif.json", "sha256": "sha256:" + "1" * 64},
            "sbom": {"path": "sbom.json", "sha256": "sha256:" + "2" * 64},
            "in_toto": {"path": "provenance.jsonl", "sha256": "sha256:" + "3" * 64},
            "document_markdown": {
                "path": "document.md",
                "sha256": "sha256:" + "4" * 64,
            },
        },
        "batches": batches,
        "summary": {"all_provider_lanes_unadmitted": True},
        "claim_limits": adjacent_provider_evidence.CLAIM_LIMITS,
    }
    raw_contents = {
        "sarif": json.dumps(
            {
                "version": "2.1.0",
                "runs": [
                    {
                        "tool": {
                            "driver": {
                                "name": "Semgrep OSS",
                                "semanticVersion": "1.0.0",
                            }
                        },
                        "results": [
                            {
                                "ruleId": "fixture",
                                "message": {"text": "fixture"},
                                "locations": [
                                    {
                                        "physicalLocation": {
                                            "artifactLocation": {"uri": "fixture.py"},
                                            "region": {
                                                "startLine": 1,
                                                "startColumn": 1,
                                                "endLine": 1,
                                                "endColumn": 1,
                                            },
                                        }
                                    }
                                ],
                            }
                        ],
                    }
                ],
            }
        ).encode(),
        "sbom": json.dumps(
            {
                "bomFormat": "CycloneDX",
                "specVersion": "1.6",
                "metadata": {
                    "tools": {
                        "components": [{"name": "syft", "version": "1.0.0"}]
                    }
                },
                "components": [
                    {"type": "library", "name": "fixture", "version": "1.0.0"}
                ],
            }
        ).encode(),
        "in_toto": (
            json.dumps(
                {
                    "_type": "https://in-toto.io/Statement/v1",
                    "predicateType": "https://slsa.dev/provenance/v1",
                    "subject": [
                        {
                            "name": "fixture",
                            "digest": {
                                "sha256": source_digest.removeprefix("sha256:")
                            },
                        }
                    ],
                    "predicate": {
                        "buildDefinition": {
                            "runDetails": {
                                "byproducts": [
                                    {
                                        "name": "artifact.subjects.json",
                                        "digest": {"sha256": "2" * 64},
                                    }
                                ]
                            }
                        }
                    },
                }
            )
            + "\n"
        ).encode(),
        "document_markdown": b"# fixture\n",
    }
    for key, contents in raw_contents.items():
        raw_path = tmp_path / payload["raw_evidence"][key]["path"]
        raw_path.write_bytes(contents)
        payload["raw_evidence"][key]["sha256"] = (
            "sha256:" + hashlib.sha256(contents).hexdigest()
        )
    (tmp_path / source_path).write_bytes(source_contents)
    path = tmp_path / "adjacent.json"
    path.write_text(json.dumps(payload), encoding="utf-8")
    result = adjacent_provider_evidence.validate(path)
    assert result["issues"] == []
    assert result["verdict"] == "supports bounded adjacent-provider envelope evidence"

    source_file = tmp_path / source_path
    source_file.write_bytes(b"def fixture():\n    return 2\n")
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert "source_content_digest_mismatch:semgrep" in (
        adjacent_provider_evidence.validate(path)["issues"]
    )
    source_file.write_bytes(source_contents)

    out_of_bounds_payload = copy.deepcopy(payload)
    for observation in out_of_bounds_payload["batches"]["software_components"][
        "observations"
    ]:
        observation["occurrence"]["start_line"] = 999
        observation["occurrence"]["end_line"] = 999
    path.write_text(json.dumps(out_of_bounds_payload), encoding="utf-8")
    occurrence_issues = adjacent_provider_evidence.validate(path)["issues"]
    assert "source_occurrence_bounds:syft:0" in occurrence_issues

    # An epoch is only one part of the identity. A relabelled batch must not
    # pass when its repository/path or content digest disagrees with the raw
    # and provenance witnesses.
    original_source = copy.deepcopy(payload["batches"]["static_security"]["source"])
    payload["batches"]["static_security"]["source"]["path"] = "unrelated.py"
    path.write_text(json.dumps(payload), encoding="utf-8")
    source_issues = adjacent_provider_evidence.validate(path)["issues"]
    assert "source_provenance_identity_mismatch:semgrep" in source_issues
    assert "raw_evidence_content_mismatch:sarif:source:0" in source_issues
    payload["batches"]["static_security"]["source"] = original_source

    payload["batches"]["artifact_provenance"]["source"]["content_digest"] = (
        "sha256:" + "9" * 64
    )
    path.write_text(json.dumps(payload), encoding="utf-8")
    digest_issues = adjacent_provider_evidence.validate(path)["issues"]
    assert "source_provenance_identity_mismatch:in-toto" in digest_issues
    assert "raw_evidence_content_mismatch:in_toto:subject_identity:0" in digest_issues
    payload["batches"]["artifact_provenance"]["source"] = copy.deepcopy(
        original_source
    )

    original_repo = payload["batches"]["software_components"]["source"]["repo"]
    payload["batches"]["software_components"]["source"]["repo"] = "unrelated-repo"
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert "source_provenance_identity_mismatch:syft" in (
        adjacent_provider_evidence.validate(path)["issues"]
    )
    payload["batches"]["software_components"]["source"]["repo"] = original_repo

    payload["batches"]["document_structure"]["provenance"]["source_refs"][0][
        "path"
    ] = "unrelated.py"
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert "source_provenance_identity_mismatch:markitdown" in (
        adjacent_provider_evidence.validate(path)["issues"]
    )
    payload["batches"]["document_structure"]["provenance"]["source_refs"][0][
        "path"
    ] = source_path

    missing_source_field = payload["batches"]["software_components"]["source"].pop(
        "content_digest"
    )
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert any(
        issue.startswith("schema:batches/software_components/source")
        for issue in adjacent_provider_evidence.validate(path)["issues"]
    )
    payload["batches"]["software_components"]["source"][
        "content_digest"
    ] = missing_source_field

    original_raw_evidence = copy.deepcopy(payload["raw_evidence"])

    raw_paths = {
        key: tmp_path / payload["raw_evidence"][key]["path"]
        for key in raw_contents
    }
    original_raw_contents = {
        key: raw_path.read_bytes() for key, raw_path in raw_paths.items()
    }
    sarif = json.loads(original_raw_contents["sarif"])
    sarif["runs"][0]["results"][0]["ruleId"] = "other"
    raw_paths["sarif"].write_text(json.dumps(sarif), encoding="utf-8")
    payload["raw_evidence"]["sarif"]["sha256"] = (
        "sha256:" + hashlib.sha256(raw_paths["sarif"].read_bytes()).hexdigest()
    )
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert "raw_evidence_content_mismatch:sarif:result_identity:0" in (
        adjacent_provider_evidence.validate(path)["issues"]
    )
    raw_paths["sarif"].write_bytes(original_raw_contents["sarif"])
    payload["raw_evidence"]["sarif"]["sha256"] = original_raw_evidence["sarif"][
        "sha256"
    ]

    sarif = json.loads(original_raw_contents["sarif"])
    sarif["runs"][0]["tool"]["driver"]["name"] = "Unrelated scanner"
    raw_paths["sarif"].write_text(json.dumps(sarif), encoding="utf-8")
    payload["raw_evidence"]["sarif"]["sha256"] = (
        "sha256:" + hashlib.sha256(raw_paths["sarif"].read_bytes()).hexdigest()
    )
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert "raw_evidence_content_mismatch:sarif:tool_identity:0" in (
        adjacent_provider_evidence.validate(path)["issues"]
    )
    raw_paths["sarif"].write_bytes(original_raw_contents["sarif"])
    payload["raw_evidence"]["sarif"]["sha256"] = original_raw_evidence["sarif"][
        "sha256"
    ]

    sbom = json.loads(original_raw_contents["sbom"])
    sbom["components"][0]["version"] = "9.9.9"
    raw_paths["sbom"].write_text(json.dumps(sbom), encoding="utf-8")
    payload["raw_evidence"]["sbom"]["sha256"] = (
        "sha256:" + hashlib.sha256(raw_paths["sbom"].read_bytes()).hexdigest()
    )
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert "raw_evidence_content_mismatch:sbom:component_identity:0" in (
        adjacent_provider_evidence.validate(path)["issues"]
    )
    raw_paths["sbom"].write_bytes(original_raw_contents["sbom"])
    payload["raw_evidence"]["sbom"]["sha256"] = original_raw_evidence["sbom"][
        "sha256"
    ]

    in_toto = json.loads(original_raw_contents["in_toto"])
    in_toto["subject"][0]["name"] = "other"
    raw_paths["in_toto"].write_text(json.dumps(in_toto) + "\n", encoding="utf-8")
    payload["raw_evidence"]["in_toto"]["sha256"] = (
        "sha256:" + hashlib.sha256(raw_paths["in_toto"].read_bytes()).hexdigest()
    )
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert "raw_evidence_content_mismatch:in_toto:subject_identity:0" in (
        adjacent_provider_evidence.validate(path)["issues"]
    )
    raw_paths["in_toto"].write_bytes(original_raw_contents["in_toto"])
    payload["raw_evidence"]["in_toto"]["sha256"] = original_raw_evidence["in_toto"][
        "sha256"
    ]

    raw_paths["document_markdown"].write_text("# other\n", encoding="utf-8")
    payload["raw_evidence"]["document_markdown"]["sha256"] = (
        "sha256:"
        + hashlib.sha256(raw_paths["document_markdown"].read_bytes()).hexdigest()
    )
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert "raw_evidence_content_mismatch:document_markdown:heading_identity:0" in (
        adjacent_provider_evidence.validate(path)["issues"]
    )
    raw_paths["document_markdown"].write_bytes(original_raw_contents["document_markdown"])
    payload["raw_evidence"]["document_markdown"]["sha256"] = original_raw_evidence[
        "document_markdown"
    ]["sha256"]

    payload["batches"]["document_structure"]["observations"][0]["subject"][
        "symbol_kind"
    ] = "paragraph"
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert "raw_evidence_content_mismatch:document_markdown:heading_identity:0" in (
        adjacent_provider_evidence.validate(path)["issues"]
    )
    payload["batches"]["document_structure"]["observations"][0]["subject"][
        "symbol_kind"
    ] = "heading"

    original_semgrep_version = payload["providers"]["semgrep"]["version"]
    payload["providers"]["semgrep"]["version"] = "0"
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert "provider_version_mismatch:semgrep" in adjacent_provider_evidence.validate(
        path
    )["issues"]
    payload["providers"]["semgrep"]["version"] = original_semgrep_version

    original_runtime_posture = payload["providers"]["semgrep"]["runtime_posture"]
    payload["providers"]["semgrep"]["runtime_posture"] = "deployed_and_admitted"
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert "provider_runtime_posture_mismatch:semgrep" in (
        adjacent_provider_evidence.validate(path)["issues"]
    )
    payload["providers"]["semgrep"]["runtime_posture"] = original_runtime_posture

    original_extractor_ref = payload["batches"]["static_security"]["provenance"][
        "extractor_ref"
    ]
    payload["batches"]["static_security"]["provenance"]["extractor_ref"] = (
        f"fixture:semgrep@1.0.0#{'1' * 64}"
    )
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert "provider_execution_extractor_ref_mismatch:semgrep" in (
        adjacent_provider_evidence.validate(path)["issues"]
    )
    payload["batches"]["static_security"]["provenance"][
        "extractor_ref"
    ] = original_extractor_ref

    original_parser_ref = payload["batches"]["static_security"]["provenance"][
        "parser_ref"
    ]
    payload["batches"]["static_security"]["provenance"]["parser_ref"] = (
        f"semgrep@9.9.9#{config_digest}"
    )
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert "provider_execution_parser_ref_mismatch:semgrep" in (
        adjacent_provider_evidence.validate(path)["issues"]
    )
    payload["batches"]["static_security"]["provenance"]["parser_ref"] = (
        original_parser_ref
    )

    payload["batches"]["static_security"]["observations"][0]["occurrence"][
        "start_line"
    ] = True
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert "invalid_observation:semgrep:0:occurrence" in (
        adjacent_provider_evidence.validate(path)["issues"]
    )
    payload["batches"]["static_security"]["observations"][0]["occurrence"][
        "start_line"
    ] = 1

    duplicate_observation = copy.deepcopy(
        payload["batches"]["static_security"]["observations"][0]
    )
    payload["batches"]["static_security"]["observations"].append(
        duplicate_observation
    )
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert "duplicate_observation_id:semgrep:semgrep:0" in (
        adjacent_provider_evidence.validate(path)["issues"]
    )
    payload["batches"]["static_security"]["observations"].pop()

    provider_metadata = payload["providers"]
    payload["providers"] = {}
    path.write_text(json.dumps(payload), encoding="utf-8")
    result = adjacent_provider_evidence.validate(path)
    assert any(issue.startswith("schema:providers") for issue in result["issues"])
    payload["providers"] = provider_metadata

    raw_evidence = copy.deepcopy(payload["raw_evidence"])
    original_raw_evidence = copy.deepcopy(raw_evidence)
    payload["raw_evidence"] = {}
    path.write_text(json.dumps(payload), encoding="utf-8")
    result = adjacent_provider_evidence.validate(path)
    assert any(issue.startswith("schema:raw_evidence") for issue in result["issues"])
    payload["raw_evidence"] = raw_evidence

    payload["raw_evidence"]["sarif"]["sha256"] = "sha256:" + "f" * 64
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert "raw_evidence_digest_mismatch:sarif" in adjacent_provider_evidence.validate(
        path
    )["issues"]
    payload["raw_evidence"]["sarif"]["sha256"] = original_raw_evidence["sarif"][
        "sha256"
    ]
    payload["raw_evidence"]["sarif"]["path"] = "../outside.sarif"
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert "raw_evidence_path_unsafe:sarif" in adjacent_provider_evidence.validate(
        path
    )["issues"]
    payload["raw_evidence"]["sarif"]["path"] = original_raw_evidence["sarif"][
        "path"
    ]

    (tmp_path / original_raw_evidence["sarif"]["path"]).unlink()
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert "raw_evidence_file_missing:sarif" in adjacent_provider_evidence.validate(
        path
    )["issues"]

    payload["claim_limits"] = ["This packet proves provider correctness."] * 3
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert any(
        "claim_limits" in issue
        for issue in adjacent_provider_evidence.validate(path)["issues"]
    )

    payload["claim_limits"] = adjacent_provider_evidence.CLAIM_LIMITS
    payload["batches"]["static_security"]["qualification"]["machine_admission"][
        "state"
    ] = "admitted"
    path.write_text(json.dumps(payload), encoding="utf-8")
    assert (
        "provider_not_bounded:semgrep"
        in adjacent_provider_evidence.validate(path)["issues"]
    )


def test_example_observation_report_supports_all_cases() -> None:
    result = run_runner("run-scenarios")
    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    assert summary["scenario_count"] == 12
    assert summary["passed_count"] == 12
    assert summary["failed_count"] == 0
    assert summary["verdict"] == "supports bounded contract"


def test_report_rejects_unbound_source_epoch_identity(tmp_path: Path) -> None:
    for field, value in (
        ("repository", "untrusted-repository"),
        ("digest", "sha256:" + "0" * 64),
    ):
        report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        report["source_epoch"][field] = value
        path = tmp_path / f"source-epoch-{field}-drift.json"
        path.write_text(json.dumps(report), encoding="utf-8")

        result = run_runner("validate-report", str(path))

        assert result.returncode == 1
        assert any(
            error.startswith("source_epoch_identity_mismatch:")
            for error in json.loads(result.stdout)["errors"]
        )


def test_operation_drift_is_rejected(tmp_path: Path) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    report["observations"][0]["operation"] = "delete"
    mutated = tmp_path / "operation-drift.json"
    mutated.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(mutated))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any(
        "operation_mismatch:rename-symbol" in error for error in payload["errors"]
    )


def test_fixture_manifest_is_digest_bound() -> None:
    result = run_runner("validate-fixture")
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["family_id"] == "refactor-torture-v1"
    assert payload["case_count"] == 12
    assert payload["fixture_digest"].startswith("sha256:")


def test_unexpected_case_is_counted_and_summary_remains_schema_valid(
    tmp_path: Path,
) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    unexpected = copy.deepcopy(report["observations"][0])
    unexpected["case_id"] = "unexpected-thirteenth-case"
    report["observations"].append(unexpected)
    mutated = tmp_path / "unexpected-case.json"
    mutated.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("run-scenarios", str(mutated))

    assert result.returncode == 1
    assert "summary validation failed" not in result.stderr
    summary = json.loads(result.stdout)
    assert summary["scenario_count"] == 13
    assert summary["passed_count"] == 12
    assert summary["failed_count"] == 1
    unexpected_summary = next(
        item
        for item in summary["per_scenario_breakdown"]
        if item["case_id"] == "observation-12-unexpected-thirteenth-case"
    )
    assert unexpected_summary["expected"] == "reject"
    assert unexpected_summary["observed"] == "reject"
    assert unexpected_summary["outcome"] == "fail"
    assert any(
        "unexpected_case:unexpected-thirteenth-case" in code
        for code in unexpected_summary["issue_codes"]
    )


def test_positive_summary_requires_canonical_passing_breakdown() -> None:
    result = run_runner("run-scenarios")
    assert result.returncode == 0, result.stderr
    summary = json.loads(result.stdout)
    schema = runner.load_json(runner.SUMMARY_SCHEMA_PATH)

    mutations = (
        (
            "failed-outcome",
            lambda value: value["per_scenario_breakdown"][0].update(outcome="fail"),
        ),
        (
            "extra-entry",
            lambda value: value["per_scenario_breakdown"].append(
                copy.deepcopy(value["per_scenario_breakdown"][0])
            ),
        ),
        (
            "non-canonical-id",
            lambda value: value["per_scenario_breakdown"][0].update(
                case_id="unexpected-case"
            ),
        ),
    )
    for _name, mutate in mutations:
        mutated = copy.deepcopy(summary)
        mutate(mutated)
        errors = runner.schema_errors(mutated, schema, "summary")
        assert any("summary:per_scenario_breakdown" in error for error in errors)


def test_affected_test_selection_must_match_fixture_oracle(tmp_path: Path) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    report["observations"][0]["affected_tests"]["selected"] = [
        "tests/not-the-alpha-test.py"
    ]
    mutated = tmp_path / "affected-test-selection-drift.json"
    mutated.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(mutated))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any(
        "affected_tests_selection_mismatch:rename-symbol" in error
        for error in payload["errors"]
    )


def test_non_applicable_affected_tests_require_empty_evidence(tmp_path: Path) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    affected_tests = report["observations"][3]["affected_tests"]
    affected_tests["status"] = "selected"
    affected_tests["selected"] = ["tests/invented.py"]
    affected_tests["oracle_ref"] = "fixture://invented-oracle"
    path = tmp_path / "non-applicable-affected-tests.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(path))

    assert result.returncode == 1
    errors = json.loads(result.stdout)["errors"]
    assert "affected_tests_not_applicable_status:add-entity" in errors
    assert "affected_tests_not_applicable_selection:add-entity" in errors
    assert "affected_tests_not_applicable_oracle:add-entity" in errors


def test_affected_test_oracle_must_be_repo_local(tmp_path: Path) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    report["observations"][0]["affected_tests"]["oracle_ref"] = (
        "https://example.invalid/oracle"
    )
    mutated = tmp_path / "nonlocal-affected-test-oracle.json"
    mutated.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(mutated))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any(
        "affected_tests_oracle_mismatch:rename-symbol" in error
        for error in payload["errors"]
    )


def test_report_rejects_partial_evidence_and_uncertain_preserved_lineage(
    tmp_path: Path,
) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    observation = report["observations"][0]
    observation["evidence_state"] = "partial"
    observation["lineage"]["confidence"] = 0.2
    observation["lineage"]["alternatives"] = 1
    path = tmp_path / "partial-lineage.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(path))

    assert result.returncode == 1
    errors = json.loads(result.stdout)["errors"]
    assert any("evidence_state_mismatch:rename-symbol" in error for error in errors)
    assert any(
        "preserved_lineage_not_certain:rename-symbol" in error for error in errors
    )


def test_report_binds_semantic_identity_to_unique_local_case_paths(
    tmp_path: Path,
) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    first = report["observations"][0]["semantic_identity"]["entities"][0]
    first["occurrences"][0].update(
        {"path": "../outside.py", "start_line": 8, "end_line": 2}
    )
    report["observations"][1]["semantic_identity"]["entities"][0]["semantic_id"] = (
        first["semantic_id"]
    )
    report["observations"][2]["semantic_identity"]["entities"][0]["occurrences"][0][
        "end_line"
    ] = 1
    path = tmp_path / "identity-drift.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(path))

    assert result.returncode == 1
    errors = json.loads(result.stdout)["errors"]
    assert any("semantic_identity_path:rename-symbol" in error for error in errors)
    assert any("semantic_identity_range:rename-symbol" in error for error in errors)
    assert any("semantic_identity_mismatch:move-symbol" in error for error in errors)
    assert any("semantic_identity_duplicate:move-symbol" in error for error in errors)
    assert any(
        "semantic_identity_occurrence:signature-change" in error for error in errors
    )


def test_report_rejects_invented_relation_identity(tmp_path: Path) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    relation = report["observations"][6]["semantic_identity"]["entities"][0][
        "relations"
    ][0]
    relation["target"] = "fixture:invented-target"
    path = tmp_path / "relation-drift.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(path))

    assert result.returncode == 1
    assert any(
        "semantic_relation_mismatch:multi-file-impact:fixture:eta.symbol" in error
        for error in json.loads(result.stdout)["errors"]
    )


def test_report_rejects_duplicate_metric_declarations(tmp_path: Path) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    report["observations"][0]["metrics"].append(
        copy.deepcopy(report["observations"][0]["metrics"][0])
    )
    path = tmp_path / "duplicate-metric.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(path))

    assert result.returncode == 1
    assert any(
        "duplicate_metric:rename-symbol:definitions_references" in error
        for error in json.loads(result.stdout)["errors"]
    )


def test_report_rejects_invalid_optional_metric_values_and_units(
    tmp_path: Path,
) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    report["observations"][0]["metrics"].append(
        {
            "metric_id": "latency",
            "value": -99,
            "unit": "bogus",
            "status": "observed",
        }
    )
    path = tmp_path / "optional-metric-drift.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(path))

    assert result.returncode == 1
    errors = json.loads(result.stdout)["errors"]
    assert "metric_unit:rename-symbol:latency:bogus" in errors
    assert "metric_range:rename-symbol:latency" in errors


def test_report_rejects_source_provenance_drift(tmp_path: Path) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    report["observations"][0]["provenance"]["source_ref"] = (
        "fixture://unrelated-source"
    )
    path = tmp_path / "source-provenance-drift.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(path))

    assert result.returncode == 1
    assert any(
        "source_provenance_mismatch:rename-symbol" in error
        for error in json.loads(result.stdout)["errors"]
    )


def test_report_rejects_inflated_branch_count_and_inconsistent_confidence(
    tmp_path: Path,
) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    lineage = report["observations"][7]["lineage"]
    lineage["alternatives"] = 100
    lineage["confidence"] = 0.01
    path = tmp_path / "inflated-lineage.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(path))

    assert result.returncode == 1
    assert any(
        "lineage_ambiguity_mismatch:split-symbol" in error
        for error in json.loads(result.stdout)["errors"]
    )


def test_report_rejects_missing_lineage_alternative_occurrence(
    tmp_path: Path,
) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    report["observations"][7]["semantic_identity"]["entities"][0][
        "occurrences"
    ].pop()
    path = tmp_path / "missing-lineage-alternative.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(path))

    assert result.returncode == 1
    assert any(
        "lineage_alternative_occurrences:split-symbol" in error
        for error in json.loads(result.stdout)["errors"]
    )


def test_report_rejects_split_merge_lineage_without_both_snapshots(
    tmp_path: Path,
) -> None:
    missing_snapshots = {
        "split-symbol": "before",
        "merge-symbol": "after",
    }
    for case_id, missing_snapshot in missing_snapshots.items():
        report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        observation = next(
            item for item in report["observations"] if item["case_id"] == case_id
        )
        for entity in observation["semantic_identity"]["entities"]:
            entity["occurrences"][:] = [
                occurrence
                for occurrence in entity["occurrences"]
                if occurrence["snapshot"] != missing_snapshot
            ]
        path = tmp_path / f"missing-branched-lineage-{case_id}.json"
        path.write_text(json.dumps(report), encoding="utf-8")

        result = run_runner("validate-report", str(path))

        assert result.returncode == 1
        errors = json.loads(result.stdout)["errors"]
        assert f"lineage_alternative_occurrences:{case_id}" in errors


def test_report_rejects_preserved_lineage_without_both_snapshots(
    tmp_path: Path,
) -> None:
    for case_id in (
        "rename-symbol",
        "move-symbol",
        "signature-change",
        "import-change",
        "multi-file-impact",
        "stale-index",
    ):
        report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        observation = next(
            item for item in report["observations"] if item["case_id"] == case_id
        )
        for entity in observation["semantic_identity"]["entities"]:
            entity["occurrences"][:] = [
                occurrence
                for occurrence in entity["occurrences"]
                if occurrence["snapshot"] == "after"
            ]
        path = tmp_path / f"missing-preserved-lineage-{case_id}.json"
        path.write_text(json.dumps(report), encoding="utf-8")

        result = run_runner("validate-report", str(path))

        assert result.returncode == 1
        errors = json.loads(result.stdout)["errors"]
        assert any(
            f"preserved_lineage_snapshots:{case_id}" in error for error in errors
        )


def test_report_rejects_duplicate_semantic_occurrence(tmp_path: Path) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    occurrences = report["observations"][0]["semantic_identity"]["entities"][0][
        "occurrences"
    ]
    occurrences.append(copy.deepcopy(occurrences[0]))
    path = tmp_path / "duplicate-semantic-occurrence.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(path))

    assert result.returncode == 1
    assert "semantic_identity_duplicate_occurrence:rename-symbol:fixture:alpha.symbol" in json.loads(
        result.stdout
    )["errors"]


def test_report_rejects_duplicate_semantic_identity(tmp_path: Path) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    entities = report["observations"][0]["semantic_identity"]["entities"]
    entities.append(copy.deepcopy(entities[0]))
    path = tmp_path / "duplicate-semantic-identity.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(path))

    assert result.returncode == 1
    errors = json.loads(result.stdout)["errors"]
    assert "semantic_identity_duplicate_id:rename-symbol:fixture:alpha.symbol" in errors


def test_report_rejects_non_finite_preserved_lineage_confidence(
    tmp_path: Path,
) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    report["observations"][0]["lineage"]["confidence"] = float("nan")
    path = tmp_path / "non-finite-lineage-confidence.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(path))

    assert result.returncode == 1
    assert any(
        "preserved_lineage_not_certain:rename-symbol" in error
        for error in json.loads(result.stdout)["errors"]
    )


def test_report_rejects_uncertain_not_applicable_lineage(tmp_path: Path) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    lineage = report["observations"][3]["lineage"]
    lineage["alternatives"] = 2
    lineage["confidence"] = 0.5
    path = tmp_path / "not-applicable-lineage.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(path))

    assert result.returncode == 1
    errors = json.loads(result.stdout)["errors"]
    assert any(
        "lineage_not_applicable_uncertain:add-entity" in error for error in errors
    )


def test_report_rejects_unbounded_invalidation_and_metric_drift(tmp_path: Path) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    observation = report["observations"][0]
    observation["invalidation"]["affected_paths"] = ["src/alpha.py", "../outside.py"]
    observation["invalidation"]["recomputed_paths"] = ["src/not-alpha.py"]
    observation["metrics"][0]["unit"] = "ratio"
    observation["metrics"][0]["value"] = -1
    path = tmp_path / "invalidation-metric-drift.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(path))

    assert result.returncode == 1
    errors = json.loads(result.stdout)["errors"]
    assert any("invalidation_path:rename-symbol" in error for error in errors)
    assert any(
        "invalidation_recompute_scope:rename-symbol" in error for error in errors
    )
    assert any(
        "metric_unit:rename-symbol:definitions_references" in error for error in errors
    )
    assert any(
        "metric_range:rename-symbol:definitions_references" in error for error in errors
    )


def test_report_rejects_invalidation_subset_even_when_paths_are_valid(
    tmp_path: Path,
) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    invalidation = report["observations"][6]["invalidation"]
    invalidation["affected_paths"] = ["src/eta.py"]
    invalidation["recomputed_paths"] = ["src/eta.py"]
    path = tmp_path / "invalidation-subset.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(path))

    assert result.returncode == 1
    errors = json.loads(result.stdout)["errors"]
    assert "invalidation_affected_paths_mismatch:multi-file-impact" in errors
    assert "invalidation_recomputed_paths_mismatch:multi-file-impact" in errors


def test_report_rejects_duplicate_invalidation_paths(tmp_path: Path) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    invalidation = report["observations"][0]["invalidation"]
    invalidation["affected_paths"] = ["src/alpha.py", "src/alpha.py"]
    invalidation["recomputed_paths"] = ["src/alpha.py", "src/alpha.py"]
    path = tmp_path / "duplicate-invalidation-paths.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(path))

    assert result.returncode == 1
    errors = json.loads(result.stdout)["errors"]
    assert "invalidation_duplicate_paths:rename-symbol:affected" in errors
    assert "invalidation_duplicate_paths:rename-symbol:recomputed" in errors


def test_report_rejects_reused_artifact_count_drift(tmp_path: Path) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    report["observations"][0]["invalidation"]["reused_artifacts"] = 999
    path = tmp_path / "reused-artifact-count-drift.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(path))

    assert result.returncode == 1
    assert "invalidation_reused_artifacts_mismatch:rename-symbol expects 0" in json.loads(
        result.stdout
    )["errors"]


def test_report_rejects_declared_parity_failure_in_ordinary_case(
    tmp_path: Path,
) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    report["observations"][0]["invalidation"]["delta_full_parity"] = "different"
    path = tmp_path / "ordinary-parity-failure.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(path))

    assert result.returncode == 1
    assert "invalidation_parity_mismatch:rename-symbol" in json.loads(
        result.stdout
    )["errors"]


def test_report_rejects_affected_test_status_and_count_contradiction(
    tmp_path: Path,
) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    observation = report["observations"][0]
    observation["affected_tests"]["status"] = "empty"
    next(
        metric
        for metric in observation["metrics"]
        if metric["metric_id"] == "affected_tests"
    )["value"] = 0
    path = tmp_path / "affected-test-contradiction.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(path))

    assert result.returncode == 1
    errors = json.loads(result.stdout)["errors"]
    assert any(
        "affected_tests_status_mismatch:rename-symbol" in error for error in errors
    )
    assert any(
        "affected_tests_metric_mismatch:rename-symbol" in error for error in errors
    )


def test_schema_errors_remain_visible_in_summary(tmp_path: Path) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    report["provider"].pop("id")
    path = tmp_path / "schema-invalid.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("run-scenarios", str(path))

    assert result.returncode == 1
    summary = json.loads(result.stdout)
    contract = next(
        item
        for item in summary["per_scenario_breakdown"]
        if item["case_id"] == "report-contract"
    )
    assert any(code.startswith("report:provider:") for code in contract["issue_codes"])


def provider_execution_payload() -> dict[str, object]:
    provider = {
        "id": "python-ast-bootstrap",
        "version": "1.0.0",
    }
    source_epoch = "sha256:" + ("1" * 64)
    state = {
        "schema_version": "abyss-stack-live-code-intelligence-state-v1",
        "status": "current",
        "provider": provider,
        "config": {"digest": "sha256:" + ("2" * 64)},
        "source": {"source_epoch": source_epoch},
        "invalidation": {
            "changed_paths": ["consumer.py"],
            "added_paths": [],
            "deleted_paths": [],
            "dependency_impacted_paths": ["consumer.py"],
            "invalidated_paths": ["consumer.py"],
            "reused_paths": ["other.py"],
            "full_rebuild": False,
            "blast_radius_universe": {
                "kind": "previous-and-current-source-files",
                "count": 2,
                "paths": ["consumer.py", "other.py"],
            },
            "blast_radius": 0.5,
        },
        "freshness": {
            "layer": "LIVE",
            "source_epoch": source_epoch,
            "provider": provider,
            "confidence": "observed",
        },
        "provenance": {
            "runtime_owner": "abyss-stack",
            "observation_meaning_owner": "aoa-kag",
            "proof_owner": "aoa-evals",
            "source_kind": "working_tree",
            "full_rebuild": False,
        },
    }
    environment_digest = "sha256:" + ("3" * 64)
    execution = {
        "case_id": "delta-full-parity",
        "mode": "delta",
        "status": "completed",
        "source_epoch": source_epoch,
        "observed_at": "2026-08-25T12:00:01Z",
        "command_ref": "test://provider-execution",
        "environment_digest": environment_digest,
        "latency_ms": 1.5,
        "resource_peak_bytes": 4096,
        "state_digest": runner.canonical_digest(state),
        "repeated_state_digest": runner.stable_provider_state_digest(state),
        "full_state_projection_digest": "sha256:" + ("4" * 64),
        "delta_state_projection_digest": "sha256:" + ("4" * 64),
        "provider_state": state,
    }
    return {
        "schema_version": "aoa_code_observation_provider_execution_v1",
        "machine_binding": {
            "contract_schema": "abyss_machine_code_intelligence_config_v1",
            "contract_ref": "config-templates/etc/abyss-machine/code-intelligence.json",
            "contract_digest": runner.MACHINE_CONTRACT_DIGEST,
            "contract_digest_kind": runner.MACHINE_CONTRACT_DIGEST_KIND,
            "contract_snapshot_epoch": runner.MACHINE_CONTRACT_SNAPSHOT_EPOCH,
            "workspace_manifest_digest": runner.MACHINE_WORKSPACE_MANIFEST_DIGEST,
            "provider_id": "python-ast-bootstrap",
            "admission_state": "not_admitted",
            "admission_receipt_ref": None,
            "owner_bindings": runner.OWNER_BINDINGS,
            "claim_limits": runner.PROVIDER_EXECUTION_CLAIM_LIMITS,
        },
        "provider": {
            "id": provider["id"],
            "version": provider["version"],
            "observation_schema": "abyss-stack-code-observation-v1",
            "state_schema": "abyss-stack-live-code-intelligence-state-v1",
            "config_digest": state["config"]["digest"],
        },
        "run": {
            "execution_id": "test-execution",
            "started_at": "2026-08-25T12:00:00Z",
            "observed_at": "2026-08-25T12:01:00Z",
            "finished_at": "2026-08-25T12:01:00Z",
            "command_ref": "test://provider-execution",
            "environment_digest": environment_digest,
            "reproducibility_state": "deterministic",
        },
        "executions": [execution],
    }


def complete_provider_execution_payload() -> dict[str, object]:
    import provider_execution

    return provider_execution.execute()


def test_provider_execution_runs_all_twelve_cases() -> None:
    result = run_runner("execute-provider")

    assert result.returncode == 0, result.stderr
    envelope = json.loads(result.stdout)
    assert envelope["execution_posture"] == "source-bound-provider-candidate"
    assert envelope["machine_binding"]["admission_state"] == "not_admitted"
    assert envelope["coverage"]["mode"] == "complete"
    assert len(envelope["executions"]) == 12
    assert envelope["executions"][4]["observation"]["deletion"]["status"] == "confirmed"
    assert envelope["executions"][7]["observation"]["lineage"]["alternatives"] >= 2
    assert envelope["executions"][8]["observation"]["lineage"]["confidence"] < 1
    assert envelope["executions"][9]["observation"]["freshness"]["status"] == "stale"
    assert envelope["executions"][10]["observation"]["parity"]["status"] == "equal"


def test_provider_execution_binds_state_to_machine_contract(tmp_path: Path) -> None:
    execution_path = tmp_path / "provider-execution.json"
    execution_path.write_text(
        json.dumps(provider_execution_payload()), encoding="utf-8"
    )

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["valid"] is True
    assert payload["admission_state"] == "not_admitted"
    assert payload["case_ids"] == ["delta-full-parity"]


def test_provider_execution_rejects_execution_after_run(tmp_path: Path) -> None:
    envelope = complete_provider_execution_payload()
    envelope["executions"][0]["observed_at"] = "2999-01-01T00:00:01Z"  # type: ignore[index]
    execution_path = tmp_path / "execution-after-run.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    errors = json.loads(result.stdout)["errors"]
    assert "execution_observed_at:execution[0]:after_run" in errors


def test_provider_execution_rejects_execution_outside_run_window(
    tmp_path: Path,
) -> None:
    envelope = complete_provider_execution_payload()
    envelope["executions"][0]["observed_at"] = "2020-01-01T00:00:01Z"  # type: ignore[index]
    path = tmp_path / "execution-before-run-window.json"
    path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(path))

    assert result.returncode == 1
    errors = json.loads(result.stdout)["errors"]
    assert "execution_observed_at:execution[0]:before_run_window" in errors


def test_provider_execution_rejects_claim_limit_drift(tmp_path: Path) -> None:
    envelope = provider_execution_payload()
    envelope["machine_binding"]["claim_limits"] = [  # type: ignore[index]
        "This provider proves runtime health and proof acceptance."
    ]
    execution_path = tmp_path / "claim-limit-drift.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    assert any(
        "claim_limits" in error for error in json.loads(result.stdout)["errors"]
    )


def test_provider_execution_rejects_state_digest_drift(tmp_path: Path) -> None:
    envelope = provider_execution_payload()
    envelope["executions"][0]["provider_state"]["status"] = "degraded"  # type: ignore[index]
    execution_path = tmp_path / "state-drift.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any("state_digest:execution[0]" in error for error in payload["errors"])


def test_provider_execution_rejects_unbounded_blast_radius(tmp_path: Path) -> None:
    envelope = provider_execution_payload()
    state = envelope["executions"][0]["provider_state"]  # type: ignore[index]
    state["invalidation"]["blast_radius"] = 0.0  # type: ignore[index]
    execution_path = tmp_path / "blast-radius-drift.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any(
        "blast_radius_denominator:execution[0]" in error for error in payload["errors"]
    )


def test_provider_execution_rejects_delete_without_deletion_event(
    tmp_path: Path,
) -> None:
    envelope = provider_execution_payload()
    envelope["executions"][0]["case_id"] = "delete-entity"  # type: ignore[index]
    execution_path = tmp_path / "missing-delete-event.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any(
        "deletion_event_missing:execution[0]" in error for error in payload["errors"]
    )


def test_provider_execution_rejects_admitted_without_receipt(tmp_path: Path) -> None:
    envelope = provider_execution_payload()
    envelope["machine_binding"]["admission_state"] = "admitted"  # type: ignore[index]
    execution_path = tmp_path / "unreceipted-admission.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any("admission_receipt" in error for error in payload["errors"])


def test_complete_provider_execution_covers_the_whole_fixture_family(
    tmp_path: Path,
) -> None:
    envelope = complete_provider_execution_payload()
    execution_path = tmp_path / "complete-provider-execution.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload["valid"] is True
    assert payload["case_ids"] == sorted(envelope["coverage"]["case_ids"])  # type: ignore[index]


def test_complete_provider_execution_rejects_unbound_environment_digest(
    tmp_path: Path,
) -> None:
    envelope = complete_provider_execution_payload()
    fake_environment_digest = "sha256:" + ("f" * 64)
    envelope["run"]["environment_digest"] = fake_environment_digest  # type: ignore[index]
    for execution in envelope["executions"]:  # type: ignore[index]
        execution["environment_digest"] = fake_environment_digest
    execution_fixture = runner.load_json(runner.PROVIDER_EXECUTION_FIXTURE_PATH)
    fake_config_digest = runner.provider_execution_config_digest(
        execution_fixture, fake_environment_digest, envelope["provider"]
    )
    envelope["provider"]["config_digest"] = fake_config_digest  # type: ignore[index]
    for execution in envelope["executions"]:  # type: ignore[index]
        state = execution["provider_state"]
        state["config"]["digest"] = fake_config_digest
        execution["state_digest"] = runner.canonical_digest(state)
        execution["repeated_state_digest"] = runner.stable_provider_state_digest(
            state
        )
    path = tmp_path / "unbound-environment-digest.json"
    path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(path))

    assert result.returncode == 1
    errors = json.loads(result.stdout)["errors"]
    assert (
        "run_environment_digest:not bound to independently derived executor metadata"
        in errors
    )


def test_complete_provider_execution_rejects_incomplete_coverage(
    tmp_path: Path,
) -> None:
    envelope = complete_provider_execution_payload()
    envelope["coverage"]["case_ids"] = envelope["coverage"]["case_ids"][:-1]  # type: ignore[index]
    execution_path = tmp_path / "incomplete-provider-execution.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any("coverage_complete" in error for error in payload["errors"])


def test_complete_provider_candidate_cannot_self_claim_admission(
    tmp_path: Path,
) -> None:
    envelope = complete_provider_execution_payload()
    envelope["machine_binding"]["admission_state"] = "admitted"  # type: ignore[index]
    envelope["machine_binding"]["admission_receipt_ref"] = "receipt://self-claimed"  # type: ignore[index]
    path = tmp_path / "complete-admitted.json"
    path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(path))

    assert result.returncode == 1
    errors = json.loads(result.stdout)["errors"]
    assert any("complete_candidate_admission" in error for error in errors)
    assert any("complete_candidate_receipt" in error for error in errors)


def test_complete_provider_execution_rejects_freshness_confidence_drift(
    tmp_path: Path,
) -> None:
    envelope = complete_provider_execution_payload()
    execution = envelope["executions"][0]  # type: ignore[index]
    state = execution["provider_state"]
    state["freshness"]["confidence"] = "degraded"
    execution["state_digest"] = runner.canonical_digest(state)
    execution["repeated_state_digest"] = runner.stable_provider_state_digest(state)
    path = tmp_path / "freshness-confidence-drift.json"
    path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(path))

    assert result.returncode == 1
    assert any(
        "freshness_confidence:execution[0]" in error
        for error in json.loads(result.stdout)["errors"]
    )


def test_delta_projection_uses_incremental_reuse_and_matches_full_projection() -> None:
    before = {
        "src/changed.py": ["def value():", "    return 1"],
        "src/reused.py": ["def reused():", "    return 2"],
    }
    after = {
        "src/changed.py": ["def value():", "    return 3"],
        "src/reused.py": ["def reused():", "    return 2"],
    }

    delta = provider_execution.delta_source_index(
        before,
        after,
        ["src/changed.py"],
        provider_execution.source_index(before),
    )

    assert delta == provider_execution.source_index(after)
    assert delta is not provider_execution.source_index(after)


def test_provider_execution_exercises_delta_path_for_delta_cases(monkeypatch) -> None:
    contract_fixture = runner.load_json(runner.FIXTURE_PATH)
    execution_fixture = runner.load_json(runner.PROVIDER_EXECUTION_FIXTURE_PATH)
    fixture_case = next(
        case for case in contract_fixture["cases"] if case["case_id"] == "rename-symbol"
    )
    scenario = next(
        case
        for case in execution_fixture["cases"]
        if case["case_id"] == "rename-symbol"
    )
    delta_calls = []

    def record_delta(before, after, invalidated, before_index):
        delta_calls.append((before, after, invalidated, before_index))
        return provider_execution.source_index(after)

    def reject_full_projection(_after):
        raise AssertionError("delta case must not use the full projection runner")

    monkeypatch.setattr(provider_execution, "delta_source_index", record_delta)
    monkeypatch.setattr(
        provider_execution, "execute_projection_once", reject_full_projection
    )

    execution = provider_execution.case_execution(
        fixture_case,
        scenario,
        {"id": "python-ast-bootstrap", "version": "1.0.0"},
        "sha256:" + "0" * 64,
        "sha256:" + "1" * 64,
    )

    assert execution["mode"] == "delta"
    assert len(delta_calls) == 3


def test_stale_execution_reuses_cached_baseline_without_reparse(monkeypatch) -> None:
    contract_fixture = runner.load_json(runner.FIXTURE_PATH)
    execution_fixture = runner.load_json(runner.PROVIDER_EXECUTION_FIXTURE_PATH)
    fixture_case = next(
        case for case in contract_fixture["cases"] if case["case_id"] == "stale-index"
    )
    scenario = next(
        case
        for case in execution_fixture["cases"]
        if case["case_id"] == "stale-index"
    )
    calls = []
    real_source_index = provider_execution.source_index

    def record_source_index(tree):
        calls.append({path: list(lines) for path, lines in tree.items()})
        return real_source_index(tree)

    def reject_full_projection(_before):
        raise AssertionError("stale execution must reuse the cached baseline")

    monkeypatch.setattr(provider_execution, "source_index", record_source_index)
    monkeypatch.setattr(
        provider_execution, "execute_projection_once", reject_full_projection
    )

    execution = provider_execution.case_execution(
        fixture_case,
        scenario,
        {"id": "python-ast-bootstrap", "version": "1.0.0"},
        "sha256:" + "0" * 64,
        "sha256:" + "1" * 64,
    )

    assert execution["status"] == "degraded"
    assert calls[0] == scenario["before"]
    assert calls.count(scenario["before"]) == 1


def test_delta_projection_parses_only_invalidated_after_paths(monkeypatch) -> None:
    before = {
        "src/changed.py": ["def value():", "    return 1"],
        "src/reused.py": ["def reused():", "    return 2"],
    }
    after = {
        "src/changed.py": ["def value():", "    return 3"],
        "src/reused.py": ["def reused():", "    return 2"],
    }
    calls = []
    real_source_index = provider_execution.source_index

    def record_source_index(tree):
        calls.append(set(tree))
        return real_source_index(tree)

    monkeypatch.setattr(provider_execution, "source_index", record_source_index)

    baseline = provider_execution.source_index(before)
    calls.clear()
    provider_execution.delta_source_index(
        before, after, ["src/changed.py"], baseline
    )

    assert calls == [{"src/changed.py"}]


def test_case_execution_reuses_cached_baseline_for_delta_after_observation(
    monkeypatch,
) -> None:
    fixture = runner.load_json(runner.FIXTURE_PATH)
    fixture_case = next(
        case for case in fixture["cases"] if case["case_id"] == "rename-symbol"
    )
    before = {
        "src/changed.py": ["def value():", "    return 1"],
        "src/reused.py": ["def reused():", "    return 2"],
    }
    after = {
        "src/changed.py": ["def value():", "    return 3"],
        "src/reused.py": ["def reused():", "    return 2"],
    }
    scenario = {"before": before, "after": after, "test_dependencies": {}}
    calls = []
    events = []
    real_source_index = provider_execution.source_index

    def record_source_index(tree):
        events.append("source-index")
        calls.append({path: list(lines) for path, lines in tree.items()})
        return real_source_index(tree)

    class RecordingMeasurement:
        def __init__(self):
            events.append("measurement-start")

        def peak_bytes(self):
            return 1

        def close(self):
            events.append("measurement-close")

    monkeypatch.setattr(provider_execution, "source_index", record_source_index)
    monkeypatch.setattr(
        provider_execution, "CaseResourceMeasurement", RecordingMeasurement
    )

    execution = provider_execution.case_execution(
        fixture_case,
        scenario,
        {"id": "python-ast-bootstrap", "version": "1.0.0"},
        "sha256:" + "0" * 64,
        "sha256:" + "1" * 64,
    )

    # The complete before tree is parsed once as the cached baseline.  Every
    # subsequent provider projection is restricted to the changed path; a
    # complete after-tree parse would invalidate the advertised reuse evidence.
    assert calls == [
        before,
        {"src/changed.py": after["src/changed.py"]},
        {"src/changed.py": after["src/changed.py"]},
        {"src/changed.py": after["src/changed.py"]},
    ]
    assert calls[0] != after
    assert events == [
        "source-index",
        "source-index",
        "source-index",
        "measurement-start",
        "source-index",
        "measurement-close",
    ]
    assert {
        symbol["path"] for symbol in execution["observation"]["after_symbols"]
    } == {"src/changed.py", "src/reused.py"}


def test_report_rejects_stale_freshness_without_independent_prior_epoch(
    tmp_path: Path,
) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    for field, current_value in (
        ("observed_at", report["run"]["observed_at"]),
        ("provider_watermark", "fixture-001"),
    ):
        mutated = copy.deepcopy(report)
        mutated_stale_index = next(
            observation
            for observation in mutated["observations"]
            if observation["case_id"] == "stale-index"
        )
        mutated_stale_index["freshness"][field] = current_value
        path = tmp_path / f"stale-{field}-current.json"
        path.write_text(json.dumps(mutated), encoding="utf-8")

        result = run_runner("validate-report", str(path))

        assert result.returncode == 1
        errors = json.loads(result.stdout)["errors"]
        assert any(
            "stale_freshness_prior_epoch:stale-index" in error for error in errors
        )


def test_report_rejects_exact_freshness_drift_from_run_and_epoch(
    tmp_path: Path,
) -> None:
    report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
    exact_observation = report["observations"][0]
    exact_observation["freshness"]["observed_at"] = "2026-08-26T15:00:00Z"
    exact_observation["freshness"]["provider_watermark"] = "fixture-000"
    exact_observation["freshness"]["source_epoch_ref"] = "source-epoch-other"
    path = tmp_path / "exact-freshness-drift.json"
    path.write_text(json.dumps(report), encoding="utf-8")

    result = run_runner("validate-report", str(path))

    assert result.returncode == 1
    errors = json.loads(result.stdout)["errors"]
    assert "freshness_observed_at_mismatch:rename-symbol exact freshness must match the report run" in errors
    assert "freshness_current_epoch_mismatch:rename-symbol must match the independently declared current epoch" in errors
    assert "freshness_provider_watermark_mismatch:rename-symbol must match the independently declared current watermark" in errors


def test_provider_execution_rejects_added_deleted_record_drift(tmp_path: Path) -> None:
    envelope = complete_provider_execution_payload()
    add_execution = next(
        item for item in envelope["executions"] if item["case_id"] == "add-entity"
    )
    delete_execution = next(
        item
        for item in envelope["executions"]
        if item["case_id"] == "delete-entity"
    )
    add_execution["observation"]["added_symbols"][0]["fingerprint"] = (
        "sha256:" + "f" * 64
    )
    delete_execution["observation"]["deleted_symbols"][0]["lineage_id"] = (
        "lineage:" + "e" * 64
    )
    path = tmp_path / "added-deleted-symbol-drift.json"
    path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(path))

    assert result.returncode == 1
    errors = json.loads(result.stdout)["errors"]
    assert any("case_added_symbols:add-entity" in error for error in errors)
    assert any("case_deleted_symbols:delete-entity" in error for error in errors)


def test_case_resource_measurement_resets_peak_between_cases() -> None:
    first = provider_execution.CaseResourceMeasurement()
    try:
        large_allocation = bytearray(2 * 1024 * 1024)
        first_peak = first.peak_bytes()
    finally:
        first.close()
    del large_allocation

    second = provider_execution.CaseResourceMeasurement()
    try:
        small_allocation = bytearray(1024)
        second_peak = second.peak_bytes()
    finally:
        second.close()
    del small_allocation

    assert first_peak > second_peak


def test_complete_provider_execution_binds_affected_test_oracle(
    tmp_path: Path, monkeypatch
) -> None:
    envelope = complete_provider_execution_payload()
    oracle = json.loads(runner.AFFECTED_TEST_ORACLE_PATH.read_text(encoding="utf-8"))
    oracle["cases"][0]["selected"] = []
    oracle_path = tmp_path / "drifted-affected-tests.json"
    oracle_path.write_text(json.dumps(oracle), encoding="utf-8")
    monkeypatch.setattr(runner, "AFFECTED_TEST_ORACLE_PATH", oracle_path)

    errors, _case_ids = runner.provider_execution_errors(envelope)
    assert any(
        "execution_affected_tests_oracle_selection:rename-symbol" in error
        for error in errors
    )


def test_complete_provider_execution_requires_reproducibility_digest(
    tmp_path: Path,
) -> None:
    envelope = complete_provider_execution_payload()
    envelope["executions"][0]["repeated_state_digest"] = None  # type: ignore[index]
    execution_path = tmp_path / "non-reproducible-provider-execution.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any("reproducibility_required" in error for error in payload["errors"])


def test_complete_provider_execution_requires_delta_full_projections(
    tmp_path: Path,
) -> None:
    envelope = complete_provider_execution_payload()
    envelope["executions"][10]["full_state_projection_digest"] = None  # type: ignore[index]
    execution_path = tmp_path / "missing-parity-projection.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any("parity_required:execution[10]" in error for error in payload["errors"])


def test_complete_provider_execution_binds_command_provenance(
    tmp_path: Path,
) -> None:
    envelope = complete_provider_execution_payload()
    envelope["executions"][0]["command_ref"] = "test://different-executor"  # type: ignore[index]
    execution_path = tmp_path / "command-provenance-drift.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    assert any(
        "execution_command_ref:execution[0]" in error
        for error in json.loads(result.stdout)["errors"]
    )


def test_complete_provider_execution_rejects_run_command_ref_drift(
    tmp_path: Path,
) -> None:
    envelope = complete_provider_execution_payload()
    forged_command = "test://unrelated-executor"
    envelope["run"]["command_ref"] = forged_command  # type: ignore[index]
    for execution in envelope["executions"]:  # type: ignore[index]
        execution["command_ref"] = forged_command
    execution_path = tmp_path / "run-command-provenance-drift.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    assert any(
        "run_command_ref" in error
        for error in json.loads(result.stdout)["errors"]
    )


def test_complete_provider_execution_rejects_fixture_unbound_config_digest(
    tmp_path: Path,
) -> None:
    envelope = complete_provider_execution_payload()
    forged_digest = "sha256:" + ("f" * 64)
    envelope["provider"]["config_digest"] = forged_digest  # type: ignore[index]
    for execution in envelope["executions"]:  # type: ignore[index]
        state = execution["provider_state"]
        state["config"]["digest"] = forged_digest
        execution["state_digest"] = runner.canonical_digest(state)
        execution["repeated_state_digest"] = runner.stable_provider_state_digest(
            state
        )
    execution_path = tmp_path / "fixture-unbound-config.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    assert any(
        "execution_config_digest" in error
        for error in json.loads(result.stdout)["errors"]
    )


def test_complete_provider_execution_rejects_forged_deletion_semantics(
    tmp_path: Path,
) -> None:
    envelope = complete_provider_execution_payload()
    envelope["executions"][4]["observation"]["deletion"]["after_absent"] = []  # type: ignore[index]
    execution_path = tmp_path / "forged-delete.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any(
        "execution[4]:deletion_after_absence" in error for error in payload["errors"]
    )


def test_complete_provider_execution_rejects_non_delete_deletion_evidence(
    tmp_path: Path,
) -> None:
    envelope = complete_provider_execution_payload()
    execution_index, execution = next(
        (index, item)
        for index, item in enumerate(envelope["executions"])
        if item["case_id"] == "rename-symbol"
    )
    execution["observation"]["deletion"]["before_present"] = ["src/alpha.py"]
    execution["observation"]["deletion"]["after_absent"] = ["src/alpha.py"]
    execution_path = tmp_path / "non-delete-deletion-evidence.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    errors = json.loads(result.stdout)["errors"]
    assert any(
        f"execution[{execution_index}]:deletion_not_applicable_nonempty"
        in error
        for error in errors
    )


def test_complete_provider_execution_rejects_overconfident_split_lineage(
    tmp_path: Path,
) -> None:
    envelope = complete_provider_execution_payload()
    envelope["executions"][7]["observation"]["lineage"]["confidence"] = 1  # type: ignore[index]
    execution_path = tmp_path / "overconfident-split.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any(
        "execution[7]:case_lineage_confidence" in error for error in payload["errors"]
    )


def test_complete_provider_execution_rejects_inflated_split_lineage(
    tmp_path: Path,
) -> None:
    envelope = complete_provider_execution_payload()
    lineage = envelope["executions"][7]["observation"]["lineage"]  # type: ignore[index]
    lineage["alternatives"] = 100
    lineage["confidence"] = 0.01
    execution_path = tmp_path / "inflated-split-lineage.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    errors = json.loads(result.stdout)["errors"]
    assert any(
        "execution[7]:case_lineage_alternatives" in error for error in errors
    )
    assert any(
        "execution[7]:case_lineage_confidence" in error for error in errors
    )


def test_complete_provider_execution_rejects_uncertain_not_applicable_lineage(
    tmp_path: Path,
) -> None:
    envelope = complete_provider_execution_payload()
    add_execution = next(
        item for item in envelope["executions"] if item["case_id"] == "add-entity"
    )
    add_execution["observation"]["lineage"]["alternatives"] = 2
    add_execution["observation"]["lineage"]["confidence"] = 0.5
    execution_path = tmp_path / "uncertain-not-applicable-lineage.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    errors = json.loads(result.stdout)["errors"]
    assert any(
        "execution[3]:case_lineage_not_applicable" in error for error in errors
    )


def test_complete_provider_execution_binds_all_parity_digests(
    tmp_path: Path,
) -> None:
    envelope = complete_provider_execution_payload()
    execution = envelope["executions"][10]  # type: ignore[index]
    forged_top_level = "sha256:" + ("f" * 64)
    forged_observation = "sha256:" + ("e" * 64)
    execution["full_state_projection_digest"] = forged_top_level
    execution["delta_state_projection_digest"] = forged_top_level
    parity = execution["observation"]["parity"]
    parity["full_projection_digest"] = forged_observation
    parity["delta_projection_digest"] = forged_observation
    execution["provider_state"]["source"]["projection_digest"] = forged_top_level
    state = execution["provider_state"]
    execution["state_digest"] = runner.canonical_digest(state)
    execution["repeated_state_digest"] = runner.stable_provider_state_digest(state)
    execution_path = tmp_path / "forged-parity-digests.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    errors = json.loads(result.stdout)["errors"]
    assert any("execution_projection_digest:execution[10]" in error for error in errors)
    assert any(
        "execution_parity_projection:execution[10]:full" in error
        for error in errors
    )
    assert any(
        "execution_parity_projection:execution[10]:delta" in error
        for error in errors
    )
    assert any(
        "execution_parity_observation:execution[10]:full" in error
        for error in errors
    )
    assert any(
        "execution_parity_observation:execution[10]:delta" in error
        for error in errors
    )


def test_complete_provider_execution_rejects_provider_fixture_version_drift(
    tmp_path: Path,
) -> None:
    envelope = complete_provider_execution_payload()
    envelope["provider"]["version"] = "self-asserted"  # type: ignore[index]
    execution_path = tmp_path / "provider-version-drift.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any("execution_provider_version" in error for error in payload["errors"])


def test_provider_execution_requires_explicit_snapshot_drift(tmp_path: Path) -> None:
    envelope = provider_execution_payload()
    envelope["machine_binding"]["current_contract_digest"] = "sha256:" + ("9" * 64)  # type: ignore[index]
    execution_path = tmp_path / "implicit-snapshot-drift.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any("snapshot_currentness" in error for error in payload["errors"])


def test_provider_execution_allows_explicit_unobserved_currentness(
    tmp_path: Path,
) -> None:
    envelope = provider_execution_payload()
    envelope["machine_binding"]["snapshot_currentness"] = "unobserved"  # type: ignore[index]
    execution_path = tmp_path / "unobserved-snapshot-currentness.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["valid"] is True


def test_provider_execution_rejects_unsafe_invalidation_path(tmp_path: Path) -> None:
    envelope = provider_execution_payload()
    envelope["executions"][0]["provider_state"]["invalidation"][
        "blast_radius_universe"
    ]["paths"] = [  # type: ignore[index]
        "consumer.py",
        "../outside.py",
    ]
    execution_path = tmp_path / "unsafe-invalidation-path.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any("unsafe_path:execution[0]" in error for error in payload["errors"])


def test_provider_execution_rejects_non_positive_latency(tmp_path: Path) -> None:
    envelope = provider_execution_payload()
    envelope["executions"][0]["latency_ms"] = 0  # type: ignore[index]
    execution_path = tmp_path / "zero-latency.json"
    execution_path.write_text(json.dumps(envelope), encoding="utf-8")

    result = run_runner("validate-provider-execution", str(execution_path))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any("latency_ms" in error for error in payload["errors"])


def test_provider_evidence_collects_and_validates_real_local_observations(
    tmp_path: Path,
) -> None:
    result = run_runner("collect-provider-evidence")

    assert result.returncode == 0, result.stderr
    evidence = json.loads(result.stdout)
    assert evidence["family_id"] == "refactor-torture-v1"
    assert {provider["id"] for provider in evidence["providers"]} == {
        "python-ast",
        "ctags-host",
    }
    for provider in evidence["providers"]:
        assert provider["admission_state"] == "not_admitted"
        if provider["availability"] == "available":
            assert len(provider["case_ids"]) == 12
            assert (
                sum(item["status"] == "observed" for item in provider["observations"])
                == 12
            )
    ctags_provider = next(
        provider for provider in evidence["providers"] if provider["id"] == "ctags-host"
    )
    if shutil.which("ctags"):
        assert ctags_provider["availability"] == "available"
    else:
        assert ctags_provider["availability"] == "not_available"

    evidence_path = tmp_path / "provider-evidence.json"
    evidence_path.write_text(result.stdout, encoding="utf-8")
    validation = run_runner("validate-provider-evidence", str(evidence_path))
    assert validation.returncode == 0, validation.stderr
    assert json.loads(validation.stdout)["valid"] is True


def test_provider_evidence_rejects_provider_metadata_drift(tmp_path: Path) -> None:
    evidence = json.loads(run_runner("collect-provider-evidence").stdout)
    for provider in evidence["providers"]:
        provider["version"] = "forged-provider-version"
        provider["command_ref"] = "forged://provider"
        provider["config_digest"] = "sha256:" + ("0" * 64)
    path = tmp_path / "provider-metadata-drift.json"
    path.write_text(json.dumps(evidence), encoding="utf-8")

    result = run_runner("validate-provider-evidence", str(path))

    assert result.returncode == 1
    errors = json.loads(result.stdout)["errors"]
    for index in range(len(evidence["providers"])):
        assert any(
            f"provider[{index}]: provider metadata {field} mismatch" in error
            for field in ("version", "command_ref", "config_digest")
            for error in errors
        )


def test_provider_evidence_cannot_claim_admission(tmp_path: Path) -> None:
    evidence = json.loads(run_runner("collect-provider-evidence").stdout)
    evidence["providers"][0]["admission_state"] = "admitted"
    evidence_path = tmp_path / "admitted-provider-evidence.json"
    evidence_path.write_text(json.dumps(evidence), encoding="utf-8")

    result = run_runner("validate-provider-evidence", str(evidence_path))

    assert result.returncode == 1
    payload = json.loads(result.stdout)
    assert any("admission_state" in error for error in payload["errors"])


def test_provider_evidence_rejects_claim_boundary_and_occurrence_drift(
    tmp_path: Path,
) -> None:
    evidence = json.loads(run_runner("collect-provider-evidence").stdout)
    evidence["claim_boundary"] = evidence["claim_boundary"].replace(
        "These observations", "The observations"
    )
    symbol = evidence["providers"][0]["observations"][0]["symbols"][0]
    symbol["start_line"] += 10
    symbol["end_line"] += 10
    path = tmp_path / "provider-evidence-drift.json"
    path.write_text(json.dumps(evidence), encoding="utf-8")

    result = run_runner("validate-provider-evidence", str(path))

    assert result.returncode == 1
    errors = json.loads(result.stdout)["errors"]
    assert any("claim_boundary" in error for error in errors)
    assert any(
        "symbol occurrence does not match independent provider output" in error
        for error in errors
    )


def test_provider_evidence_rejects_duplicate_symbol_occurrence(tmp_path: Path) -> None:
    evidence = json.loads(run_runner("collect-provider-evidence").stdout)
    observation = evidence["providers"][0]["observations"][0]
    observation["symbols"].append(copy.deepcopy(observation["symbols"][0]))
    path = tmp_path / "duplicate-provider-symbol.json"
    path.write_text(json.dumps(evidence), encoding="utf-8")

    result = run_runner("validate-provider-evidence", str(path))

    assert result.returncode == 1
    errors = json.loads(result.stdout)["errors"]
    assert any("duplicate symbol occurrence" in error for error in errors)


def test_provider_evidence_rejects_claim_limit_drift(tmp_path: Path) -> None:
    evidence = json.loads(run_runner("collect-provider-evidence").stdout)
    evidence["providers"][0]["claim_limits"] = [
        *evidence["providers"][0]["claim_limits"],
        "This provider proves admission and runtime health.",
    ]
    path = tmp_path / "provider-evidence-claim-limit-drift.json"
    path.write_text(json.dumps(evidence), encoding="utf-8")

    result = run_runner("validate-provider-evidence", str(path))

    assert result.returncode == 1
    assert any(
        "claim_limits" in error for error in json.loads(result.stdout)["errors"]
    )


def test_report_rejects_non_finite_resource_metrics(tmp_path: Path) -> None:
    for metric_id, value in (
        ("latency", float("nan")),
        ("resource_cost", float("inf")),
    ):
        report = json.loads(EXAMPLE.read_text(encoding="utf-8"))
        observation = report["observations"][10]
        metric = next(
            item for item in observation["metrics"] if item["metric_id"] == metric_id
        )
        metric["value"] = value
        path = tmp_path / f"non-finite-{metric_id}.json"
        path.write_text(json.dumps(report), encoding="utf-8")

        result = run_runner("validate-report", str(path))

        assert result.returncode == 1
        errors = json.loads(result.stdout)["errors"]
        assert any(
            f"metric_not_finite:delta-full-parity:{metric_id}" in error
            for error in errors
        )


def test_provider_agreement_rejects_placeholder_observation(tmp_path: Path) -> None:
    facts = ["definition:render"]
    payload = {
        "schema_version": "aoa_code_observation_provider_agreement_v1",
        "observed_at": "2026-08-29T00:00:00Z",
        "required_facts": facts,
        "claim_boundary": provider_agreement.CLAIM_BOUNDARY,
        "envelopes": [
            _agreement_envelope(provider_id, facts)
            for provider_id in ("tree-sitter", "scip", "lsp")
        ],
    }
    payload["envelopes"][0]["observations"] = [{}]
    path = tmp_path / "placeholder-agreement.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    result = provider_agreement.validate(path)

    assert any(
        issue.startswith("invalid_normalized_observation:tree-sitter:0")
        for issue in result["issues"]
    )


def test_adjacent_provider_evidence_rejects_placeholder_observation(
    tmp_path: Path,
) -> None:
    source_epoch = "commit:" + "a" * 40
    source_repo = "fixture"
    source_path = "fixture.py"
    source_digest = "sha256:" + "1" * 64
    specs = {
        "static_security": ("semgrep", "static-security"),
        "software_components": ("syft", "software-components"),
        "artifact_provenance": ("in-toto", "artifact-provenance"),
        "document_structure": ("markitdown", "document-structure"),
    }
    batches = {
        key: {
            "schema_version": "aoa-code-observation-v1",
            "capability_class": capability,
            "provider": {
                "id": provider_id,
                "version": "1.0.0",
                "config_digest": "sha256:" + "0" * 64,
                "lane": {"id": provider_id, "status": "supplied_unadmitted"},
            },
            "currentness": {
                "provider": {
                    "id": provider_id,
                    "version": "1.0.0",
                    "config_digest": "sha256:" + "0" * 64,
                }
            },
            "provenance": {
                "extractor_ref": f"fixture:{provider_id}@1.0.0#sha256:{'0' * 64}",
                "parser_ref": f"{provider_id}@1.0.0#sha256:{'0' * 64}",
                "source_refs": [
                    {
                        "repo": source_repo,
                        "path": source_path,
                        "role": "primary_source",
                        "content_digest": source_digest,
                    }
                ],
            },
            "source": {
                "repo": source_repo,
                "path": source_path,
                "source_epoch": source_epoch,
                "content_digest": source_digest,
            },
            "parse_status": "parsed",
            "observations": [{}],
            "qualification": {"machine_admission": {"state": "not_admitted"}},
        }
        for key, (provider_id, capability) in specs.items()
    }
    payload = {
        "schema": "abyssos_adjacent_provider_evidence_v1",
        "goal_id": "fixture",
        "observed_at": "2026-08-29T00:00:00Z",
        "source_epoch": source_epoch,
        "artifact": {
            "sha256": "sha256:" + "1" * 64,
            "subject_digest": "sha256:" + "2" * 64,
            "signature_status": "missing",
            "admission_status": "not_admitted",
        },
        "providers": {
            provider_id: {"version": "1.0.0", "runtime_posture": "candidate_unadmitted"}
            for provider_id, _capability in specs.values()
        },
        "raw_evidence": {
            "sarif": {"path": "sarif.json", "sha256": "sha256:" + "1" * 64},
            "sbom": {"path": "sbom.json", "sha256": "sha256:" + "2" * 64},
            "in_toto": {"path": "provenance.jsonl", "sha256": "sha256:" + "3" * 64},
            "document_markdown": {
                "path": "document.md",
                "sha256": "sha256:" + "4" * 64,
            },
        },
        "batches": batches,
        "summary": {"all_provider_lanes_unadmitted": True},
        "claim_limits": adjacent_provider_evidence.CLAIM_LIMITS,
    }
    path = tmp_path / "placeholder-adjacent.json"
    path.write_text(json.dumps(payload), encoding="utf-8")

    result = adjacent_provider_evidence.validate(path)

    assert any(
        issue.startswith("invalid_observation:semgrep:0") for issue in result["issues"]
    )
