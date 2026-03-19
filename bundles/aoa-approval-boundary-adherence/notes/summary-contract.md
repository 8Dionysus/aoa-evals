# Summary Contract

This starter bundle is a `diagnostic` boundary surface.

Use it when the main question is:
- did the agent classify safe, approval-gated, and out-of-bounds actions correctly on this authority surface?

Do not use it as the main eval for:
- general task ambiguity
- non-authority requirement conflicts
- end-to-end workflow quality outside approval handling

Use `aoa-ambiguity-handling` when the main question is incomplete or conflicting task meaning rather than permission.

Public summaries for this bundle should:
- keep the authority boundary explicit
- distinguish refusal from pause-for-approval from safe proceed
- avoid implying broader safety guarantees than the fixture surface supports
