**Summary**
- Like `UPCHECK`, but applies `CUP`/`CDOWN` to `PALAM` for a specified character index.

**Tags**
- characters
- io

**Syntax**
- `CUPCHECK [charaIndex]`

**Arguments**
- `charaIndex` (optional, int; default `0`; omission emits a warning): the character index to apply changes to.

**Semantics**
- Reads the target character’s per-character arrays:
  - `CUP` and `CDOWN`
  - and that character’s `PALAM`
- If `charaIndex` is out of range, returns immediately:
  - no changes are applied, nothing is printed
  - `CUP`/`CDOWN` are **not** cleared.
- Otherwise, it computes the loop bound `length` as follows (note the ordering):
  - Start with `length = PALAM.Length`.
  - If `PALAM.Length > CUP.Length`, set `length = CUP.Length`.
  - If `PALAM.Length > CDOWN.Length`, set `length = CDOWN.Length`.
- For each parameter index `i` such that `0 <= i < length`:
  - Negative and zero deltas are ignored: if `CUP[i] <= 0` and `CDOWN[i] <= 0`, this index is skipped.
  - Otherwise:
    - Let `old = PALAM[i]`.
    - Apply the change in an `unchecked` context: `PALAM[i] = old + CUP[i] - CDOWN[i]`.
    - If output is not being skipped, prints one line (and ends the line) in the same format as `UPCHECK`, but using `CUP`/`CDOWN`:
      - `PALAMNAME[i] + " " + old + ("+" + CUP[i] if CUP[i] > 0) + ("-" + CDOWN[i] if CDOWN[i] > 0) + "=" + PALAM[i]`
      - Each printed change ends the line immediately (i.e. it is printed as its own line).
- After finishing, clears **all elements** of that character’s `CUP` and `CDOWN` arrays to `0`.
- If output skipping is active (via `SKIPDISP`), changes are still applied and `CUP`/`CDOWN` are still cleared, but nothing is printed.

**Errors & validation**
- None specific to this instruction (out-of-range just returns).

**Examples**
```erabasic
CUP:TARGET:0 = 10
CUPCHECK TARGET
```

**Progress state**
- complete
