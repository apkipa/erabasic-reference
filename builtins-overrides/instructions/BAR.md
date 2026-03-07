**Summary**
- Prints a bracketed bar-graph string representing the ratio `value / maxValue`.

**Tags**
- io

**Syntax**
- `BAR value, maxValue, length`

**Arguments**
- `value` (int): numerator.
- `maxValue` (int): denominator; must evaluate to `> 0`.
- `length` (int): bar width; must satisfy `1 <= length <= 99`.

**Semantics**
- Computes `filled = clamp(value * length / maxValue, 0, length)` using 64-bit integer arithmetic (integer overflow wraps).
- Produces and prints:
  - `[` + (`BarChar1` repeated `filled`) + (`BarChar2` repeated `length - filled`) + `]`
- `BarChar1` / `BarChar2` are configurable:
  - `BarChar1` default `*`
  - `BarChar2` default `.`
- Does **not** append a newline; use `BARL` if you want a newline.
- If output skipping is active (via `SKIPDISP`), this instruction is skipped.

**Errors & validation**
- Runtime errors if:
  - `maxValue <= 0`
  - `length <= 0`
  - `length >= 100`

**Examples**
```erabasic
BAR 2, 10, 20
PRINTL (2/10)
```

**Progress state**
- complete
