**Summary**
- Dumps the engine’s legacy RNG state into the `RANDDATA` variable.

**Tags**
- random

**Syntax**
- `DUMPRAND`

**Arguments**
- None.

**Semantics**
- The legacy RNG used here is SFMT with the MT19937 parameter set.
- If `UseNewRandom` is enabled in JSON config:
  - Emits a warning and does nothing.
- Otherwise:
  - Writes the legacy RNG state into `RANDDATA`.
  - `RANDDATA` must have length `625`.
  - Layout: elements `0..623` receive the 624 state words; element `624` receives the current index.
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- Runtime error if `RANDDATA` does not have length `625`.

**Examples**
- `DUMPRAND`

**Progress state**
- complete
