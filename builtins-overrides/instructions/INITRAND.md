**Summary**
- Initializes the engine’s legacy RNG state from the `RANDDATA` variable.

**Tags**
- random

**Syntax**
- `INITRAND`

**Arguments**
- None.

**Semantics**
- The legacy RNG used here is SFMT with the MT19937 parameter set.
- If `UseNewRandom` is enabled in JSON config:
  - Emits a warning and does nothing.
- Otherwise:
  - Loads the legacy RNG state from `RANDDATA`.
  - `RANDDATA` must have length `625`.
  - Layout: elements `0` through `623` are the 624 state words; element `624` is the current index.
  - On load, elements `0` through `623` are interpreted as unsigned 32-bit values.
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- Runtime error if `RANDDATA` does not have length `625`.

**Examples**
- `INITRAND`

**Progress state**
- complete
