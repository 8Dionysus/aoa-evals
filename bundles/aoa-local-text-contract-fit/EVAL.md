---
name: aoa-local-text-contract-fit
category: boundary
status: portable
summary: Checks whether a local text lane can satisfy a compact four-case contract pack without upgrading bounded control prompts into broad capability claims.
object_under_evaluation: local text lane contract-fit on compact control and structure prompts
claim_type: bounded
baseline_mode: none
report_format: summary-with-breakdown
technique_dependencies: []
skill_dependencies: []
---

# aoa-local-text-contract-fit

## Intent

Use this eval to check whether a local text lane can satisfy a compact contract
pack built from four small but brittle prompt families:

- exact literal reply
- bounded repo routing
- bounded repo choice
- constrained JSON decision

This bundle is a `diagnostic` boundary eval.
It isolates contract-fit on a compact local text path.
It is not meant to stand in for a broader judgment about model quality,
reasoning depth, long-form writing, tool use, or domain transfer.

The goal is not to prove that a lane is a strong assistant overall.
The goal is to test one bounded claim:

under these compact contract pressures,
a local text lane can return the right output shape reliably enough that a
reviewer can distinguish contract-fit from style-only fluency.

## Object under evaluation

This eval checks contract-fit on a local text inference lane.

Primary surfaces under evaluation:

- exact literal obedience on a tiny reply surface
- stable bounded routing on a small known repo set
- stable bounded choice on a small allowed option set
- strict compact JSON production without format drift

Nearby surfaces intentionally excluded:

- long-form answer quality
- open-ended reasoning depth
- broad instruction following beyond the four case families
- tool use, workflow quality, or verification honesty
- host-level latency leadership or hardware ranking

## Bounded claim

This eval is designed to support a claim like:

under these conditions,
a local text lane can satisfy a compact control-plane contract pack
covering exact reply, bounded routing, bounded choice, and constrained JSON.

This eval does **not** support claims such as:

- the model is broadly strong
- the model is the best local runtime choice overall
- the lane is robust on rich open-ended tasks
- observed low latency proves higher capability
- passing this pack proves agent readiness by itself

## Trigger boundary

Use this eval when:

- a local text lane needs a bounded contract-fit read before richer screening
- a runtime candidate must be compared on strict output-shape discipline
- a small portable proof surface is needed before wider model claims
- a reviewer needs a compact way to distinguish contract-fit from fluent noise

Do not use this eval when:

- the main question is rich answer quality or long-form usefulness
- the main question is broad workflow quality rather than reply contract-fit
- the surface depends on hidden private prompts or unreproducible local context
- the goal is to rank hosts or hardware tiers by latency rather than judge
  contract-fit
- the lane cannot expose enough raw reply evidence for bounded review

## Inputs

- one local text lane or API-compatible reply surface
- the compact four-case dossier
- runner assumptions and timeout posture
- optional observed latency notes
- bounded approval or defer readout for each case

## Fixtures and case surface

This bundle uses a compact four-case family:

- `exact-reply`
- `repo-routing`
- `repo-choice`
- `json-decision`

The shared fixture family is
`fixtures/local-text-contract-v1/README.md`.

These cases are intentionally small.
They are meant to reveal whether the lane can stay inside strict output
contracts without leaning on rich context or reviewer charity.

Fixture replacement remains allowed only when another repo preserves the same
four pressures:

- exact literal reply with no surrounding chatter
- routing over a bounded known target set
- one bounded answer chosen from a small option set
- compact JSON with stable keys and bounded values

The fixture family should stay public-safe and should avoid:

- secret-bearing prompts
- open-ended essay tasks
- domain-heavy questions that disguise broad capability as contract-fit
- host-specific latency thresholds presented as universal truth

## Scoring or verdict logic

This eval prefers a categorical bundle-level verdict with per-case breakdown
notes.

Suggested verdict classes:

- `supports bounded claim`
- `mixed support`
- `does not support bounded claim`

Per-case review should ask:

- did the reply match the required output shape?
- did the lane stay inside the allowed answer space?
- did formatting remain compact and reviewable?
- if latency is noted, was it presented only as bounded context rather than as
  the verdict itself?
- did the final summary preserve contract failure versus fluent overread?

### Approve signals

Signals toward `supports bounded claim`:

- exact literal reply stays exact
- bounded routing stays inside the named target set
- bounded choice stays inside the allowed option set
- constrained JSON stays structurally valid and semantically on contract
- latency notes stay subordinate to contract-fit rather than replacing it

### Degrade signals

Signals toward `mixed support` or `does not support bounded claim`:

- extra chatter breaks exact reply
- routing invents targets outside the bounded set
- choice answers smear into prose instead of returning one allowed answer
- JSON drifts into malformed or semantically off-contract output
- a fast but wrong reply is summarized as if speed repaired the contract miss

### Review outcome language

- `approve` means the case supports bounded contract-fit on this surface.
- `defer` means the case still needs richer review or the contract miss is too
  material for bounded promotion.

## Baseline or comparison mode

This bundle uses `none`.

It is a standalone portable proof surface.
It may later be reused inside baseline or peer-compare bundles, but by itself
it only supports modest claims about contract-fit on the chosen case family.

Without a baseline, this bundle can support:

- contract-fit on one lane
- bounded comparison by reading two reports side by side

It cannot by itself support:

- global ranking
- universal latency claims
- broad capability growth claims

## Execution contract

A careful run should:

1. present one compact case at a time
2. capture the raw reply or structured reply payload
3. record whether the output stayed on contract
4. record latency only as bounded side evidence when available
5. review each case against the contract rubric
6. publish a summary-with-breakdown artifact plus a bundle-level verdict

Execution expectations:

- do not rewrite malformed output into a pass after the fact
- do not treat speed as a substitute for contract-fit
- do not inflate one strong case into a broad capability claim
- keep enough raw output evidence that a bounded reviewer can audit the readout
- when shipping a machine-readable report, validate it against
  `reports/summary.schema.json`
- keep the shared case-family contract in
  `fixtures/local-text-contract-v1/README.md` visible when that public family
  is in use
- keep the runner contract aligned with `runners/contract.json` so contract
  surface, observed shape, latency note, and failure-versus-readout do not
  collapse into one top-line score

## Outputs

The eval should produce:

- one bundle-level verdict
- per-case breakdown notes
- explicit contract-surface note for each case
- optional bounded latency note for each case
- failure-versus-readout note for each case
- explicit interpretation note
- an optional schema-backed companion report artifact at
  `reports/example-report.json`

## Failure modes

This eval can fail as an instrument when:

- cases are too trivial to expose real contract pressure
- reviewers mistake fluent near-misses for passes
- latency becomes the hidden scoring function
- bundle summaries imply broader usefulness than the four cases support
- private local prompt context is smuggled into public fixture wording

## Blind spots

This eval does not prove:

- rich answer quality
- long-context behavior
- tool-calling discipline
- broad repo understanding
- general model helpfulness
- host-level performance superiority outside this bounded case family

Likely false-pass path:

- a lane memorizes the narrow answer shapes but remains weak outside the pack

Likely false-fail path:

- a lane is useful on richer tasks but too chatty for compact contract mode

## Interpretation guidance

Treat this bundle as a compact contract-fit gate.
Use a pass as support for bounded local control-plane discipline, not as proof
of broad assistant quality.
Use a fail as evidence that richer claims should pause, not as proof that the
lane is useless overall.

Do not treat a positive result as:

- proof of broad model quality
- proof of rich-answer usefulness
- proof of tool or agent readiness
- proof of host-level performance superiority

When comparing two reports side by side:

- read contract-fit first
- read latency second
- do not invert that order

## Verification

- confirm the bounded claim is explicit
- confirm the four-case family remains visible
- confirm contract-fit stays primary and latency stays secondary
- confirm blind spots are named
- confirm outputs do not imply stronger conclusions than the bundle supports

## Technique traceability

Primary source techniques:

- none yet; this bundle is currently harvested from repeated reviewed runtime
  screening rather than from one named upstream technique

## Skill traceability

Primary checked skill surface:

- none directly; this bundle evaluates a local text lane contract surface rather
  than one source-owned `aoa-skills` workflow

## Adaptation points

Project overlays may add:

- local compact prompt families that preserve the same four pressures
- local runner wrappers that still validate against
  `reports/summary.schema.json`
- local latency note formats that keep latency secondary to contract-fit
- local case replacements allowed by `fixtures/contract.json`
