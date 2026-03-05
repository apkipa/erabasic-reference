**Summary**
- Prints a one-line summary of a character’s non-zero marks (`MARK`), then ends the line.

**Tags**
- io
- characters

**Syntax**
- `PRINT_MARK`
- `PRINT_MARK <charaIndex>`

**Arguments**
- `charaIndex` (optional, int; default `0` with a warning if omitted): index into the current character list.

**Semantics**
- If output skipping is active (via `SKIPDISP`), this instruction is skipped (no output).
- Validates `charaIndex` at runtime; out-of-range raises an error.
- Builds a summary string `s` as follows:
  - Let `mark[]` be the target character’s `MARK` 1D array.
  - Let `names[]` be the constant CSV name list `MARKNAME`.
  - For `i` such that `0 <= i < mark.Length`:
    - If `i >= names.Length`: stop the loop (`break`).
    - If `mark[i] == 0`: continue.
    - If `names[i]` is null/empty: continue (engine uses `string.IsNullOrEmpty`).
    - Append: `names[i] + "LV" + mark[i] + " "` (note the trailing space).
  - `s` is the concatenation of all appended parts; it may be the empty string.
- Prints `s`, then ends the line.
  - If `s` is empty, this still outputs a blank line.

**Errors & validation**
- Runtime error if `charaIndex` is out of range.

**Examples**
```erabasic
PRINT_MARK TARGET
```

**Progress state**
- complete
