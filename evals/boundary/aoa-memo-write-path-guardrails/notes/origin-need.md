# Origin Need

`aoa-memo-write-path-guardrails` exists because the memory architecture now has
real local memo ports, MCP access, reviewed intake, and reviewed corpus objects.

That means the next proof question is no longer only "can memory be recalled?"
or "can a reviewed candidate land?" The sharper question is whether the write
path prevents poisoned, untrusted, stale, over-promoted, or action-bearing
material from quietly becoming durable reviewed memory.

The current memo eval cluster already covers recall, contradiction, writeback
acts, and reviewed-candidate adoption. This bundle fills the missing boundary
slot: candidate to reviewed memory must be guarded before downstream recall,
KAG, stats, playbooks, or agents consume it.
