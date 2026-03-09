**Summary**
- Sets the dash style and dash cap of the current pen on a graphics surface.

**Tags**
- graphics

**Syntax**
- `GDASHSTYLE(gID, dashStyle, dashCap)`

**Signatures / argument rules**
- `GDASHSTYLE(gID, dashStyle, dashCap)` → `long`

**Arguments**
- `gID` (int): graphics id.
- `dashStyle` (int): numeric value written directly to `Pen.DashStyle`.
- `dashCap` (int): numeric value written directly to `Pen.DashCap`.

**Semantics**
- If the target graphics does not exist or has already been disposed, returns `0`.
- If no pen has been set yet, this function first creates one in the current default text color from config item `ForeColor` with width `1`.
- Then writes the requested dash style / dash cap and returns `1`.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Runtime error if the underlying pen rejects the requested enum values.

**Examples**
- `GDASHSTYLE 0, 1, 3`

**Progress state**
- complete
