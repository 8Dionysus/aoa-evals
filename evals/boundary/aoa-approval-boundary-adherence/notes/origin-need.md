# Origin Need

Approval handling is one of the easiest places for an agent to overclaim safety.

Without a bounded diagnostic surface, it is too easy to blur together:
- safe action
- pause-for-approval action
- genuinely out-of-bounds action

`aoa-approval-boundary-adherence` exists to keep that authority question narrow and reviewable.

It does not try to prove general safety.
It asks the smaller bounded question:
- did the agent classify permission and approval boundaries honestly on this surface?
