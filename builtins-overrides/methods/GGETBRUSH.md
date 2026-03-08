**Summary**
- Returns the current brush color of a graphics surface as unsigned ARGB.

**Tags**
- graphics

**Syntax**
- `GGETBRUSH(gID)`

**Signatures / argument rules**
- `GGETBRUSH(gID)` → `long`

**Arguments**
- `gID` (int): graphics id.

**Semantics**
- If the target graphics does not exist or has already been disposed, returns `0`.
- Otherwise returns the current brush color as `0xAARRGGBB` in the range `0 <= value <= 0xFFFFFFFF`.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Runtime error if no brush has been set yet.

**Examples**
- `PRINTFORML {GGETBRUSH(0)}`

**Progress state**
- complete
