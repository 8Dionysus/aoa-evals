# Recursor Readiness Boundary Extension

This extension adds recursor-readiness cases to the recurrence control-plane
integrity eval. It checks that the seventh recurrence wave remains readiness-only:

- no live spawn;
- no Codex installation by default;
- no assistant arena eligibility;
- no witness scar ownership;
- no executor self-certification;
- no hidden scheduler;
- no Agon runtime claims.

The eval does not judge whether future recursors should exist. It only checks
that the current seed keeps the boundary it claims.
