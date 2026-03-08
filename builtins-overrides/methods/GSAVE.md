**Summary**
- Saves a created graphics surface to the save directory as a PNG file.

**Tags**
- graphics
- files

**Syntax**
- `GSAVE(gID, fileNo)`

**Signatures / argument rules**
- `GSAVE(gID, fileNo)` → `long`

**Arguments**
- `gID` (int): graphics id.
- `fileNo` (int): save slot number.

**Semantics**
- If the graphics surface does not exist or has already been disposed, returns `0`.
- If `fileNo < 0` or `fileNo > 2147483647`, returns `0`.
- Otherwise writes the bitmap to `sav/img{fileNo:0000}.png`, creating the save directory if needed, and returns `1` on success.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Returns `0` on file-system or image-save failure.

**Examples**
- `GSAVE 0, 12`

**Progress state**
- complete
