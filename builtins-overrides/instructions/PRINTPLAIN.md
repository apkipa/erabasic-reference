**Summary**
- Outputs a raw string argument as plain text, without automatic button conversion.

**Tags**
- io

**Syntax**
- `PRINTPLAIN`
- `PRINTPLAIN <raw text>`

**Arguments**
- `<raw text>`: the literal remainder of the line (not a string expression).

- Omitted arguments / defaults:
  - If omitted, the argument is treated as the empty string; empty output produces no output segment.

**Semantics**
- If output skipping is active (`SKIPDISP` / `skipPrint`), this instruction is skipped (no output).
- Appends the raw string to the print buffer as a “plain” segment:
  - It is **not** scanned for numeric button patterns like `[0]`.
  - It still uses the current style (`SETCOLOR`, font style, etc.).
- Does not add a newline and does not flush by itself.

**Errors & validation**
- None.

**Examples**
```erabasic
; This will NOT become a clickable button:
PRINTPLAIN [0] Save
PRINTL
```

**Progress state**
- complete
