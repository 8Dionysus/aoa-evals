# A2A Summon Return Checkpoint V1

Shared fixture family for `aoa-a2a-summon-return-checkpoint`.

Use this family when the bounded question is whether one reviewed
`aoa-summon` child-return route preserves the visible chain from summon request
through SDK A2A decision, Codex-local target, reviewed child result,
checkpoint bridge, memo writeback candidate, runtime dry-run receipt contract,
and routing re-entry.

Canonical case archetypes:
- one Codex-local reviewed child route that returns through checkpoint relaunch
- one reviewed child result that remains subordinate to the parent reviewed
  artifact
- one memo writeback candidate that stays weaker than canon memory
- one runtime dry-run receipt contract with `dry_run=true` and
  `live_automation=false`
- one routing re-entry target that returns to the playbook-owned route instead
  of copying authority into routing

Family invariants:
- the summon request and result stay schema-checkable against `aoa-summon` v3
- the SDK fixture remains a control-plane assembly, not runtime execution
- checkpoint bridge hints stay provisional under the reviewed artifact
- eval and memo surfaces remain proof and writeback candidates, not owner truth
- runtime closeout remains dry-run unless a later reviewed runtime owner path
  explicitly promotes it

Replacement boundary:
- local repos may replace the concrete case only if the same route pressures
  remain visible and public-safe
- replacements must not depend on hidden raw traces, live automation, private
  runtime logs, or unreviewed memo promotion
