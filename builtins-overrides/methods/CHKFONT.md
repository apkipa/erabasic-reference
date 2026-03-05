**Summary**
- Tests whether a given font family name is available to the engine.

**Tags**
- ui

**Syntax**
- `CHKFONT(name)`

**Signatures / argument rules**
- `CHKFONT(name)` → `long`

**Arguments**
- `name` (string): font family name to look up.

**Semantics**
- Returns `1` if `name` exactly matches (`==`) the `.Name` of:
  - any system-installed font family, or
  - any font family loaded into the engine’s private font collection.
- Otherwise returns `0`.

**Errors & validation**
- (none)

**Examples**
- `ok = CHKFONT("Arial")`

**Progress state**
- complete

