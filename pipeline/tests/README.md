# Pipeline Tests

Run from the `pipeline/` directory:

```bash
pip install -r requirements-dev.txt
pytest
```

Tests run fully offline — no API keys, network calls, or database required.

## Rule: all new pipeline functionality must have tests

Any new function, module, or behaviour added to `pipeline/` must ship with
corresponding tests in this directory before the work is considered complete.

Coverage required:
- **Happy path** — the normal successful case
- **Edge cases** — empty inputs, null fields, boundary values
- **Error paths** — exceptions, bad data, external failures

One test file per production module (`test_<module>.py`). Shared fixtures live in `conftest.py`.
