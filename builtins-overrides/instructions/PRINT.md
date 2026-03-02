**Summary**
- Prints a **raw literal string** (the remainder of the source line) into the console output buffer.
- See also: `PRINTV` (variadic expressions), `PRINTS` (string expression), `PRINTFORM` (FORM scanned at load-time), `PRINTFORMS` (FORM scanned at runtime).
- This entry also documents **common PRINT-family semantics** (suffix letters, buffering, `K`/`D`, `C`/`LC`).

**Syntax**
- `PRINT`
- `PRINT <raw text>`
- `PRINT;<raw text>`

**Arguments**
- `<raw text>` is **not an expression**. It is taken as the raw character sequence after the instruction delimiter.
- The parser consumes exactly one delimiter character after the keyword:
  - a single space / tab
  - or a full-width space if `SystemAllowFullSpace` is enabled
  - or a semicolon `;`
- Because only *one* delimiter character is consumed:
  - `PRINT X` prints `X` (the one space was consumed as delimiter).
  - `PRINT  X` prints `" X"` (the second space remains in the argument).
  - `PRINT;X` prints `X` (no leading whitespace in the argument).

**Defaults / optional arguments**
- If omitted, the argument is treated as the empty string.

**Semantics**
- Output is appended to the engine’s **print buffer** (it is not necessarily flushed to the UI immediately).
- Common behavior across the PRINT family:
  - `...L` variants: after output, flush and append a newline (`Console.NewLine()`).
  - `...W` variants: like `...L`, then wait for a key (`Console.ReadAnyKey()`).
  - `...N` variants: wait for a key **without ending the logical output line** (implementation detail: prints with `lineEnd=false` before flushing).
  - `...K` variants: apply kana conversion to the produced string, as configured by `FORCEKANA` (`ConvertStringType`).
  - `...D` variants: ignore `SETCOLOR`’s *color* for this output (still respects font style and font name).
  - `...C` / `...LC` variants: output a fixed-width *cell* using `Config.PrintCLength`; width is measured in **Shift-JIS byte count** (implementation detail).
- `PRINT` itself:
  - Uses the raw literal argument as the output string.
  - Treats the output as ending a logical line (`lineEnd=true`) even though it does not insert a newline by itself.

**Errors & validation**
- None for `PRINT` itself (argument is optional and not parsed as an expression).

**Examples**
- `PRINT Hello`
- `PRINT;Hello`
- `PRINT  (leading space is preserved)`
