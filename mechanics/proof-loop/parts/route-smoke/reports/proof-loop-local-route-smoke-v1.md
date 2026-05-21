# Proof Loop Local Route Smoke v1

## Role

This report records one public-safe local route-smoke for
`mechanics/proof-loop/`.

The route under review is:

`proof question -> selection route -> source proof object -> support contract -> candidate evidence packet -> bundle-local review -> bounded report -> optional receipt`

This file is a bounded report artifact. It is not an eval result receipt,
bundle promotion, generated reader, runtime intake artifact, sibling-owner
approval, or proof of full proof-loop completeness.

## Object Under Evaluation

The object under evaluation is the local routeability of the active proof-loop
mechanic after package creation.

The bounded question is whether one low-context agent can follow the local
`aoa-evals` route from proof question to bounded report without importing
runtime, sibling, generated, or receipt authority.

## Selected Source Proof Object

- Selected eval candidate: `aoa-verification-honesty`
- Selection route: `EVAL_SELECTION.md` and `EVAL_INDEX.md`
- Source bundle: `evals/workflow/aoa-verification-honesty/EVAL.md`
- Manifest: `evals/workflow/aoa-verification-honesty/eval.yaml`
- Reason for selection: the current refactor depends on honest separation of
  executed, skipped, blocked, and inferential verification claims.

The selected bundle owns the verification-truthfulness claim. The proof-loop
mechanic owns only the route between source surfaces.

## Support Contract

The support contract for this smoke run is:

- shared fixture family:
  `mechanics/proof-infra/parts/fixture-families/fixtures/verification-honesty-v1/README.md`
- bundle fixture contract:
  `evals/workflow/aoa-verification-honesty/fixtures/contract.json`
- runner contract:
  `evals/workflow/aoa-verification-honesty/runners/contract.json`
- report schema:
  `evals/workflow/aoa-verification-honesty/reports/summary.schema.json`
- example report:
  `evals/workflow/aoa-verification-honesty/reports/example-report.json`

This smoke does not create a new bundle-local machine-readable result. A later
actual eval-result run must use the selected bundle's report schema and review
contract directly.

## Candidate Evidence Packet

This smoke uses only public-safe repo-local route evidence:

- `mechanics/proof-loop/README.md`
- `mechanics/proof-object/README.md`
- `mechanics/proof-infra/README.md`
- `mechanics/audit/README.md`
- `mechanics/boundary-bridge/README.md`
- `mechanics/publication-receipts/README.md`
- `docs/EVAL_REVIEW_GUIDE.md`
- `reports/README.md`
- this report

No raw operator trace, private host fact, live runtime artifact, or sibling
repository edit is part of this packet.

No runtime candidate packet is accepted by this smoke.
No sibling proof ref is required by this smoke.

## Bundle-Local Review Boundary

The review result is a bounded route-smoke only.

It supports this narrow read:

one local proof-loop path can be followed from a selected proof question to a
bounded report while keeping generated readers, candidate evidence, sibling
refs, reports, and receipts below source bundle review.

It does not support these reads:

- `aoa-verification-honesty` passed a new case corpus;
- the selected bundle should change status;
- a runtime or sibling candidate was accepted;
- a publication receipt should be emitted;
- the proof-loop mechanic is now a proof authority.

## Failure vs Readout

The failure class this smoke is meant to catch is route collapse:

- selection skips the source proof object;
- support contract is omitted;
- candidate evidence becomes accepted verdict meaning;
- report wording implies bundle promotion;
- receipt wording outranks reviewed report wording.

The readout stays weaker than those claims. It records only that this one local
route can land in a bounded report artifact.

## Result

- Report result: bounded route-smoke
- Bounded report: `mechanics/proof-loop/parts/route-smoke/reports/proof-loop-local-route-smoke-v1.md`
- Receipt result: no eval result receipt
- Bundle status result: no bundle promotion
- Runtime result: no runtime intake or dispatch
- Sibling result: no sibling-owner approval or edit
- Next route: defer/handoff to the selected bundle's report schema and review
  guide when an actual eval-result run is needed

## Blind Spots

- This smoke does not exercise every proof-loop branch.
- This smoke does not run a real `aoa-verification-honesty` case corpus.
- This smoke does not publish a receipt or test live receipt append behavior.
- This smoke does not prove that future runtime or sibling packets are valid.
- This smoke does not replace `python scripts/validate_repo.py` or the full
  release check.

## Validation

The route-smoke surface is guarded by `scripts/validate_repo.py`.

When this report, the proof-loop mechanic, or the decision note changes, run:

```bash
python scripts/validate_repo.py
python scripts/validate_semantic_agents.py
python -m pytest -q tests/test_validate_repo.py -k proof_loop
```
