"""Root route-card-only district contracts."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

from validators.common import ValidationIssue


PROOF_TOPOLOGY_NAME = "docs/architecture/PROOF_TOPOLOGY.md"
ROOT_ROUTE_CARD_GUARD_DECISION_NAME = "docs/decisions/AOA-EV-D-0051-root-route-card-guard.md"
ROOT_ROUTE_CARD_ONLY_DISTRICTS: dict[str, tuple[str, ...]] = {
    "config": ("AGENTS.md", "README.md"),
    "examples": ("AGENTS.md", "README.md"),
    "fixtures": ("AGENTS.md", "README.md"),
    "manifests": ("AGENTS.md", "README.md"),
    "reports": ("AGENTS.md", "README.md"),
    "runners": ("AGENTS.md", "README.md"),
    "schemas": ("AGENTS.md", "README.md"),
    "scorers": ("AGENTS.md", "README.md"),
    "templates": ("AGENTS.md", "README.md"),
}
ROOT_ROUTE_CARD_README_REQUIRED_TOKENS: dict[str, tuple[str, ...]] = {
    "config/README.md": (
        "compatibility route card",
        "Active root config payloads route to the operation that owns them",
        "Operating Card",
        "mechanics/agon/parts/*/config/",
        "mechanics/boundary-bridge/parts/latest-sibling-canary/config/",
    ),
    "examples/README.md": (
        "compatibility route card",
        "Active root examples payloads route beside the source that owns their",
        "Operating Card",
        "evals/**/examples/",
        "mechanics/audit/parts/",
    ),
    "fixtures/README.md": (
        "compatibility route card",
        "Active fixture families live under the owning mechanic part",
        "Operating Card",
        "mechanics/proof-infra/parts/fixture-families/fixtures/",
        "mechanics/comparison-spine/parts/",
    ),
    "manifests/README.md": (
        "compatibility route card",
        "Active root manifest payloads route next to the mechanic part",
        "Operating Card",
        "mechanics/agon/parts/*/manifests/",
        "mechanics/recurrence/parts/control-plane-integrity/manifests/",
        "mechanics/recurrence/parts/portable-proof-beacons/manifests/",
    ),
    "reports/README.md": (
        "compatibility route card",
        "Active root reports payloads route to the owning bundle or mechanic part",
        "Operating Card",
        "Current top-level shared dossiers",
        "none",
        "mechanics/proof-loop/parts/route-smoke/reports/",
        "mechanics/release-support/parts/",
        "eval-claim strength stays with source bundles and reviewed reports",
    ),
    "runners/README.md": (
        "compatibility route card",
        "Operating Card",
        "mechanics/proof-infra/parts/reportable-contracts/runners/reportable_proof_contract.md",
        "Use [AGENTS.md](AGENTS.md) for runner contract rules",
    ),
    "schemas/README.md": (
        "compatibility route card",
        "Active root schema payloads route to mechanic-local owners",
        "Operating Card",
        "mechanics/proof-object/parts/eval-contracts/schemas/",
        "mechanics/proof-infra/parts/reportable-contracts/schemas/",
        "mechanics/questbook/parts/",
    ),
    "scorers/README.md": (
        "compatibility route card",
        "Operating Card",
        "mechanics/proof-infra/parts/reportable-contracts/scorers/bounded_rubric_breakdown.py",
        "Use [AGENTS.md](AGENTS.md) for scorer helper rules",
    ),
    "templates/README.md": (
        "compatibility route card",
        "Active root template payloads route to the eval authoring template",
        "Operating Card",
        "mechanics/proof-object/parts/eval-authoring/templates/EVAL.template.md",
    ),
}
ROOT_ROUTE_CARD_README_FORBIDDEN_TOKENS = (
    "Shared fixture naming discipline:",
    "Shared dossier naming discipline",
    "Do not recreate active root runner payloads",
    "Do not recreate active root scorer helper aliases",
)
ROOT_ROUTE_CARD_GUARD_DECISION_REQUIRED_TOKENS = (
    "Root Route-card Guard",
    "route-card-only surfaces",
    "docs/architecture/PROOF_TOPOLOGY.md",
    "validator allowlist",
    "does not forbid bundle-local examples or reports",
)


@dataclass(frozen=True)
class RootRouteCardContext:
    require_tokens: Callable[
        [Path, str, Iterable[str], list[ValidationIssue]],
        str,
    ]


def validate_root_route_card_districts(
    repo_root: Path,
    *,
    context: RootRouteCardContext,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []

    for district_name, allowed_names in ROOT_ROUTE_CARD_ONLY_DISTRICTS.items():
        district = repo_root / district_name
        if not district.is_dir():
            issues.append(
                ValidationIssue(
                    district_name,
                    "route-card-only root district is missing",
                )
            )
            continue

        allowed = set(allowed_names)
        for allowed_name in allowed_names:
            if not (district / allowed_name).is_file():
                issues.append(
                    ValidationIssue(
                        f"{district_name}/{allowed_name}",
                        "route-card file is missing",
                    )
                )

        for path in sorted(district.rglob("*")):
            relative_name = path.relative_to(district).as_posix()
            if relative_name not in allowed:
                issues.append(
                    ValidationIssue(
                        path.relative_to(repo_root).as_posix(),
                        "active payload or stray directory must not live in a route-card-only root district",
                    )
                )

    for path_name, tokens in ROOT_ROUTE_CARD_README_REQUIRED_TOKENS.items():
        text = context.require_tokens(repo_root, path_name, tokens, issues)
        if not text:
            continue
        first_heading = next(
            (line.strip() for line in text.splitlines() if line.startswith("# ")),
            "",
        )
        if "Route" not in first_heading:
            issues.append(
                ValidationIssue(
                    path_name,
                    "route-card-only root README heading must name itself as a Route surface",
                )
            )
        for forbidden_token in ROOT_ROUTE_CARD_README_FORBIDDEN_TOKENS:
            if forbidden_token in text:
                issues.append(
                    ValidationIssue(
                        path_name,
                        "route-card-only root README must keep operational discipline in AGENTS.md",
                    )
                )

    context.require_tokens(
        repo_root,
        ROOT_ROUTE_CARD_GUARD_DECISION_NAME,
        ROOT_ROUTE_CARD_GUARD_DECISION_REQUIRED_TOKENS,
        issues,
    )
    context.require_tokens(
        repo_root,
        "docs/decisions/README.md",
        (ROOT_ROUTE_CARD_GUARD_DECISION_NAME, "Root Route-card Guard"),
        issues,
    )
    context.require_tokens(
        repo_root,
        PROOF_TOPOLOGY_NAME,
        (
            "active examples payloads route",
            "active root config or manifest payload routes require a topology decision",
            "active root reports payload routes require a topology decision",
            "compatibility route",
        ),
        issues,
    )

    return issues
