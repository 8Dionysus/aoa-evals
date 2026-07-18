# Local Eval Suite Execution Contract

- Decision ID: AOA-EV-D-0245
- Status: Accepted
- Date: 2026-07-10
- Owner surface: `mechanics/proof-object/parts/eval-authoring/schemas/local-eval-suite-execution.schema.json`, `scripts/validate_local_eval_port.py`, and `docs/guides/LOCAL_EVAL_PORT_STANDARD.md`

## Index Metadata

- Original date: 2026-07-10
- Surface classes: local-eval-port, validation, agent-route, MCP access plane
- Mechanic parents: proof-object
- Guard families: local suite execution, source freshness, path confinement, no-execution routing
- Posture: accepted execution-contract rationale

## Context

The local eval-port standard allowed `evals/suites/*.suite.md` notes to preserve
suite pressure. Inventory and Eval Forge then inferred a runnable suite from
the note's presence. A note does not identify a machine-safe argv, working
directory, timeout, accepted exit codes, entrypoint, or the source revision it
was reviewed against. That inference could route stale prose as executable
support and gave read-only routing surfaces no reliable way to distinguish
missing, malformed, stale, and ready suite contracts.

## Options Considered

- Keep treating every `.suite.md` note as runnable.
- Put a free-form shell command in Markdown frontmatter.
- Add a source JSON sidecar with schema, path, hash, authority, and invocation
  boundaries while keeping the Markdown note human-readable and non-runnable.
- Let inventory, Eval Forge, readiness, or MCP execute a discovered sidecar.

## Decision

Use `evals/suites/<slug>.suite.json` with
`schema_version: local_eval_suite_execution_v1` as the only machine-readable
local suite execution contract.

The sidecar carries `runner.kind: python_pytest` with exact
`python|python3 [-B] -m pytest [allowlisted flags]
<cwd-relative-entrypoint-arg>` grammar,
repo-relative `runner.cwd`, timeout, accepted success exit codes, and file/tree
SHA256 tracked sources. `entrypoint_ref` is canonical repo-relative source
identity; the final argv token occurs once and must resolve from `runner.cwd`
to that exact file without traversal.
The only plugin option is the fixed write-avoidance pair
`-p no:cacheprovider`; arbitrary argv-selected plugin loading remains invalid.
The contract does not suppress or prove ambient pytest plugins, config files,
or environment variables. Owner/apply records those runtime influences through
the required environment capture before interpreting an execution receipt.
`auto_run_allowed`, `proof_authority`, `promotion_allowed`, and
`runtime_reproducibility_proven` are fixed to `false`;
`jit_revalidation_required`, `environment_capture_required`, and
`execution_receipt_required` are fixed to `true`; and readiness scope is
`source-contract-ready`.

Resolve owner identity from the Git common-dir and `origin` repository name
when available. For a non-Git portable extraction, accept the declared owner
only when at least two recognized source manifests agree:
`evals/PORT.yaml`, `capabilities/port.manifest.json`, or
`skills/port.manifest.json`. Conflicting declarations are invalid; a fixture
without two agreeing declarations falls back to its target basename. The PORT,
suite/report notes, and sidecars must use that canonical owner. A named
worktree or extraction-directory basename is not repository identity when
stronger source agreement exists.

Suite execution state is exactly `absent`, `invalid`, `stale`, or `ready`.
Multiple sidecars aggregate in this priority:
`invalid > stale > ready > absent`.

Inventory, Eval Forge, readiness, dashboard, session-start, promotion review,
generated readers, and MCP may inspect and route the contract but never invoke
`runner.argv`. `ready` means only that source contract and tracked hashes are
current; it does not establish a pinned interpreter, dependency environment,
or reproducible runtime. Only the selected repository owner or
`aoa-eval-apply` may proceed, after JIT revalidation, and must invoke the exact
validated argv, working directory, timeout, and accepted exit codes while
capturing environment metadata and an execution receipt.

`AOA-EV-D-0241` is not widened. MCP may continue writing `.suite.md` notes,
but `.suite.json` sidecars remain read-only to MCP until a separate decision.

## Rationale

The sidecar separates human design pressure from executable intent and makes
source freshness deterministic. A typed runner with an exact semantic grammar
closes interpreter/module/dispatcher bypasses that shell-free tokenization alone
does not close. Repo-relative, non-symlink paths prevent checkout escape;
tracked hashes make source drift visible before application. Canonical Git
identity keeps named worktrees valid without letting arbitrary directory names
redefine ownership. Keeping all discovery and readiness surfaces inspect-only
preserves the existing proof and mutation boundaries.

The typed argv allowlist is not a sandbox. Ambient pytest plugin discovery,
configuration, environment, interpreter, and installed dependency state remain
runtime evidence to capture, not properties proven by the source sidecar.

## Consequences

- Positive: `.suite.md` alone can no longer be misreported as runnable.
- Positive: owner/apply receives an exact, reviewable invocation contract.
- Positive: stale sources route to hash review instead of silent execution.
- Positive: named worktrees retain the PORT/common-dir/origin owner identity.
- Positive: portable non-Git extractions retain owner identity across arbitrary
  destination directory names when independent owner manifests agree.
- Positive: a lone or conflicting portable declaration cannot override the
  fallback identity.
- Positive: inline interpreter execution, arbitrary executables, alternate
  modules, and runtime dispatch wrappers cannot masquerade as reviewed pytest
  entrypoints.
- Positive: generated readiness paths remain on the canonical owner checkout
  even when the builder reads an isolated implementation worktree.
- Tradeoff: each runnable local suite needs a reviewed JSON sidecar and hash
  refresh when tracked sources change.
- Tradeoff: tree hashes use a repository-defined deterministic algorithm, so
  producers must use the validator helper rather than an ad hoc directory hash.
- Tradeoff: `ready` remains source-contract readiness; reproducible-runtime
  claims require stronger pinned environment evidence outside this sidecar.
- Follow-up: owner/apply must JIT-revalidate and preserve environment plus
  execution receipt evidence for each invocation.
- Follow-up: stack MCP consumers dual-read inventory v1 and v2 during rollout;
  every consumer normalizes v1/unknown input first, so even an injected ready
  field maps to `absent`, never runnable.

## Current Applicability

As of 2026-07-18:

- Still valid: local suite execution is owner-local support below central
  proof authority.
- Changed: runnable routing now requires a source-contract-ready JSON sidecar,
  a canonical owner identity, typed `python_pytest` argv, JIT revalidation,
  environment capture, and an execution receipt.
- Changed: non-Git portable owner identity requires agreement from at least two
  recognized owner manifests instead of treating an extraction directory name
  as canonical repository identity.
- Superseded by: none.

## Boundaries

This decision does not define a central verdict, score, regression result,
baseline, proof acceptance, receipt, or promotion route.

It does not authorize inventory, Eval Forge, readiness, dashboard,
session-start, promotion review, generated readers, or MCP to execute a suite.

It does not authorize MCP to create or update `.suite.json` sidecars.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
