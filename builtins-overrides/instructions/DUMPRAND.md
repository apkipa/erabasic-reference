**Summary**
- Dumps the engine’s legacy RNG state into the `RANDDATA` variable.

**Tags**
- random

**Syntax**
- `DUMPRAND`

**Arguments**
- None.

**Semantics**
- If `UseNewRandom` is enabled in JSON config:
  - Emits a warning and does nothing.
- Otherwise:
  - Writes the legacy RNG state into `RANDDATA`.
  - `RANDDATA` must have length 625; otherwise a runtime error is raised.
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- None.

**Examples**
- `DUMPRAND`

**Progress state**
- complete
