**Summary**
- Measures text with an explicit font specification.

**Tags**
- graphics
- text

**Syntax**
- `GGETTEXTSIZE(text, fontName, fontSize [, fontStyle])`

**Signatures / argument rules**
- `GGETTEXTSIZE(text, fontName, fontSize)` → `long`
- `GGETTEXTSIZE(text, fontName, fontSize, fontStyle)` → `long`

**Arguments**
- `text` (string): text to measure.
- `fontName` (string): font family name.
- `fontSize` (int): pixel size.
- `fontStyle` (optional, int; default `0`): bitmask `1=bold`, `2=italic`, `4=strikeout`, `8=underline`.

**Semantics**
- Measures the string using the supplied font specification without drawing anything.
- Returns the measured width.
- Also stores the measured height in `RESULT:1`. Other `RESULT` slots are not written by this function.

**Errors & validation**
- Runtime error in `WINAPI` text-drawing mode; these graphics built-ins are GDI+-only.
- Runtime error if the underlying font creation or measurement path fails.

**Examples**
- `width = GGETTEXTSIZE("Hello", "Arial", 48, 1)`

**Progress state**
- complete
