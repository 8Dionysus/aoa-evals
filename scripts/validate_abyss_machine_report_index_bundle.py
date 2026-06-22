#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib
import json
import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any


def _find_repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "AGENTS.md").is_file() and (parent / "scripts" / "generate_eval_report_index.py").is_file():
            return parent
    raise RuntimeError("could not find aoa-evals repository root")


REPO_ROOT = _find_repo_root()
DEFAULT_MANIFEST = (
    REPO_ROOT
    / "mechanics"
    / "release-support"
    / "parts"
    / "artifact-bundles"
    / "manifests"
    / "report_index.bundle.json"
)
DEFAULT_SUBJECT = REPO_ROOT / "generated" / "eval_report_index.min.json"
EXPECTED_REQUIRED_CONTROLS = ["abi_signature", "sbom", "slsa_in_toto"]
ARTIFACT_CLASS = "aoa_evals_generated_report_index_bundle"


def _candidate_abyss_machine_roots() -> list[Path]:
    candidates: list[Path] = []
    env_root = os.environ.get("ABYSS_MACHINE_REPO_ROOT")
    if env_root:
        candidates.append(Path(env_root))
    candidates.extend(
        [
            REPO_ROOT.parent / "abyss-machine",
            Path.home() / "src" / "abyss-machine",
            Path("/srv/AbyssOS/abyss-machine"),
        ]
    )
    return candidates


def _public_seed_root() -> Path:
    return Path(os.environ.get("ABYSS_MACHINE_PUBLIC_SEED_ROOT", "/usr/local/share/abyss-machine")).expanduser()


def _import_from_package_root(package_root: Path) -> tuple[Any, Path, str] | None:
    root = package_root.expanduser().resolve()
    if (root / "abyss_machine" / "artifact_bundles.py").is_file():
        sys.path.insert(0, str(root))
        return importlib.import_module("abyss_machine.artifact_bundles"), _public_seed_root(), str(root)
    return None


def _import_artifact_bundles() -> tuple[Any, Path | None, str | None]:
    package_root = os.environ.get("ABYSS_MACHINE_PACKAGE_ROOT")
    if package_root:
        imported = _import_from_package_root(Path(package_root))
        if imported is not None:
            return imported
    for candidate in _candidate_abyss_machine_roots():
        root = candidate.expanduser().resolve()
        module_root = root / "src"
        if (module_root / "abyss_machine" / "artifact_bundles.py").is_file():
            sys.path.insert(0, str(module_root))
            return importlib.import_module("abyss_machine.artifact_bundles"), root, None
    installed = _import_from_package_root(Path("/usr/local/libexec"))
    if installed is not None:
        return installed
    artifact_bundles = importlib.import_module("abyss_machine.artifact_bundles")
    return artifact_bundles, getattr(artifact_bundles, "REPO_ROOT", None), None


def _load_json(path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def _portable_ref(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return resolved.name


def _default_tmp_root() -> Path | None:
    for raw in (os.environ.get("ABYSS_MACHINE_TMP_ROOT"), "/srv/abyss-machine/tmp"):
        if not raw:
            continue
        path = Path(raw)
        if path.is_dir():
            return path
    return None


def _assert_generated_index_public_safe(subject: Path) -> None:
    text = subject.read_text(encoding="utf-8")
    forbidden = [
        str(REPO_ROOT.resolve()),
        str(Path.home()),
        "/srv/abyss-machine",
        "/var/lib/abyss-machine",
        "/etc/abyss-machine",
        "PASSWORD=",
        "TOKEN=",
        "SECRET=",
    ]
    leaked = [item for item in forbidden if item and item in text]
    if leaked:
        raise ValueError("generated report index contains private or machine-local markers: " + ", ".join(leaked))


def _assert_public_sidecars_do_not_leak_local_roots(bundle_dir: Path, abyss_machine_root: Path | None) -> None:
    forbidden = [str(REPO_ROOT.resolve())]
    if abyss_machine_root is not None:
        forbidden.append(str(abyss_machine_root.resolve()))
    leaks: list[str] = []
    for path in sorted(bundle_dir.iterdir()):
        if path.is_file() and path.suffix in {".json", ".jsonl"}:
            text = path.read_text(encoding="utf-8")
            if any(item and item in text for item in forbidden):
                leaks.append(path.name)
    if leaks:
        raise ValueError("public artifact sidecars leak local repo roots: " + ", ".join(leaks))


def _assert_public_registry_does_not_leak_local_roots(registry_dir: Path, abyss_machine_root: Path | None) -> None:
    forbidden = [str(REPO_ROOT.resolve())]
    if abyss_machine_root is not None:
        forbidden.append(str(abyss_machine_root.resolve()))
    leaks: list[str] = []
    for path in sorted(registry_dir.rglob("*")) if registry_dir.exists() else []:
        if path.is_file() and path.suffix in {".json", ".jsonl"}:
            text = path.read_text(encoding="utf-8")
            if any(item and item in text for item in forbidden):
                leaks.append(path.name)
    if leaks:
        raise ValueError("public artifact registry leaks local repo roots: " + ", ".join(leaks))


def _assert_expected_controls(verify: dict[str, Any]) -> None:
    required = verify.get("required_controls")
    verified = verify.get("verified_controls")
    if required != EXPECTED_REQUIRED_CONTROLS:
        raise ValueError(f"unexpected required controls: {required!r}")
    if verified != EXPECTED_REQUIRED_CONTROLS:
        raise ValueError(f"unexpected verified controls: {verified!r}")


def _copy_bundle(bundle_dir: Path, target: Path) -> Path:
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(bundle_dir, target)
    return target


def _registry_roundtrip(
    artifact_bundles: Any,
    bundle_dir: Path,
    registry_dir: Path,
    *,
    lifecycle_state: str,
    evidence_ref: str,
) -> dict[str, Any]:
    registered = artifact_bundles.write_bundle_registry_record(
        bundle_dir,
        registry_dir,
        lifecycle_state=lifecycle_state,
        consumer_refs=["aoa-evals:generated-report-index"],
        evidence_refs=[evidence_ref],
    )
    latest = artifact_bundles.read_bundle_registry(registry_dir, artifact_class=ARTIFACT_CLASS)
    latest_record = latest.get("latest_by_artifact_class", {}).get(ARTIFACT_CLASS)
    return {
        "ok": bool(
            registered.get("ok")
            and isinstance(latest_record, dict)
            and latest_record.get("record_id") == registered.get("record", {}).get("record_id")
            and latest_record.get("lifecycle_state") == lifecycle_state
        ),
        "registered": registered,
        "latest": latest,
    }


def _registry_roundtrip_with_subject_store(
    artifact_bundles: Any,
    bundle_dir: Path,
    registry_dir: Path,
    store_root: Path,
    *,
    lifecycle_state: str,
    evidence_ref: str,
) -> dict[str, Any]:
    env_root = "ABYSS_MACHINE_ARTIFACT_SUBJECT_STORE_ROOT"
    env_roots = "ABYSS_MACHINE_ARTIFACT_SUBJECT_STORE_ROOTS"
    old_root = os.environ.get(env_root)
    old_roots = os.environ.get(env_roots)
    os.environ[env_root] = str(store_root)
    os.environ[env_roots] = str(store_root)
    try:
        return _registry_roundtrip(
            artifact_bundles,
            bundle_dir,
            registry_dir,
            lifecycle_state=lifecycle_state,
            evidence_ref=evidence_ref,
        )
    finally:
        if old_root is None:
            os.environ.pop(env_root, None)
        else:
            os.environ[env_root] = old_root
        if old_roots is None:
            os.environ.pop(env_roots, None)
        else:
            os.environ[env_roots] = old_roots


def _trust_gate_allow_latest(artifact_bundles: Any, registry_dir: Path, registry_roundtrip: dict[str, Any]) -> dict[str, Any]:
    record = registry_roundtrip.get("registered", {}).get("record", {})
    trust_gate = artifact_bundles.trust_gate(
        registry_dir,
        artifact_class=ARTIFACT_CLASS,
        subject_digest=str(record.get("subject_digest") or ""),
        consumer_intent="agent",
        expected_source_repo="aoa-evals",
    )
    inspected_claims = trust_gate.get("inspected_claims", {})
    return {
        "ok": bool(
            trust_gate.get("ok")
            and trust_gate.get("verdict") in {"allow", "warn"}
            and trust_gate.get("decision", {}).get("model") == "fail_closed_consumer_admission"
            and trust_gate.get("decision", {}).get("allow") is True
            and inspected_claims.get("registry_latest", {}).get("selected_record_is_latest") is True
            and inspected_claims.get("controls", {}).get("required_controls_missing") == []
            and inspected_claims.get("source", {}).get("source_repo_matched") is True
        ),
        "trust_gate": trust_gate,
    }


def _verify_missing_sbom(artifact_bundles: Any, abyss_repo_root: Path, bundle_dir: Path, tmp_root: Path) -> dict[str, Any]:
    candidate = _copy_bundle(bundle_dir, tmp_root / "missing-sbom")
    for name in (artifact_bundles.SBOM_CYCLONEDX_SIDECAR, artifact_bundles.SBOM_SPDX_SIDECAR):
        path = candidate / name
        if path.exists():
            path.unlink()
    verification = artifact_bundles.verify_bundle(candidate, repo_root=abyss_repo_root)
    return {
        "ok": verification.get("ok") is False and bool(verification.get("missing")),
        "verification": verification,
    }


def _verify_wrong_slsa_subject(
    artifact_bundles: Any,
    abyss_repo_root: Path,
    bundle_dir: Path,
    tmp_root: Path,
) -> dict[str, Any]:
    candidate = _copy_bundle(bundle_dir, tmp_root / "wrong-slsa-subject")
    path = candidate / artifact_bundles.SLSA_INTOTO_SIDECAR
    statement = json.loads(path.read_text(encoding="utf-8").splitlines()[0])
    statement["subject"][0]["digest"]["sha256"] = "0" * 64
    path.write_text(json.dumps(statement, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    verification = artifact_bundles.verify_bundle(candidate, repo_root=abyss_repo_root)
    return {
        "ok": verification.get("ok") is False
        and any("SLSA/in-toto sidecar does not cover artifact subject digests" in item for item in verification.get("errors", [])),
        "verification": verification,
    }


def _verify_private_report_marker(subject: Path, tmp_root: Path) -> dict[str, Any]:
    candidate = tmp_root / "private-eval-report-index.min.json"
    shutil.copyfile(subject, candidate)
    candidate.write_text(candidate.read_text(encoding="utf-8") + "\nTOKEN=private-negative\n", encoding="utf-8")
    try:
        _assert_generated_index_public_safe(candidate)
    except ValueError as exc:
        return {"ok": "generated report index contains private or machine-local markers" in str(exc), "error": str(exc)}
    return {"ok": False, "error": "private generated report marker was not detected"}


def _verify_unverified_latest_rejected(artifact_bundles: Any, bundle_dir: Path, tmp_root: Path) -> dict[str, Any]:
    candidate = _copy_bundle(bundle_dir, tmp_root / "unverified-latest")
    for name in (artifact_bundles.SBOM_CYCLONEDX_SIDECAR, artifact_bundles.SBOM_SPDX_SIDECAR):
        path = candidate / name
        if path.exists():
            path.unlink()
    registered = artifact_bundles.write_bundle_registry_record(
        candidate,
        tmp_root / "unverified-registry",
        lifecycle_state="release-ready",
    )
    return {
        "ok": registered.get("ok") is False
        and any("successful bundle verification" in item for item in registered.get("errors", [])),
        "registered": registered,
    }


def _verify_terminal_registry_state(artifact_bundles: Any, bundle_dir: Path, tmp_root: Path) -> dict[str, Any]:
    registry_dir = tmp_root / "terminal-registry"
    release_ready = _registry_roundtrip(
        artifact_bundles,
        bundle_dir,
        registry_dir,
        lifecycle_state="release-ready",
        evidence_ref="terminal-state-rehearsal",
    )
    revoked = artifact_bundles.write_bundle_registry_record(
        bundle_dir,
        registry_dir,
        lifecycle_state="revoked",
        revocation_reason="aoa-evals report index terminal-state rehearsal",
    )
    revoked_gate = artifact_bundles.trust_gate(
        registry_dir,
        artifact_class=ARTIFACT_CLASS,
        record_id=str(release_ready.get("registered", {}).get("record", {}).get("record_id") or ""),
        consumer_intent="agent",
    )
    after_revoke = artifact_bundles.read_bundle_registry(registry_dir, artifact_class=ARTIFACT_CLASS)
    return {
        "ok": bool(
            release_ready.get("ok")
            and revoked.get("ok")
            and revoked_gate.get("verdict") == "deny"
            and revoked_gate.get("decision", {}).get("allow") is False
            and revoked_gate.get("inspected_claims", {}).get("lifecycle", {}).get("terminal_state") is True
            and not after_revoke.get("latest_by_artifact_class")
        ),
        "release_ready": release_ready,
        "revoked": revoked,
        "revoked_trust_gate": revoked_gate,
        "after_revoke": after_revoke,
    }


def _verify_materialized_subject_store(
    artifact_bundles: Any,
    manifest: Path,
    bundle_dir: Path,
    registry_dir: Path,
    tmp_root: Path,
) -> dict[str, Any]:
    store_root = tmp_root / "subject-store"
    pre_registry = _registry_roundtrip(
        artifact_bundles,
        bundle_dir,
        registry_dir,
        lifecycle_state="release-ready",
        evidence_ref="materialized-subject-store-precondition",
    )
    materialized = artifact_bundles.materialize_artifact_subjects(
        bundle_dir,
        store_root=store_root,
        registry_dir=registry_dir,
        manifest_ref=manifest,
        consumer_intent="agent",
        expected_source_repo="aoa-evals",
    )
    refreshed_registry = _registry_roundtrip_with_subject_store(
        artifact_bundles,
        bundle_dir,
        registry_dir,
        store_root,
        lifecycle_state="release-ready",
        evidence_ref="materialized-subject-store-rehearsal",
    )
    latest_record = refreshed_registry.get("latest", {}).get("latest_by_artifact_class", {}).get(ARTIFACT_CLASS, {})
    store_status = latest_record.get("artifact_subject_store") if isinstance(latest_record, dict) else {}
    gate = artifact_bundles.trust_gate(
        registry_dir,
        artifact_class=ARTIFACT_CLASS,
        subject_digest=str(materialized.get("aggregate_digest") or ""),
        consumer_intent="agent",
        expected_source_repo="aoa-evals",
    )
    return {
        "ok": bool(
            pre_registry.get("ok")
            and materialized.get("ok")
            and refreshed_registry.get("ok")
            and isinstance(store_status, dict)
            and store_status.get("ok") is True
            and gate.get("verdict") == "allow"
        ),
        "pre_registry": pre_registry,
        "materialized": materialized,
        "refreshed_registry": refreshed_registry,
        "trust_gate": gate,
    }


def _run_adversarial_checks(
    artifact_bundles: Any,
    abyss_repo_root: Path,
    manifest: Path,
    subject: Path,
    bundle_dir: Path,
    registry_dir: Path,
) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="aoa-evals-report-index-negative-", dir=_default_tmp_root()) as tmp:
        tmp_root = Path(tmp)
        checks = {
            "missing_sbom": _verify_missing_sbom(artifact_bundles, abyss_repo_root, bundle_dir, tmp_root),
            "wrong_slsa_subject": _verify_wrong_slsa_subject(artifact_bundles, abyss_repo_root, bundle_dir, tmp_root),
            "private_report_marker": _verify_private_report_marker(subject, tmp_root),
            "unverified_latest_rejected": _verify_unverified_latest_rejected(artifact_bundles, bundle_dir, tmp_root),
            "terminal_registry_state": _verify_terminal_registry_state(artifact_bundles, bundle_dir, tmp_root),
            "materialized_subject_store": _verify_materialized_subject_store(
                artifact_bundles,
                manifest,
                bundle_dir,
                registry_dir,
                tmp_root,
            ),
        }
    return {
        "ok": all(bool(item.get("ok")) for item in checks.values()),
        "checks": checks,
    }


def _validate_in_bundle_dir(manifest: Path, subject: Path, bundle_dir: Path, registry_dir: Path, *, clean: bool) -> dict[str, Any]:
    artifact_bundles, abyss_machine_root, package_root = _import_artifact_bundles()
    _assert_generated_index_public_safe(subject)
    if clean and bundle_dir.exists():
        shutil.rmtree(bundle_dir)
    if clean and registry_dir.exists():
        shutil.rmtree(registry_dir)
    bundle_dir.mkdir(parents=True, exist_ok=True)

    abyss_repo_root = abyss_machine_root or artifact_bundles.REPO_ROOT
    producer_command = "python scripts/validate_abyss_machine_report_index_bundle.py"
    build = artifact_bundles.build_sidecars(
        bundle_dir,
        manifest_ref=manifest,
        repo_root=abyss_repo_root,
        producer_command=producer_command,
    )
    sign = artifact_bundles.sign_bundle(bundle_dir, repo_root=abyss_repo_root)
    verify = artifact_bundles.verify_bundle(bundle_dir, repo_root=abyss_repo_root)
    release_check = artifact_bundles.release_check(bundle_dir, repo_root=abyss_repo_root)
    _assert_expected_controls(verify)
    _assert_public_sidecars_do_not_leak_local_roots(bundle_dir, abyss_machine_root)
    registry = _registry_roundtrip(
        artifact_bundles,
        bundle_dir,
        registry_dir,
        lifecycle_state="release-ready",
        evidence_ref=_portable_ref(bundle_dir) + "/artifact.verify.json",
    )
    trust_gate = _trust_gate_allow_latest(artifact_bundles, registry_dir, registry)
    _assert_public_registry_does_not_leak_local_roots(registry_dir, abyss_machine_root)
    adversarial = _run_adversarial_checks(artifact_bundles, abyss_repo_root, manifest, subject, bundle_dir, registry_dir)

    manifest_payload = _load_json(manifest)
    return {
        "ok": bool(
            build.get("ok")
            and sign.get("ok")
            and verify.get("ok")
            and release_check.get("ok")
            and registry.get("ok")
            and trust_gate.get("ok")
            and adversarial.get("ok")
        ),
        "schema": "aoa_evals_abyss_machine_report_index_artifact_bundle_validation_v1",
        "manifest_ref": _portable_ref(manifest),
        "subject_ref": _portable_ref(subject),
        "bundle_dir": _portable_ref(bundle_dir),
        "registry_dir": _portable_ref(registry_dir),
        "artifact_class": manifest_payload.get("artifact_class"),
        "required_controls": verify.get("required_controls"),
        "verified_controls": verify.get("verified_controls"),
        "abyss_machine_repo_root": str(abyss_repo_root),
        "abyss_machine_package_root": package_root,
        "registry": registry,
        "trust_gate": trust_gate,
        "adversarial_checks": adversarial,
        "steps": {
            "build_sidecars": build,
            "sign": sign,
            "verify": verify,
            "release_check": release_check,
        },
    }


def validate_bundle(
    manifest: Path,
    subject: Path,
    bundle_dir: Path | None,
    registry_dir: Path | None,
    *,
    clean: bool,
) -> dict[str, Any]:
    if bundle_dir is not None:
        target_registry = registry_dir or bundle_dir.parent / "report-index-registry"
        return _validate_in_bundle_dir(manifest, subject, bundle_dir, target_registry, clean=clean)

    tmp_root = _default_tmp_root()
    with tempfile.TemporaryDirectory(prefix="aoa-evals-report-index-bundle-", dir=tmp_root) as tmp:
        target = Path(tmp) / "report-index"
        target_registry = Path(tmp) / "report-index-registry"
        return _validate_in_bundle_dir(manifest, subject, target, target_registry, clean=False)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate generated aoa-evals report index through abyss-machine artifact bundles.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--subject", type=Path, default=DEFAULT_SUBJECT)
    parser.add_argument("--bundle-dir", type=Path)
    parser.add_argument("--registry-dir", type=Path)
    parser.add_argument("--no-clean", action="store_true", help="do not remove the previous generated bundle directory first")
    parser.add_argument("--json", action="store_true", help="print the full validation payload")
    args = parser.parse_args()

    manifest = args.manifest if args.manifest.is_absolute() else REPO_ROOT / args.manifest
    subject = args.subject if args.subject.is_absolute() else REPO_ROOT / args.subject
    bundle_dir = None
    if args.bundle_dir is not None:
        bundle_dir = args.bundle_dir if args.bundle_dir.is_absolute() else REPO_ROOT / args.bundle_dir
    registry_dir = None
    if args.registry_dir is not None:
        registry_dir = args.registry_dir if args.registry_dir.is_absolute() else REPO_ROOT / args.registry_dir

    payload = validate_bundle(manifest, subject, bundle_dir, registry_dir, clean=not args.no_clean)
    if args.json:
        print(json.dumps(payload, sort_keys=True))
    elif payload["ok"]:
        print(
            "[ok] abyss-machine report index artifact bundle verified: "
            f"{payload['bundle_dir']} ({', '.join(payload['verified_controls'])}; registry={payload['registry_dir']})"
        )
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
