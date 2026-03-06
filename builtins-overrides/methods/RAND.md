**Summary**
- Returns a random integer in a half-open range using the engine's current RNG mode.

**Tags**
- math

**Syntax**
- `RAND(max)`
- `RAND(min, max)`

**Signatures / argument rules**
- `RAND(max)` → `long`
- `RAND(min, max)` → `long`

**Arguments**
- `min` (optional, int; default `0`): inclusive lower bound.
- `max` (int): exclusive upper bound.

**Semantics**
- Returns a random integer `r` such that `min <= r < max`.
- RNG engine selection depends on JSON `UseNewRandom`:
  - `UseNewRandom=NO` (legacy mode): uses the legacy SFMT generator with the MT19937 parameter set. The returned value is computed as `min + (nextUInt64 % (max - min))`. This is deterministic for a given seed/state, but it is not perfectly unbiased when `(max - min)` does not divide `2^64`.
  - `UseNewRandom=YES` (new mode): uses a host `.NET System.Random` instance and its `NextInt64(max - min)` behavior, then adds `min`. `RANDOMIZE`, `INITRAND`, and `DUMPRAND` do not control this mode.
- In new mode, the host `System.Random` instance is created when the runtime creates its variable-evaluator state; scripts have no built-in way to reseed or snapshot it.

**Errors & validation**
- Runtime error if `max <= min`.
  - In particular, `RAND(0)` and `RAND(<negative>)` are errors.

**Examples**
- `RAND(10)` returns a value in `0 <= r < 10`.
- `RAND(5, 8)` returns `5`, `6`, or `7`.

**Progress state**
- complete

