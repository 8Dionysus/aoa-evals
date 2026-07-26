# Example bounded source-contract readout

Verdict: `supports bounded claim`

All eight checked-in public-safe scenarios matched their expected accept or
reject state:

- a well-shaped read-plane packet was accepted;
- endpoint evidence could not ground a result;
- central proof could not become owner acceptance;
- a read plane could not authorize an effect;
- an asserted axis could not omit revision and freshness evidence;
- honest insufficient evidence remained valid;
- central proof could not authorize admission.
- evidence could not expire before the packet observation window closed.

This example is a source-contract readout only. It contains no live MCP,
registry, consumer, owner-acceptance, or rollback evidence and must not be used
as an admission receipt.
