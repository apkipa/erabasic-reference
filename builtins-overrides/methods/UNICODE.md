**Summary**
- Returns a one-code-unit string for a BMP Unicode value.

**Tags**
- text

**Syntax**
- `UNICODE(code)`

**Signatures / argument rules**
- `UNICODE(code)` → `string`

**Arguments**
- `code` (int): Unicode value to convert.

**Semantics**
- Accepts only `0 <= code <= 0xFFFF`.
- On success, returns a string containing exactly one UTF-16 code unit.
- No surrogate-pair composition is performed:
  - supplementary scalar values above `0xFFFF` are rejected,
  - values satisfying `0xD800 <= code <= 0xDFFF` are returned as single code units.
- Control-code handling:
  - `LF` (`0x000A`) and `CR` (`0x000D`) are allowed,
  - other control values satisfying `0x0000 <= code <= 0x001E` and values satisfying `0x007F <= code <= 0x009F` cause a warning and return `""`.

**Errors & validation**
- Runtime error if `code` is outside `0 <= code <= 0xFFFF`.

**Examples**
- `UNICODE(0x2661)` → `"♡"`

**Progress state**
- complete
