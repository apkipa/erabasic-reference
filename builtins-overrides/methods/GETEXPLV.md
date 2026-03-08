**Summary**
- Converts a raw value into a level number by comparing it against the current `EXPLV` threshold table.

**Tags**
- numeric

**Syntax**
- `GETEXPLV(value, maxLv)`

**Signatures / argument rules**
- `GETEXPLV(value, maxLv)` → `long`

**Arguments**
- `value` (int): value to compare against the current `EXPLV` thresholds.
- `maxLv` (int): maximum level boundary to inspect.

**Semantics**
- Reads the current runtime `EXPLV` array, not a baked copy.
- For each `i` with `0 <= i < maxLv`, compares `value` against `EXPLV:i+1`.
- Returns the first `i` such that `value < EXPLV:i+1`.
- If no such `i` exists, returns `maxLv`.
- Therefore the result is effectively “how many leading level boundaries are less than or equal to `value`”, capped at `maxLv`.
- No clamping is applied to `maxLv`:
  - if `maxLv <= 0`, the loop is skipped and the function returns `maxLv` as-is,
  - if `maxLv` is larger than the readable `EXPLV` boundary range, the function fails when it reads past the table.

**Errors & validation**
- No special validation beyond normal integer-argument evaluation.
- Runtime failure if `maxLv` makes the function read beyond the current `EXPLV` array.

**Examples**
- `lv = GETEXPLV(PALAM:0, 5)`

**Progress state**
- complete
