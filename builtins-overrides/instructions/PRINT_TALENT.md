**Summary**
- Prints a one-line summary of a character’s enabled talents (`TALENT`), then ends the line.

**Tags**
- io
- characters

**Syntax**
- `PRINT_TALENT`
- `PRINT_TALENT <charaIndex>`

**Arguments**
- `charaIndex` (optional, int; default `0` with a warning if omitted): index into the current character list.

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output).
- Validates `charaIndex` at runtime; out-of-range raises an error.
- Builds a summary string `s` as follows:
  - Let `talent[]` be the target character’s `TALENT` 1D array.
  - Let `names[]` be the constant CSV name list `TALENTNAME`.
  - For `i` such that `0 <= i < talent.Length`:
    - If `i >= names.Length`: stop the loop (`break`).
    - If `talent[i] == 0`: continue.
    - If `names[i]` is null/empty: continue (engine uses `string.IsNullOrEmpty`).
    - Append: `"[" + names[i] + "]"` (no spaces are added by the engine).
  - `s` is the concatenation of all appended parts; it may be the empty string.
- Prints `s`, then ends the line.
  - If `s` is empty, this still outputs a blank line.

**Errors & validation**
- Runtime error if `charaIndex` is out of range.

**Examples**
```erabasic
PRINT_TALENT TARGET
```

**Progress state**
- complete
