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
- `<src>` (string expression): sprite name.
- `<srcb>` (optional, string expression): sprite name used when the region is selected/focused.
  - If this evaluates to `""`, it is treated as omitted.
- `<srcm>` (optional, string expression): mapping-sprite name used by mouse-input mapping color side channels (see `html-output.md` and `INPUT`).
- `<width>` / `<height>` / `<ypos>` (optional, int expressions): mixed numeric attributes.
  - Each numeric argument may be followed by a `px` suffix token to indicate pixels (e.g. `80px`).
  - Without `px`, the value is interpreted as a percentage of the current font size (in pixels): `valuePx = value * FontSize / 100`.
  - Numeric argument order is `width`, then `height`, then `ypos`.

**Semantics**
- Skipped when output skipping is active (via `SKIPDISP`).
- Appends an image part to the current print buffer (no implicit newline).
- The image part is equivalent to emitting an HTML `<img ...>` tag and letting the HTML renderer handle it:
  - `src=<src>`, `srcb=<srcb>`, `srcm=<srcm>`
  - `width=<width>`, `height=<height>`, `ypos=<ypos>` (only included when the numeric value is non-zero)
- See `html-output.md` (“Inline images: `<img ...>`”) for rendering rules:
  - If `height` is omitted or `0`, it defaults to the current font size (pixels).
  - If `width` is omitted or `0`, the original aspect ratio is preserved.
  - Negative `width` / `height` values flip the image horizontally/vertically.
  - If the sprite cannot be resolved, the tag is rendered as literal text.

**Errors & validation**
- Argument parse-time errors if more than 3 numeric arguments are provided, or if string arguments appear after numeric arguments.

**Examples**
- `PRINT_IMG "FACE_001"`
- `PRINT_IMG "FACE_001", 80px` (explicit pixel width)
- `PRINT_IMG "FACE_001", 120, 120` (width/height as percent of font size)

**Progress state**
- complete
