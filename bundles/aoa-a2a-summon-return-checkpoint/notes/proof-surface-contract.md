# Proof Surface Contract

This bundle checks the contract around one reviewed A2A summon return route.

The route must preserve:

- one inspectable `summon_request`
- one inspectable `summon_decision`
- one SDK-owned A2A decision or reviewed closeout request
- one Codex-local target with source grounding
- one reviewed child result
- one return plan and one checkpoint bridge plan
- one eval packet and one memo writeback reference that stay subordinate
- one runtime dry-run receipt that does not claim live automation

The bundle may degrade or fail when any one of those surfaces is present only
as prose, appears after the fact, or acts stronger than its owning repository.

This is a proof surface, not a runtime runner.
