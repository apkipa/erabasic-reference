**Summary**
- Returns the current font-style bitmask of a graphics surface.

**Tags**
- graphics
- text

**Syntax**
- `GGETFONTSTYLE(gID)`

**Signatures / argument rules**
- `GGETFONTSTYLE(gID)` → `long`

**Arguments**
- `gID` (int): graphics id.

**Semantics**
- If the target graphics does not exist or has already been disposed, returns `0`.
- Otherwise returns the stored style bitmask using `1=bold`, `2=italic`, `4=strikeout`, `8=underline`.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Runtime error if no font has been set yet.

**Examples**
- `PRINTFORML {GGETFONTSTYLE(0)}`

**Progress state**
- complete
