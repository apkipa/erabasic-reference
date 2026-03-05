**Summary**
- Returns the number of milliseconds elapsed since `0001-01-01 00:00:00` (local time).

**Tags**
- time

**Syntax**
- `GETMILLISECOND()`

**Signatures / argument rules**
- `GETMILLISECOND()` → `long`

**Arguments**
- (none)

**Semantics**
- Returns `DateTime.Now.Ticks / 10000` (ticks are 100-nanosecond units).

**Errors & validation**
- (none)

**Examples**
- `ms = GETMILLISECOND()`

**Progress state**
- complete
