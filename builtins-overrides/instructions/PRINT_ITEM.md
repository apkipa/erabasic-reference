**Summary**
- Prints a one-line summary of currently owned items (`ITEM`), then ends the line.

**Tags**
- io

**Syntax**
- `PRINT_ITEM`

**Arguments**
- None.

**Semantics**
- If output skipping is active (`SKIPDISP` / `skipPrint`), this instruction is skipped (no output).
- Builds a Japanese summary string `s` as follows:
  - Let `count[]` be the integer array `ITEM`.
  - Let `names[]` be the string array `ITEMNAME`.
  - Let `length = min(count.Length, names.Length)`.
  - Start with `s = "所持アイテム："`.
  - For each `i` such that `0 <= i < length`:
    - If `count[i] == 0`: continue.
    - If `names[i] != null`: append `names[i]` (note: unlike some other lists, empty string is not filtered out here).
    - Append: `"(" + count[i] + ") "` (note the trailing space).
  - If no `i` satisfied `count[i] != 0`, append `"なし"`.
- Prints `s`, then ends the line.

**Errors & validation**
- None specific to this instruction.

**Examples**
- `PRINT_ITEM`

**Progress state**
- complete
