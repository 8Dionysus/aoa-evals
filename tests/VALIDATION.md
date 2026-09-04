# Tests Validation

This on-demand route owns exact local checks for the surrounding source surface.

## Commands

```bash
python -m pytest -q tests
```

For the complete suite, including bundle and mechanic tests:

```bash
python -m pytest -q -n 2 --dist loadfile
```

The development requirements include pytest-xdist. Keep small affected runs
serial: worker startup is not free. File-based scheduling keeps module fixtures
together; unchanged-tree catalog assertions share one source collection with
private deep copies, while negative temporary-tree tests still validate their
own inputs. Remove the worker options to reproduce a serial full run.

Shared checks live in [VALIDATION.md — Non-mutating checks](../VALIDATION.md#non-mutating-checks).
