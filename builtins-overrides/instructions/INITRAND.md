**Summary**
- Initializes the engine’s legacy RNG state from the `RANDDATA` variable.

**Tags**
- random

**Syntax**
- `INITRAND`

**Arguments**
- None.

**Semantics**
- If `UseNewRandom` is enabled in JSON config:
  - Emits a warning and does nothing.
- Otherwise:
  - Loads the legacy RNG state from `RANDDATA`.
  - `RANDDATA` must have length 625; otherwise a runtime error is raised.
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- None.

**Examples**
- `INITRAND`

**Progress state**
- complete
