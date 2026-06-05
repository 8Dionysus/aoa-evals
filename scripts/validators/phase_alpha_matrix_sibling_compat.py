"""Phase Alpha matrix strict sibling compatibility contracts."""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Iterable, Mapping

from validators.phase_alpha_matrix_common import (
    PHASE_ALPHA_EVAL_MATRIX_NAME,
    PHASE_ALPHA_PLAYBOOK_MATRIX_NAME,
    REPO_REF_PREFIX,
    ValidationIssue,
    display_location,
    load_builder_module,
    load_json_payload,
    load_mapping_entries,
    parse_repo_ref,
    relative_location,
    validate_repo_relative_contract_path,
)


def load_phase_alpha_eval_matrix_builder(repo_root: Path):
    return load_builder_module(repo_root)


def validate_phase_alpha_matrix_sibling_compat(
    repo_root: Path,
    *,
    sibling_root: Path,
    repo_ref_roots: Mapping[str, Path],
    strict_sibling_compat: bool,
    visible_roots: Iterable[Path] = (),
    builder_loader: Callable[[Path], object] = load_phase_alpha_eval_matrix_builder,
) -> list[ValidationIssue]:
    issues: list[ValidationIssue] = []
    if not strict_sibling_compat:
        return issues

    generated_path = repo_root / PHASE_ALPHA_EVAL_MATRIX_NAME
    generated_location = relative_location(generated_path, repo_root)
    payload = load_json_payload(generated_path, issues, root=repo_root)
    if payload is None:
        return issues
    if not isinstance(payload, dict):
        issues.append(ValidationIssue(generated_location, "generated phase alpha eval matrix must be an object"))
        return issues

    if not sibling_root.exists():
        issues.append(
            ValidationIssue(
                display_location(sibling_root, visible_roots),
                "strict sibling compatibility requires available aoa-playbooks root",
            )
        )
        return issues

    try:
        builder = builder_loader(repo_root)
        expected = builder.build_phase_alpha_eval_matrix_payload()
    except Exception as exc:
        issues.append(ValidationIssue(generated_location, str(exc)))
        return issues

    if payload != expected:
        issues.append(
            ValidationIssue(
                generated_location,
                "generated phase alpha eval matrix is out of date or mismatched",
            )
        )

    playbook_matrix_path = sibling_root / PHASE_ALPHA_PLAYBOOK_MATRIX_NAME
    playbook_matrix_location = display_location(playbook_matrix_path, visible_roots)
    playbook_matrix = load_json_payload(
        playbook_matrix_path,
        issues,
        visible_roots=visible_roots,
    )
    playbook_runs = load_mapping_entries(
        playbook_matrix,
        array_key="runs",
        key_name="run_id",
        location=playbook_matrix_location,
        issues=issues,
    )

    runs = payload.get("runs")
    if not isinstance(runs, list):
        issues.append(ValidationIssue(generated_location, "runs must be a list"))
        return issues

    seen_run_ids: list[str] = []
    for index, item in enumerate(runs):
        location = f"{generated_location}.runs[{index}]"
        if not isinstance(item, dict):
            issues.append(ValidationIssue(location, "run entry must be an object"))
            continue
        run_id = item.get("run_id")
        if not isinstance(run_id, str):
            issues.append(ValidationIssue(location, "run_id must be a string"))
            continue
        seen_run_ids.append(run_id)
        source_run = playbook_runs.get(run_id)
        if source_run is None:
            issues.append(ValidationIssue(location, f"run_id '{run_id}' does not resolve in aoa-playbooks"))
            continue

        for field_name in ("sequence", "playbook_id", "playbook_name"):
            if item.get(field_name) != source_run.get(field_name):
                issues.append(ValidationIssue(location, f"{field_name} must match aoa-playbooks phase alpha run matrix"))

        if item.get("runtime_lane") != source_run.get("runtime_path_key"):
            issues.append(ValidationIssue(location, "runtime_lane must match aoa-playbooks runtime_path_key"))

        required_evals = item.get("required_evals")
        if not isinstance(required_evals, list) or not required_evals:
            issues.append(ValidationIssue(location, "required_evals must be a non-empty list"))
            continue

        observed_anchors: list[str] = []
        for eval_index, eval_item in enumerate(required_evals):
            eval_location = f"{location}.required_evals[{eval_index}]"
            if not isinstance(eval_item, dict):
                issues.append(ValidationIssue(eval_location, "required eval entry must be an object"))
                continue
            eval_anchor = eval_item.get("eval_anchor")
            if not isinstance(eval_anchor, str):
                issues.append(ValidationIssue(eval_location, "eval_anchor must be a string"))
                continue
            observed_anchors.append(eval_anchor)
            evidence_refs = eval_item.get("evidence_refs")
            if not isinstance(evidence_refs, list) or not evidence_refs:
                issues.append(ValidationIssue(eval_location, "evidence_refs must be a non-empty list"))
                continue
            if len(evidence_refs) != len(set(evidence_refs)):
                issues.append(ValidationIssue(eval_location, "evidence_refs must not duplicate refs"))
            for ref_index, ref in enumerate(evidence_refs):
                ref_location = f"{eval_location}.evidence_refs[{ref_index}]"
                if not isinstance(ref, str) or not ref:
                    issues.append(ValidationIssue(ref_location, "evidence ref must be a non-empty string"))
                    continue
                if ref.startswith(REPO_REF_PREFIX):
                    parse_repo_ref(
                        ref,
                        location=ref_location,
                        issues=issues,
                        repo_ref_roots=repo_ref_roots,
                        strict_sibling_compat=strict_sibling_compat,
                    )
                else:
                    validate_repo_relative_contract_path(
                        repo_root,
                        ref,
                        location=ref_location,
                        issues=issues,
                    )

        if observed_anchors != source_run.get("eval_anchors"):
            issues.append(ValidationIssue(location, "required_evals must stay ordered to aoa-playbooks eval_anchors"))

    if seen_run_ids != [item.get("run_id") for item in runs if isinstance(item, dict)]:
        issues.append(ValidationIssue(generated_location, "runs must keep deterministic ordering"))
    if set(seen_run_ids) != set(playbook_runs):
        missing = sorted(set(playbook_runs) - set(seen_run_ids))
        extra = sorted(set(seen_run_ids) - set(playbook_runs))
        if missing:
            issues.append(ValidationIssue(generated_location, "missing phase alpha runs: " + ", ".join(missing)))
        if extra:
            issues.append(ValidationIssue(generated_location, "unexpected phase alpha runs: " + ", ".join(extra)))

    return issues


__all__ = (
    "load_phase_alpha_eval_matrix_builder",
    "validate_phase_alpha_matrix_sibling_compat",
)
