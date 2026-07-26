# Organ Access Admission Integrity Fixture Family

This bundle-local public-safe fixture family contains:

- `packets/valid-read.json`, a structurally valid bounded read-plane packet;
- `packets/insufficient-read.json`, an honest insufficient-evidence packet;
- `scenarios/*.json`, deterministic accept/reject cases and bounded mutations.

The machine-readable packet contract is
`../schemas/organ-access-proof-packet.schema.json`.

Local replacement may change fictional owner, organ, capability, protocol, and
revision labels only if all sixteen maturity axes and the checked-in forbidden
inferences remain visible. Fixtures must not contain credentials, private
payloads, private registry rows, or production endpoints.
