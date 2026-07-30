# Active-organ experiment contracts

## Role

This document routes the shared experiment-control contracts for the
`aoa-memo` active-organ research program.

The source schemas are:

- C21 `ModelPromptProviderHardwarePin`:
  `../schemas/active-organ-model-prompt-provider-hardware-pin.schema.json`;
- C22 `MemoryExperimentManifest`:
  `../schemas/active-organ-memory-experiment-manifest.schema.json`;
- C23 `MemoryRunStatusReceipt`:
  `../schemas/active-organ-memory-run-status-receipt.schema.json`.

They support repeatable experiment execution. They do not define bundle-local
proof meaning, accept evidence, compute a verdict, promote a policy, authorize
training, edit a model, mutate memory semantics, or prove a live runtime.

## Owner split

`aoa-evals` owns the experiment pin, preregistered manifest, run-status shape,
and their validation. Stronger meaning remains separated:

| Meaning | Stronger owner |
| --- | --- |
| memory objects, recall, intervention, lifecycle, and forgetting | `aoa-memo` |
| route admission and orchestration | `aoa-sdk` |
| runtime delivery and runtime evidence | `abyss-stack` |
| host capability and storage/resource facts | `abyss-machine` |
| measurement grammar | `aoa-stats` |
| bounded claim and verdict | source `EVAL.md`, `eval.yaml`, admitted evidence, and bundle-local verdict logic |
| production or policy authority | sole operator and the named effect owner |

## C21 pin

C21 freezes the exact model artifact and inference parameters, prompt-template
and system-policy identities and digests, provider/API/adapter, C18/C19 host
evidence refs, runtime artifact and dependency lock, and environment contract.
It is refs-only. Prompt text, credentials, and private hardware captures are
forbidden. The pin is evidence, not training, model-editing, or production
authority.

## C22 manifest

C22 preregisters exactly three arms:

- A: `memory_disabled`;
- B: `explicit_pull_only`;
- C: `active_organ_policy_gated`.

The manifest freezes the corpus and split digests, seeds, C21 pins, C18/C19
host plan, A/B/C policies, cost/quality/latency/outcome metrics, falsifiers,
stop conditions, budget ceilings, randomization, paired-task posture, retry
policy, privacy rules, and comparison-plan ref before the first scored run.
Any material change creates a new manifest version and excludes incompatible
runs explicitly. The manifest admits only the experiment; it cannot widen
production authority or establish a verdict.

`preregistration.manifest_sha256` is the canonical v1 self-digest. Compute it
from UTF-8 JSON with sorted keys, compact separators, one trailing newline, and
that same field replaced by `sha256:` plus 64 zeroes. The semantic validator
recomputes it, so any post-freeze content change fails closed even when the JSON
shape remains schema-valid.

## C23 receipt

C23 separates `complete`, `partial`, `invalid`, `aborted`, and `blocked`.
Executed, skipped, and blocked checks remain distinct. A green process is only
an execution fact: `benefit_claim_state` always remains
`not_established_by_run_status`. Comparison usability is false for partial,
invalid, aborted, and blocked receipts. Outcome and cost measurements enter
through owner refs and later bundle-local review.

## Version compatibility and migration

The v1 schemas are strict and fail closed on unknown fields or versions.

- Additive documentation clarification does not change schema identity.
- Adding optional metadata is allowed only when it does not weaken an
  authority, privacy, preregistration, status, or comparison invariant.
- A required-field change, enum change, arm-treatment change, authority change,
  privacy change, or status-semantics change requires a new schema version and
  a new `$id`.
- C21 pins and C22 manifests are immutable once a scored run references them.
- A corrected C23 status is a new immutable receipt with
  `supersedes_receipt_ref`; the earlier receipt remains traceable.
- Migration validates the old artifact, constructs the new version from
  owner-resolved refs, validates it against the new schema and semantic
  validator, and records explicit exclusions for runs that cannot satisfy the
  new contract.
- Unknown or unverifiable versions never receive compatibility coercion and
  cannot enter comparison or verdict review.

Executable validation and negative cases are routed by the part README,
VALIDATION marker, and parent parts `AGENTS.md`.
