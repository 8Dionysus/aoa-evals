# Provider evidence fixture

This small source corpus lets the bundle observe real local Python-AST and
host-Ctags symbol evidence for every `refactor-torture-v1` case. The collector
parses only these checked-in synthetic files and records source paths, symbol
kinds, and line spans; it does not claim that either implementation is
correct, admitted, current outside this source snapshot, or authoritative for
KAG or proof.

`manifest.json` is the source-to-case map. `source/` is deliberately public-safe
and contains no repository or provider-internal identifiers. Python-AST uses
the standard-library `ast` module. Ctags is optional: an unavailable host
binary is emitted as explicit `not_available` evidence rather than treated as
a passing provider result.

The evidence artifact remains separate from the machine-bound provider
execution envelope. Both providers are `not_admitted`; the machine owner,
runtime owner, normalized-observation owner, and proof owner retain their
respective boundaries.
