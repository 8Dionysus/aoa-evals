# Release Support / Artifact Bundles Part

## Role

This part owns repo-local release artifact bundle manifests for `aoa-evals`.

It tells the OS Abyss `abyss-machine` verifier which release carrier this repo
publishes for validation. It does not define signing policy or proof meaning.

## Source Surfaces

- `mechanics/release-support/parts/artifact-bundles/manifests/report_index.bundle.json`
- `scripts/validate_abyss_machine_report_index_bundle.py`
- `generated/eval_report_index.min.json`
- `docs/validation/validation_lanes.json`

The `manifests/` payload subdirectory carries release-support bundle manifests.
`mechanics/release-support/parts/artifact-bundles/manifests/report_index.bundle.json`
describes `generated/eval_report_index.min.json` as an OS Abyss artifact bundle
subject for the root `abyss-machine` verifier, with lifecycle and registry
consumer contract metadata for release-ready selection.
Signing controls stay in `abyss-machine` artifact policy.

## Inputs

- generated report-index carrier from `generated/eval_report_index.min.json`;
- `abyss-machine` artifact policy and verifier implementation;
- local release lane command authority from `docs/validation/validation_lanes.json`;
- CI or local verifier dependency through `ABYSS_MACHINE_REPO_ROOT`, a sibling
  `abyss-machine` checkout, or an installed `abyss_machine` package.

## Outputs

- release-support bundle manifest payloads under `manifests/`;
- release-check validation that builds temporary sidecars, signs or records the
  policy decision, verifies the bundle, promotes durable release-ready evidence
  with source and host-managed trust-root metadata, materializes the
  report-index subject store, checks release-ready/latest selection, checks the
  consumer `trust-gate`, and runs the `abyss-machine` release check;
- blocking release failures when ABI/SBOM/SLSA controls required by
  `abyss-machine` policy are missing or invalid;
- adversarial release-carrier checks for missing SBOM, wrong SLSA subject,
  private generated-report markers, unverified latest registration, terminal
  lifecycle states, and revoked-record `trust-gate` denial.

## Stronger Owner Split

This part owns the local manifest that names the carried `aoa-evals` artifact.

`abyss-machine` owns artifact classes, ABI epochs, sidecar formats, signing
requirements, deferred-control reasons, and verifier behavior. Bundle-local eval
sources and reports own proof meaning. `generated/eval_report_index.min.json`
remains a derived reader; its release bundle validation proves carrier
integrity, not eval claim strength.

## Stop-Lines

| Pressure | Route |
| --- | --- |
| signing doctrine, artifact-class policy, sidecar schema, or verifier behavior changes | `abyss-machine` policy/verifier route |
| generated report index treated as proof authority | bundle-local eval sources and reports |
| release bundle validation treated as tag, GitHub Release, PR approval, or observed GitHub `Repo Validation` | current git, GitHub, tag, and release evidence |
| local host/runtime/private evidence promoted into public artifact sidecars | OS Abyss local provenance route and public-safety validator failure |
| GitHub workflow treated as the only verifier backend | local OS Abyss verifier route through `ABYSS_MACHINE_REPO_ROOT`, sibling checkout, or installed package |

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable
command ownership is centralized in the parent `parts/AGENTS.md` lane.

## Next Route

Use this part when changing which generated release carrier `aoa-evals` asks
`abyss-machine` to verify. Use `abyss-machine` when changing the policy,
sidecar, or verifier contract itself.
