"""Validate exact adjacent-provider evidence without promoting admission."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker


BUNDLE_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = BUNDLE_ROOT / "schemas/adjacent-provider-evidence.schema.json"
EXPECTED = {
    "static_security": ("semgrep", "static-security"),
    "software_components": ("syft", "software-components"),
    "artifact_provenance": ("in-toto", "artifact-provenance"),
    "document_structure": ("markitdown", "document-structure"),
}
OBSERVATION_CONTRACT = {
    "static_security": ("static-security", {"security_finding"}, "sarif:"),
    "software_components": (
        "software-components",
        {"software_component"},
        "component:",
    ),
    "artifact_provenance": ("artifact-provenance", {"artifact_subject"}, "provenance:"),
    "document_structure": (
        "document-structure",
        {"heading", "paragraph", "table", "list", "document_element"},
        "document:",
    ),
}
CLAIM_LIMITS = [
    "Actual provider execution and common-envelope normalization are shown.",
    "Candidate execution does not establish artifact admission or deployed runtime availability.",
    "The packet does not establish scanner completeness, SBOM completeness, document fidelity, semantic proof, landing, or owner acceptance.",
]
RAW_EVIDENCE_KEYS = {
    "static_security": "sarif",
    "software_components": "sbom",
    "artifact_provenance": "in_toto",
    "document_structure": "document_markdown",
}
EXPECTED_PROVIDER_IDS = {provider_id for provider_id, _ in EXPECTED.values()}
# SARIF's driver name is a human-facing identity rather than the normalized
# provider id.  Keep the accepted identity explicit so a packet cannot retain
# Semgrep's version/results while naming an unrelated scanner.
EXPECTED_SARIF_DRIVER_NAMES = {"semgrep": {"Semgrep OSS"}}
# Adjacent batches predate the envelope's ``sha256:``-qualified artifact
# references and carry their provider configuration digest as raw hex.  Keep
# accepting both representations while requiring a complete cryptographic
# digest rather than an arbitrary non-empty token.
_DIGEST_RE = re.compile(r"^(?:sha256:)?[0-9a-f]{64}$")
_RAW_DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
# Adjacent evidence is normally staged beside the packet.  The supplied
# AbyssOS packet also points at a host-managed artifact bundle for its in-toto
# output; keep that explicit store as the only permitted external root.
_HOST_ARTIFACT_ROOT = Path("/srv/abyss-machine/artifacts")


def _normalize_provider_version(value: Any, provider_id: str) -> str | None:
    """Normalize a provider-labelled version without accepting substrings.

    The host metadata for MarkItDown is labelled ``markitdown 0.1.7`` while
    the adjacent batch carries ``0.1.7``.  Strip only that explicit provider
    label (and an optional conventional ``v`` prefix), then compare the
    resulting version strings exactly.  In particular, ``0`` must not match
    ``1.0.0`` merely because it is a substring.
    """

    if not isinstance(value, str):
        return None
    normalized = value.strip()
    if not normalized:
        return None
    provider_prefix = provider_id.casefold() + " "
    if normalized.casefold().startswith(provider_prefix):
        normalized = normalized[len(provider_prefix) :].strip()
    if normalized[:1].casefold() == "v":
        normalized = normalized[1:].strip()
    return normalized or None


def _raw_evidence_path(packet_path: Path, declared_path: Any) -> tuple[Path | None, str | None]:
    """Resolve one raw ref without allowing arbitrary host-file claims."""

    if (
        not isinstance(declared_path, str)
        or not declared_path.strip()
        or "\x00" in declared_path
        or "://" in declared_path
    ):
        return None, "path_unsafe"
    try:
        candidate = Path(declared_path)
        resolved = (
            candidate if candidate.is_absolute() else packet_path.parent / candidate
        ).resolve(strict=False)
        packet_root = packet_path.parent.resolve(strict=False)
        allowed_roots = [packet_root]
        if _HOST_ARTIFACT_ROOT.exists():
            allowed_roots.append(_HOST_ARTIFACT_ROOT.resolve(strict=False))
        if not any(
            resolved == root or root in resolved.parents for root in allowed_roots
        ):
            return None, "path_unsafe"
    except (OSError, RuntimeError, TypeError, ValueError):
        return None, "path_unsafe"
    if not resolved.is_file():
        return None, "file_missing"
    return resolved, None


def _raw_evidence_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def _raw_issue(raw_key: str, kind: str, detail: str) -> str:
    return f"raw_evidence_{kind}:{raw_key}:{detail}"


def _source_uri_matches(source_path: Any, uri: Any) -> bool:
    if not isinstance(source_path, str) or not source_path.strip():
        return False
    if not isinstance(uri, str) or not uri.strip():
        return False
    normalized_uri = uri.removeprefix("file://").replace("\\", "/")
    normalized_source = source_path.replace("\\", "/")
    if normalized_source.startswith("./"):
        normalized_source = normalized_source[2:]
    return normalized_uri == normalized_source or normalized_uri.endswith(
        "/" + normalized_source
    )


def _source_path_is_safe(value: Any) -> bool:
    """Accept only a repository-relative source path, never a host locator."""

    if not isinstance(value, str) or not value.strip() or "\x00" in value:
        return False
    normalized = value.replace("\\", "/")
    if "://" in normalized:
        return False
    try:
        candidate = PurePosixPath(normalized)
    except (TypeError, ValueError):
        return False
    return not candidate.is_absolute() and ".." not in candidate.parts


def _packet_source_path(
    packet_path: Path, source_path: Any
) -> tuple[Path | None, str | None]:
    """Resolve packet-local source bytes used to witness ``content_digest``."""

    if not _source_path_is_safe(source_path):
        return None, "path_unsafe"
    try:
        packet_root = packet_path.parent.resolve(strict=False)
        resolved = (packet_root / source_path).resolve(strict=False)
    except (OSError, RuntimeError, TypeError, ValueError):
        return None, "path_unsafe"
    if resolved != packet_root and packet_root not in resolved.parents:
        return None, "path_unsafe"
    if not resolved.is_file():
        return None, "file_missing"
    return resolved, None


def _source_identity_issues(
    batch: dict[str, Any],
    provider_id: str,
    source_epoch: Any,
    packet_path: Path,
) -> list[str]:
    """Bind the normalized source identity to its provenance witness.

    ``source_epoch`` alone is not an identity: two unrelated trees can share a
    relabelled epoch.  Require the repository-relative path and content digest,
    then require one provenance source reference to carry the same tuple.
    Raw-format validators bind the path/digest to the formats that expose them.
    """

    source = batch.get("source")
    if not isinstance(source, dict):
        return [f"source_identity_missing:{provider_id}"]
    repo = source.get("repo")
    path = source.get("path")
    content_digest = source.get("content_digest")
    issues: list[str] = []
    if not isinstance(repo, str) or not repo.strip():
        issues.append(f"source_identity_missing:{provider_id}:repo")
    if not _source_path_is_safe(path):
        issues.append(f"source_identity_path_unsafe:{provider_id}")
    source_digest = _digest_hex(content_digest)
    if source_digest is None:
        issues.append(f"source_identity_missing:{provider_id}:content_digest")
    if source.get("source_epoch") != source_epoch:
        issues.append(f"source_epoch_mismatch:{provider_id}")

    source_file, source_file_issue = _packet_source_path(packet_path, path)
    if source_file_issue == "path_unsafe":
        issues.append(f"source_path_unsafe:{provider_id}")
    elif source_file_issue == "file_missing":
        issues.append(f"source_file_missing:{provider_id}")
    elif source_file is not None and source_digest is not None:
        try:
            actual_digest = _raw_evidence_digest(source_file).removeprefix("sha256:")
            if actual_digest != source_digest:
                issues.append(f"source_content_digest_mismatch:{provider_id}")
        except OSError:
            issues.append(f"source_file_unreadable:{provider_id}")

    provenance = batch.get("provenance")
    source_refs = provenance.get("source_refs") if isinstance(provenance, dict) else None
    matching_ref = (
        isinstance(source_refs, list)
        and isinstance(repo, str)
        and isinstance(path, str)
        and source_digest is not None
        and any(
            isinstance(source_ref, dict)
            and source_ref.get("repo") == repo
            and source_ref.get("path") == path
            and _digest_hex(source_ref.get("content_digest")) == source_digest
            for source_ref in source_refs
        )
    )
    if not matching_ref:
        issues.append(f"source_provenance_identity_mismatch:{provider_id}")
    return issues


def _raw_sarif_issues(batch: dict[str, Any], document: Any) -> list[str]:
    raw_key = "sarif"
    if not isinstance(document, dict) or document.get("version") != "2.1.0":
        return [_raw_issue(raw_key, "format_invalid", "sarif_version")]
    runs = document.get("runs")
    if not isinstance(runs, list) or not runs:
        return [_raw_issue(raw_key, "format_invalid", "runs")]

    records: dict[tuple[int, int], dict[str, Any]] = {}
    issues: list[str] = []
    provider = batch.get("provider", {})
    provider_id = provider.get("id") if isinstance(provider, dict) else None
    provider_version = provider.get("version") if isinstance(provider, dict) else None
    expected_driver_names = EXPECTED_SARIF_DRIVER_NAMES.get(provider_id, set())
    for run_index, run in enumerate(runs):
        if not isinstance(run, dict):
            issues.append(_raw_issue(raw_key, "format_invalid", f"run:{run_index}"))
            continue
        tool = run.get("tool")
        driver = tool.get("driver", {}) if isinstance(tool, dict) else {}
        driver_name = driver.get("name") if isinstance(driver, dict) else None
        if not isinstance(driver, dict) or not isinstance(driver_name, str):
            issues.append(
                _raw_issue(raw_key, "format_invalid", f"tool:{run_index}")
            )
        elif driver_name not in expected_driver_names:
            issues.append(
                _raw_issue(raw_key, "content_mismatch", f"tool_identity:{run_index}")
            )
        observed_version = (
            driver.get("semanticVersion")
            if isinstance(driver, dict)
            else None
        ) or (driver.get("version") if isinstance(driver, dict) else None)
        if observed_version != provider_version:
            issues.append(
                _raw_issue(raw_key, "content_mismatch", f"tool_version:{run_index}")
            )
        results = run.get("results")
        if not isinstance(results, list):
            issues.append(
                _raw_issue(raw_key, "format_invalid", f"results:{run_index}")
            )
            continue
        for result_index, result in enumerate(results):
            if isinstance(result, dict):
                records[(run_index, result_index)] = result
            else:
                issues.append(
                    _raw_issue(
                        raw_key,
                        "format_invalid",
                        f"result:{run_index}:{result_index}",
                    )
                )
    if not records:
        issues.append(_raw_issue(raw_key, "format_invalid", "results_empty"))

    observations = batch.get("observations", [])
    declared_keys: set[tuple[int, int]] = set()
    for observation_index, observation in enumerate(observations):
        if not isinstance(observation, dict):
            issues.append(
                _raw_issue(
                    raw_key, "content_mismatch", f"observation:{observation_index}"
                )
            )
            continue
        semantic_key = observation.get("semantic_key")
        match = (
            re.fullmatch(r"sarif:(\d+):(\d+):(.+)", semantic_key)
            if isinstance(semantic_key, str)
            else None
        )
        if match is None:
            issues.append(
                _raw_issue(raw_key, "content_mismatch", f"semantic_key:{observation_index}")
            )
            continue
        location = (int(match.group(1)), int(match.group(2)))
        if location in declared_keys or location not in records:
            issues.append(
                _raw_issue(raw_key, "content_mismatch", f"result_ref:{observation_index}")
            )
            continue
        declared_keys.add(location)
        result = records[location]
        rule_id = result.get("ruleId")
        subject = observation.get("subject", {})
        if not isinstance(subject, dict):
            subject = {}
        message = result.get("message")
        if (
            not isinstance(rule_id, str)
            or rule_id != match.group(3)
            or subject.get("label") != rule_id
            or subject.get("qualified_name") != rule_id
            or not isinstance(message, dict)
            or not isinstance(message.get("text"), str)
        ):
            issues.append(
                _raw_issue(raw_key, "content_mismatch", f"result_identity:{observation_index}")
            )
        locations = result.get("locations")
        physical = (
            locations[0].get("physicalLocation")
            if isinstance(locations, list) and locations and isinstance(locations[0], dict)
            else None
        )
        region = physical.get("region") if isinstance(physical, dict) else None
        artifact_location = (
            physical.get("artifactLocation") if isinstance(physical, dict) else None
        )
        occurrence = (
            observation.get("occurrence", {})
            if isinstance(observation, dict)
            else {}
        )
        if not isinstance(occurrence, dict):
            occurrence = {}
        expected_coordinates = (
            region.get("startLine"),
            region.get("startColumn"),
            region.get("endLine"),
            region.get("endColumn"),
        ) if isinstance(region, dict) else (None,) * 4
        actual_coordinates = (
            occurrence.get("start_line"),
            occurrence.get("start_column"),
            occurrence.get("end_line"),
            occurrence.get("end_column"),
        )
        if actual_coordinates != expected_coordinates:
            issues.append(
                _raw_issue(raw_key, "content_mismatch", f"location:{observation_index}")
            )
        if not isinstance(artifact_location, dict) or not _source_uri_matches(
            batch.get("source", {}).get("path"), artifact_location.get("uri")
        ):
            issues.append(
                _raw_issue(raw_key, "content_mismatch", f"source:{observation_index}")
            )
    if len(observations) != len(records) or declared_keys != set(records):
        issues.append(_raw_issue(raw_key, "content_mismatch", "result_coverage"))
    return issues


def _raw_sbom_issues(batch: dict[str, Any], document: Any) -> list[str]:
    raw_key = "sbom"
    if (
        not isinstance(document, dict)
        or document.get("bomFormat") != "CycloneDX"
        or not isinstance(document.get("specVersion"), str)
    ):
        return [_raw_issue(raw_key, "format_invalid", "cyclonedx_header")]
    components = document.get("components")
    if not isinstance(components, list) or not components:
        return [_raw_issue(raw_key, "format_invalid", "components")]
    metadata = document.get("metadata")
    tools_root = metadata.get("tools", {}) if isinstance(metadata, dict) else {}
    tools = tools_root.get("components", []) if isinstance(tools_root, dict) else []
    if not isinstance(tools, list):
        return [_raw_issue(raw_key, "format_invalid", "tools")]
    provider = batch.get("provider", {})
    if not any(
        isinstance(tool, dict)
        and tool.get("name") == provider.get("id")
        and tool.get("version") == provider.get("version")
        for tool in tools
    ):
        return [_raw_issue(raw_key, "content_mismatch", "tool_identity")]

    issues: list[str] = []
    observations = batch.get("observations", [])
    declared_indexes: set[int] = set()
    for observation_index, observation in enumerate(observations):
        if not isinstance(observation, dict):
            issues.append(
                _raw_issue(raw_key, "content_mismatch", f"observation:{observation_index}")
            )
            continue
        semantic_key = observation.get("semantic_key")
        match = (
            re.fullmatch(r"component:(\d+):(.+)", semantic_key)
            if isinstance(semantic_key, str)
            else None
        )
        if match is None:
            issues.append(
                _raw_issue(raw_key, "content_mismatch", f"semantic_key:{observation_index}")
            )
            continue
        component_index = int(match.group(1))
        if component_index in declared_indexes or component_index >= len(components):
            issues.append(
                _raw_issue(raw_key, "content_mismatch", f"component_ref:{observation_index}")
            )
            continue
        declared_indexes.add(component_index)
        component = components[component_index]
        subject = observation.get("subject", {})
        if not isinstance(subject, dict):
            subject = {}
        name = component.get("name") if isinstance(component, dict) else None
        version = component.get("version") if isinstance(component, dict) else None
        expected_name = (
            f"{name}@{version}"
            if isinstance(version, str)
            else name
            if isinstance(name, str) and component.get("type") == "file"
            else None
        )
        if (
            not isinstance(name, str)
            or match.group(2) != expected_name
            or subject.get("label") != name
            or subject.get("qualified_name") != expected_name
        ):
            issues.append(
                _raw_issue(raw_key, "content_mismatch", f"component_identity:{observation_index}")
            )
    if len(observations) != len(components) or declared_indexes != set(range(len(components))):
        issues.append(_raw_issue(raw_key, "content_mismatch", "component_coverage"))
    return issues


def _digest_hex(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    candidate = value.removeprefix("sha256:")
    return candidate if re.fullmatch(r"[0-9a-f]{64}", candidate) else None


def _raw_in_toto_issues(
    batch: dict[str, Any], document_text: str, artifact: dict[str, Any]
) -> list[str]:
    raw_key = "in_toto"
    statements: list[dict[str, Any]] = []
    issues: list[str] = []
    for line_index, line in enumerate(document_text.splitlines()):
        if not line.strip():
            continue
        try:
            statement = json.loads(line)
        except json.JSONDecodeError:
            issues.append(_raw_issue(raw_key, "format_invalid", f"jsonl:{line_index}"))
            continue
        if not isinstance(statement, dict):
            issues.append(_raw_issue(raw_key, "format_invalid", f"statement:{line_index}"))
            continue
        statements.append(statement)
    if not statements:
        return issues + [_raw_issue(raw_key, "format_invalid", "statements_empty")]

    subjects: list[tuple[dict[str, Any], dict[str, Any]]] = []
    byproducts: list[dict[str, Any]] = []
    provider = batch.get("provider", {})
    provider_config = provider.get("config", {}) if isinstance(provider, dict) else {}
    expected_predicate_type = (
        provider_config.get("predicate_type")
        if isinstance(provider_config, dict)
        else None
    )
    for statement_index, statement in enumerate(statements):
        if statement.get("_type") != "https://in-toto.io/Statement/v1":
            issues.append(_raw_issue(raw_key, "format_invalid", f"type:{statement_index}"))
        if not isinstance(statement.get("predicateType"), str):
            issues.append(_raw_issue(raw_key, "format_invalid", f"predicate:{statement_index}"))
        elif expected_predicate_type and statement["predicateType"] != expected_predicate_type:
            issues.append(_raw_issue(raw_key, "content_mismatch", f"predicate:{statement_index}"))
        predicate = statement.get("predicate")
        if not isinstance(predicate, dict):
            issues.append(
                _raw_issue(raw_key, "format_invalid", f"predicate_body:{statement_index}")
            )
            predicate = {}
        statement_subjects = statement.get("subject")
        if not isinstance(statement_subjects, list):
            issues.append(_raw_issue(raw_key, "format_invalid", f"subjects:{statement_index}"))
            continue
        for subject in statement_subjects:
            if isinstance(subject, dict):
                subjects.append((subject, statement))
            else:
                issues.append(_raw_issue(raw_key, "format_invalid", f"subject:{statement_index}"))
        run_details = predicate.get("runDetails", {})
        if not isinstance(run_details, dict):
            run_details = {}
        if not run_details:
            build_definition = predicate.get("buildDefinition", {})
            if isinstance(build_definition, dict):
                run_details = build_definition.get("runDetails", {})
        if not isinstance(run_details, dict):
            run_details = {}
        statement_byproducts = run_details.get("byproducts", []) if isinstance(run_details, dict) else []
        if isinstance(statement_byproducts, list):
            byproducts.extend(
                item for item in statement_byproducts if isinstance(item, dict)
            )
    observations = batch.get("observations", [])
    declared_indexes: set[int] = set()
    raw_subject_digests: set[str] = set()
    for observation_index, (subject_record, _statement) in enumerate(subjects):
        name = subject_record.get("name")
        subject_digest = (
            subject_record.get("digest", {}).get("sha256")
            if isinstance(subject_record.get("digest"), dict)
            else None
        )
        digest_hex = _digest_hex(subject_digest)
        if not isinstance(name, str) or digest_hex is None:
            issues.append(_raw_issue(raw_key, "format_invalid", f"subject_identity:{observation_index}"))
            continue
        raw_subject_digests.add(digest_hex)
        observation = (
            observations[observation_index]
            if observation_index < len(observations)
            and isinstance(observations[observation_index], dict)
            else {}
        )
        semantic_key = observation.get("semantic_key")
        match = (
            re.fullmatch(r"provenance:subject:(\d+):(.+)", semantic_key)
            if isinstance(semantic_key, str)
            else None
        )
        subject = observation.get("subject", {})
        if not isinstance(subject, dict):
            subject = {}
        if match is None:
            issues.append(_raw_issue(raw_key, "content_mismatch", f"semantic_key:{observation_index}"))
            continue
        subject_index = int(match.group(1))
        if subject_index in declared_indexes or subject_index != observation_index:
            issues.append(_raw_issue(raw_key, "content_mismatch", f"subject_ref:{observation_index}"))
        declared_indexes.add(subject_index)
        source_digest = _digest_hex(batch.get("source", {}).get("content_digest"))
        if (
            match.group(2) != name
            or subject.get("label") != name
            or subject.get("qualified_name") != name
            or source_digest is None
            or source_digest != digest_hex
        ):
            issues.append(_raw_issue(raw_key, "content_mismatch", f"subject_identity:{observation_index}"))
    if len(observations) != len(subjects) or declared_indexes != set(range(len(subjects))):
        issues.append(_raw_issue(raw_key, "content_mismatch", "subject_coverage"))

    artifact_digest = _digest_hex(artifact.get("sha256"))
    if artifact_digest is not None and artifact_digest not in raw_subject_digests:
        issues.append(_raw_issue(raw_key, "content_mismatch", "artifact_subject_digest"))
    expected_subject_digest = _digest_hex(artifact.get("subject_digest"))
    byproduct_digests: set[str] = set()
    for item in byproducts:
        digest_record = item.get("digest")
        if isinstance(digest_record, dict):
            digest = _digest_hex(digest_record.get("sha256"))
            if digest is not None:
                byproduct_digests.add(digest)
    if expected_subject_digest is not None and expected_subject_digest not in byproduct_digests:
        issues.append(_raw_issue(raw_key, "content_mismatch", "artifact_byproduct_digest"))
    return issues


def _raw_markdown_issues(batch: dict[str, Any], document_text: str) -> list[str]:
    raw_key = "document_markdown"
    if not document_text.strip() or "\x00" in document_text:
        return [_raw_issue(raw_key, "format_invalid", "document_text")]
    headings: list[tuple[int, str]] = []
    for line_number, line in enumerate(document_text.splitlines(), start=1):
        match = re.match(r"^#{1,6}[ \t]+(.+?)[ \t]*#*[ \t]*$", line)
        if match:
            label = match.group(1).strip()
            if label:
                headings.append((line_number, label))
    if not headings:
        return [_raw_issue(raw_key, "format_invalid", "headings_empty")]

    issues: list[str] = []
    observations = batch.get("observations", [])
    declared_indexes: set[int] = set()
    for observation_index, observation in enumerate(observations):
        if not isinstance(observation, dict):
            issues.append(
                _raw_issue(raw_key, "content_mismatch", f"observation:{observation_index}")
            )
            continue
        semantic_key = observation.get("semantic_key")
        match = (
            re.fullmatch(r"document:(\d+):heading:([0-9a-f]{16})", semantic_key)
            if isinstance(semantic_key, str)
            else None
        )
        if match is None:
            issues.append(_raw_issue(raw_key, "content_mismatch", f"semantic_key:{observation_index}"))
            continue
        heading_index = int(match.group(1))
        if heading_index in declared_indexes or heading_index >= len(headings):
            issues.append(_raw_issue(raw_key, "content_mismatch", f"heading_ref:{observation_index}"))
            continue
        declared_indexes.add(heading_index)
        line_number, label = headings[heading_index]
        subject = observation.get("subject", {})
        if not isinstance(subject, dict):
            subject = {}
        occurrence = observation.get("occurrence", {})
        if not isinstance(occurrence, dict):
            occurrence = {}
        if (
            match.group(2) != hashlib.sha256(label.encode("utf-8")).hexdigest()[:16]
            or subject.get("label") != label
            or subject.get("symbol_kind") != "heading"
            or not isinstance(subject.get("qualified_name"), str)
            or not subject["qualified_name"].endswith(f"#{heading_index}")
            or occurrence.get("start_line") != line_number
            or occurrence.get("end_line") != line_number
        ):
            issues.append(_raw_issue(raw_key, "content_mismatch", f"heading_identity:{observation_index}"))
    if len(observations) != len(headings) or declared_indexes != set(range(len(headings))):
        issues.append(_raw_issue(raw_key, "content_mismatch", "heading_coverage"))
    return issues


def _raw_format_issues(
    key: str,
    batch: dict[str, Any],
    raw_path: Path,
    artifact: dict[str, Any],
) -> list[str]:
    raw_key = RAW_EVIDENCE_KEYS[key]
    try:
        raw_bytes = raw_path.read_bytes()
        raw_text = raw_bytes.decode("utf-8")
    except (OSError, UnicodeDecodeError):
        return [_raw_issue(raw_key, "format_invalid", "utf8")]
    if key == "static_security":
        try:
            document = json.loads(raw_text)
        except json.JSONDecodeError:
            return [_raw_issue(raw_key, "format_invalid", "json")]
        return _raw_sarif_issues(batch, document)
    if key == "software_components":
        try:
            document = json.loads(raw_text)
        except json.JSONDecodeError:
            return [_raw_issue(raw_key, "format_invalid", "json")]
        return _raw_sbom_issues(batch, document)
    if key == "artifact_provenance":
        return _raw_in_toto_issues(batch, raw_text, artifact)
    return _raw_markdown_issues(batch, raw_text)


def _provider_execution_issues(
    key: str,
    batch: dict[str, Any],
    providers: Any,
    raw_evidence: Any,
    packet_path: Path,
    artifact: dict[str, Any],
) -> list[str]:
    """Require provenance that the advertised provider output really exists.

    The batch itself carries the normalized observation, but a positive
    adjacent-provider result also claims actual candidate output.  Keep that
    claim bound to a provider version/configuration, parser provenance, and a
    digest-bearing raw output reference.  An empty top-level provider map must
    therefore never be enough for a positive result.
    """

    provider_id, _capability_class = EXPECTED[key]
    issues: list[str] = []
    provider = batch.get("provider", {})
    provider_meta = providers.get(provider_id) if isinstance(providers, dict) else None
    if not isinstance(provider_meta, dict):
        issues.append(f"provider_provenance_missing:{provider_id}")
    else:
        runtime_version = provider_meta.get("version")
        batch_version = provider.get("version")
        if not isinstance(runtime_version, str) or not runtime_version.strip():
            issues.append(f"provider_version_missing:{provider_id}")
        elif not isinstance(batch_version, str) or not batch_version.strip():
            issues.append(f"provider_version_missing:{provider_id}")
        elif _normalize_provider_version(runtime_version, provider_id) != _normalize_provider_version(
            batch_version, provider_id
        ):
            issues.append(f"provider_version_mismatch:{provider_id}")
        if not isinstance(provider_meta.get("runtime_posture"), str) or not provider_meta[
            "runtime_posture"
        ].strip():
            issues.append(f"provider_runtime_posture_missing:{provider_id}")

    config_digest = provider.get("config_digest")
    if not isinstance(config_digest, str) or _DIGEST_RE.fullmatch(config_digest) is None:
        issues.append(f"provider_config_missing:{provider_id}")
    lane = provider.get("lane")
    if not isinstance(lane, dict) or lane.get("id") != provider_id:
        issues.append(f"provider_lane_identity_missing:{provider_id}")
    currentness = batch.get("currentness")
    if not isinstance(currentness, dict) or currentness.get("provider") != {
        "id": provider_id,
        "version": provider.get("version"),
        "config_digest": config_digest,
    }:
        issues.append(f"provider_currentness_mismatch:{provider_id}")

    provenance = batch.get("provenance")
    if not isinstance(provenance, dict):
        issues.append(f"provider_execution_provenance_missing:{provider_id}")
    else:
        for field in ("extractor_ref", "parser_ref"):
            value = provenance.get(field)
            if not isinstance(value, str) or not value.strip():
                issues.append(f"provider_execution_{field}_missing:{provider_id}")
        source_refs = provenance.get("source_refs")
        if not isinstance(source_refs, list) or not source_refs:
            issues.append(f"provider_execution_source_refs_missing:{provider_id}")

    raw_key = RAW_EVIDENCE_KEYS[key]
    raw_ref = raw_evidence.get(raw_key) if isinstance(raw_evidence, dict) else None
    if not isinstance(raw_ref, dict):
        issues.append(f"raw_evidence_missing:{raw_key}")
    else:
        declared_path = raw_ref.get("path")
        raw_path, path_issue = _raw_evidence_path(packet_path, declared_path)
        if path_issue == "path_unsafe":
            issues.append(f"raw_evidence_path_unsafe:{raw_key}")
        elif path_issue == "file_missing":
            issues.append(f"raw_evidence_file_missing:{raw_key}")
        if _RAW_DIGEST_RE.fullmatch(str(raw_ref.get("sha256", ""))) is None:
            issues.append(f"raw_evidence_digest_missing:{raw_key}")
        elif raw_path is not None:
            try:
                if _raw_evidence_digest(raw_path) != raw_ref["sha256"]:
                    issues.append(f"raw_evidence_digest_mismatch:{raw_key}")
            except OSError:
                issues.append(f"raw_evidence_file_unreadable:{raw_key}")
        if raw_path is not None:
            issues.extend(_raw_format_issues(key, batch, raw_path, artifact))
    return issues


def _observation_issue(key: str, observation: Any) -> str | None:
    if not isinstance(observation, dict):
        return "not_object"
    capability_class, symbol_kinds, semantic_prefix = OBSERVATION_CONTRACT[key]
    if observation.get("capability_class") != capability_class:
        return "capability_class"
    if (
        observation.get("observation_kind") != "symbol"
        or observation.get("relation") is not None
    ):
        return "observation_kind"
    if (
        not isinstance(observation.get("observation_id"), str)
        or not observation["observation_id"]
    ):
        return "observation_id"
    semantic_key = observation.get("semantic_key")
    if not isinstance(semantic_key, str) or not semantic_key.startswith(
        semantic_prefix
    ):
        return "semantic_key"
    subject = observation.get("subject")
    if not isinstance(subject, dict) or any(
        not isinstance(subject.get(field), str) or not subject[field]
        for field in ("label", "qualified_name", "symbol_id", "symbol_kind")
    ):
        return "subject"
    if subject["symbol_kind"] not in symbol_kinds:
        return "subject_kind"
    occurrence = observation.get("occurrence")
    coordinate_fields = ("start_line", "start_column", "end_line", "end_column")
    if not isinstance(occurrence, dict) or any(
        not isinstance(occurrence.get(field), int) or occurrence[field] < 1
        for field in coordinate_fields
    ):
        return "occurrence"
    if (occurrence["end_line"], occurrence["end_column"]) < (
        occurrence["start_line"],
        occurrence["start_column"],
    ):
        return "occurrence_order"
    confidence = observation.get("confidence")
    value = confidence.get("value") if isinstance(confidence, dict) else None
    if (
        not isinstance(confidence, dict)
        or confidence.get("evidence_class") != "observed"
        or isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not 0 < value <= 1
    ):
        return "confidence"
    return None


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _digest(value: Any) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(encoded).hexdigest()


def validate(path: Path) -> dict[str, Any]:
    payload = _load(path)
    schema_errors = sorted(
        Draft202012Validator(
            _load(SCHEMA_PATH), format_checker=FormatChecker()
        ).iter_errors(payload),
        key=lambda error: list(error.absolute_path),
    )
    issues = [
        "schema:"
        + "/".join(str(part) for part in error.absolute_path)
        + ":"
        + error.message
        for error in schema_errors
    ]
    evidence: dict[str, Any] = {}
    if not schema_errors:
        if payload.get("claim_limits") != CLAIM_LIMITS:
            issues.append("claim_limits_mismatch")
        for key, (provider_id, capability_class) in EXPECTED.items():
            batch = payload["batches"][key]
            provider = batch.get("provider", {})
            source = batch.get("source", {})
            qualification = batch.get("qualification", {})
            admission = qualification.get("machine_admission", {})
            if provider.get("id") != provider_id:
                issues.append(f"provider_identity_mismatch:{key}")
            if batch.get("capability_class") != capability_class:
                issues.append(f"capability_class_mismatch:{key}")
            if (
                provider.get("lane", {}).get("status") != "supplied_unadmitted"
                or admission.get("state") != "not_admitted"
            ):
                issues.append(f"provider_not_bounded:{provider_id}")
            issues.extend(
                _source_identity_issues(
                    batch,
                    provider_id,
                    payload.get("source_epoch"),
                    path,
                )
            )
            count = len(batch.get("observations", []))
            if count < 1:
                issues.append(f"observation_missing:{provider_id}")
            for observation_index, observation in enumerate(
                batch.get("observations", [])
            ):
                observation_issue = _observation_issue(key, observation)
                if observation_issue is not None:
                    issues.append(
                        f"invalid_observation:{provider_id}:{observation_index}:{observation_issue}"
                    )
            issues.extend(
                _provider_execution_issues(
                    key,
                    batch,
                    payload.get("providers"),
                    payload.get("raw_evidence"),
                    path,
                    payload.get("artifact", {}),
                )
            )
            evidence[key] = {
                "provider_id": provider_id,
                "capability_class": capability_class,
                "observation_count": count,
            }
        summary = payload.get("summary", {})
        if summary.get("all_provider_lanes_unadmitted") is not True:
            issues.append("summary_admission_posture_mismatch")
        if payload.get("artifact", {}).get("admission_status") != "not_admitted":
            issues.append("artifact_admission_overclaim")
    issues = sorted(set(issues))
    return {
        "schema_version": "aoa_adjacent_provider_envelope_evidence_result_v1",
        "evidence_digest": _digest(payload),
        "evidence": evidence,
        "issues": issues,
        "verdict": (
            "supports bounded adjacent-provider envelope evidence"
            if not issues
            else "does not support bounded adjacent-provider envelope evidence"
        ),
        "claim_limit": (
            "The result supports actual output presence and common-envelope integrity for the supplied exact packet only; "
            "it is not artifact admission, deployed runtime health, provider completeness, landing, or owner acceptance."
        ),
    }
