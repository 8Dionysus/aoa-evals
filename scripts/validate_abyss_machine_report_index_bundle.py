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


def _import_artifact_bundles() -> tuple[Any, Path | None]:
    for candidate in _candidate_abyss_machine_roots():
        root = candidate.expanduser().resolve()
        module_root = root / "src"
        if (module_root / "abyss_machine" / "artifact_bundles.py").is_file():
            sys.path.insert(0, str(module_root))
            return importlib.import_module("abyss_machine.artifact_bundles"), root
    return importlib.import_module("abyss_machine.artifact_bundles"), None


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


def _assert_expected_controls(verify: dict[str, Any]) -> None:
    required = verify.get("required_controls")
    verified = verify.get("verified_controls")
    if required != EXPECTED_REQUIRED_CONTROLS:
        raise ValueError(f"unexpected required controls: {required!r}")
    if verified != EXPECTED_REQUIRED_CONTROLS:
        raise ValueError(f"unexpected verified controls: {verified!r}")


def _validate_in_bundle_dir(manifest: Path, subject: Path, bundle_dir: Path, *, clean: bool) -> dict[str, Any]:
    artifact_bundles, abyss_machine_root = _import_artifact_bundles()
    _assert_generated_index_public_safe(subject)
    if clean and bundle_dir.exists():
        shutil.rmtree(bundle_dir)
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

    manifest_payload = _load_json(manifest)
    return {
        "ok": bool(build.get("ok") and sign.get("ok") and verify.get("ok") and release_check.get("ok")),
        "schema": "aoa_evals_abyss_machine_report_index_artifact_bundle_validation_v1",
        "manifest_ref": _portable_ref(manifest),
        "subject_ref": _portable_ref(subject),
        "bundle_dir": _portable_ref(bundle_dir),
        "artifact_class": manifest_payload.get("artifact_class"),
        "required_controls": verify.get("required_controls"),
        "verified_controls": verify.get("verified_controls"),
        "steps": {
            "build_sidecars": build,
            "sign": sign,
            "verify": verify,
            "release_check": release_check,
        },
    }


def validate_bundle(manifest: Path, subject: Path, bundle_dir: Path | None, *, clean: bool) -> dict[str, Any]:
    if bundle_dir is not None:
        return _validate_in_bundle_dir(manifest, subject, bundle_dir, clean=clean)

    tmp_root = _default_tmp_root()
    with tempfile.TemporaryDirectory(prefix="aoa-evals-report-index-bundle-", dir=tmp_root) as tmp:
        target = Path(tmp) / "report-index"
        return _validate_in_bundle_dir(manifest, subject, target, clean=False)


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate generated aoa-evals report index through abyss-machine artifact bundles.")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--subject", type=Path, default=DEFAULT_SUBJECT)
    parser.add_argument("--bundle-dir", type=Path)
    parser.add_argument("--no-clean", action="store_true", help="do not remove the previous generated bundle directory first")
    parser.add_argument("--json", action="store_true", help="print the full validation payload")
    args = parser.parse_args()

    manifest = args.manifest if args.manifest.is_absolute() else REPO_ROOT / args.manifest
    subject = args.subject if args.subject.is_absolute() else REPO_ROOT / args.subject
    bundle_dir = None
    if args.bundle_dir is not None:
        bundle_dir = args.bundle_dir if args.bundle_dir.is_absolute() else REPO_ROOT / args.bundle_dir

    payload = validate_bundle(manifest, subject, bundle_dir, clean=not args.no_clean)
    if args.json:
        print(json.dumps(payload, sort_keys=True))
    elif payload["ok"]:
        print(
            "[ok] abyss-machine report index artifact bundle verified: "
            f"{payload['bundle_dir']} ({', '.join(payload['verified_controls'])})"
        )
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
