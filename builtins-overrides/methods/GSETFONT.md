**Summary**
- Sets the font used by `GDRAWTEXT` on a graphics surface.

**Tags**
- graphics
- text

**Syntax**
- `GSETFONT(gID, fontName, fontSize [, fontStyle])`

**Signatures / argument rules**
- `GSETFONT(gID, fontName, fontSize)` → `long`
- `GSETFONT(gID, fontName, fontSize, fontStyle)` → `long`

**Arguments**
- `gID` (int): graphics id.
- `fontName` (string): font family name.
- `fontSize` (int): pixel size.
- `fontStyle` (optional, int; default `0`): bitmask `1=bold`, `2=italic`, `4=strikeout`, `8=underline`.

**Semantics**
- If the target graphics does not exist or has already been disposed, returns `0`.
- Tries loaded private font families first, then normal font lookup by name.
- On success stores both the font object and the requested style bitmask, and returns `1`.
- The stored font remains attached to that graphics surface until disposal or the next `GSETFONT`.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if `gID` is negative or exceeds 32-bit range.
- Returns `0` if font creation fails.

**Examples**
- `GSETFONT 0, "Arial", 48, 1`

**Progress state**
- complete
