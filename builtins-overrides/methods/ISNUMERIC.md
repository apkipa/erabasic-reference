**Summary**
- Returns whether a string is accepted by the engine's numeric-literal predicate.

**Tags**
- text

**Syntax**
- `ISNUMERIC(str)`

**Signatures / argument rules**
- `ISNUMERIC(str)` → `long`

**Arguments**
- `str` (string): string to test.

**Semantics**
- Returns `0` immediately if `str` contains any multi-byte character under the current language encoding.
- Returns `0` if `str` does not start with:
  - a digit, or
  - `+` / `-` followed by a digit.
- Otherwise checks the engine's integer-literal family, plus an optional trailing `.` followed only by decimal digits.
- Accepted integer-literal features include:
  - `0x` / `0X` hexadecimal prefixes,
  - `0b` / `0B` binary prefixes,
  - `e` / `E` and `p` / `P` exponent markers.
- Compatibility quirks:
  - base prefixes are recognized only when the string itself starts with `0`; a leading sign prevents `0x` / `0b` recognition,
  - after an exponent marker, this predicate requires the next character to be a digit, so signed exponents are **not** accepted here.
- Returns `1` for accepted text and `0` for most rejected text.

**Errors & validation**
- Some exponent forms can still raise a runtime error instead of returning `0` if exponent evaluation overflows the 64-bit signed range.

**Examples**
- `ISNUMERIC("123")` → `1`
- `ISNUMERIC("12a")` → `0`

**Progress state**
- complete
