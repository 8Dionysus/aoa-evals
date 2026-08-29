---
name: aoa-code-observation-refactor-integrity
category: capability
status: draft
summary: Checks whether a provider-neutral code-observation envelope stays coherent across refactor-sensitive lineage, freshness, invalidation, provenance, parity, and affected-test cases without claiming provider correctness.
object_under_evaluation: provider-neutral code-observation envelope under controlled refactor cases
claim_type: bounded
baseline_mode: none
report_format: summary-with-breakdown
technique_dependencies: []
skill_dependencies: []
capability_dependencies: []
---

# aoa-code-observation-refactor-integrity

## Intent

This draft capability eval makes one PROVEN slice concrete for code
intelligence: it checks whether a provider-neutral observation envelope stays
internally coherent across controlled refactor pressure.

The bundle is deliberately contract-first. A fixture provider can exercise the
route without pretending to be a live LSP, an indexed KAG source, a parser, a
SCIP implementation, or an admitted proof owner.

## Object under evaluation

The object is a bounded code-observation envelope containing:

- a provider identity and configuration digest;
- a source epoch and freshness reference;
- live and indexed observation-plane labels;
- semantic identity and lineage posture;
- invalidation scope and delta/full parity evidence;
- explicit metrics, provenance, and affected-test selection.

An optional provider-execution envelope binds actual provider state to the
reviewed `abyss-machine` code-intelligence contract, provider identity, source
epoch, invalidation universe, latency/resource measurements, and a
timestamp-stripped reproducibility digest. It is an evidence bridge for this
bundle, not an admission receipt or a normalized observation report. The
machine binding carries the G41 snapshot epoch, workspace-manifest digest, and
raw contract-file digest; a later retrievable file is not silently substituted
when those identities drift.

The bundle also contains a source-owned execution fixture and deterministic
provider candidate. `runners/run_scenarios.py execute-provider` materializes
before/after source trees, parses both snapshots, computes actual symbol
fingerprints and dependency invalidation, records explicit deletion absence,
derives affected tests from the fixture-local graph, and runs full/delta parity.
The emitted envelope is `source-bound-provider-candidate` with
`admission_state=not_admitted`; it is not a current installed-provider or
machine-health observation.

The bundle also has a separate source-observation evidence route. It parses a
checked-in synthetic source corpus with Python's standard-library AST parser
and, when present, host Ctags. That route records complete case visibility but
marks both providers `not_admitted`; it does not turn symbol visibility into
provider correctness, live runtime state, KAG meaning, or proof.

The reusable cases live at
`mechanics/proof-infra/parts/fixture-families/fixtures/refactor-torture-v1/`.
The bundle-local fixture contract connects that public-safe family to this
claim surface.

## Bounded claim

Under the synthetic refactor-torture cases, an observation report supports a
bounded contract claim when every case preserves its declared operation,
lineage/freshness expectation, invalidation scope, required planes, metrics,
and provenance, with explicit treatment for ambiguity, parity,
reproducibility, and affected tests.

This eval does not support claims that:

- a parser, Tree-sitter, SCIP, LSP, ctags, KAG, or provider is correct;
- a live or indexed source is current outside the supplied source epoch;
- an observation is accepted as canonical owner truth;
- a green runner is an aoa-evals proof verdict, owner acceptance, deployment,
  runtime, transport, or semantic-acceptance receipt.

Complete provider-execution coverage is not inferred from a four-case or
otherwise unlabelled scratch envelope; a whole-family claim requires an
explicit `coverage.mode: complete` declaration.

## Trigger boundary

Use this eval when:

- the question is whether a code-observation report keeps refactor-sensitive
  contract fields visible and internally consistent;
- a provider-neutral contract needs synthetic pressure before provider-specific
  evidence is available;
- lineage, freshness, invalidation, parity, or affected-test fields may be
  silently omitted by a report.

Do not use this eval when:

- provider-specific parser/index/LSP validation is the question;
- `aoa-kag` canonical navigation admission is the question;
- `abyss-stack` runtime or transport evidence is the question;
- source/CI, artifact admission, deployment, or owner acceptance is the
  question;
- a reviewed PROVEN verdict is the question.

## Inputs

- the shared `refactor-torture-v1` fixture manifest;
- one provider-neutral raw observation report;
- an optional actual provider-execution envelope validated against the
  `abyss-machine` machine-contract digest and owner split;
- optional bounded provider-observation evidence from the checked-in source
  corpus, with Python-AST and optional host-Ctags observations;
- provider identity and configuration digest;
- source epoch, observation planes, and case-specific evidence fields.

## Fixtures and case surface

The reusable public-safe family is
`mechanics/proof-infra/parts/fixture-families/fixtures/refactor-torture-v1/`.

The twelve cases cover rename, move, signature change, add, delete, import
change, multi-file impact, split, merge, stale index, delta/full parity, and
affected-test selection. The bundle-local `fixtures/contract.json` owns the
connection between this family and the bundle claim.

## Scoring or verdict logic

The runner first validates the raw envelope against its JSON Schema, then
checks every case against the manifest. A case fails when its operation,
required plane, expected lineage/freshness posture, invalidation scope,
required metric, provenance, or stronger local oracle is missing or mismatched.

The categorical bundle verdict is either:

- `supports bounded contract`;
- `does not support bounded contract`.

The report keeps case-level issue codes and pass/fail outcomes visible.

## Baseline or comparison mode

This bundle uses `none`. It is a standalone contract-integrity check over one
bounded synthetic observation envelope. It does not compare providers, source
epochs, runtimes, or model quality.

## Execution contract

1. Load the shared fixture manifest and compute its canonical digest.
2. Validate a raw observation report against the local JSON Schema.
3. Check all twelve case-specific semantic invariants.
4. When supplied, validate provider-observation evidence against its source
   manifest. Available providers must expose one observation per case; the
   evidence remains explicitly not admitted.
5. When supplied, validate provider execution separately with
   `validate-provider-execution`; this binds runtime state and fixture case IDs
   without converting the result into a proof, admission, or acceptance claim.
   Its `coverage.mode: complete` path additionally requires every fixture case,
   reproducibility digests, safe invalidation/deletion accounting, observed
   symbol snapshots, stable-lineage evidence, freshness epochs, affected-test
   selection, and the delta/full parity projections for the parity case.
6. Execute the source-bound provider candidate with `execute-provider`, then
   validate that emitted envelope through the same complete-coverage boundary.
   This produces candidate evidence only; it does not manufacture machine
   admission or provider acceptance.
7. Emit a deterministic categorical summary with one breakdown entry per case.

The raw report is evidence input. The summary is a candidate report artifact,
not a promoted proof result.

## Outputs

- fixture validation JSON;
- raw report validation JSON;
- provider-execution binding JSON with explicit admission and owner-boundary
  fields;
- source-bound complete provider-execution envelope with one observed execution
  for each torture case;
- provider-observation evidence JSON with source-root, case-coverage, provider,
  and non-admission fields;
- a deterministic summary with one breakdown entry per case;
- explicit issue codes for missing or inconsistent evidence.

## Failure modes

This eval can fail as an instrument when:

- contract completeness is mistaken for provider correctness;
- plane labels are read as canonical owner truth;
- a synthetic parity or affected-test oracle is overread as production proof;
- a green runner is promoted without independent owner review.

## Blind spots

This eval does not prove:

- parser recall, index completeness, or provider correctness;
- LSP or runtime latency and resource safety in production;
- admission, installation, trust, or deployment of the bound provider;
- completeness or correctness of a host Ctags installation beyond the emitted
  local observations;
- cross-repository semantic identity or actual blast-radius accuracy;
- the quality of a selected test set or canonical KAG currentness;
- proof acceptance, deployment, runtime, transport, or owner acceptance.

## Interpretation guidance

Treat a positive result as support for one bounded claim: the supplied
synthetic observation envelope is internally complete and coherent under the
declared refactor cases.

Keep the bundle `draft`, `review_required: true`, and `export_ready: false`
until aoa-evals owner review explicitly changes that posture. A positive result
does not establish provider quality, currentness beyond the named epoch, or any
stronger owner-plane acceptance.

Do not treat a positive result as:

- provider correctness or canonical navigation admission;
- production performance, semantic blast-radius accuracy, or selected-test
  quality;
- a promoted proof verdict, deployment, runtime, transport, or owner
  acceptance.

## Verification

- validate the shared fixture manifest;
- validate the example raw observation report;
- collect and validate the bounded local provider-observation evidence;
- validate a complete provider-execution envelope and its negative cases;
- execute and validate the source-bound provider candidate across all twelve
  cases, including deletion, lineage ambiguity, stale-state and parity;
- run the deterministic scenario summary;
- run the focused bundle test and owner repository validators.

## Technique traceability

No direct technique dependency is claimed by this draft bundle.

## Skill traceability

No direct callable skill dependency remains. Provider, KAG, runtime, and owner
acceptance questions route to their owning surfaces.

## Adaptation points

- add provider-specific fixture adapters only after an owner-reviewed need;
- keep source epoch and provenance fields explicit when real evidence is added;
- keep legacy scratch provider-execution envelopes explicitly partial; do not
  infer whole-family coverage without the complete coverage declaration;
- treat the source-bound executor as a candidate evidence generator, not as the
  reviewed installed provider or a substitute for a later exact MACHINE/LIVE
  disposition;
- add a reviewed comparison or baseline only through the appropriate owner
  route, not by widening this standalone contract bundle.
