**Summary**
- Returns a numeric timestamp encoding of the current local time.

**Tags**
- time

**Syntax**
- `GETTIME()`

**Signatures / argument rules**
- `GETTIME()` → `long`

**Arguments**
- (none)

**Semantics**
- Returns a base-10 integer encoding:
  - `YYYYMMDDHHMMSSmmm` (year, month, day, hour, minute, second, millisecond; local time).
- Components are combined as:
  - `(((((year * 100 + month) * 100 + day) * 100 + hour) * 100 + minute) * 100 + second) * 1000 + millisecond`.
- Note: the engine reads each component from `DateTime.Now` separately. If the system clock crosses a boundary during evaluation, different components may come from different instants.

**Errors & validation**
- (none)

**Examples**
- `GETTIME()` at `2026-03-05 09:07:02.004` returns `20260305090702004`.

**Progress state**
- complete
