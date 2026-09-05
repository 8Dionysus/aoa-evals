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

The root `pytest.ini` anchors discovery in this repository without changing
pytest's test selection or assertion rewriting. This also keeps nested
worktrees from inheriting a parent project's pytest configuration and conftest
setup. For a small edit, pass the affected test file or node directly; the
full-suite command above remains the broad check.

For generated-route validator edits, these tests need no third-party pytest
plugins. Their affected-feedback command avoids unrelated plugin startup:

```bash
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTEST_ADDOPTS= python -m pytest -q tests/test_generated_route_residue.py
```

This is not the full release gate. Keep required plugins enabled when selecting
other families that use them (for example, xdist for the parallel full suite).

Shared checks live in [VALIDATION.md — Non-mutating checks](../VALIDATION.md#non-mutating-checks).
