**Summary**
- Dumps the engine’s legacy RNG state into the `RANDDATA` variable.

**Syntax**
- `DUMPRAND`

**Arguments**
- None.

**Defaults / optional arguments**
- None.

**Semantics**
- If `UseNewRandom` is enabled in JSON config:
  - Emits a warning and does nothing (implementation detail).
- Otherwise:
  - Writes the legacy RNG state into `RANDDATA` (via `MTRandom.GetRand(RANDDATA)`).
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- None.

**Examples**
- `DUMPRAND`

**Progress state**
- complete

