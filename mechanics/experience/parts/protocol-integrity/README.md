# Experience / Protocol Integrity Part

## Role

This part owns the support route for `aoa-experience-protocol-integrity`.

It keeps the public-safe fixture family and validation test under the
Experience mechanic while the source proof bundle stays under `evals/`.

## Source Surfaces

- `evals/boundary/aoa-experience-protocol-integrity/EVAL.md`
- `mechanics/experience/parts/protocol-integrity/fixtures/experience-verdict-protocol-integrity-v1/README.md`
- `mechanics/experience/parts/protocol-integrity/tests/test_experience_protocol_integrity.py`

## Inputs

- experience verdict bundle metadata;
- report schema and example report;
- protocol boundary notes and fixture contract.

## Outputs

- bounded protocol-integrity proof readings;
- one fixture family contract;
- owner handoff route when protocol evidence depends on stronger owner truth.

## Stronger Owner Split

`Agents-of-Abyss` owns Experience doctrine and protocol meaning. The source
proof bundle owns the bounded claim. Owner repositories own local review and
the underlying experience being evaluated.

`aoa-evals` owns only the protocol-integrity proof wording, fixture contract,
validation test, blind spots, and bundle-local interpretation for
`aoa-experience-protocol-integrity`.

## Stop-Lines

This part does not own Experience doctrine and must not claim:

- runtime authority;
- governance authority;
- certification authority;
- owner-local review acceptance;
- proof that the underlying experience succeeded.

## Validation

Use [VALIDATION](VALIDATION.md) for this part's validation route. Executable command ownership is centralized in the parent `parts/AGENTS.md` lane.
