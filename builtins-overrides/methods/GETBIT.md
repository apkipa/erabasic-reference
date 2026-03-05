**Summary**
- Extracts a single bit from a 64-bit integer.

**Tags**
- math

**Syntax**
- `GETBIT(n, m)`

**Signatures / argument rules**
- `GETBIT(n, m)` → `long`

**Arguments**
- `n` (int): treated as a signed 64-bit value.
- `m` (int): bit position, must satisfy `0 <= m <= 63` (`0` = least-significant bit).

**Semantics**
- Returns `((n >> m) & 1)`.

**Errors & validation**
- Runtime error if `m < 0` or `m > 63`.

**Examples**
- `GETBIT(5, 0)` returns `1`.
- `GETBIT(5, 2)` returns `1`.
- `GETBIT(5, 1)` returns `0`.

**Progress state**
- complete

