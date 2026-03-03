**Summary**
- Returns a substring where `start`/`length` are measured in the engine’s current language-encoding byte count (not Unicode code units).

**Syntax**
- `SUBSTRING(str [, start [, length]])`
- Optional arguments can be omitted by leaving an empty argument slot (e.g. `SUBSTRING(str, , 10)`).

**Signatures / argument rules**
- `SUBSTRING(str)` → `string`
- `SUBSTRING(str, start)` → `string`
- `SUBSTRING(str, start, length)` → `string`

**Arguments**
- `str`: string.
- `start` (optional): int (language-length offset; see Semantics).
- `length` (optional): int (language-length count; `<0` means “to end”).

**Defaults / optional arguments**
- If `start` is omitted (or omitted as an empty slot): defaults to `0`.
- If `length` is omitted (or omitted as an empty slot): defaults to `-1` (meaning “to end”).

**Semantics**
- The engine defines a “language length” for strings:
  - If `str` is ASCII-only: `total = str.Length`.
  - Otherwise: `total = ByteCount(str)` under the engine’s configured language encoding (see `useLanguage` / `Config.Language`).
- Special cases:
  - If `start >= total` or `length == 0`: returns `""`.
  - If `length < 0` or `length > total`: `length` is treated as `total` (effectively “to end”).
  - If `start <= 0` and `length == total`: returns `str` unchanged.
- Start position selection (character-boundary rounding):
  - If `start <= 0`, the substring starts at the first character.
  - If `start > 0`, the engine advances from the beginning, accumulating `ByteCount(char)` until the accumulated count becomes `>= start`; the substring then starts at the *next* character position reached by that scan.
  - This means `start` values that fall “inside” a multi-byte character effectively round up to the next character boundary (the multi-byte character is skipped).
- Length selection (character-boundary rounding):
  - Starting from the chosen start character, the engine appends characters while accumulating `ByteCount(char)` until the accumulated count becomes `>= length`, or until end-of-string.
  - This means the returned substring may exceed `length` in bytes if the last included character is multi-byte.

**Errors & validation**
- Argument type/count errors are rejected by the engine’s function-method argument checker.

**Examples**
- `SUBSTRING("ABCDE", 1, 2)` → `"BC"` (ASCII)

**Progress state**
- complete
