# Shared Fixtures

This directory stores public-safe shared fixture families for `aoa-evals`.

These fixture families are reusable proof artifacts, not hidden benchmark dumps.

A shared fixture family should:
- preserve the bounded claim surface it supports
- explain what another repo must keep when replacing cases locally
- stay reviewable without private context
- remain weaker than the bundle-local `EVAL.md` meaning it serves

Current shared families:
- `bounded-change-paired-v1` for artifact/process pairing on the bounded change corpus
- `bounded-change-paired-v2` for a second matched artifact/process pairing slice on the same bounded change corpus
- `frozen-same-task-v1` for frozen same-task regression against one named baseline target
- `repeated-window-bounded-v1` for ordered repeated-window movement on one named workflow surface

Shared fixture naming discipline:
- keep the primary family path in `shared_fixture_family_path`
- record any additional reusable family paths in `additional_shared_fixture_family_paths`
- keep bundle-local `EVAL.md` meaning stronger than the shared family name
