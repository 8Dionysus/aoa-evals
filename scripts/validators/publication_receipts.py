"""Publication receipt payload, live-log, and intake dry-review contracts."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable, Mapping

import yaml
from jsonschema import Draft202012Validator, SchemaError


STATS_EVENT_ENVELOPE_SCHEMA_NAME = "stats-event-envelope.schema.json"
EVAL_RESULT_RECEIPT_SCHEMA_NAME = "eval-result-receipt.schema.json"
PUBLICATION_RECEIPTS_PARTS_ROOT = "mechanics/publication-receipts/parts"
STATS_EVENT_ENVELOPE_SCHEMA_PATH = (
    f"{PUBLICATION_RECEIPTS_PARTS_ROOT}/stats-envelope-mirror/schemas/{STATS_EVENT_ENVELOPE_SCHEMA_NAME}"
)
EVAL_RESULT_RECEIPT_SCHEMA_PATH = (
    f"{PUBLICATION_RECEIPTS_PARTS_ROOT}/receipt-payload/schemas/{EVAL_RESULT_RECEIPT_SCHEMA_NAME}"
)
EVAL_RESULT_RECEIPT_GUIDE_NAME = (
    f"{PUBLICATION_RECEIPTS_PARTS_ROOT}/receipt-payload/docs/EVAL_RESULT_RECEIPT_GUIDE.md"
)
EVAL_RESULT_RECEIPT_EXAMPLE_NAME = (
    f"{PUBLICATION_RECEIPTS_PARTS_ROOT}/receipt-payload/examples/eval_result_receipt.example.json"
)
EVAL_RESULT_RECEIPT_PUBLISHER_NAME = (
    f"{PUBLICATION_RECEIPTS_PARTS_ROOT}/live-publisher/scripts/publish_live_receipts.py"
)
LIVE_EVAL_RECEIPT_LOG_NAME = ".aoa/live_receipts/eval-result-receipts.jsonl"
PROOF_LOOP_LOCAL_REPORT_NAME = (
    "evals/workflow/aoa-verification-honesty/reports/"
    "aoa-evals-slice-19-lifecycle-contract.report.json"
)
RECEIPT_INTAKE_DRY_REVIEW_NAME = (
    "mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json"
)
RECEIPT_INTAKE_DRY_REVIEW_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0024-receipt-intake-dry-review.md"
)
PROOF_LOOP_MECHANIC_README_NAME = "mechanics/proof-loop/README.md"
PUBLICATION_RECEIPTS_MECHANIC_README_NAME = "mechanics/publication-receipts/README.md"
PUBLICATION_RECEIPTS_MECHANIC_AGENTS_NAME = "mechanics/publication-receipts/AGENTS.md"
PUBLICATION_RECEIPTS_MECHANIC_PROVENANCE_NAME = "mechanics/publication-receipts/PROVENANCE.md"
PUBLICATION_RECEIPTS_RECEIPT_PAYLOAD_PART_README_NAME = (
    f"{PUBLICATION_RECEIPTS_PARTS_ROOT}/receipt-payload/README.md"
)
PUBLICATION_RECEIPTS_STATS_ENVELOPE_PART_README_NAME = (
    f"{PUBLICATION_RECEIPTS_PARTS_ROOT}/stats-envelope-mirror/README.md"
)
PUBLICATION_RECEIPTS_LIVE_PUBLISHER_PART_README_NAME = (
    f"{PUBLICATION_RECEIPTS_PARTS_ROOT}/live-publisher/README.md"
)
PUBLICATION_RECEIPTS_INTAKE_DRY_REVIEW_PART_README_NAME = (
    f"{PUBLICATION_RECEIPTS_PARTS_ROOT}/intake-dry-review/README.md"
)
PUBLICATION_RECEIPTS_PART_CONTRACT_GUARD_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0057-publication-receipts-part-contract-guard.md"
)
PUBLICATION_RECEIPTS_MECHANIC_DECISION_NAME = (
    "docs/decisions/AOA-EV-D-0013-publication-receipts-mechanic-package.md"
)
PUBLICATION_RECEIPTS_LEGACY_INDEX_NAME = "mechanics/publication-receipts/legacy/INDEX.md"
PUBLICATION_RECEIPTS_LEGACY_DISTILLATION_LOG_NAME = (
    "mechanics/publication-receipts/legacy/DISTILLATION_LOG.md"
)
PUBLICATION_RECEIPTS_LEGACY_RAW_README_NAME = (
    "mechanics/publication-receipts/legacy/raw/README.md"
)
EVAL_REPORT_INDEX_NAME = "generated/eval_report_index.min.json"
SOURCE_EVALS_DIR_NAME = "evals"
SCHEMAS_DIR_NAME = "schemas"
REPO_REF_PREFIX = "repo:"
DECISION_RECORDS_README_NAME = "docs/decisions/README.md"
DECISION_INDEX_PATHS = (
    Path("docs/decisions/indexes/by-number.md"),
    Path("docs/decisions/indexes/by-date.md"),
    Path("docs/decisions/indexes/by-surface.md"),
    Path("docs/decisions/indexes/by-mechanic.md"),
    Path("docs/decisions/indexes/by-validation-guard.md"),
)
PART_README_PATH_RE = re.compile(r"^mechanics/([^/]+)/parts/([^/]+)/README\.md$")
MECHANIC_PARENT_README_PATH_RE = re.compile(r"^mechanics/([^/]+)/README\.md$")
RFC3339_DATE_TIME_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}[Tt]\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:[Zz]|[+-]\d{2}:\d{2})$"
)
FORMAT_CHECKER = Draft202012Validator.FORMAT_CHECKER


@FORMAT_CHECKER.checks("date-time", raises=(ValueError,))
def _is_date_time(value: object) -> bool:
    if not isinstance(value, str):
        return True
    if RFC3339_DATE_TIME_RE.fullmatch(value) is None:
        return False
    normalized = value[:-1] + "+00:00" if value[-1:].lower() == "z" else value
    normalized = normalized.replace("t", "T", 1)
    parsed = datetime.fromisoformat(normalized)
    return parsed.tzinfo is not None and parsed.utcoffset() is not None


EVAL_RESULT_RECEIPT_REQUIRED_TOKENS = (
    "## Core Rule",
    "`eval_result_receipt`",
    "`stats-event-envelope`",
    "`supersedes`",
    "meaning stays with bundle-local review",
    "repo-global score",
    "## Receipt Pressure Routes",
    "Proof-canon pressure routes",
)
RECEIPT_INTAKE_DRY_REVIEW_REQUIRED_TOKENS = (
    "receipt_intake_dry_review",
    "candidate_payload_preview",
    "eval-result-receipt.schema.json",
    "stats-event-envelope.schema.json",
    "publish_live_receipts.py",
    ".aoa/live_receipts/eval-result-receipts.jsonl",
    "dry_review_only",
    "not_published",
    "not_created",
    "not_attempted",
    "publication pressure routes to a receipt envelope",
    "runtime acceptance pressure",
)
RECEIPT_INTAKE_DRY_REVIEW_DECISION_REQUIRED_TOKENS = (
    RECEIPT_INTAKE_DRY_REVIEW_NAME,
    "eval_result_receipt",
    "stats-event-envelope",
    ".aoa/live_receipts/",
    "candidate_payload_preview",
    "event_id",
    "dry review is weaker than a receipt",
    "Do not infer that an eval result receipt was published",
)
MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS = (
    "`PROVENANCE.md` is the active-to-archive bridge for this mechanic.",
    "Use active surfaces first:",
    "DIRECTION.md",
    "PARTS.md",
    "parts/",
    "legacy archive",
    "legacy/README.md",
    "owns its own details",
    "archive details stay in the legacy archive",
)
PUBLICATION_RECEIPTS_MECHANIC_REQUIRED_TOKENS = (
    "Owned Operation",
    "mechanics/publication-receipts/parts/receipt-payload/docs/EVAL_RESULT_RECEIPT_GUIDE.md",
    "mechanics/publication-receipts/parts/receipt-payload/schemas/eval-result-receipt.schema.json",
    "mechanics/publication-receipts/parts/stats-envelope-mirror/schemas/stats-event-envelope.schema.json",
    "mechanics/publication-receipts/parts/receipt-payload/examples/eval_result_receipt.example.json",
    "mechanics/publication-receipts/parts/live-publisher/scripts/publish_live_receipts.py",
    "mechanics/publication-receipts/parts/live-publisher/tests/test_publish_live_receipts.py",
    "mechanics/publication-receipts/parts/live-publisher/tests/test_live_receipt_log.py",
    "mechanics/publication-receipts/parts/intake-dry-review/tests/test_receipt_intake_dry_review.py",
    ".aoa/live_receipts/eval-result-receipts.jsonl",
    "eval_result_receipt",
    "stats-event-envelope",
    "optional receipt",
    "bundle-local verdict meaning",
    "repo-global score",
    "python scripts/validate_repo.py",
    "python scripts/validate_semantic_agents.py",
)
PUBLICATION_RECEIPTS_MECHANIC_AGENTS_REQUIRED_TOKENS = (
    "eval-result receipt",
    "stats-event-envelope",
    ".aoa/live_receipts/",
    "bundle-local report",
    "aoa-stats",
    "append-only",
    "public-safe",
    "python scripts/validate_repo.py",
)
PUBLICATION_RECEIPTS_MECHANIC_DECISION_REQUIRED_TOKENS = (
    "mechanics/publication-receipts/",
    "eval-result receipt",
    "stats-envelope-mirror",
    "aoa-stats",
    "does not move `.aoa/live_receipts/`",
    "bundle-local report",
    "repo-global score",
)
PUBLICATION_RECEIPTS_MECHANIC_PROVENANCE_REQUIRED_TOKENS = MECHANIC_PROVENANCE_BRIDGE_POSTURE_REQUIRED_TOKENS
PUBLICATION_RECEIPTS_LEGACY_INDEX_REQUIRED_TOKENS = (
    "docs/EVAL_RESULT_RECEIPT_GUIDE.md",
    "mechanics/publication-receipts/parts/receipt-payload/docs/EVAL_RESULT_RECEIPT_GUIDE.md",
    "schemas/eval-result-receipt.schema.json",
    "mechanics/publication-receipts/parts/receipt-payload/schemas/eval-result-receipt.schema.json",
    "scripts/publish_live_receipts.py",
    "mechanics/publication-receipts/parts/live-publisher/scripts/publish_live_receipts.py",
    "reports/eval-result-receipt-intake-dry-review-v1.json",
    "mechanics/publication-receipts/parts/intake-dry-review/reports/eval-result-receipt-intake-dry-review-v1.json",
    ".aoa/live_receipts/eval-result-receipts.jsonl",
)
PUBLICATION_RECEIPTS_LEGACY_DISTILLATION_REQUIRED_TOKENS = (
    "publication-receipts",
    "receipt-payload",
    "stats-envelope-mirror",
    "live-publisher",
    "intake-dry-review",
    "Current route:",
    "new publication-receipt work starts in the owning active part",
)
PUBLICATION_RECEIPTS_LEGACY_RAW_README_REQUIRED_TOKENS = (
    "No raw payload copies",
    "git history",
    "active publication-receipts",
)
PUBLICATION_RECEIPTS_PART_README_COMMON_TOKENS = (
    "## Inputs",
    "## Outputs",
    "## Stronger Owner Split",
    "## Stop-Lines",
    "## Validation",
    "python scripts/validate_repo.py",
)
PUBLICATION_RECEIPTS_RECEIPT_PAYLOAD_PART_REQUIRED_TOKENS = (
    "Receipt Payload Part",
    "eval_result_receipt",
    "schemas/eval-result-receipt.schema.json",
    "examples/eval_result_receipt.example.json",
    "reviewed bounded report",
    "source bundle",
    "The payload is a publication sidecar",
    "schema-valid payload reads as a published receipt",
) + PUBLICATION_RECEIPTS_PART_README_COMMON_TOKENS
PUBLICATION_RECEIPTS_STATS_ENVELOPE_PART_REQUIRED_TOKENS = (
    "Stats Envelope Mirror Part",
    "schemas/stats-event-envelope.schema.json",
    "canonical `aoa-stats`",
    "event-kind vocabulary",
    "owner-local live receipt log",
    "dry-review artifacts",
    "mirror edit reads as canonical `aoa-stats` schema work",
) + PUBLICATION_RECEIPTS_PART_README_COMMON_TOKENS
PUBLICATION_RECEIPTS_LIVE_PUBLISHER_PART_REQUIRED_TOKENS = (
    "Live Publisher Part",
    "scripts/publish_live_receipts.py",
    "tests/test_publish_live_receipts.py",
    "tests/test_live_receipt_log.py",
    "append-only JSONL writes",
    "duplicate `event_id` skips",
    "dry-review payload preview looks publishable",
) + PUBLICATION_RECEIPTS_PART_README_COMMON_TOKENS
PUBLICATION_RECEIPTS_INTAKE_DRY_REVIEW_PART_REQUIRED_TOKENS = (
    "Intake Dry Review Part",
    "receipt_intake_dry_review",
    "candidate_payload_preview",
    "`receipt_status` stays",
    "`not_published`",
    "top-level `event_kind`, `event_id`, `observed_at`, `object_ref`,",
    "`.aoa/live_receipts/` append appears",
) + PUBLICATION_RECEIPTS_PART_README_COMMON_TOKENS
PUBLICATION_RECEIPTS_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS = (
    "Publication Receipts Part Contract Guard",
    "mechanics/publication-receipts/parts/receipt-payload/README.md",
    "mechanics/publication-receipts/parts/stats-envelope-mirror/README.md",
    "mechanics/publication-receipts/parts/live-publisher/README.md",
    "mechanics/publication-receipts/parts/intake-dry-review/README.md",
    "part-level contracts",
    "receipt-payload",
    "stats-envelope-mirror",
    "live-publisher",
    "intake-dry-review",
    "stronger owner split",
    "stop-lines",
    "not_published",
    "python scripts/validate_repo.py",
)


@dataclass(frozen=True)
class ValidationIssue:
    location: str
    message: str


def relative_location(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def format_schema_path(path_parts: Iterable[Any]) -> str:
    parts: list[str] = []
    for part in path_parts:
        if isinstance(part, int):
            parts.append(f"[{part}]")
        elif parts:
            parts.append(f".{part}")
        else:
            parts.append(str(part))
    return "".join(parts)


def read_text_or_issue(path: Path, issues: list[ValidationIssue], *, root: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path, root), "file is missing"))
        return ""


def markdown_heading_section(text: str, heading: str) -> str:
    marker = ""
    heading_level = 0
    start = -1
    for level in (3, 2):
        pattern = re.compile(rf"(?m)^{'#' * level} {re.escape(heading)}\s*$")
        match = pattern.search(text)
        if match:
            marker = match.group(0)
            heading_level = level
            start = match.start()
            break
    if start == -1:
        return ""
    next_h2 = text.find("\n## ", start + len(marker))
    next_h3 = text.find("\n### ", start + len(marker)) if heading_level > 2 else -1
    candidates = [index for index in (next_h2, next_h3) if index != -1]
    end = min(candidates) if candidates else len(text)
    return text[start:end]


def mechanic_parent_validation_route_text(repo_root: Path, readme_name: str) -> str:
    match = MECHANIC_PARENT_README_PATH_RE.match(readme_name)
    if match is None:
        return ""
    agents_path = repo_root / "mechanics" / match.group(1) / "AGENTS.md"
    if not agents_path.is_file():
        return ""
    return agents_path.read_text(encoding="utf-8")


def part_validation_route_text(repo_root: Path, readme_name: str) -> str:
    match = PART_README_PATH_RE.match(readme_name)
    if match is None:
        return ""
    parent_name, part_name = match.groups()
    part_relative = f"mechanics/{parent_name}/parts/{part_name}"
    validation_name = f"{part_relative}/VALIDATION.md"
    chunks: list[str] = []
    validation_path = repo_root / validation_name
    if validation_path.is_file():
        chunks.append(validation_path.read_text(encoding="utf-8"))
    agents_path = repo_root / "mechanics" / parent_name / "parts" / "AGENTS.md"
    if agents_path.is_file():
        agents_text = agents_path.read_text(encoding="utf-8")
        child_section = markdown_heading_section(agents_text, f"`{validation_name}`")
        if child_section:
            chunks.append(child_section)
    return "\n\n".join(chunks)


def require_tokens(
    *,
    repo_root: Path,
    path_name: str,
    tokens: Iterable[str],
    issues: list[ValidationIssue],
) -> str:
    path = repo_root / path_name
    text = read_text_or_issue(path, issues, root=repo_root)
    if not text:
        return ""
    search_text = text
    if path_name == DECISION_RECORDS_README_NAME:
        index_texts = []
        for relative_path in DECISION_INDEX_PATHS:
            index_path = repo_root / relative_path
            if index_path.is_file():
                index_texts.append(index_path.read_text(encoding="utf-8"))
        if index_texts:
            search_text = "\n\n".join((text, *index_texts))
    for token in tokens:
        token_search_text = search_text
        if PART_README_PATH_RE.match(path_name) and token.lstrip("`").startswith("python "):
            token_search_text = "\n\n".join((text, part_validation_route_text(repo_root, path_name)))
        elif MECHANIC_PARENT_README_PATH_RE.match(path_name) and token.lstrip("`").startswith("python "):
            token_search_text = "\n\n".join((text, mechanic_parent_validation_route_text(repo_root, path_name)))
        if token not in token_search_text:
            issues.append(ValidationIssue(path_name, f"file must mention '{token}'"))
    return text


def validate_publication_receipts_route_surfaces(repo_root: Path) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    for path_name, tokens in (
        (PUBLICATION_RECEIPTS_MECHANIC_README_NAME, PUBLICATION_RECEIPTS_MECHANIC_REQUIRED_TOKENS),
        (PUBLICATION_RECEIPTS_MECHANIC_AGENTS_NAME, PUBLICATION_RECEIPTS_MECHANIC_AGENTS_REQUIRED_TOKENS),
        (PUBLICATION_RECEIPTS_MECHANIC_PROVENANCE_NAME, PUBLICATION_RECEIPTS_MECHANIC_PROVENANCE_REQUIRED_TOKENS),
        (
            PUBLICATION_RECEIPTS_RECEIPT_PAYLOAD_PART_README_NAME,
            PUBLICATION_RECEIPTS_RECEIPT_PAYLOAD_PART_REQUIRED_TOKENS,
        ),
        (
            PUBLICATION_RECEIPTS_STATS_ENVELOPE_PART_README_NAME,
            PUBLICATION_RECEIPTS_STATS_ENVELOPE_PART_REQUIRED_TOKENS,
        ),
        (
            PUBLICATION_RECEIPTS_LIVE_PUBLISHER_PART_README_NAME,
            PUBLICATION_RECEIPTS_LIVE_PUBLISHER_PART_REQUIRED_TOKENS,
        ),
        (
            PUBLICATION_RECEIPTS_INTAKE_DRY_REVIEW_PART_README_NAME,
            PUBLICATION_RECEIPTS_INTAKE_DRY_REVIEW_PART_REQUIRED_TOKENS,
        ),
        (
            PUBLICATION_RECEIPTS_PART_CONTRACT_GUARD_DECISION_NAME,
            PUBLICATION_RECEIPTS_PART_CONTRACT_GUARD_DECISION_REQUIRED_TOKENS,
        ),
        (
            DECISION_RECORDS_README_NAME,
            (
                PUBLICATION_RECEIPTS_PART_CONTRACT_GUARD_DECISION_NAME,
                "Publication Receipts Part Contract Guard",
            ),
        ),
        (PUBLICATION_RECEIPTS_LEGACY_INDEX_NAME, PUBLICATION_RECEIPTS_LEGACY_INDEX_REQUIRED_TOKENS),
        (
            PUBLICATION_RECEIPTS_LEGACY_DISTILLATION_LOG_NAME,
            PUBLICATION_RECEIPTS_LEGACY_DISTILLATION_REQUIRED_TOKENS,
        ),
        (
            PUBLICATION_RECEIPTS_LEGACY_RAW_README_NAME,
            PUBLICATION_RECEIPTS_LEGACY_RAW_README_REQUIRED_TOKENS,
        ),
        (PUBLICATION_RECEIPTS_MECHANIC_DECISION_NAME, PUBLICATION_RECEIPTS_MECHANIC_DECISION_REQUIRED_TOKENS),
    ):
        require_tokens(repo_root=repo_root, path_name=path_name, tokens=tokens, issues=issues)
    return issues


def load_json_payload(path: Path, issues: list[ValidationIssue], *, root: Path) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path, root), "file is missing"))
        return None
    except json.JSONDecodeError as exc:
        issues.append(ValidationIssue(relative_location(path, root), f"invalid JSON: {exc}"))
        return None


def load_yaml_file(path: Path, issues: list[ValidationIssue], *, root: Path) -> Any | None:
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        issues.append(ValidationIssue(relative_location(path, root), "file is missing"))
        return None
    except yaml.YAMLError as exc:
        issues.append(ValidationIssue(relative_location(path, root), f"invalid YAML: {exc}"))
        return None


def validate_inline_schema(
    schema: object,
    *,
    location: str,
    issues: list[ValidationIssue],
) -> bool:
    if not isinstance(schema, dict):
        issues.append(ValidationIssue(location, "schema must parse to an object"))
        return False
    try:
        Draft202012Validator.check_schema(schema)
    except SchemaError as exc:
        issues.append(ValidationIssue(location, f"invalid JSON schema: {exc.message}"))
        return False
    return True


def get_schema_validator_with_format(schema: dict[str, Any]) -> Draft202012Validator:
    return Draft202012Validator(schema, format_checker=FORMAT_CHECKER)


def validate_against_schema(
    data: Any,
    schema_name: str,
    location: str,
    issues: list[ValidationIssue],
    *,
    validator: Draft202012Validator | None = None,
    fallback_repo_root: Path,
) -> bool:
    active_validator = validator
    if active_validator is None:
        schema_paths_by_name = {
            STATS_EVENT_ENVELOPE_SCHEMA_NAME: Path(STATS_EVENT_ENVELOPE_SCHEMA_PATH),
            EVAL_RESULT_RECEIPT_SCHEMA_NAME: Path(EVAL_RESULT_RECEIPT_SCHEMA_PATH),
        }
        schema_path = fallback_repo_root / schema_paths_by_name[schema_name]
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        active_validator = get_schema_validator_with_format(schema)

    schema_errors = sorted(
        active_validator.iter_errors(data),
        key=lambda error: (list(error.absolute_path), error.message),
    )
    for error in schema_errors:
        error_path = format_schema_path(error.absolute_path)
        if error_path:
            message = f"schema violation at '{error_path}': {error.message}"
        else:
            message = f"schema violation: {error.message}"
        issues.append(ValidationIssue(location, message))
    return not schema_errors


def parse_repo_ref(
    raw_ref: Any,
    *,
    location: str,
    issues: list[ValidationIssue],
    repo_ref_roots: Mapping[str, Path],
    strict_sibling_compat: bool,
) -> tuple[str, Path, str | None] | None:
    if not isinstance(raw_ref, str) or not raw_ref:
        issues.append(ValidationIssue(location, "reference must be a non-empty string"))
        return None
    if not raw_ref.startswith(REPO_REF_PREFIX):
        issues.append(ValidationIssue(location, "reference must start with 'repo:'"))
        return None

    payload = raw_ref[len(REPO_REF_PREFIX) :]
    if "/" not in payload:
        issues.append(
            ValidationIssue(location, "reference must include a repo name and repo-relative path")
        )
        return None

    repo_name, path_with_anchor = payload.split("/", 1)
    repo_root = repo_ref_roots.get(repo_name)
    if repo_root is None:
        issues.append(ValidationIssue(location, f"unknown repo in reference: '{repo_name}'"))
        return None

    path_text, _, anchor = path_with_anchor.partition("#")
    if not path_text:
        issues.append(ValidationIssue(location, "reference path must not be empty"))
        return None

    target = repo_root / path_text
    if repo_name != "aoa-evals" and not strict_sibling_compat:
        return repo_name, target, anchor or None
    if not repo_root.exists():
        issues.append(
            ValidationIssue(
                location,
                f"strict sibling compatibility requires available repo root for {repo_name}: {repo_root}",
            )
        )
        return None
    if not target.exists():
        issues.append(
            ValidationIssue(location, f"reference target does not exist: {repo_name}/{path_text}")
        )
        return None

    return repo_name, target, anchor or None


def discover_eval_dirs(repo_root: Path) -> dict[str, Path]:
    source_root = repo_root / SOURCE_EVALS_DIR_NAME
    if not source_root.is_dir():
        raise FileNotFoundError(f"missing source eval directory at {source_root}")

    eval_dirs: dict[str, Path] = {}
    for manifest_path in sorted(source_root.glob("**/eval.yaml")):
        eval_dir = manifest_path.parent
        eval_name = eval_dir.name
        if eval_name in eval_dirs:
            raise ValueError(
                "duplicate source eval directory name "
                f"'{eval_name}' at {relative_location(eval_dirs[eval_name], repo_root)} "
                f"and {relative_location(eval_dir, repo_root)}"
            )
        eval_dirs[eval_name] = eval_dir
    return eval_dirs


def source_eval_dir(repo_root: Path, eval_name: str) -> Path:
    try:
        return discover_eval_dirs(repo_root).get(
            eval_name,
            repo_root / SOURCE_EVALS_DIR_NAME / eval_name,
        )
    except (FileNotFoundError, ValueError):
        return repo_root / SOURCE_EVALS_DIR_NAME / eval_name


def validate_eval_result_receipt_surfaces(
    repo_root: Path,
    *,
    aoa_stats_root: Path,
    repo_ref_roots: Mapping[str, Path],
    strict_sibling_compat: bool,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    guide_path = repo_root / EVAL_RESULT_RECEIPT_GUIDE_NAME
    envelope_schema_path = repo_root / STATS_EVENT_ENVELOPE_SCHEMA_PATH
    payload_schema_path = repo_root / EVAL_RESULT_RECEIPT_SCHEMA_PATH
    example_path = repo_root / EVAL_RESULT_RECEIPT_EXAMPLE_NAME

    guide_text = read_text_or_issue(guide_path, issues, root=repo_root)
    if guide_text:
        for token in EVAL_RESULT_RECEIPT_REQUIRED_TOKENS:
            if token not in guide_text:
                issues.append(
                    ValidationIssue(
                        relative_location(guide_path, repo_root),
                        f"eval result receipt guide must mention '{token}'",
                    )
                )

    envelope_schema = load_json_payload(envelope_schema_path, issues, root=repo_root)
    envelope_validator: Draft202012Validator | None = None
    if isinstance(envelope_schema, dict):
        envelope_schema_valid = True
        if envelope_schema.get("title") != "aoa-evals stats event envelope":
            issues.append(
                ValidationIssue(
                    relative_location(envelope_schema_path, repo_root),
                    "stats event envelope schema title must be 'aoa-evals stats event envelope'",
                )
            )
            envelope_schema_valid = False
        canonical_schema_ref = envelope_schema.get("x-canonical_schema_ref")
        if canonical_schema_ref != "repo:aoa-stats/schemas/stats-event-envelope.schema.json":
            issues.append(
                ValidationIssue(
                    relative_location(envelope_schema_path, repo_root),
                    "stats event envelope mirror must point to repo:aoa-stats/schemas/stats-event-envelope.schema.json",
                )
            )
            envelope_schema_valid = False
        canonical_envelope_path = aoa_stats_root / SCHEMAS_DIR_NAME / STATS_EVENT_ENVELOPE_SCHEMA_NAME
        if canonical_envelope_path.exists():
            canonical_envelope = load_json_payload(canonical_envelope_path, issues, root=aoa_stats_root)
            if isinstance(canonical_envelope, dict):
                local_enum = (
                    envelope_schema.get("properties", {})
                    .get("event_kind", {})
                    .get("enum")
                )
                canonical_enum = (
                    canonical_envelope.get("properties", {})
                    .get("event_kind", {})
                    .get("enum")
                )
                if local_enum != canonical_enum:
                    issues.append(
                        ValidationIssue(
                            relative_location(envelope_schema_path, repo_root),
                            "stats event envelope mirror enum must match ../aoa-stats/schemas/stats-event-envelope.schema.json",
                        )
                    )
        try:
            Draft202012Validator.check_schema(envelope_schema)
        except SchemaError as exc:
            issues.append(
                ValidationIssue(
                    relative_location(envelope_schema_path, repo_root),
                    f"invalid JSON schema: {exc.message}",
                )
            )
            envelope_schema_valid = False
        if envelope_schema_valid:
            envelope_validator = get_schema_validator_with_format(envelope_schema)
    elif envelope_schema is not None:
        issues.append(
            ValidationIssue(
                relative_location(envelope_schema_path, repo_root),
                "stats event envelope schema must be a JSON object",
            )
        )

    payload_schema = load_json_payload(payload_schema_path, issues, root=repo_root)
    payload_validator: Draft202012Validator | None = None
    if isinstance(payload_schema, dict):
        payload_schema_valid = True
        if payload_schema.get("title") != "aoa-evals eval result receipt":
            issues.append(
                ValidationIssue(
                    relative_location(payload_schema_path, repo_root),
                    "eval result receipt schema title must be 'aoa-evals eval result receipt'",
                )
            )
            payload_schema_valid = False
        try:
            Draft202012Validator.check_schema(payload_schema)
        except SchemaError as exc:
            issues.append(
                ValidationIssue(
                    relative_location(payload_schema_path, repo_root),
                    f"invalid JSON schema: {exc.message}",
                )
            )
            payload_schema_valid = False
        if payload_schema_valid:
            payload_validator = get_schema_validator_with_format(payload_schema)
    elif payload_schema is not None:
        issues.append(
            ValidationIssue(
                relative_location(payload_schema_path, repo_root),
                "eval result receipt schema must be a JSON object",
            )
        )

    example_payload = load_json_payload(example_path, issues, root=repo_root)
    if isinstance(example_payload, dict):
        if envelope_validator is not None:
            validate_against_schema(
                example_payload,
                STATS_EVENT_ENVELOPE_SCHEMA_NAME,
                relative_location(example_path, repo_root),
                issues,
                validator=envelope_validator,
                fallback_repo_root=repo_root,
            )
        if example_payload.get("event_kind") != "eval_result_receipt":
            issues.append(
                ValidationIssue(
                    relative_location(example_path, repo_root),
                    "eval result receipt example must keep event_kind as 'eval_result_receipt'",
                )
            )

        object_ref = example_payload.get("object_ref")
        if isinstance(object_ref, dict):
            if object_ref.get("repo") != "aoa-evals":
                issues.append(
                    ValidationIssue(
                        relative_location(example_path, repo_root),
                        "eval result receipt example object_ref.repo must be 'aoa-evals'",
                    )
                )
            if object_ref.get("kind") != "eval_bundle":
                issues.append(
                    ValidationIssue(
                        relative_location(example_path, repo_root),
                        "eval result receipt example object_ref.kind must be 'eval_bundle'",
                    )
                )

        evidence_refs = example_payload.get("evidence_refs")
        seen_primary = False
        if isinstance(evidence_refs, list):
            for index, evidence_ref in enumerate(evidence_refs):
                if not isinstance(evidence_ref, dict):
                    continue
                ref = evidence_ref.get("ref")
                if isinstance(ref, str):
                    parse_repo_ref(
                        ref,
                        location=f"{relative_location(example_path, repo_root)}.evidence_refs[{index}].ref",
                        issues=issues,
                        repo_ref_roots=repo_ref_roots,
                        strict_sibling_compat=strict_sibling_compat,
                    )
                if evidence_ref.get("role") == "primary":
                    seen_primary = True
        if not seen_primary:
            issues.append(
                ValidationIssue(
                    relative_location(example_path, repo_root),
                    "eval result receipt example must include one primary evidence ref",
                )
            )

        payload = example_payload.get("payload")
        if isinstance(payload, dict):
            if payload_validator is not None:
                validate_against_schema(
                    payload,
                    EVAL_RESULT_RECEIPT_SCHEMA_NAME,
                    f"{relative_location(example_path, repo_root)}.payload",
                    issues,
                    validator=payload_validator,
                    fallback_repo_root=repo_root,
                )
            bundle_ref = payload.get("bundle_ref")
            if isinstance(bundle_ref, str):
                parse_repo_ref(
                    bundle_ref,
                    location=f"{relative_location(example_path, repo_root)}.payload.bundle_ref",
                    issues=issues,
                    repo_ref_roots=repo_ref_roots,
                    strict_sibling_compat=strict_sibling_compat,
                )
            report_ref = payload.get("report_ref")
            if isinstance(report_ref, str):
                parse_repo_ref(
                    report_ref,
                    location=f"{relative_location(example_path, repo_root)}.payload.report_ref",
                    issues=issues,
                    repo_ref_roots=repo_ref_roots,
                    strict_sibling_compat=strict_sibling_compat,
                )
            if (
                isinstance(object_ref, dict)
                and isinstance(payload.get("eval_name"), str)
                and payload["eval_name"] != object_ref.get("id")
            ):
                issues.append(
                    ValidationIssue(
                        relative_location(example_path, repo_root),
                        "eval result receipt example payload.eval_name must match object_ref.id",
                    )
                )
            if (
                isinstance(report_ref, str)
                and isinstance(evidence_refs, list)
                and report_ref
                not in {
                    entry.get("ref")
                    for entry in evidence_refs
                    if isinstance(entry, dict)
                }
            ):
                issues.append(
                    ValidationIssue(
                        relative_location(example_path, repo_root),
                        "eval result receipt example payload.report_ref must also appear in evidence_refs",
                    )
                )
            interpretation_bound = payload.get("interpretation_bound")
            if isinstance(interpretation_bound, str) and "Example only." not in interpretation_bound:
                issues.append(
                    ValidationIssue(
                        relative_location(example_path, repo_root),
                        "eval result receipt example interpretation_bound must keep example-only posture explicit",
                    )
                )
        else:
            issues.append(
                ValidationIssue(
                    relative_location(example_path, repo_root),
                    "eval result receipt example payload must be an object",
                )
            )
    elif example_payload is not None:
        issues.append(
            ValidationIssue(
                relative_location(example_path, repo_root),
                "eval result receipt example must be a JSON object",
            )
        )

    return issues


def validate_live_receipt_log(
    repo_root: Path,
    *,
    fallback_repo_root: Path,
    repo_ref_roots: Mapping[str, Path],
    strict_sibling_compat: bool,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    log_path = repo_root / LIVE_EVAL_RECEIPT_LOG_NAME
    log_location = relative_location(log_path, repo_root)
    envelope_schema_path = repo_root / STATS_EVENT_ENVELOPE_SCHEMA_PATH
    envelope_schema_location = relative_location(envelope_schema_path, repo_root)
    if envelope_schema_path.exists():
        envelope_schema = load_json_payload(envelope_schema_path, issues, root=repo_root)
    elif repo_root != fallback_repo_root:
        envelope_schema = load_json_payload(
            fallback_repo_root / STATS_EVENT_ENVELOPE_SCHEMA_PATH,
            issues,
            root=fallback_repo_root,
        )
    else:
        envelope_schema = load_json_payload(envelope_schema_path, issues, root=repo_root)
    if not isinstance(envelope_schema, dict):
        if envelope_schema is not None:
            issues.append(ValidationIssue(envelope_schema_location, "stats event envelope schema must be a JSON object"))
        return issues
    if not validate_inline_schema(envelope_schema, location=envelope_schema_location, issues=issues):
        return issues
    envelope_validator = get_schema_validator_with_format(envelope_schema)
    try:
        raw_lines = log_path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return [ValidationIssue(log_location, "file is missing")]

    receipt_count = 0
    seen_event_ids: set[str] = set()
    for line_number, raw_line in enumerate(raw_lines, start=1):
        line = raw_line.strip()
        if not line:
            continue

        receipt_count += 1
        entry_location = f"{log_location}:{line_number}"
        try:
            receipt = json.loads(line)
        except json.JSONDecodeError as exc:
            issues.append(ValidationIssue(entry_location, f"invalid JSON: {exc.msg}"))
            continue
        if not isinstance(receipt, dict):
            issues.append(
                ValidationIssue(entry_location, "live eval receipt log entry must be a JSON object")
            )
            continue

        validate_against_schema(
            receipt,
            STATS_EVENT_ENVELOPE_SCHEMA_NAME,
            entry_location,
            issues,
            validator=envelope_validator,
            fallback_repo_root=fallback_repo_root,
        )
        if receipt.get("event_kind") != "eval_result_receipt":
            issues.append(
                ValidationIssue(
                    entry_location,
                    "live eval receipt log entry must keep event_kind as 'eval_result_receipt'",
                )
            )

        event_id = receipt.get("event_id")
        if isinstance(event_id, str) and event_id:
            if event_id in seen_event_ids:
                issues.append(
                    ValidationIssue(
                        entry_location,
                        f"duplicate event_id '{event_id}' is not allowed in the live eval receipt log",
                    )
                )
            seen_event_ids.add(event_id)

        object_ref = receipt.get("object_ref")
        if isinstance(object_ref, dict):
            if object_ref.get("repo") != "aoa-evals":
                issues.append(
                    ValidationIssue(
                        entry_location,
                        "live eval receipt log object_ref.repo must be 'aoa-evals'",
                    )
                )
            if object_ref.get("kind") != "eval_bundle":
                issues.append(
                    ValidationIssue(
                        entry_location,
                        "live eval receipt log object_ref.kind must be 'eval_bundle'",
                    )
                )

        evidence_refs = receipt.get("evidence_refs")
        seen_primary = False
        evidence_ref_values: set[str] = set()
        if isinstance(evidence_refs, list):
            for index, evidence_ref in enumerate(evidence_refs):
                if not isinstance(evidence_ref, dict):
                    continue
                raw_ref = evidence_ref.get("ref")
                if isinstance(raw_ref, str):
                    evidence_ref_values.add(raw_ref)
                    parse_repo_ref(
                        raw_ref,
                        location=f"{entry_location}.evidence_refs[{index}].ref",
                        issues=issues,
                        repo_ref_roots=repo_ref_roots,
                        strict_sibling_compat=strict_sibling_compat,
                    )
                if evidence_ref.get("role") == "primary":
                    seen_primary = True
            if not seen_primary:
                issues.append(
                    ValidationIssue(
                        entry_location,
                        "live eval receipt log entry must include one primary evidence ref",
                    )
                )

        payload = receipt.get("payload")
        if isinstance(payload, dict):
            validate_against_schema(
                payload,
                EVAL_RESULT_RECEIPT_SCHEMA_NAME,
                f"{entry_location}.payload",
                issues,
                fallback_repo_root=fallback_repo_root,
            )

            bundle_ref = payload.get("bundle_ref")
            if isinstance(bundle_ref, str):
                parse_repo_ref(
                    bundle_ref,
                    location=f"{entry_location}.payload.bundle_ref",
                    issues=issues,
                    repo_ref_roots=repo_ref_roots,
                    strict_sibling_compat=strict_sibling_compat,
                )
                if bundle_ref not in evidence_ref_values:
                    issues.append(
                        ValidationIssue(
                            entry_location,
                            "live eval receipt log payload.bundle_ref must also appear in evidence_refs",
                        )
                    )

            report_ref = payload.get("report_ref")
            if isinstance(report_ref, str):
                parse_repo_ref(
                    report_ref,
                    location=f"{entry_location}.payload.report_ref",
                    issues=issues,
                    repo_ref_roots=repo_ref_roots,
                    strict_sibling_compat=strict_sibling_compat,
                )
                if report_ref not in evidence_ref_values:
                    issues.append(
                        ValidationIssue(
                            entry_location,
                            "live eval receipt log payload.report_ref must also appear in evidence_refs",
                        )
                    )

            if (
                isinstance(object_ref, dict)
                and isinstance(payload.get("eval_name"), str)
                and payload["eval_name"] != object_ref.get("id")
            ):
                issues.append(
                    ValidationIssue(
                        entry_location,
                        "live eval receipt log payload.eval_name must match object_ref.id",
                    )
                )

            if (
                isinstance(object_ref, dict)
                and isinstance(object_ref.get("version"), str)
                and isinstance(payload.get("bundle_status"), str)
                and payload["bundle_status"] != object_ref["version"]
            ):
                issues.append(
                    ValidationIssue(
                        entry_location,
                        "live eval receipt log payload.bundle_status must match object_ref.version when version is present",
                    )
                )

    if receipt_count == 0:
        issues.append(
            ValidationIssue(
                log_location,
                "live eval receipt log must contain at least one receipt entry",
            )
        )
    return issues


def validate_receipt_intake_dry_review_surface(
    repo_root: Path,
    *,
    fallback_repo_root: Path,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    review_path = repo_root / RECEIPT_INTAKE_DRY_REVIEW_NAME
    location = RECEIPT_INTAKE_DRY_REVIEW_NAME

    require_tokens(
        repo_root=repo_root,
        path_name=RECEIPT_INTAKE_DRY_REVIEW_NAME,
        tokens=RECEIPT_INTAKE_DRY_REVIEW_REQUIRED_TOKENS,
        issues=issues,
    )
    require_tokens(
        repo_root=repo_root,
        path_name=RECEIPT_INTAKE_DRY_REVIEW_DECISION_NAME,
        tokens=RECEIPT_INTAKE_DRY_REVIEW_DECISION_REQUIRED_TOKENS,
        issues=issues,
    )
    for path_name, tokens in (
        (
            PROOF_LOOP_MECHANIC_README_NAME,
            (
                RECEIPT_INTAKE_DRY_REVIEW_NAME,
                "Receipt Intake Dry Review",
                "`receipt_status` stays `not_published`",
            ),
        ),
        (
            PUBLICATION_RECEIPTS_MECHANIC_README_NAME,
            (
                RECEIPT_INTAKE_DRY_REVIEW_NAME,
                "dry review",
                "`receipt_status` as `not_published`",
            ),
        ),
        (
            "reports/README.md",
            (
                RECEIPT_INTAKE_DRY_REVIEW_NAME,
                "receipt-intake",
                "`not_published`",
            ),
        ),
        (
            "ROADMAP.md",
            ("Publication receipt posture", "mechanics/publication-receipts/README.md"),
        ),
        ("CHANGELOG.md", (RECEIPT_INTAKE_DRY_REVIEW_NAME, "validator coverage")),
        (
            "docs/decisions/README.md",
            (RECEIPT_INTAKE_DRY_REVIEW_DECISION_NAME, "real eval-result receipt publication"),
        ),
    ):
        require_tokens(repo_root=repo_root, path_name=path_name, tokens=tokens, issues=issues)

    payload = load_json_payload(review_path, issues, root=repo_root)
    if not isinstance(payload, dict):
        if payload is not None:
            issues.append(ValidationIssue(location, "receipt intake dry review must be a JSON object"))
        return issues

    for field in (
        "event_kind",
        "event_id",
        "observed_at",
        "run_ref",
        "session_ref",
        "actor_ref",
        "object_ref",
        "evidence_refs",
        "payload",
    ):
        if field in payload:
            issues.append(
                ValidationIssue(
                    location,
                    f"receipt intake dry review must not contain publishable receipt field {field!r}",
                )
            )

    expected_refs = {
        "source_report_ref": f"repo:aoa-evals/{PROOF_LOOP_LOCAL_REPORT_NAME}",
        "source_bundle_ref": "repo:aoa-evals/evals/workflow/aoa-verification-honesty/EVAL.md",
        "source_manifest_ref": "repo:aoa-evals/evals/workflow/aoa-verification-honesty/eval.yaml",
        "report_index_ref": "repo:aoa-evals/generated/eval_report_index.min.json",
        "receipt_payload_schema_ref": f"repo:aoa-evals/{EVAL_RESULT_RECEIPT_SCHEMA_PATH}",
        "event_envelope_schema_ref": f"repo:aoa-evals/{STATS_EVENT_ENVELOPE_SCHEMA_PATH}",
        "publisher_ref": f"repo:aoa-evals/{EVAL_RESULT_RECEIPT_PUBLISHER_NAME}",
        "owner_local_log_ref": f"repo:aoa-evals/{LIVE_EVAL_RECEIPT_LOG_NAME}",
    }
    for key, expected in expected_refs.items():
        value = payload.get(key)
        if value != expected:
            issues.append(ValidationIssue(location, f"{key} must be {expected!r}"))
            continue
        local_path = repo_root / expected.removeprefix("repo:aoa-evals/")
        if not local_path.exists():
            issues.append(ValidationIssue(location, f"{key} target is missing: {expected}"))

    expected_top_level = {
        "artifact_kind": "receipt_intake_dry_review",
        "schema_version": 1,
        "review_id": "eval-result-receipt-intake-dry-review-v1",
        "reviewed_at": "2026-05-19",
    }
    for key, expected in expected_top_level.items():
        if payload.get(key) != expected:
            issues.append(ValidationIssue(location, f"{key} must be {expected!r}"))

    source_report_path = repo_root / PROOF_LOOP_LOCAL_REPORT_NAME
    source_report = load_json_payload(source_report_path, issues, root=repo_root)
    manifest = load_yaml_file(source_eval_dir(repo_root, "aoa-verification-honesty") / "eval.yaml", issues, root=repo_root)
    report_index = load_json_payload(repo_root / EVAL_REPORT_INDEX_NAME, issues, root=repo_root)
    preview = payload.get("candidate_payload_preview")

    payload_schema_path = repo_root / EVAL_RESULT_RECEIPT_SCHEMA_PATH
    if not payload_schema_path.exists() and repo_root != fallback_repo_root:
        payload_schema_path = fallback_repo_root / EVAL_RESULT_RECEIPT_SCHEMA_PATH
    payload_schema = load_json_payload(payload_schema_path, issues, root=payload_schema_path.parents[5])
    payload_validator: Draft202012Validator | None = None
    if isinstance(payload_schema, dict):
        try:
            Draft202012Validator.check_schema(payload_schema)
        except SchemaError as exc:
            issues.append(
                ValidationIssue(
                    EVAL_RESULT_RECEIPT_SCHEMA_PATH,
                    f"invalid JSON schema: {exc.message}",
                )
            )
        else:
            payload_validator = get_schema_validator_with_format(payload_schema)

    if isinstance(preview, dict):
        if payload_validator is not None:
            validate_against_schema(
                preview,
                EVAL_RESULT_RECEIPT_SCHEMA_NAME,
                f"{location}.candidate_payload_preview",
                issues,
                validator=payload_validator,
                fallback_repo_root=fallback_repo_root,
            )

        if isinstance(source_report, dict):
            expected_report_values = {
                "eval_name": source_report.get("eval_name"),
                "bundle_status": source_report.get("bundle_status"),
                "verdict": source_report.get("verdict"),
            }
            for key, expected in expected_report_values.items():
                if preview.get(key) != expected:
                    issues.append(
                        ValidationIssue(
                            f"{location}.candidate_payload_preview",
                            f"{key} must match source report value {expected!r}",
                        )
                    )
            case_count = len(source_report.get("per_case_breakdown", []))
            if preview.get("case_count") != case_count:
                issues.append(
                    ValidationIssue(
                        f"{location}.candidate_payload_preview",
                        "case_count must match source report per_case_breakdown length",
                    )
                )

        if isinstance(manifest, dict):
            if preview.get("report_format") != manifest.get("report_format"):
                issues.append(
                    ValidationIssue(
                        f"{location}.candidate_payload_preview",
                        "report_format must match source manifest report_format",
                    )
                )
            if preview.get("bundle_status") != manifest.get("status"):
                issues.append(
                    ValidationIssue(
                        f"{location}.candidate_payload_preview",
                        "bundle_status must match source manifest status",
                    )
                )
            if manifest.get("baseline_mode") == "none" and preview.get("comparison_mode") != "none":
                issues.append(
                    ValidationIssue(
                        f"{location}.candidate_payload_preview",
                        "comparison_mode must stay 'none' when the source manifest baseline_mode is 'none'",
                    )
                )

        if preview.get("claim_scope") != "bundle_scoped":
            issues.append(
                ValidationIssue(
                    f"{location}.candidate_payload_preview",
                    "claim_scope must stay 'bundle_scoped' for this dry review",
                )
            )
        if preview.get("bundle_ref") != expected_refs["source_bundle_ref"]:
            issues.append(
                ValidationIssue(
                    f"{location}.candidate_payload_preview",
                    "bundle_ref must match the dry review source_bundle_ref",
                )
            )
        if preview.get("report_ref") != expected_refs["source_report_ref"]:
            issues.append(
                ValidationIssue(
                    f"{location}.candidate_payload_preview",
                    "report_ref must match the dry review source_report_ref",
                )
            )
        interpretation_bound = preview.get("interpretation_bound")
        if not isinstance(interpretation_bound, str):
            issues.append(
                ValidationIssue(
                    f"{location}.candidate_payload_preview",
                    "interpretation_bound must be a string",
                )
            )
        else:
            for token in (
                "Dry review only.",
                "publication pressure routes to a receipt envelope",
                ".aoa/live_receipts/",
                "verdict meaning stays with bundle-local review",
            ):
                if token not in interpretation_bound:
                    issues.append(
                        ValidationIssue(
                            f"{location}.candidate_payload_preview.interpretation_bound",
                            f"interpretation_bound must mention '{token}'",
                        )
                    )
    else:
        issues.append(ValidationIssue(location, "candidate_payload_preview must be a JSON object"))

    if isinstance(report_index, dict):
        reports = report_index.get("reports")
        indexed_paths = {
            entry.get("source_report_path")
            for entry in reports
            if isinstance(entry, dict)
        } if isinstance(reports, list) else set()
        if PROOF_LOOP_LOCAL_REPORT_NAME not in indexed_paths:
            issues.append(
                ValidationIssue(
                    location,
                    f"report_index_ref must index {PROOF_LOOP_LOCAL_REPORT_NAME}",
                )
            )

    source_alignment = payload.get("source_alignment")
    if isinstance(source_alignment, dict):
        for key in (
            "eval_name_matches_report",
            "bundle_status_matches_manifest",
            "report_format_matches_manifest",
            "verdict_matches_report",
        ):
            if source_alignment.get(key) is not True:
                issues.append(ValidationIssue(f"{location}.source_alignment", f"{key} must be true"))
        if source_alignment.get("case_count_source") != "per_case_breakdown length":
            issues.append(
                ValidationIssue(
                    f"{location}.source_alignment",
                    "case_count_source must stay 'per_case_breakdown length'",
                )
            )
    else:
        issues.append(ValidationIssue(location, "source_alignment must be a JSON object"))

    checks = payload.get("intake_checks")
    if isinstance(checks, list):
        by_id = {entry.get("check_id"): entry for entry in checks if isinstance(entry, dict)}
        expected_check_results = {
            "source_report_exists": "pass",
            "source_report_is_indexed": "pass",
            "candidate_payload_preview_validates_against_payload_schema": "pass",
            "stats_event_envelope_created": "not_attempted",
            "receipt_publisher_run": "not_attempted",
            "owner_local_live_log_append": "not_attempted",
        }
        for check_id, expected_result in expected_check_results.items():
            entry = by_id.get(check_id)
            if not isinstance(entry, dict):
                issues.append(ValidationIssue(f"{location}.intake_checks", f"missing check_id {check_id!r}"))
                continue
            if entry.get("result") != expected_result:
                issues.append(
                    ValidationIssue(
                        f"{location}.intake_checks.{check_id}",
                        f"result must be {expected_result!r}",
                    )
                )
            evidence_ref = entry.get("evidence_ref")
            if not isinstance(evidence_ref, str) or not evidence_ref.startswith("repo:aoa-evals/"):
                issues.append(
                    ValidationIssue(
                        f"{location}.intake_checks.{check_id}",
                        "evidence_ref must point at a repo:aoa-evals/ surface",
                    )
                )
    else:
        issues.append(ValidationIssue(location, "intake_checks must be a list"))

    publication_boundary = payload.get("publication_boundary")
    if isinstance(publication_boundary, dict):
        expected_boundary_values = {
            "publication_status": "dry_review_only",
            "receipt_status": "not_published",
            "event_envelope_status": "not_created",
            "live_log_append_status": "not_attempted",
            "publisher_execution_status": "not_attempted",
        }
        for key, expected in expected_boundary_values.items():
            if publication_boundary.get(key) != expected:
                issues.append(
                    ValidationIssue(
                        f"{location}.publication_boundary",
                        f"{key} must be {expected!r}",
                    )
                )
        boundary = publication_boundary.get("boundary")
        if not isinstance(boundary, str):
            issues.append(
                ValidationIssue(
                    f"{location}.publication_boundary",
                    "boundary must be a string",
                )
            )
        else:
            for token in (
                "receipt envelope pressure",
                "stats sidecar pressure",
                "live log pressure",
                "proof or bundle promotion pressure",
                "runtime acceptance pressure",
            ):
                if token not in boundary:
                    issues.append(
                        ValidationIssue(
                            f"{location}.publication_boundary.boundary",
                            f"boundary must mention '{token}'",
                        )
                    )
    else:
        issues.append(ValidationIssue(location, "publication_boundary must be a JSON object"))

    claim_limit = payload.get("claim_limit")
    if not isinstance(claim_limit, str):
        issues.append(ValidationIssue(location, "claim_limit must be a string"))
    else:
        for token in (
            "Publication pressure routes",
            "live receipt memory append routes",
            "runtime evidence acceptance routes",
            "bundle promotion routes",
            "strategic closeout stays with the goal owner",
        ):
            if token not in claim_limit:
                issues.append(ValidationIssue(location, f"claim_limit must mention '{token}'"))

    return issues
