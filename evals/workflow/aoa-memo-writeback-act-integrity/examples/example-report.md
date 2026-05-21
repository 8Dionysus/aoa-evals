# Example Report

## Bundle

- bundle: `aoa-memo-writeback-act-integrity`
- bundle shape: `diagnostic`
- verdict: `mixed support`

This example answers the memo writeback-act question first:
did one bounded runtime-to-memo adoption path keep runtime closure, reviewed
adoption, receipt visibility, and recall alignment inspectable without turning
the act into proof that generic memo automation is ready?
Its machine-readable companion lives at `reports/example-report.json`.

## Breakdown

- runtime boundary honesty: `strong`
- review to adoption alignment: `mixed`
- receipt visibility: `mixed`
- recall surface alignment: `strong`

## Strongest Signals

- strongest support: the reviewed run and adopted memo object keep the writeback reason explicit instead of hiding it in runtime residue
- strongest risk: receipt visibility can still look stronger than it is if one confirmed path gets mistaken for generic ledger readiness

## Case Notes

| case id | read path | writeback reading | candidate note | review note | receipt note | recall note |
|---|---|---|---|---|---|---|
| MWA-01 | runtime closure -> reviewed run | supports bounded claim | the runtime decision names the bounded act directly | the reviewed run keeps the reason human-readable | receipt visibility is not needed yet at this step | the later memo object stays tied to the same closure reason |
| MWA-02 | reviewed run -> adopted memo object -> receipt mirror | mixed support | the candidate boundary is still explicit | the adoption step remains visible | receipt visibility exists, but one mirror is not generic ledger proof | the adopted object is recallable without becoming broader doctrine |

## Interpretation Boundary

This read supports only bounded runtime-to-memo writeback-act integrity on the
inspected owner-local path. It does not prove contradiction handling,
reviewed-candidate promotion, future scar or retention readiness, live
memory-ledger behavior, or general memory quality.
