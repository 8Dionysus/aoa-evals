# Eval Forge Readiness Layer

- Decision ID: AOA-EV-D-0244
- Status: Accepted
- Date: 2026-06-26
- Owner surface: `docs/guides/EVAL_FORGE_READINESS_LAYER.md`

## Index Metadata

- Original date: 2026-06-26
- Surface classes: agent-route, local-eval-port, validation, MCP access plane, session evidence
- Mechanic parents: proof-object, audit
- Guard families: eval-forge readiness, local-port boundary, candidate-only mining, MCP write confinement, freshness drift
- Posture: accepted readiness-layer rationale

## Context

OS Abyss now has central `aoa-evals` proof bundles, repo-local `evals/` ports,
session-mining candidate packets, support-registry classification, and an
`aoa-evals-mcp` access plane. Those parts are useful, but a new agent session
still needs one route that answers:

- which existing evals or local ports should be checked first;
- when to reject noise instead of creating a candidate;
- how to preserve session evidence without promoting it to proof;
- how to dry-run local writes through MCP without widening authority;
- which freshness and dirty-state gates can make a result unsafe to trust.

Without a readiness layer, agents can rediscover the pieces in a different
order, shrink the work into prose, or accidentally treat generated/session/MCP
readouts as stronger than source proof.

## Options Considered

- Keep the surfaces separate and rely on `aoa-eval` skill routing.
- Move all eval creation into central `aoa-evals` bundles immediately.
- Treat Eval Forge as a readiness layer over central proof, local ports,
  candidate-only session evidence, and MCP write gates.

## Decision

Choose the readiness layer.

`aoa-evals` owns the Eval Forge readiness guide and checker. Repo-local
`evals/` ports own local pressure capture. `.aoa` owns raw/session evidence
only as candidate evidence. `abyss-stack` owns the runnable `aoa-evals-mcp`
package and may expose dry-run-first, path-bounded local-port writes with audit
receipts. Central proof adoption, verdicts, scoring, regression posture, and
bundle promotion remain in `aoa-evals`.

## Rationale

This route lets a large agent session start from one current packet instead of
from scattered memory. It also keeps authority layers separate:

- local ports make pressure cheap to capture without becoming proof doctrine;
- session-mining packets can preserve real failures without becoming reviewed
  truth;
- support-registry classes stop write-capable scripts from being treated as
  direct eval application;
- MCP write receipts make local mutation auditable while still below central
  proof authority;
- freshness gates keep stale mirrors, live-tail lag, generated dashboards, and
  dirty repos visible before a proof claim is made.

## Consequences

- Positive: future agents can use the readiness entrypoint and see the current
  route, blockers, candidate queue, local-port status, support classification,
  and verification routes.
- Positive: manual session mining can remain strict and useful because rejected
  and deferred cases are part of the route, not lost context.
- Tradeoff: readiness can show warnings while live sessions are still changing;
  warnings are allowed only when they are explicit and routed to their owner.
- Follow-up: if MCP ever needs central writes, evidence acceptance, verdicts,
  scoring, receipt publication, or non-stdio exposure, create a new decision
  before implementation.

## Current Applicability

As of 2026-07-16:

- Still valid: `aoa-evals` is the proof owner and the readiness layer is a
  routing/checking surface only.
- Changed: agents should start eval-control work from
  `docs/guides/EVAL_FORGE_READINESS_LAYER.md` and
  `scripts/check_eval_forge_readiness.py`; local suite routing now reports the
  `absent`/`invalid`/`stale`/`ready` execution state from AOA-EV-D-0245, where
  ready means source-contract-ready and still requires owner/apply JIT
  revalidation, environment capture, and an execution receipt.
- Changed: `aoa-eval` is selected by the current `aoa-skills`
  `os-user-default` profile and the logical
  `portable-consumer-advertised` build profile. Readiness checks source,
  logical export, release revision, catalog, OS-profile selection, and current
  installation as separate signals; prompt visibility remains fresh-session
  host evidence.
- Superseded by: none.

## Review Log

### 2026-07-18 - Adopt the v2 OS profile and logical export contract

- Previous assumption: `aoa-eval` remained a deferred source outside the
  normal user profile and required a physical repo-local portable copy.
- New reality: the accepted v2 `aoa-skills` contract selects the owner package
  in `os-user-default` and describes its portable delivery logically through
  `portable-consumer-advertised`, the export map, and the release revision.
- Check correction: readiness now separates owner-source contract readiness,
  managed-copy installation, and fresh prompt visibility. No one signal proves
  selection, execution, or outcome benefit.
- Validation: source-only refresh, OS-profile check, focused contract tests,
  fresh-session inspection, generated parity, and repository validation.

### 2026-07-16 - Align skill posture with the consolidated capability ecosystem

- Previous assumption: readiness could verify the former
  `user-aoa-foundation` profile, runtime discovery index, and trigger harness
  as current `aoa-eval` adoption signals.
- New reality: those surfaces were retired. `user-default` contains only
  `aoa-decision`; `aoa-eval` remains a deferred explicit source in
  `repo-capability-sources`, and fresh-session prompt visibility stays host
  evidence.
- Check correction: dashboard `--check` compares source-derived fields and
  JSON-to-Markdown snapshot parity; a naturally newer MCP, `.aoa`, Git, or
  local-port observation remains freshness evidence rather than false source
  drift.
- Reason: keeping removed surfaces in the dashboard turned correct profile
  absence into a false failure and obscured the owner-approved deferred
  disposition.
- Source surfaces updated: Eval Forge readiness guide, generated route card,
  readiness builder, session-start reader, script inventory, generated
  dashboard, and focused contract tests.
- Validation: current `aoa-skills` profile verifier, fresh prompt inspection,
  generated parity, focused tests, and repository validation.

### 2026-07-10 - Add inspect-only local suite execution readiness

- Previous assumption: suite-note presence was enough for the readiness layer
  to suggest local apply.
- New reality: only a source-contract-ready execution sidecar suggests
  owner/apply; absent, invalid, and stale states route to design or repair, and
  readiness itself never claims pinned runtime reproducibility.
- Compatibility correction: Forge, dashboard, and promotion consumers
  normalize v1/unknown inventory first; injected ready state becomes `absent`.
- Portability correction: generated readiness and MCP-root paths name the
  canonical owner checkout, never the implementation `.worktrees/` path.
- Reason: readiness must not turn prose, malformed paths, or stale source
  hashes into executable support.
- Source surfaces updated: Eval Forge router, readiness dashboard/check,
  session-start packet, promotion dry-run, local-port inventory v2, and their
  owner docs.
- Validation: use the current owner validation route; historical run evidence
  remains in Git and CI history.

## Boundaries

Do not infer that Eval Forge can accept proof, compute verdicts, set scores,
mint baselines, promote candidates, mutate central bundles through MCP, or make
session evidence reviewed truth.

Do not infer that Eval Forge, readiness, dashboard, session-start, promotion
review, inventory, generated readers, or MCP may execute local suite argv.

Do not infer that a warning-free readiness check proves an eval claim. It proves
that the routing layer is ready enough to choose the next owner surface.

## Validation

Current executable checks are owned by
`docs/validation/COMMAND_AUTHORITY.md` and the nearest `AGENTS.md`.
