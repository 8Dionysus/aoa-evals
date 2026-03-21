# Reportable Proof Contract

This runner surface defines the minimum public contract for bundles that ship machine-readable report artifacts.

## Required inputs

A compliant bundle-local runner contract should name:
- the bounded inputs it expects
- the fixture contract it depends on, if any
- the scorer helper paths it uses, if any
- the bundle-local report schema
- the bundle-local example report artifact

## Required execution discipline

A compliant run should:
1. keep the bounded claim surface explicit
2. use only the fixture family or replacement allowed by the fixture contract
3. produce the public report artifact after the bounded read, not before it
4. validate the report artifact against the bundle-local schema
5. keep the report artifact weaker than the bundle-local `EVAL.md` interpretation boundary

## Required output discipline

A schema-backed report artifact should:
- keep the bundle status visible
- keep the claim boundary explicit
- include the main bounded verdict or comparative reading
- carry limitations that remain readable to a human reviewer

The schema is a report contract, not a stronger truth claim.
