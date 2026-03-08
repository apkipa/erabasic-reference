**Summary**
- Returns the current pen width of a graphics surface.

**Tags**
- graphics

**Syntax**
- `GGETPENWIDTH(gID)`

**Signatures / argument rules**
- `GGETPENWIDTH(gID)` → `long`

**Arguments**
- `gID` (int): graphics id.

**Semantics**
- If the target graphics does not exist or has already been disposed, returns `0`.
- Otherwise returns the current pen width truncated to `long`.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Runtime error if no pen has been set yet.

**Examples**
- `PRINTFORML {GGETPENWIDTH(0)}`

**Progress state**
- complete
