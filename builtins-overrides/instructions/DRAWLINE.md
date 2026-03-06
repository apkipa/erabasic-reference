**Summary**
- Draws a horizontal line across the console using the configured `DRAWLINE` pattern.

**Tags**
- io

**Syntax**
- `DRAWLINE`

**Arguments**
- None.

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output).
- The engine appends the precomputed default draw-line string to the current pending print buffer and then ends the line.
- Pattern source:
  - the base pattern comes from config `DrawLineString` (default `"-"`),
  - the runtime precomputes a width-fitted expanded string from that pattern during initialization.
- Width-fitting rule:
  - repeat the pattern until the measured display width reaches or exceeds the current drawable width,
  - then trim one character at a time from the end until the measured width is less than or equal to the drawable width.
- Rendering:
  - the line text is printed using regular font style regardless of the current font style,
  - the instruction then ends the line and refreshes the display.
- Important boundary behavior:
  - `DRAWLINE` does **not** automatically flush earlier buffered output before appending the line string,
  - so if buffered text already exists, the draw-line string is appended to that same pending line and the combined result is what gets committed when the line is ended.
- Related helpers:
  - `GETLINESTR(pattern)` exposes the same width-fitting algorithm for an arbitrary pattern string,
  - `DRAWLINEFORM` uses the same expansion rule for its runtime string argument.

**Errors & validation**
- None (arguments are not accepted).

**Examples**
```erabasic
DRAWLINE
PRINTL Header
DRAWLINE
```

**Progress state**
- complete
