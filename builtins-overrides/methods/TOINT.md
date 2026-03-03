**Summary**
- Parses a string into an integer using the engine’s numeric-literal reader.
- Returns `0` for many invalid inputs, but some invalid numeric-literal forms raise an error (see Errors & validation).

**Syntax**
- `TOINT(str)`

**Signatures / argument rules**
- `TOINT(str)` → `long`

**Arguments**
- `str`: string expression.

**Defaults / optional arguments**
- None.

**Semantics**
- Returns `0` if `str` is `null` or `""`.
- Rejects any string containing at least one multi-byte character under the engine’s configured language encoding:
  - If `LangByteCount(str) > str.Length`, returns `0`.
- Rejects strings that do not start with:
  - a digit, or
  - `+`/`-` followed by a digit.
- Parses the leading integer literal using the engine’s integer-literal reader (the same routine used by the lexer/parser):
  - recognizes `0x...` / `0X...` (hex) and `0b...` / `0B...` (binary)
  - recognizes exponent suffixes `e`/`E` (base-10) and `p`/`P` (base-2) with a (signed) integer exponent
    - Implementation detail: exponent digits are parsed by the same digit-reader used for the main literal (so the accepted exponent digit set depends on the literal’s base).
- After the integer literal:
  - If end-of-string: return the parsed value.
  - If the next character is `.`: the remainder must be digits only; this fractional part is validated but ignored.
  - Otherwise: return `0`.

**Errors & validation**
- Argument type/count errors are rejected by the engine’s function-method argument checker.
- Even though many invalid strings return `0`, the underlying integer-literal reader can raise runtime errors for some inputs, including (non-exhaustive):
  - out-of-range / overflow while parsing the integer literal
  - invalid binary digit in a `0b...` literal (e.g. `0b2`)
  - malformed exponent forms (e.g. `1e` without exponent digits)

**Examples**
- `TOINT("123")` → `123`
- `TOINT("123.45")` → `123`
- `TOINT("0x10")` → `16`
- `TOINT("abc")` → `0`

**Progress state**
- complete
