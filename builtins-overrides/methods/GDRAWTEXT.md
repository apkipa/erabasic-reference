**Summary**
- Draws a string onto a graphics surface and exposes measured size through `RESULT`.

**Tags**
- graphics
- text

**Syntax**
- `GDRAWTEXT(gID, text)`
- `GDRAWTEXT(gID, text, x, y)`

**Signatures / argument rules**
- `GDRAWTEXT(gID, text)` → `long`
- `GDRAWTEXT(gID, text, x, y)` → `long`

**Arguments**
- `gID` (int): graphics id.
- `text` (string): text to draw.
- `x` (optional, int; default `0`): draw x coordinate.
- `y` (optional, int; default `0`): draw y coordinate.

**Semantics**
- If the target graphics does not exist or has already been disposed, returns `0`.
- Two-argument form draws at `(0, 0)`.
- Four-argument form draws at `(x, y)`.
- Fill / outline behavior follows the current graphics state: the fill uses the current brush or `Config.ForeColor` when no brush is set, and the outline uses the current pen or `Config.ForeColor` when no pen is set.
- Font behavior follows the current graphics state: if no font has been set with `GSETFONT`, drawing uses `Config.FontName` at size `100` with the current console font style.
- On success returns `1`, stores measured width in `RESULT:1`, and stores measured height in `RESULT:2`. `RESULT:0` is not used by this function.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Runtime error if `x` or `y` is outside signed 32-bit range.

**Examples**
- `GDRAWTEXT 0, "Hello", 20, 30`

**Progress state**
- complete
