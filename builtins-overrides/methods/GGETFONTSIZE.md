**Summary**
- Returns the current font size of a graphics surface.

**Tags**
- graphics
- text

**Syntax**
- `GGETFONTSIZE(gID)`

**Signatures / argument rules**
- `GGETFONTSIZE(gID)` → `long`

**Arguments**
- `gID` (int): graphics id.

**Semantics**
- If the target graphics does not exist or has already been disposed, returns `0`.
- Otherwise returns the stored font size as an integer.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Runtime error if no font has been set yet.

**Examples**
- `PRINTFORML {GGETFONTSIZE(0)}`

**Progress state**
- complete
