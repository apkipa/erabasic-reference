**Summary**
- Prints a multi-column view of a character’s parameters (`PALAM`) using `PRINTC`-style cells.

**Tags**
- io
- characters

**Syntax**
- `PRINT_PALAM`
- `PRINT_PALAM <charaIndex>`

**Arguments**
- `charaIndex` (optional, int; default `0`; omission emits a warning): index into the current character list.

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output).
- Validates `charaIndex` at runtime; out-of-range raises an error.
- For each parameter code `i` such that `0 <= i < 100`, it computes a cell string `s` and prints it if present:
  - Let `param = PALAM[charaIndex, i]`.
  - Let `name = PALAMNAME[i]` (treat `null` as `""`).
  - If `param == 0` and `name == ""`: omit this cell (no output).
  - Otherwise:
    - Let `paramlv = PALAMLV` (global array).
    - Choose the bar fill character `c` and its threshold `border`:
      - Start with `c = '-'` and `border = paramlv[1]`.
      - If `param >= border`: set `c = '='`, `border = paramlv[2]`.
      - If `param >= border`: set `c = '>'`, `border = paramlv[3]`.
      - If `param >= border`: set `c = '*'`, `border = paramlv[4]`.
    - Build a 10-character bar string `bar`:
      - If `border <= 0` or `border <= param`: bar fill is 10 copies of `c`.
      - Else if `param <= 0`: bar fill is 10 copies of `'.'`.
      - Else:
        - Compute `filled = floor(param * 10 / border)` using integer division (integer overflow wraps).
        - Bar fill is `filled` copies of `c` followed by `10 - filled` copies of `'.'`.
    - Build the final cell string:
      - `name + "[" + barFill + "]" + paramText`
      - where `paramText` is `param` formatted as a decimal integer right-aligned in width 6 (equivalent to C# interpolated `{param,6}` under `CultureInfo.InvariantCulture`).
- Each produced cell string is printed via `PRINTC`-style output with right alignment.
  - Therefore, cell width/counting follows `PRINTC`'s hardcoded Shift-JIS byte-count rule (code page 932), not derived runtime value `LanguageCodePage`.
- Keeps a per-line cell counter:
  - After each printed cell, `count += 1`.
  - If config item `PrintCPerLine` is greater than `0` and `count % PrintCPerLine == 0`, it flushes pending output.
- After finishing the loop, it flushes pending output and refreshes the display.
- This instruction does not automatically append a trailing newline.

**Errors & validation**
- Runtime error if `charaIndex` is out of range.

**Examples**
```erabasic
PRINT_PALAM TARGET
```

**Progress state**
- complete
