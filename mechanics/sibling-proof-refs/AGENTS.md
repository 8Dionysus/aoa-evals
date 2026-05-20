# AGENTS.md

## Applies to

`mechanics/sibling-proof-refs/` and the sibling proof-reference compatibility
route.

## Role

This package protects the sibling-reference loop:

`repo-qualified ref -> sibling owner route -> compatibility posture -> latest-sibling canary -> bundle-local review`

## Read before editing

1. root `AGENTS.md`
2. `DESIGN.md`
3. `DESIGN.AGENTS.md`
4. `docs/PROOF_TOPOLOGY.md`
5. `docs/SIBLING_PROOF_REFS.md`
6. `mechanics/README.md`
7. `mechanics/sibling-proof-refs/README.md`
8. `docs/decisions/0003-sibling-proof-reference-compatibility.md`
9. `docs/decisions/0008-sibling-proof-refs-mechanic-package.md`
10. `scripts/sibling_canary_matrix.json`
11. `scripts/run_sibling_canary.py`

## Boundaries

- Do not edit sibling repos unless the user explicitly routes that owner work.
- Do not treat sibling path existence as proof authority or owner acceptance.
- Do not repair generated readers by hand.
- Do not keep old sibling paths as active topology without legacy posture.
- Do not use latest-sibling canary output as a bundle verdict.

## Validation

Run:

```bash
python scripts/validate_repo.py
python scripts/run_sibling_canary.py --repo-root . --format json
python scripts/validate_semantic_agents.py
```

## Closeout

Report which sibling owner, refs, compatibility posture, canary result, and
local proof surfaces changed. Say explicitly whether sibling repos were left
untouched.
