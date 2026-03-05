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
- The engine prints a precomputed “draw line” string and then ends the line.
- Pattern source:
  - The base pattern comes from config `DrawLineString` (default `"-"`).
- The engine precomputes an expanded line string from `DrawLineString` on initialization.
- Expansion algorithm:
  - Uses the UI’s drawable width (in pixels) as the target, and measures display width using the default font metrics.
  - Builds a string by repeating the pattern string until its measured display width is at least the target width.
  - Then trims one character at a time from the end until the measured width is at most the target width.
  - Returns the resulting string.
- Rendering:
  - The line is printed using regular style regardless of the current font style.
  - The engine then ends the line (flushes the buffer and refreshes the display).
- Important: `DRAWLINE` does not automatically flush existing buffered output *before* printing the line. If you need the line to start at the left edge, end the current logical line first (e.g. `PRINTL`) before calling `DRAWLINE`.

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
