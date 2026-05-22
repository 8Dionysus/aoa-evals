# Example Report

## Bundle

- bundle: `aoa-memo-write-path-guardrails`
- bundle shape: `diagnostic`
- verdict: `mixed support`

This example answers the first memo write-path safety question:
does the local candidate to reviewed corpus route keep source trust, ingestion
risk, derivation lineage, action-safety separation, durable landing gates, and
authority split visible before memory becomes durable?

Its machine-readable companion lives at `reports/example-report.json`.

## Breakdown

- source trust classification: `strong`
- ingestion risk marking: `mixed`
- derivation lineage: `mixed`
- action-safety separation: `mixed`
- durable landing gate: `strong`
- authority split: `strong`

## Strongest Signals

- strongest guardrail: reviewed landing rejects candidate-only, untrusted,
  missing-evidence, and missing-receipt packets before durable corpus object
  creation
- strongest risk: poisoning subtypes and action-safety separation need broader
  packet-backed validation before broad resistance can be claimed

## Case Notes

| case id | read path | reading | note |
|---|---|---|---|
| WPG-INTAKE-01 | local memo export -> reviewed intake -> landing receipt -> object | supports bounded claim | durable memory appears only through aoa-memo reviewed landing |
| WPG-RISK-01 | write-path docs -> candidate packet -> validator | mixed support | the risk taxonomy is visible, but some fields remain stronger in docs than in enforced packet shape |

## Interpretation Boundary

This read supports only a bounded write-path guardrail claim.
It does not prove general memory poisoning resistance, final source truth,
authorization safety, KAG lift correctness, vector retrieval quality, or broad
platform security.
