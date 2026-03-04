**Summary**
- Prints a one-line summary of a character’s non-zero experiences (`EXP`), then ends the line.

**Tags**
- io
- characters

**Syntax**
- `PRINT_EXP`
- `PRINT_EXP <charaIndex>`

**Arguments**
- `charaIndex` (optional): int expression; index into the current character list.
  - If omitted, the engine uses `0` and emits a warning (argument-builder behavior).

- Omitted arguments / defaults:
  - Omitted `charaIndex` defaults to `0` (with a warning).

**Semantics**
- If output skipping is active (`SKIPDISP` / `skipPrint`), this instruction is skipped (no output).
- Validates `charaIndex` at runtime; out-of-range raises an error.
- Builds a summary string `s` as follows:
  - Let `exp[]` be the target character’s `EXP` 1D array.
  - Let `names[]` be the constant CSV name list `EXPNAME`.
  - For `i` such that `0 <= i < exp.Length`:
    - If `i >= names.Length`: stop the loop (`break`).
    - If `exp[i] == 0`: continue.
    - If `names[i]` is null/empty: continue (engine uses `string.IsNullOrEmpty`).
    - Append: `names[i] + exp[i] + " "` (note the trailing space).
  - `s` is the concatenation of all appended parts; it may be the empty string.
- Prints `s`, then ends the line.
  - If `s` is empty, this still outputs a blank line.

**Errors & validation**
- Runtime error if `charaIndex` is out of range.

**Examples**
```erabasic
PRINT_EXP TARGET
```

**Progress state**
- complete
