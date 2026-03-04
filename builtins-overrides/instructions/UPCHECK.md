**Summary**
- Applies the `UP`/`DOWN` delta arrays to `PALAM` for the current `TARGET` character, and prints each applied change.

**Tags**
- characters
- io

**Syntax**
- `UPCHECK`

**Arguments**
- None.

**Semantics**
- Reads:
  - global arrays `UP` and `DOWN`
  - the current `TARGET` character index
  - the target character’s `PALAM` array
  - parameter names from `PALAMNAME`
- If `TARGET` is out of range (`TARGET < 0` or `TARGET >= CHARANUM`):
  - no parameter changes are applied, and nothing is printed
  - it still clears `UP` and `DOWN` to `0` (see below).
- Otherwise, it computes the loop bound `length` as follows (note the ordering):
  - Start with `length = PALAM.Length`.
  - If `PALAM.Length > UP.Length`, set `length = UP.Length`.
  - If `PALAM.Length > DOWN.Length`, set `length = DOWN.Length`.
- For each parameter index `i` such that `0 <= i < length`:
  - Negative and zero deltas are ignored: if `UP[i] <= 0` and `DOWN[i] <= 0`, this index is skipped (no change, no output).
  - Otherwise:
    - Let `old = PALAM[i]`.
    - Apply the change in an `unchecked` context: `PALAM[i] = old + UP[i] - DOWN[i]`.
    - If output is not being skipped, prints one line (and ends the line) in this exact format:
      - `PALAMNAME[i] + " " + old + ("+" + UP[i] if UP[i] > 0) + ("-" + DOWN[i] if DOWN[i] > 0) + "=" + PALAM[i]`
      - Notes:
        - There are no parentheses around `+...` / `-...`.
        - If `PALAMNAME[i]` is `null`, it is treated as `""` (so the line starts with a space).
        - Each printed change ends the line immediately (i.e. it is printed as its own line).
- After finishing, clears **all elements** of `UP` and `DOWN` to `0`.
- If output skipping is active (`SKIPDISP` / `skipPrint`), changes are still applied and `UP`/`DOWN` are still cleared, but nothing is printed.

**Errors & validation**
- None specific to this instruction.

**Examples**
```erabasic
UP:0 = 123
UP:1 = 456
UPCHECK
```

**Progress state**
- complete
