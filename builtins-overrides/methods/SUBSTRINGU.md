**Summary**
- Returns a substring where `start` and `length` are measured in UTF-16 code units.

**Tags**
- text

**Syntax**
- `SUBSTRINGU(str [, start [, length]])`

**Signatures / argument rules**
- `SUBSTRINGU(str)` → `string`
- `SUBSTRINGU(str, start)` → `string`
- `SUBSTRINGU(str, start, length)` → `string`

**Arguments**
- `str` (string): input string.
- `start` (optional, int; default `0`): UTF-16 code-unit start index.
- `length` (optional, int; default `-1`): UTF-16 code-unit count; `< 0` means "to end".

**Semantics**
- Indexing/counting uses the same unit as `STRLENSU` (`.NET` `string.Length`).
- Normalization rules:
  - If `start >= str.Length` or `length == 0`, returns `""`.
  - If `length < 0` or `length > str.Length`, `length` is first replaced with `str.Length`.
  - If `start <= 0`, the effective start becomes `0`.
  - If `start + length > str.Length`, `length` is clamped to the remaining suffix length.
- After normalization, returns `.NET` `str.Substring(start, length)`.
- Because indexing is by UTF-16 code unit, a supplementary character occupies two positions and can be split by `start`/`length`.

**Errors & validation**
- Argument type/count errors are rejected by the engine's function-method argument checker.

**Examples**
- `SUBSTRINGU("ABCDE", 1, 2)` → `"BC"`

**Progress state**
- complete
