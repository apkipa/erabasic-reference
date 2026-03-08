**Summary**
- Returns the current pen color of a graphics surface as unsigned ARGB.

**Tags**
- graphics

**Syntax**
- `GGETPEN(gID)`

**Signatures / argument rules**
- `GGETPEN(gID)` → `long`

**Arguments**
- `gID` (int): graphics id.

**Semantics**
- If the target graphics does not exist or has already been disposed, returns `0`.
- Otherwise returns the current pen color as `0xAARRGGBB` in the range `0 <= value <= 0xFFFFFFFF`.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Runtime error if no pen has been set yet.

**Examples**
- `PRINTFORML {GGETPEN(0)}`

**Progress state**
- complete
