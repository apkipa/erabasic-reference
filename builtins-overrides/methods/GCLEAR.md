**Summary**
- Clears an entire graphics surface, or a clipped rectangle of it, to one color.

**Tags**
- graphics

**Syntax**
- `GCLEAR(gID, cARGB)`
- `GCLEAR(gID, cARGB, x, y, width, height)`

**Signatures / argument rules**
- `GCLEAR(gID, cARGB)` → `long`
- `GCLEAR(gID, cARGB, x, y, width, height)` → `long`

**Arguments**
- `gID` (int): graphics id.
- `cARGB` (int): color in `0xAARRGGBB` form.
- `x` (optional, int): clip-rectangle x coordinate for the six-argument form.
- `y` (optional, int): clip-rectangle y coordinate for the six-argument form.
- `width` (optional, int): clip-rectangle width for the six-argument form.
- `height` (optional, int): clip-rectangle height for the six-argument form.

**Semantics**
- If the target graphics does not exist or has already been disposed, returns `0`.
- Two-argument form clears the entire surface.
- Six-argument form sets a clip rectangle and clears only that clipped region.
- Unlike the rectangle-reading helpers used by other graphics built-ins, the six-argument form performs no wrapper-side range validation on `x`, `y`, `width`, or `height`; each is simply cast to 32-bit integer and passed on.
- On success returns `1`.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Runtime error if `cARGB < 0` or `cARGB > 0xFFFFFFFF`.

**Examples**
- `GCLEAR 0, 0xFFFFFFFF`

**Progress state**
- complete
