#!/usr/bin/env python3
"""Return bounded aoa-evals owner, routing, and source-contract packets.

This helper is intentionally read-only.  The compact generated catalog may
route selection, but source EVAL.md and eval.yaml remain authoritative.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


CATALOG_RELATIVE_PATH = Path("generated/eval_catalog.min.json")
PORT_MANIFEST_RELATIVE_PATH = Path("skills/port.manifest.json")
SOURCE_RECEIPT_NAME = ".aoa-skill-source.json"
SOURCE_BUNDLE_RELATIVE_PATH = Path("skills/aoa-evals")
READINESS_RELATIVE_PATH = Path("docs/guides/EVAL_FORGE_READINESS_LAYER.md")
CANDIDATE_PACKET_ROOT = Path(
    "mechanics/audit/parts/candidate-readers/packets"
)
SOURCE_SECTION_NAMES = (
    "Intent",
    "Object under evaluation",
    "Bounded claim",
    "Trigger boundary",
    "Blind spots",
    "Interpretation guidance",
)
CATALOG_FIELDS = (
    "name",
    "summary",
    "object_under_evaluation",
    "category",
    "status",
    "claim_type",
    "baseline_mode",
    "eval_path",
)
MANIFEST_SCALAR_FIELDS = (
    "name",
    "category",
    "status",
    "object_under_evaluation",
    "claim_type",
    "baseline_mode",
    "verdict_shape",
    "report_format",
    "maturity_score",
    "rigor_level",
    "repeatability",
    "portability_level",
    "review_required",
    "validation_strength",
    "export_ready",
    "blind_spot_disclosure",
    "score_interpretation_bound",
)
QUERY_TEXT_FIELDS = (
    ("name", 4),
    ("summary", 4),
    ("object_under_evaluation", 3),
    ("category", 1),
    ("claim_type", 1),
    ("status", 1),
)
QUERY_TOKEN = re.compile(r"[a-z0-9]+")
EVAL_NAME_REF = re.compile(r"`(aoa-[a-z0-9-]+)`")


class PacketError(RuntimeError):
    """A bounded packet cannot be produced from the declared owner."""


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _owner_path(owner_root: Path, relative_path: Path) -> Path:
    if relative_path.is_absolute() or ".." in relative_path.parts:
        raise PacketError(f"unsafe owner-relative path: {relative_path}")
    path = (owner_root / relative_path).resolve()
    try:
        path.relative_to(owner_root)
    except ValueError as exc:
        raise PacketError(f"path escapes owner root: {relative_path}") from exc
    if not path.is_file():
        raise PacketError(f"required owner file is missing: {relative_path}")
    return path


def _load_json(path: Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PacketError(f"{label} is unreadable") from exc
    if not isinstance(payload, dict):
        raise PacketError(f"{label} must contain a JSON object")
    return payload


def _load_owner(
    owner_root_value: Path,
) -> tuple[Path, dict[str, Any], dict[str, Any]]:
    owner_root = owner_root_value.expanduser().resolve()
    if not owner_root.is_dir():
        raise PacketError("owner root must be an existing absolute directory")

    port_path = _owner_path(owner_root, PORT_MANIFEST_RELATIVE_PATH)
    port = _load_json(port_path, "owner skill port manifest")
    if port.get("owner_repo") != "aoa-evals":
        raise PacketError("owner skill port manifest does not belong to aoa-evals")
    bundles = port.get("bundles")
    if not isinstance(bundles, list) or not any(
        isinstance(bundle, dict)
        and bundle.get("name") == "aoa-evals"
        and bundle.get("path") == "skills/aoa-evals"
        for bundle in bundles
    ):
        raise PacketError("owner skill port manifest does not admit skills/aoa-evals")

    catalog_path = _owner_path(owner_root, CATALOG_RELATIVE_PATH)
    catalog = _load_json(catalog_path, "generated eval catalog")
    if not isinstance(catalog.get("evals"), list):
        raise PacketError("generated eval catalog has no eval list")
    return owner_root, port, catalog


def _safe_source_bundle(owner_root: Path, source_path_value: str) -> Path:
    source_path = Path(source_path_value)
    if (
        source_path != SOURCE_BUNDLE_RELATIVE_PATH
        or source_path.is_absolute()
        or ".." in source_path.parts
    ):
        raise PacketError("source receipt names an unexpected bundle path")
    source_bundle = (owner_root / source_path).resolve()
    try:
        source_bundle.relative_to(owner_root)
    except ValueError as exc:
        raise PacketError("source receipt bundle path escapes owner root") from exc
    if not source_bundle.is_dir() or not (source_bundle / "SKILL.md").is_file():
        raise PacketError("source receipt bundle is missing its SKILL.md")
    return source_bundle


def _resolve_owner(
    owner_root_text: str | None,
) -> tuple[Path, dict[str, Any], dict[str, Any], dict[str, Any]]:
    bundle_dir = Path(__file__).resolve().parent.parent

    if owner_root_text:
        explicit_root = Path(owner_root_text).expanduser()
        if not explicit_root.is_absolute():
            raise PacketError("explicit owner root must be absolute")
        owner_root, port, catalog = _load_owner(explicit_root)
        _safe_source_bundle(owner_root, str(SOURCE_BUNDLE_RELATIVE_PATH))
        return owner_root, port, catalog, {
            "route": "explicit-owner-root",
            "bundle_dir": str(bundle_dir),
            "owner_root": str(owner_root),
            "source_path": str(SOURCE_BUNDLE_RELATIVE_PATH),
            "claim_limit": (
                "explicit local owner route; owner authority and current parity "
                "remain bounded by the inspected source and manifest"
            ),
        }

    receipt_path = bundle_dir / SOURCE_RECEIPT_NAME
    if receipt_path.exists():
        if not receipt_path.is_file():
            raise PacketError("same-bundle source receipt is not a regular file")
        receipt = _load_json(receipt_path, "same-bundle source receipt")
        required = {
            "schema_version": "aoa_skill_source_receipt_v1",
            "name": "aoa-evals",
            "owner_repo": "aoa-evals",
            "source_path": str(SOURCE_BUNDLE_RELATIVE_PATH),
        }
        for field, expected in required.items():
            if receipt.get(field) != expected:
                raise PacketError(
                    f"same-bundle source receipt has unexpected {field}"
                )
        owner_root_value = receipt.get("owner_root")
        if (
            not isinstance(owner_root_value, str)
            or not Path(owner_root_value).is_absolute()
        ):
            raise PacketError("same-bundle source receipt lacks absolute owner_root")
        owner_root, port, catalog = _load_owner(Path(owner_root_value))
        _safe_source_bundle(owner_root, str(receipt["source_path"]))
        return owner_root, port, catalog, {
            "route": "source-receipt",
            "receipt_path": str(receipt_path),
            "owner_root": str(owner_root),
            "owner_ref": receipt.get("owner_ref"),
            "owner_dirty": receipt.get("owner_dirty"),
            "source_path": receipt.get("source_path"),
            "version": receipt.get("version"),
            "digest": receipt.get("digest"),
            "claim_limit": receipt.get("claim_limit"),
        }

    owner_root_candidate = bundle_dir.parent.parent.resolve()
    expected_bundle = (
        owner_root_candidate / SOURCE_BUNDLE_RELATIVE_PATH
    ).resolve()
    if bundle_dir != expected_bundle:
        raise PacketError(
            "same-bundle source receipt is missing outside the canonical owner home"
        )
    owner_root, port, catalog = _load_owner(owner_root_candidate)
    _safe_source_bundle(owner_root, str(SOURCE_BUNDLE_RELATIVE_PATH))
    return owner_root, port, catalog, {
        "route": "canonical-owner-home",
        "bundle_dir": str(bundle_dir),
        "owner_root": str(owner_root),
        "source_path": str(SOURCE_BUNDLE_RELATIVE_PATH),
        "claim_limit": (
            "canonical source-home route; package location does not itself prove "
            "any eval claim or installed-copy parity"
        ),
    }


def _compact_card(entry: dict[str, Any]) -> dict[str, Any]:
    return {field: entry.get(field) for field in CATALOG_FIELDS}


def _query_terms(query: str) -> list[str]:
    return list(dict.fromkeys(QUERY_TOKEN.findall(query.casefold())))


def _route_score(entry: dict[str, Any], query_terms: list[str]) -> tuple[int, list[str]]:
    score = 0
    matched: set[str] = set()
    for field, weight in QUERY_TEXT_FIELDS:
        value = entry.get(field)
        if not isinstance(value, str):
            continue
        field_terms = set(QUERY_TOKEN.findall(value.casefold()))
        for term in query_terms:
            if term in field_terms:
                score += weight
                matched.add(term)
    return score, sorted(matched)


def _source_neighbor_hints(
    owner_root: Path,
    entry: dict[str, Any],
    known_names: set[str],
) -> list[str]:
    eval_path_value = entry.get("eval_path")
    current_name = entry.get("name")
    if not isinstance(eval_path_value, str) or not isinstance(current_name, str):
        return []
    eval_text = _owner_path(owner_root, Path(eval_path_value)).read_text(
        encoding="utf-8"
    )
    sections = _markdown_sections(eval_text)
    relevant_text = "\n".join(
        sections.get(name, "")
        for name in ("Intent", "Blind spots", "Interpretation guidance")
    )
    hints: list[str] = []
    for candidate in EVAL_NAME_REF.findall(relevant_text):
        if (
            candidate != current_name
            and candidate in known_names
            and candidate not in hints
        ):
            hints.append(candidate)
    return hints


def _markdown_sections(text: str) -> dict[str, str]:
    wanted = {name.casefold(): name for name in SOURCE_SECTION_NAMES}
    found: dict[str, list[str]] = {}
    current: str | None = None
    for line in text.splitlines():
        match = re.match(r"^##\s+(.+?)\s*$", line)
        if match:
            normalized = match.group(1).strip().casefold()
            current = wanted.get(normalized)
            if current is not None:
                found[current] = []
            continue
        if current is not None:
            found[current].append(line)
    return {
        name: "\n".join(found[name]).strip()
        for name in SOURCE_SECTION_NAMES
        if name in found
    }


def _manifest_scalars(text: str) -> dict[str, Any]:
    allowed = set(MANIFEST_SCALAR_FIELDS)
    scalars: dict[str, Any] = {}
    for line in text.splitlines():
        match = re.match(r"^([a-z][a-z0-9_]*)\s*:\s*(.*?)\s*$", line)
        if not match or match.group(1) not in allowed:
            continue
        key, raw_value = match.groups()
        if raw_value in {"true", "false"}:
            value: Any = raw_value == "true"
        elif re.fullmatch(r"-?[0-9]+", raw_value):
            value = int(raw_value)
        else:
            value = raw_value
        scalars[key] = value
    return scalars


def _catalog_packet(
    owner_root: Path,
    catalog: dict[str, Any],
    source_route: dict[str, Any],
    query: str | None,
    limit: int,
) -> dict[str, Any]:
    source_entries = [
        entry for entry in catalog["evals"] if isinstance(entry, dict)
    ]
    known_names = {
        entry["name"]
        for entry in source_entries
        if isinstance(entry.get("name"), str)
    }
    query_terms = _query_terms(query or "")
    entries: list[dict[str, Any]] = []
    matched_entry_count = 0
    if query_terms:
        scored: list[tuple[int, str, dict[str, Any], list[str]]] = []
        for entry in source_entries:
            score, matched = _route_score(entry, query_terms)
            if score > 0:
                scored.append(
                    (score, str(entry.get("name", "")), entry, matched)
                )
        scored.sort(key=lambda row: (-row[0], row[1]))
        matched_entry_count = len(scored)
        for score, _name, entry, matched in scored[:limit]:
            card = _compact_card(entry)
            card["route_score"] = score
            card["matched_terms"] = matched
            card["source_neighbor_hints"] = _source_neighbor_hints(
                owner_root, entry, known_names
            )
            entries.append(card)
        route_status = "matched" if entries else "no_match"
    else:
        entries = [_compact_card(entry) for entry in source_entries]
        entries.sort(key=lambda entry: str(entry.get("name", "")))
        route_status = "full_catalog"
    return {
        "schema_version": "aoa_evals_skill_route_catalog_v1",
        "owner_root": str(owner_root),
        "owner_source": source_route,
        "route_source": str(CATALOG_RELATIVE_PATH),
        "route_source_kind": (
            "generated_shortlist_with_source_neighbor_hints"
            if query_terms
            else "generated_compact_reader"
        ),
        "route_status": route_status,
        "query": query,
        "query_terms": query_terms,
        "catalog_version": catalog.get("catalog_version"),
        "total_entry_count": len(source_entries),
        "returned_entry_count": len(entries),
        "truncated": bool(query_terms and matched_entry_count > limit),
        "entries": entries,
        "claim_limit": (
            "lexical routing shortlist only; score is not semantic fit or proof; "
            "neighbor hints are source-derived navigation, not fit; source "
            "EVAL.md and eval.yaml must support the selected fit, neighbor "
            "rejection, and proof ceiling"
        ),
    }


def _contract_packet(
    owner_root: Path,
    catalog: dict[str, Any],
    source_route: dict[str, Any],
    names: list[str],
) -> dict[str, Any]:
    if not names or len(names) > 2:
        raise PacketError("contract mode requires one or two exact eval names")
    if len(set(names)) != len(names):
        raise PacketError("contract names must be unique")

    by_name = {
        entry.get("name"): entry
        for entry in catalog["evals"]
        if isinstance(entry, dict) and isinstance(entry.get("name"), str)
    }
    packets: list[dict[str, Any]] = []
    for name in names:
        entry = by_name.get(name)
        if entry is None:
            raise PacketError(f"unknown exact eval name: {name}")
        eval_path_value = entry.get("eval_path")
        if not isinstance(eval_path_value, str):
            raise PacketError(f"catalog entry has no eval_path: {name}")
        eval_relative = Path(eval_path_value)
        eval_path = _owner_path(owner_root, eval_relative)
        manifest_relative = eval_relative.with_name("eval.yaml")
        manifest_path = _owner_path(owner_root, manifest_relative)
        eval_text = eval_path.read_text(encoding="utf-8")
        manifest_text = manifest_path.read_text(encoding="utf-8")
        sections = _markdown_sections(eval_text)
        missing_sections = [
            section for section in SOURCE_SECTION_NAMES if section not in sections
        ]
        if missing_sections:
            raise PacketError(
                f"{name} lacks required source sections: {', '.join(missing_sections)}"
            )
        manifest = _manifest_scalars(manifest_text)
        if manifest.get("name") != name:
            raise PacketError(f"source manifest name mismatch for {name}")
        packets.append(
            {
                "name": name,
                "catalog_card": _compact_card(entry),
                "source_eval_path": str(eval_relative),
                "source_eval_sha256": _sha256(eval_path),
                "source_manifest_path": str(manifest_relative),
                "source_manifest_sha256": _sha256(manifest_path),
                "source_manifest": manifest,
                "source_sections": sections,
            }
        )
    return {
        "schema_version": "aoa_evals_skill_source_contract_packet_v1",
        "owner_root": str(owner_root),
        "owner_source": source_route,
        "contracts": packets,
        "claim_limit": (
            "bounded selection/rejection evidence only; execution, report, "
            "maturity, and proof verdict require their own source and evidence reads"
        ),
    }


def _source_packet(
    owner_root: Path,
    port: dict[str, Any],
    source_route: dict[str, Any],
) -> dict[str, Any]:
    bundle_version: str | None = None
    for bundle in port.get("bundles", []):
        if (
            isinstance(bundle, dict)
            and bundle.get("name") == "aoa-evals"
            and bundle.get("path") == str(SOURCE_BUNDLE_RELATIVE_PATH)
        ):
            version = bundle.get("version")
            if isinstance(version, str):
                bundle_version = version
            break
    return {
        "schema_version": "aoa_evals_skill_owner_source_v1",
        "owner_root": str(owner_root),
        "owner_source": source_route,
        "owner_manifest_path": str(PORT_MANIFEST_RELATIVE_PATH),
        "source_bundle_path": str(SOURCE_BUNDLE_RELATIVE_PATH),
        "source_bundle_version": bundle_version,
        "owner_route_path": "AGENTS.md",
        "claim_limit": (
            "validated owner-source return only; this packet does not select an "
            "eval, accept evidence, establish a verdict, or authorize a change"
        ),
    }


def _review_context_packet(
    owner_root: Path,
    port: dict[str, Any],
    source_route: dict[str, Any],
    report_value: str | None,
    packet_id: str,
) -> dict[str, Any]:
    readiness_path = _owner_path(owner_root, READINESS_RELATIVE_PATH)

    packet_root = (owner_root / CANDIDATE_PACKET_ROOT).resolve()
    try:
        packet_root.relative_to(owner_root)
    except ValueError as exc:
        raise PacketError("candidate packet root escapes owner root") from exc
    if not packet_root.is_dir():
        raise PacketError("candidate packet root is missing")

    matches: list[tuple[Path, dict[str, Any]]] = []
    for candidate_path in sorted(packet_root.rglob("*.json")):
        try:
            candidate = _load_json(candidate_path, "candidate packet")
        except PacketError:
            continue
        if candidate.get("packet_id") == packet_id:
            matches.append((candidate_path, candidate))
    if len(matches) != 1:
        raise PacketError(
            f"expected exactly one candidate packet for {packet_id}, found {len(matches)}"
        )
    candidate_path, candidate = matches[0]
    candidate_relative = candidate_path.relative_to(owner_root)

    if report_value is not None:
        report_relative = Path(report_value)
        if report_relative.suffix != ".md":
            raise PacketError(
                "review report must be an owner-relative Markdown file"
            )
        report_path = _owner_path(owner_root, report_relative)
        report_route = "explicit-report"
    else:
        report_candidates: list[tuple[Path, Path]] = []
        evidence_refs = candidate.get("evidence_refs")
        if not isinstance(evidence_refs, list):
            raise PacketError("candidate packet has no evidence_refs list")
        for ref in evidence_refs:
            if not isinstance(ref, str):
                continue
            path_text = ref.partition("#")[0]
            relative = Path(path_text)
            if (
                relative.is_absolute()
                or ".." in relative.parts
                or not relative.name.endswith(".manual-review.md")
            ):
                continue
            try:
                path = _owner_path(owner_root, relative)
            except PacketError:
                continue
            pair = (relative, path)
            if pair not in report_candidates:
                report_candidates.append(pair)
        if len(report_candidates) != 1:
            raise PacketError(
                "candidate packet must declare exactly one existing "
                "*.manual-review.md evidence ref when --report is omitted; "
                f"found {len(report_candidates)}"
            )
        report_relative, report_path = report_candidates[0]
        report_route = "packet-evidence-ref"

    report_text = report_path.read_text(encoding="utf-8")
    if packet_id not in report_text:
        raise PacketError("review report does not mention the exact candidate packet")

    explicit_source_bundle_fields: dict[str, Any] = {}
    for field in (
        "source_eval_path",
        "source_bundle_path",
        "source_bundle",
        "accepted_source_bundle",
        "source_bundle_refs",
    ):
        value = candidate.get(field)
        if value not in (None, "", []):
            explicit_source_bundle_fields[field] = value

    source_packet = _source_packet(owner_root, port, source_route)
    return {
        "schema_version": "aoa_evals_skill_review_context_v1",
        "owner_root": str(owner_root),
        "owner_source": source_route,
        "source_bundle_version": source_packet["source_bundle_version"],
        "packet_id": packet_id,
        "report_route": report_route,
        "material_paths": {
            "owner_route": source_packet["owner_route_path"],
            "readiness_contract": str(READINESS_RELATIVE_PATH),
            "review_report": str(report_relative),
            "candidate_packet": str(candidate_relative),
        },
        "material_sha256": {
            "readiness_contract": _sha256(readiness_path),
            "review_report": _sha256(report_path),
            "candidate_packet": _sha256(candidate_path),
        },
        "candidate_route_fields": {
            "candidate_only": candidate.get("candidate_only"),
            "proof_authority": candidate.get("proof_authority"),
            "promotion_allowed": candidate.get("promotion_allowed"),
            "candidate_state": candidate.get("candidate_state"),
            "promotion_forbidden_until": candidate.get(
                "promotion_forbidden_until"
            ),
            "explicit_source_bundle_fields": explicit_source_bundle_fields,
            "explicit_source_bundle_link_status": (
                "present" if explicit_source_bundle_fields else "absent"
            ),
        },
        "claim_limit": (
            "exact owner and material-path navigation plus copied candidate route "
            "fields only; read the returned owner files for proof meaning, report "
            "interpretation, evidence acceptance, and disposition"
        ),
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Read bounded aoa-evals owner-source, routing, or source-contract "
            "packets."
        )
    )
    parser.add_argument(
        "--owner-root",
        help=(
            "explicit canonical owner root for direct owner-home use; installed "
            "copies resolve their same-bundle source receipt automatically"
        ),
    )
    subparsers = parser.add_subparsers(dest="mode", required=True)
    subparsers.add_parser("source")
    review_context = subparsers.add_parser("review-context")
    review_context.add_argument("--report")
    review_context.add_argument("--packet-id", required=True)
    catalog = subparsers.add_parser("catalog")
    catalog.add_argument("--query")
    catalog.add_argument("--limit", type=int, default=8)
    contracts = subparsers.add_parser("contracts")
    contracts.add_argument("--name", action="append", required=True)
    return parser


def main() -> int:
    args = _parser().parse_args()
    try:
        if getattr(args, "limit", 1) < 1:
            raise PacketError("catalog limit must be positive")
        owner_root, port, catalog, source_route = _resolve_owner(args.owner_root)
        if args.mode == "source":
            packet = _source_packet(owner_root, port, source_route)
        elif args.mode == "review-context":
            packet = _review_context_packet(
                owner_root,
                port,
                source_route,
                args.report,
                args.packet_id,
            )
        elif args.mode == "catalog":
            packet = _catalog_packet(
                owner_root,
                catalog,
                source_route,
                args.query,
                args.limit,
            )
        else:
            packet = _contract_packet(
                owner_root,
                catalog,
                source_route,
                args.name,
            )
    except PacketError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(
        json.dumps(
            packet,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
