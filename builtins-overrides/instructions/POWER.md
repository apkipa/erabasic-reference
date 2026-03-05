**Summary**
- Computes an integer power using `Math.Pow` and stores the result into a destination integer variable.

**Tags**
- math

**Syntax**
- `POWER <dest>, <x>, <y>`

**Arguments**
- `<dest>`: changeable integer variable term (destination).
- `<x>` (int): base.
- `<y>` (int): exponent.

**Semantics**
- Evaluates `<x>` and `<y>` as integers, converts them to `double`, then computes `pow = Math.Pow(x, y)`.
- Validates the computed `pow`:
  - If `pow` is NaN → error.
  - If `pow` is infinite → error.
  - If `pow >= long.MaxValue` or `pow <= long.MinValue` → error.
- Stores `(long)pow` into `<dest>` (C# cast truncation toward zero for non-integer results).

**Errors & validation**
- Argument parsing fails if `<dest>` is not a changeable integer variable term.
- Runtime errors for NaN/infinite/overflow results as described above.

**Examples**
- `POWER A, 2, 10` (sets `A` to `1024`)
- `POWER A, 2, -1` (sets `A` to `0` due to truncation of `0.5`)

**Progress state**
- complete
