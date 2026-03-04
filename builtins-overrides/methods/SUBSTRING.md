**Summary**
- Returns a substring where `start`/`length` are measured in the engine’s “language length” units (the same unit returned by `STRLEN`).

**Tags**
- text

**Syntax**
- `SUBSTRING(str [, start [, length]])`

**Signatures / argument rules**
- `SUBSTRING(str)` → `string`
- `SUBSTRING(str, start)` → `string`
- `SUBSTRING(str, start, length)` → `string`

**Arguments**
- `str` (string): input string.
- `start` (optional, int; default `0`): language-length offset; see Semantics.
- `length` (optional, int; default `-1`): language-length count (`<0` means “to end”).

**Semantics**
- Let `total = STRLEN(str)` (the engine’s “language length” of `str`).
- `start` and `length` are measured in this same unit.
- Special cases:
  - If `start >= total` or `length == 0`: returns `""`.
  - If `length < 0` or `length > total`: `length` is treated as `total` (effectively “to end”).
  - If `start <= 0` and `length == total`: returns `str` unchanged.
- Start position selection (character-boundary rounding):
  - If `start <= 0`, the substring starts at the first character.
  - If `start > 0`, the engine advances from the beginning, accumulating the per-character byte count under the current language encoding until the accumulated count becomes `>= start`; the substring then starts at the *next* character position reached by that scan.
  - This means `start` values that fall “inside” a multi-byte character effectively round up to the next character boundary (the multi-byte character is skipped).
- Length selection (character-boundary rounding):
  - Starting from the chosen start character, the engine appends characters while accumulating the per-character byte count under the current language encoding until the accumulated count becomes `>= length`, or until end-of-string.
  - This means the returned substring may exceed `length` in bytes if the last included character is multi-byte.

**Errors & validation**
- Argument type/count errors are rejected by the engine’s function-method argument checker.

**Examples**
- `SUBSTRING("ABCDE", 1, 2)` → `"BC"` (ASCII)

**Progress state**
- complete
