**Summary**
- Seeds the legacy RNG with a specified integer seed.

**Tags**
- random

**Syntax**
- `RANDOMIZE`
- `RANDOMIZE <seed>`

**Arguments**
- `<seed>` (optional, int; default `0`): seed value.

**Semantics**
- The legacy RNG used here is SFMT with the MT19937 parameter set.
- If `UseNewRandom` is enabled in JSON config:
  - Emits a warning and does nothing.
  - The new-mode RNG used by `RAND` remains the host `.NET System.Random` instance.
- Otherwise:
  - Re-seeds the legacy RNG with `<seed>` truncated to 32 bits (i.e. low 32 bits used as an unsigned seed).
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- None (besides normal integer-expression evaluation errors).

**Examples**
- `RANDOMIZE 0`
- `RANDOMIZE 12345`

**Progress state**
- complete
