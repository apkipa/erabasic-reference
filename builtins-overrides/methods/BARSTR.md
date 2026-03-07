**Summary**
- Returns the same bar string that `BAR`/`BARL` would print with the same arguments.

**Tags**
- io

**Syntax**
- `BARSTR(value, maxValue, length)`

**Signatures / argument rules**
- `BARSTR(value, maxValue, length)` → `string`

**Arguments**
- `value` (int): numerator.
- `maxValue` (int): denominator; must evaluate to `> 0`.
- `length` (int): bar width; must satisfy `1 <= length <= 99`.

**Semantics**
- Produces:
  - `[` + (`BarChar1` repeated `filled`) + (`BarChar2` repeated `length - filled`) + `]`
  - where `filled = clamp(value * length / maxValue, 0, length)`.
- `BarChar1` / `BarChar2` are configurable (defaults: `*` and `.`).
- As a standalone statement (method-as-statement form), the returned string is written to `RESULTS`.

**Errors & validation**
- Runtime errors if:
  - `maxValue <= 0`
  - `length <= 0`
  - `length >= 100`

**Examples**
```erabasic
S '= BARSTR(HP, MAXHP, 20)
PRINTFORML %S%
```

**Progress state**
- complete
