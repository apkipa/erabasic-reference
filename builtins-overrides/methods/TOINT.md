**Summary**
- Parses a string into an integer using the engine’s numeric-literal reader. Returns `0` for most invalid inputs.

**Signatures / argument rules**
- `TOINT(str)` → `long`

**Arguments**
- `str`: string expression.

**Semantics**
- Returns `0` if `str` is null/empty.
- Returns `0` if the string contains non-ASCII/multibyte characters (engine checks encoded byte length vs `str.Length`).
- Accepts only strings that:
  - start with a digit, or with `+`/`-` followed by a digit, and
  - after the initial number, either end-of-string or a decimal point `.` followed only by digits.
- The numeric part is parsed with the engine’s integer reader (supports `0x...`, `0b...`, and exponent forms such as `e`/`p` where applicable).
- If a fractional part exists (e.g. `"123.45"`), it is validated but ignored; the returned value is the integer part.

**Errors & validation**
- May throw if the numeric part overflows the engine’s integer range (the underlying reader raises an out-of-range error).

**Examples**
- `TOINT("123")` → `123`
- `TOINT("123.45")` → `123`
- `TOINT("0x10")` → `16`
- `TOINT("abc")` → `0`
