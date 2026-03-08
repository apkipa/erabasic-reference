**Summary**
- Loads a saved PNG slot into a not-yet-created graphics surface.

**Tags**
- graphics
- files

**Syntax**
- `GLOAD(gID, fileNo)`

**Signatures / argument rules**
- `GLOAD(gID, fileNo)` → `long`

**Arguments**
- `gID` (int): graphics id.
- `fileNo` (int): save slot number.

**Semantics**
- If the target graphics surface already exists, returns `0` without overwriting it.
- If `fileNo` is outside `0 <= value <= 2147483647`, returns `0`.
- Loads from `sav/img{fileNo:0000}.png`.
- If the file does not exist, cannot be decoded, or exceeds the engine image-size limit, returns `0`.
- On success creates the graphics surface from that image and returns `1`.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Non-`CodeEE` load failures collapse to return value `0`.

**Examples**
- `GLOAD 0, 12`

**Progress state**
- complete
