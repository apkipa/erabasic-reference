**Summary**
- Returns the current font family name of a graphics surface.

**Tags**
- graphics
- text

**Syntax**
- `GGETFONT(gID)`

**Signatures / argument rules**
- `GGETFONT(gID)` → `string`

**Arguments**
- `gID` (int): graphics id.

**Semantics**
- If the target graphics does not exist or has already been disposed, returns `""`.
- Otherwise returns the stored font family name.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Runtime error if no font has been set yet.

**Examples**
- `PRINTFORM %GGETFONT(0)%`

**Progress state**
- complete
