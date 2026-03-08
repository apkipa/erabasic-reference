**Summary**
- Sets the current outline pen of a graphics surface.

**Tags**
- graphics

**Syntax**
- `GSETPEN(gID, cARGB, width)`

**Signatures / argument rules**
- `GSETPEN(gID, cARGB, width)` → `long`

**Arguments**
- `gID` (int): graphics id.
- `cARGB` (int): color in `0xAARRGGBB` form.
- `width` (int): pen width.

**Semantics**
- If the target graphics does not exist or has already been disposed, returns `0`.
- On success replaces the current pen, preserving the previous dash style / dash cap if a pen was already present.
- No wrapper-side validation is performed on `width`; it is passed directly to the pen constructor.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Runtime error if `cARGB` is outside `0 <= value <= 0xFFFFFFFF`.
- Runtime error if the underlying pen constructor rejects `width`.

**Examples**
- `GSETPEN 0, 0xFFFF0000, 3`

**Progress state**
- complete
