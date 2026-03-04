**Summary**
- Prints a one-line summary of a character’s non-zero abilities (`ABL`), then ends the line.

**Tags**
- io
- characters

**Syntax**
- `PRINT_ABL`
- `PRINT_ABL <charaIndex>`

**Arguments**
- `charaIndex` (optional): int expression; index into the current character list.
  - If omitted, the engine uses `0` and emits a warning (argument-builder behavior).

- Omitted arguments / defaults:
  - Omitted `charaIndex` defaults to `0` (with a warning).

**Semantics**
- If output skipping is active (`SKIPDISP` / `skipPrint`), this instruction is skipped (no output).
- Validates `charaIndex` at runtime; out-of-range raises an error.
- Builds a summary string `s` as follows:
  - Let `abl[]` be the target character’s `ABL` 1D array.
  - Let `names[]` be the constant CSV name list `ABLNAME`.
  - For `i` such that `0 <= i < abl.Length`:
    - If `i >= names.Length`: stop the loop (`break`).
    - If `abl[i] == 0`: continue.
    - If `names[i]` is null/empty: continue (engine uses `string.IsNullOrEmpty`).
    - Append: `names[i] + "LV" + abl[i] + " "` (note the trailing space).
  - `s` is the concatenation of all appended parts; it may be the empty string.
- Prints `s`, then ends the line.
  - If `s` is empty, this still outputs a blank line.

**Errors & validation**
- Runtime error if `charaIndex` is out of range (`charaIndex < 0` or `charaIndex >= CHARANUM`).

**Examples**
```erabasic
PRINT_ABL TARGET
```

**Progress state**
- complete
