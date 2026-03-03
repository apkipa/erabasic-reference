**Summary**
- Initializes the engine’s legacy RNG state from the `RANDDATA` variable.

**Syntax**
- `INITRAND`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- If `UseNewRandom` is enabled in JSON config:
  - Emits a warning and does nothing (implementation detail).
- Otherwise:
  - Loads the legacy RNG state from `RANDDATA` (via `MTRandom.SetRand(RANDDATA)`).
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- None.

**Examples**
- `INITRAND`

**Progress state**
- complete

