**Summary**
- Appends an inline image part to the current output line (equivalent to an `<img ...>` element in the HTML output model).

**Tags**
- ui

**Syntax**
- `PRINT_IMG <src>`
- `PRINT_IMG <src>, <srcb>`
- `PRINT_IMG <src>, <srcb>, <srcm>`
- `PRINT_IMG <src>, <srcb>, <srcm>, <width> [, <height> [, <ypos>]]`
- `PRINT_IMG <src>, <width> [, <height> [, <ypos>]]`

**Arguments**
- `<src>` (string): main sprite name.
- `<srcb>` (optional, string; default `""`): sprite name used when the region is selected/focused.
- `<srcm>` (optional, string; default `""`): mapping-sprite name used by mouse-input mapping color side channels (see `html-output.md` and `INPUT`).
- `<width>` / `<height>` / `<ypos>` (optional, int): mixed numeric attributes.
  - Numeric arguments are positional: `width`, then `height`, then `ypos`.
  - Each numeric argument may be followed by a `px` suffix token to indicate pixels (e.g. `80px`).
  - Without `px`, the value is interpreted as a percentage of the current font size (in pixels): `valuePx = value * FontSize / 100`.

**Semantics**
- Skipped when output skipping is active (via `SKIPDISP`).
- Appends an image part to the current print buffer (no implicit newline).
- Argument parsing is two-phase:
  - First, `PRINT_IMG` reads up to three leading string slots: `src`, then `srcb`, then `srcm`.
  - Once the first numeric argument appears, the parse switches to numeric mode, and all remaining arguments must also be numeric.
- To supply `srcm` while leaving `srcb` absent, pass an empty string placeholder for `srcb`.
- Empty `srcb` / `srcm` omit the corresponding HTML attribute.
- The image part is equivalent to emitting an HTML `<img ...>` tag and letting the HTML renderer handle it:
  - `src=<src>`
  - `srcb=<srcb>` only when `srcb` is non-empty
  - `srcm=<srcm>` only when `srcm` is non-empty
  - `width=<width>`, `height=<height>`, `ypos=<ypos>` only when the numeric value is non-zero
- See `html-output.md` (“Inline images: `<img ...>`”) for rendering rules:
  - If `height` is omitted or `0`, it defaults to the current font size (pixels).
  - If `width` is omitted or `0`, the original aspect ratio is preserved.
  - Negative `width` / `height` values flip the image horizontally/vertically.
  - If the sprite cannot be resolved, the tag is rendered as literal text.

**Errors & validation**
- Parse-time error if `<src>` is omitted.
- Parse-time error if a string argument appears after numeric arguments have started.
- Parse-time error if more than 3 numeric arguments are provided.

**Examples**
- `PRINT_IMG "FACE_001"`
- `PRINT_IMG "FACE_001", 80px` (explicit pixel width)
- `PRINT_IMG "FACE_001", "", "FACE_001_MAP"` (set `srcm` while leaving `srcb` absent)
- `PRINT_IMG "FACE_001", 120, 120` (width/height as percent of font size)

**Progress state**
- complete
