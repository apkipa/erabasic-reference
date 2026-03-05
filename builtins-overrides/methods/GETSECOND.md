**Summary**
- Returns the number of seconds elapsed since `0001-01-01 00:00:00` (local time).

**Tags**
- time

**Syntax**
- `GETSECOND()`

**Signatures / argument rules**
- `GETSECOND()` → `long`

**Arguments**
- (none)

**Semantics**
- Returns `DateTime.Now.Ticks / 10000000` (ticks are 100-nanosecond units).

**Errors & validation**
- (none)

**Examples**
- `sec = GETSECOND()`

**Progress state**
- complete
