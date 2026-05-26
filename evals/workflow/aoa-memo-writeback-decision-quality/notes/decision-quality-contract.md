# Decision Quality Contract

This bundle evaluates one `aoa-memo-writeback` application as a decision, not
as a memory object.

## Decision Outcomes

The reviewed output must name exactly one decision outcome:

- `write_candidate`
- `prepare_export`
- `no_writeback_needed`
- `route_only_debt`
- `needs_owner_review`
- `blocked`

The outcome is correct only when it matches the evidence posture, owner route,
review posture, privacy posture, and local memo port status.

## Required Separation

Keep these surfaces separate in the report:

- invocation fit: whether `aoa-memo-writeback` was the right skill to apply
- owner route: owner repo and stronger owner route
- evidence search: what was inspected, skipped, not applicable, or missing
- memory-worthiness: what bounded fact survived and what noise was rejected
- decision outcome: the selected output and why alternatives were rejected
- missed-evidence risk: what a later reviewer may still need to inspect
- privacy posture: what stayed out of public packets

## Strong Signals

Strong support requires:

- a bounded memory-worthy pressure such as route law, owner-boundary correction,
  MCP/service contract, eval/proof posture, repeated failure/fix, or consumer
  handoff
- inspectable evidence refs instead of summary-only claims
- owner route named before writeback decision
- generic progress rejected when no bounded memory question survives
- route-only repos treated as debt instead of receiving fake packets
- missing or insufficient search named in the output

## Stop-Lines

Do not read this eval as:

- durable memory review
- write-path guardrail proof
- central `aoa-memo` write approval
- source claim truth
- recall precision proof
- permission to quote raw `.aoa` transcript content publicly
