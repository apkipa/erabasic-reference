**Summary**
- Seeds the engine’s legacy RNG (Mersenne Twister) with a specified integer seed.

**Syntax**
- `RANDOMIZE`
- `RANDOMIZE <seed>`

**Arguments**
- `<seed>` (optional): integer expression. If omitted, the seed defaults to `0`.

**Defaults / optional arguments**
- `<seed>` defaults to `0`.

**Semantics**
- If `UseNewRandom` is enabled in JSON config:
  - Emits a warning and does nothing (implementation detail).
- Otherwise:
  - Replaces the engine’s legacy RNG instance with `new MTRandom(<seed>)`.
- Does not assign `RESULT`/`RESULTS`.

**Errors & validation**
- None (besides normal integer-expression evaluation errors).

**Examples**
- `RANDOMIZE 0`
- `RANDOMIZE 12345`

**Progress state**
- complete

