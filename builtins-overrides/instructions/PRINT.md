**Summary**
- Prints a **raw literal string** (the remainder of the source line) into the console output buffer.
- This entry also documents **common PRINT-family semantics** (suffix letters, buffering, `K`/`D`, `C`/`LC`).

**Tags**
- io

**Syntax**
- `PRINT`
- `PRINT <raw text>`
- `PRINT;<raw text>`

**Arguments**
- `<raw text>` (optional, default `""`): raw text, not an expression.
- `<raw text>` is taken as the raw character sequence after the instruction delimiter.
- The parser consumes exactly one delimiter character after the keyword:
  - a single space / tab
  - or a full-width space if `SystemAllowFullSpace` is enabled
  - or a semicolon `;`
- Because only *one* delimiter character is consumed:
  - `PRINT X` prints `X` (the one space was consumed as delimiter).
  - `PRINT  X` prints `" X"` (the second space remains in the argument).
  - `PRINT;X` prints `X` (no leading whitespace in the argument).

**Semantics**
- Output is appended to the engine’s **print buffer** (it is not necessarily flushed to the UI immediately).
- If output skipping is active (`SKIPDISP`):
  - These instructions are skipped before execution by the interpreter.
  - Arguments are not evaluated and there are no side effects.
- Argument/evaluation modes by base variant (before suffix letters):
  - `PRINT*` (raw): uses the raw literal remainder-of-line (not an expression).
  - `PRINTS*`: evaluates one string expression.
  - `PRINTV*`: evaluates a comma-separated list of expressions; each element must be either integer or string; results are concatenated with no separator (left-to-right).
  - `PRINTFORM*`: parses its argument as a FORM/formatted string at load/parse time, then evaluates it at runtime.
  - `PRINTFORMS*`: evaluates one string expression to obtain a format-string source, then parses and evaluates it as a FORM string at runtime (see below).
- Suffix letters and their meaning (parser order is important):
  - `C` / `LC` (cell output): after building the output string, outputs a fixed-width cell:
    - `...C` uses right alignment, `...LC` uses left alignment.
    - This is **not** the same as the newline suffix `L`; for example, `PRINTLC` means “left-aligned cell”, not “PRINTL + C”.
    - Cell formatting rules are defined by the console implementation; see `PRINTC` / `PRINTLC`.
    - Cell variants do not use the `...L / ...W / ...N` newline/wait handling; they only append a cell to the buffer.
  - `K` (kana conversion): applies kana conversion as configured by `FORCEKANA`.
  - `D` (ignore SETCOLOR color): ignores `SETCOLOR`’s *color* for this output (font name/style still apply).
  - `L` (newline): after printing, flushes the current buffer and appends a newline.
  - `W` (wait): like `L`, then waits for a key.
  - `N` (wait without ending the logical line): prints without ending the logical line, then flushes and waits like `W`.
    - The *next* flushed output will be merged onto the same logical line.
- FORM-at-runtime behavior (`PRINTFORMS*`):
  - Evaluates the string expression to `src`.
  - Normalizes escapes (the same escape-handling used by FORM strings).
  - Parses `src` as a FORM string up to end-of-line, then evaluates it and prints the result.
- `PRINT` itself:
  - Uses the raw literal argument as the output string.
  - Treats the output as ending a logical line (even though it does not insert a newline by itself).

**Errors & validation**
- None for `PRINT` itself (argument is optional and not parsed as an expression).

**Examples**
- `PRINT Hello`
- `PRINT;Hello`
- `PRINT  (leading space is preserved)`

**Progress state**
- complete
