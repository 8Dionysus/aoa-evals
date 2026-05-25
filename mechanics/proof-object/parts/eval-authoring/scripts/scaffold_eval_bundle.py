#!/usr/bin/env python3
"""Route-first scaffold helper for aoa-evals source eval bundles."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Sequence

import jsonschema
import yaml


REPO_ROOT = Path(__file__).resolve().parents[5]
PART_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = PART_ROOT / "schemas" / "eval-need.schema.json"
CATALOG_PATH = "generated/eval_catalog.min.json"
COMPARISON_FAMILY_BY_BASELINE_MODE = {
    "fixed-baseline": ("comparison", "fixed-baseline"),
    "peer-compare": ("comparison", "peer-compare"),
    "longitudinal-window": ("comparison", "longitudinal-window"),
}
STOPWORDS = {
    "about",
    "after",
    "agent",
    "before",
    "being",
    "bundle",
    "bundles",
    "candidate",
    "claim",
    "does",
    "eval",
    "evidence",
    "from",
    "into",
    "need",
    "proof",
    "review",
    "route",
    "surface",
    "that",
    "this",
    "through",
    "when",
    "with",
    "workflow",
}
CANONICAL_HEADINGS = (
    "Intent",
    "Object under evaluation",
    "Bounded claim",
    "Trigger boundary",
    "Inputs",
    "Fixtures and case surface",
    "Scoring or verdict logic",
    "Baseline or comparison mode",
    "Execution contract",
    "Outputs",
    "Failure modes",
    "Blind spots",
    "Interpretation guidance",
    "Verification",
    "Technique traceability",
    "Skill traceability",
    "Adaptation points",
)


class ScaffoldError(RuntimeError):
    """Raised when the proposal cannot produce a safe scaffold result."""


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate an eval_need_v1 packet and optionally scaffold a draft source eval bundle."
    )
    parser.add_argument("--proposal", required=True, help="Path to eval_need_v1 JSON packet.")
    parser.add_argument("--repo-root", default=REPO_ROOT.as_posix(), help="aoa-evals repo root.")
    parser.add_argument(
        "--allow-new",
        action="store_true",
        help="Allow a new draft bundle when no existing route is required.",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write scaffold files. Without this, the helper returns a dry-run plan.",
    )
    parser.add_argument("--json", action="store_true", help="Emit machine-readable result.")
    return parser.parse_args(argv)


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ScaffoldError(f"{path}: invalid JSON: {exc}") from exc


def validate_proposal(proposal: Any) -> list[str]:
    schema = load_json(SCHEMA_PATH)
    validator = jsonschema.Draft202012Validator(schema)
    errors = sorted(
        validator.iter_errors(proposal),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    messages: list[str] = []
    for error in errors:
        location = ".".join(str(part) for part in error.absolute_path)
        if location:
            messages.append(f"{location}: {error.message}")
        else:
            messages.append(error.message)
    return messages


def load_catalog(repo_root: Path) -> tuple[list[dict[str, Any]], list[str]]:
    catalog_path = repo_root / CATALOG_PATH
    if not catalog_path.is_file():
        return [], [f"{CATALOG_PATH} is missing; duplicate checks are reduced"]
    payload = load_json(catalog_path)
    if not isinstance(payload, dict):
        raise ScaffoldError(f"{CATALOG_PATH}: catalog payload must be an object")
    entries = payload.get("evals")
    if not isinstance(entries, list):
        raise ScaffoldError(f"{CATALOG_PATH}: .evals must be a list")
    return [entry for entry in entries if isinstance(entry, dict)], []


def tokens_from(value: Any) -> set[str]:
    if value is None:
        return set()
    text = json.dumps(value, sort_keys=True) if isinstance(value, (dict, list)) else str(value)
    tokens = {
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if len(token) >= 4 and token not in STOPWORDS
    }
    return tokens


def score_existing_match(proposal: dict[str, Any], entry: dict[str, Any]) -> tuple[int, list[str]]:
    score = 0
    reasons: list[str] = []
    entry_name = str(entry.get("name", ""))
    related = set(proposal.get("related_eval_refs") or [])

    if entry_name == proposal.get("name"):
        score += 100
        reasons.append("same eval name already exists")
    if entry_name in related:
        score += 80
        reasons.append("proposal names this eval as related")
    for field_name, weight in (
        ("category", 8),
        ("claim_type", 5),
        ("baseline_mode", 5),
        ("report_format", 3),
    ):
        if entry.get(field_name) == proposal.get(field_name):
            score += weight
            reasons.append(f"same {field_name}")

    proposal_tokens = tokens_from(
        [
            proposal.get("proof_question"),
            proposal.get("origin_need"),
            proposal.get("summary"),
            proposal.get("object_under_evaluation"),
            proposal.get("expected_use_when"),
            proposal.get("blind_spot_notes"),
        ]
    )
    entry_tokens = tokens_from(
        [
            entry.get("name"),
            entry.get("summary"),
            entry.get("object_under_evaluation"),
            entry.get("category"),
        ]
    )
    overlap = sorted(proposal_tokens & entry_tokens)
    if overlap:
        token_score = min(36, len(overlap) * 4)
        score += token_score
        reasons.append("token overlap: " + ", ".join(overlap[:6]))

    return score, reasons


def find_existing_matches(
    proposal: dict[str, Any],
    catalog_entries: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    for entry in catalog_entries:
        score, reasons = score_existing_match(proposal, entry)
        if score < 16:
            continue
        matches.append(
            {
                "name": entry.get("name"),
                "score": score,
                "category": entry.get("category"),
                "status": entry.get("status"),
                "eval_path": entry.get("eval_path"),
                "reasons": reasons,
            }
        )
    return sorted(matches, key=lambda item: (-int(item["score"]), str(item["name"])))[:8]


def target_bundle_dir(repo_root: Path, proposal: dict[str, Any]) -> Path:
    baseline_mode = str(proposal["baseline_mode"])
    family = COMPARISON_FAMILY_BY_BASELINE_MODE.get(baseline_mode)
    if family is None:
        family = (str(proposal["category"]),)
    return repo_root / "evals" / Path(*family) / str(proposal["name"])


def technique_ids(proposal: dict[str, Any]) -> list[str]:
    return [
        str(item["id"])
        for item in proposal.get("technique_dependencies", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    ]


def skill_names(proposal: dict[str, Any]) -> list[str]:
    return [
        str(item["name"])
        for item in proposal.get("skill_dependencies", [])
        if isinstance(item, dict) and isinstance(item.get("name"), str)
    ]


def frontmatter_for(proposal: dict[str, Any]) -> dict[str, Any]:
    frontmatter: dict[str, Any] = {
        "name": proposal["name"],
        "category": proposal["category"],
        "status": "draft",
        "summary": proposal["summary"],
        "object_under_evaluation": proposal["object_under_evaluation"],
        "claim_type": proposal["claim_type"],
        "baseline_mode": proposal["baseline_mode"],
        "report_format": proposal["report_format"],
        "technique_dependencies": technique_ids(proposal),
        "skill_dependencies": skill_names(proposal),
    }
    comparison_surface = proposal.get("comparison_surface")
    if comparison_surface is not None:
        frontmatter["comparison_surface"] = comparison_surface
    return frontmatter


def manifest_for(proposal: dict[str, Any]) -> dict[str, Any]:
    manifest: dict[str, Any] = {
        "name": proposal["name"],
        "category": proposal["category"],
        "status": "draft",
        "object_under_evaluation": proposal["object_under_evaluation"],
        "claim_type": proposal["claim_type"],
        "baseline_mode": proposal["baseline_mode"],
        "verdict_shape": proposal.get("verdict_shape", "categorical"),
        "report_format": proposal["report_format"],
        "maturity_score": 1,
        "rigor_level": "bounded",
        "repeatability": "moderate",
        "portability_level": "local-shaped",
        "review_required": True,
        "validation_strength": "baseline",
        "export_ready": True,
        "blind_spot_disclosure": "required-and-present",
        "score_interpretation_bound": "explicit",
        "technique_dependencies": proposal.get("technique_dependencies", []),
        "skill_dependencies": proposal.get("skill_dependencies", []),
        "comparison_surface": proposal.get("comparison_surface"),
        "relations": [
            {"type": "complements", "target": ref}
            for ref in proposal.get("related_eval_refs", [])
            if ref != proposal["name"]
        ],
        "evidence": [
            {"kind": "origin_need", "path": "notes/origin-need.md"},
            {"kind": "integrity_check", "path": "checks/eval-integrity-check.md"},
        ],
    }
    return manifest


def bullet_list(items: Sequence[Any], fallback: str) -> str:
    values = [str(item).strip() for item in items if str(item).strip()]
    if not values:
        values = [fallback]
    return "\n".join(f"- {value}" for value in values)


def section_bodies(proposal: dict[str, Any]) -> dict[str, str]:
    use_when = bullet_list(proposal.get("expected_use_when", []), "the bounded proof question matches this object")
    blind_spots = bullet_list(proposal.get("blind_spot_notes", []), "broader capability outside this bounded claim")
    source_refs = bullet_list(proposal.get("source_refs", []), "source refs still need review")
    candidate_refs = bullet_list(
        proposal.get("candidate_evidence_refs", []),
        "candidate evidence refs still need review",
    )
    quest_refs = bullet_list(proposal.get("quest_refs", []), "no quest refs named")
    baseline_mode = proposal["baseline_mode"]
    comparison_sentence = (
        "No comparison surface is claimed yet."
        if baseline_mode == "none"
        else f"The proposed comparison mode is `{baseline_mode}` and still requires bundle-local review."
    )
    return {
        "Intent": (
            f"{proposal['proof_question']}\n\n"
            "This is a draft source proof object scaffold. It is diagnostic until bundle-local review says otherwise."
        ),
        "Object under evaluation": (
            f"{proposal['object_under_evaluation']}\n\n"
            "Nearby source, runtime, quest, and generated-reader surfaces stay subordinate to this bundle's reviewed claim."
        ),
        "Bounded claim": (
            f"Under the named conditions, this eval can support only this bounded claim: {proposal['summary']}\n\n"
            "This draft does not support broad intelligence, general safety, trust, or autonomous-self claims."
        ),
        "Trigger boundary": (
            "Use this eval when:\n"
            f"{use_when}\n\n"
            "Do not use this eval when:\n"
            "- an existing source eval already owns the bounded question\n"
            "- raw runtime evidence has not been reduced to a public-safe candidate packet\n"
            "- the pressure is still only a quest obligation"
        ),
        "Inputs": (
            "- bounded proof question\n"
            "- source bundle or proposal context\n"
            "- public-safe evidence refs when available\n"
            "- bundle-local reviewer judgment\n\n"
            "Candidate evidence refs:\n"
            f"{candidate_refs}\n\n"
            "Quest refs:\n"
            f"{quest_refs}"
        ),
        "Fixtures and case surface": (
            "The fixture surface is not materialized yet. Draft authoring must name public-safe cases before promotion."
        ),
        "Scoring or verdict logic": (
            "The draft verdict is categorical and review-led: support, mixed support, unsupported, or not reviewable."
        ),
        "Baseline or comparison mode": comparison_sentence,
        "Execution contract": (
            "Run only after the source bundle, support artifacts, and evidence refs are reviewable. "
            "Do not treat scaffold creation as execution proof."
        ),
        "Outputs": (
            "- bounded draft report outline\n"
            "- bundle-local review notes\n"
            "- evidence acceptance or rejection notes after review"
        ),
        "Failure modes": (
            "- duplicate bundle for an existing proof surface\n"
            "- runtime evidence accepted before bundle-local review\n"
            "- vague quest pressure promoted too early\n"
            "- scaffold text mistaken for proof"
        ),
        "Blind spots": (
            "This eval does not prove:\n"
            f"{blind_spots}"
        ),
        "Interpretation guidance": (
            "Treat any future positive result as support for one bounded claim.\n\n"
            "Do not treat a positive result as:\n"
            "- evidence acceptance without bundle-local review\n"
            "- a runtime health verdict\n"
            "- a public starter recommendation\n"
            "- proof that neighboring evals are unnecessary"
        ),
        "Verification": (
            "- confirm the bounded claim is explicit\n"
            "- confirm existing eval routes were inspected first\n"
            "- confirm candidate evidence stayed candidate-only\n"
            "- confirm origin need and integrity check evidence resolve publicly\n"
            "- run the proof-object validation lane before promotion\n\n"
            "Source refs:\n"
            f"{source_refs}"
        ),
        "Technique traceability": bullet_list(technique_ids(proposal), "none yet"),
        "Skill traceability": bullet_list(skill_names(proposal), "none yet"),
        "Adaptation points": (
            "- local fixtures\n"
            "- local runners\n"
            "- bundle-local report schema\n"
            "- candidate evidence review packets"
        ),
    }


def render_eval_markdown(proposal: dict[str, Any]) -> str:
    sections = section_bodies(proposal)
    parts = [
        "---",
        yaml.safe_dump(frontmatter_for(proposal), sort_keys=False).strip(),
        "---",
        "",
        f"# {proposal['name']}",
    ]
    for heading in CANONICAL_HEADINGS:
        parts.extend(["", f"## {heading}", "", sections[heading]])
    return "\n".join(parts).rstrip() + "\n"


def render_origin_need(proposal: dict[str, Any]) -> str:
    return (
        "# Origin Need\n\n"
        f"{proposal['origin_need']}\n\n"
        "## Proof Question\n\n"
        f"{proposal['proof_question']}\n\n"
        "## Route Posture\n\n"
        "This note records pre-authoring pressure only. It is not proof acceptance.\n"
    )


def render_integrity_check(proposal: dict[str, Any]) -> str:
    return (
        "# Eval Integrity Check\n\n"
        "- source eval route checked before authoring\n"
        "- origin need recorded\n"
        "- blind spots named\n"
        "- candidate evidence remains below bundle-local review\n"
        "- public starter posture not changed by this scaffold\n\n"
        f"Initial route: `{proposal['authoring_route']}`.\n"
    )


def planned_files(bundle_dir: Path) -> dict[Path, str]:
    return {
        bundle_dir / "EVAL.md": "eval markdown",
        bundle_dir / "eval.yaml": "eval manifest",
        bundle_dir / "notes" / "origin-need.md": "origin need evidence",
        bundle_dir / "checks" / "eval-integrity-check.md": "integrity check evidence",
    }


def write_scaffold(bundle_dir: Path, proposal: dict[str, Any]) -> list[str]:
    if bundle_dir.exists():
        raise ScaffoldError(f"{bundle_dir}: target bundle directory already exists")
    files = {
        bundle_dir / "EVAL.md": render_eval_markdown(proposal),
        bundle_dir / "eval.yaml": yaml.safe_dump(manifest_for(proposal), sort_keys=False),
        bundle_dir / "notes" / "origin-need.md": render_origin_need(proposal),
        bundle_dir / "checks" / "eval-integrity-check.md": render_integrity_check(proposal),
    }
    for path, text in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return [path.as_posix() for path in files]


def route_result(
    *,
    proposal: dict[str, Any],
    repo_root: Path,
    allow_new: bool,
    write: bool,
) -> dict[str, Any]:
    validation_errors = validate_proposal(proposal)
    if validation_errors:
        return {
            "schema_version": "eval_birth_route_result_v1",
            "outcome": "invalid_proposal",
            "proposal_name": proposal.get("name") if isinstance(proposal, dict) else None,
            "errors": validation_errors,
        }

    catalog_entries, route_notes = load_catalog(repo_root)
    matches = find_existing_matches(proposal, catalog_entries)
    target_dir = target_bundle_dir(repo_root, proposal)
    target_relative = target_dir.relative_to(repo_root).as_posix()
    authoring_route = proposal["authoring_route"]

    if authoring_route != "new_draft_bundle":
        return {
            "schema_version": "eval_birth_route_result_v1",
            "outcome": authoring_route,
            "proposal_name": proposal["name"],
            "target_path": target_relative,
            "existing_matches": matches,
            "route_notes": [
                *route_notes,
                "proposal did not request a new source bundle scaffold",
            ],
            "created_paths": [],
        }

    exact_conflicts = [match for match in matches if match["name"] == proposal["name"]]
    if exact_conflicts:
        return {
            "schema_version": "eval_birth_route_result_v1",
            "outcome": "existing_route_required",
            "proposal_name": proposal["name"],
            "target_path": target_relative,
            "existing_matches": exact_conflicts,
            "route_notes": [
                *route_notes,
                "same eval name already exists; source bundle must be inspected or edited instead",
            ],
            "created_paths": [],
        }

    if matches and not allow_new:
        return {
            "schema_version": "eval_birth_route_result_v1",
            "outcome": "existing_route_required",
            "proposal_name": proposal["name"],
            "target_path": target_relative,
            "existing_matches": matches,
            "route_notes": [
                *route_notes,
                "inspect likely existing routes before authoring a parallel draft",
            ],
            "created_paths": [],
        }

    if not allow_new:
        return {
            "schema_version": "eval_birth_route_result_v1",
            "outcome": "new_draft_requires_allow_new",
            "proposal_name": proposal["name"],
            "target_path": target_relative,
            "existing_matches": matches,
            "route_notes": [
                *route_notes,
                "no blocking existing route found; pass --allow-new after review to prepare a draft scaffold",
            ],
            "created_paths": [],
        }

    if target_dir.exists():
        return {
            "schema_version": "eval_birth_route_result_v1",
            "outcome": "target_exists",
            "proposal_name": proposal["name"],
            "target_path": target_relative,
            "existing_matches": matches,
            "route_notes": [
                *route_notes,
                "target source bundle path already exists",
            ],
            "created_paths": [],
        }

    if not write:
        return {
            "schema_version": "eval_birth_route_result_v1",
            "outcome": "dry_run_new_draft",
            "proposal_name": proposal["name"],
            "target_path": target_relative,
            "existing_matches": matches,
            "route_notes": [
                *route_notes,
                "dry run only; pass --write to create scaffold files",
            ],
            "created_paths": [path.relative_to(repo_root).as_posix() for path in planned_files(target_dir)],
        }

    created_paths = write_scaffold(target_dir, proposal)
    return {
        "schema_version": "eval_birth_route_result_v1",
        "outcome": "created_new_draft",
        "proposal_name": proposal["name"],
        "target_path": target_relative,
        "existing_matches": matches,
        "route_notes": [
            *route_notes,
            "draft scaffold created; run validate_repo.py and build_catalog.py --check after review",
        ],
        "created_paths": [Path(path).relative_to(repo_root).as_posix() for path in created_paths],
    }


def print_text_result(result: dict[str, Any]) -> None:
    print(f"outcome: {result['outcome']}")
    if result.get("target_path"):
        print(f"target_path: {result['target_path']}")
    for match in result.get("existing_matches", []):
        print(f"match: {match['name']} score={match['score']} path={match.get('eval_path')}")
    for note in result.get("route_notes", []):
        print(f"note: {note}")
    for error in result.get("errors", []):
        print(f"error: {error}")
    for path in result.get("created_paths", []):
        print(f"path: {path}")


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = Path(args.repo_root).resolve()
    proposal_path = Path(args.proposal)
    if not proposal_path.is_absolute():
        proposal_path = Path.cwd() / proposal_path
    try:
        proposal = load_json(proposal_path)
        if not isinstance(proposal, dict):
            raise ScaffoldError(f"{proposal_path}: proposal must be a JSON object")
        result = route_result(
            proposal=proposal,
            repo_root=repo_root,
            allow_new=args.allow_new,
            write=args.write,
        )
    except ScaffoldError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print_text_result(result)
    return 1 if result.get("outcome") == "invalid_proposal" else 0


if __name__ == "__main__":
    raise SystemExit(main())
