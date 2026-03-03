**Summary**
- Deletes a numbered save slot file (`saveXX.sav`) if it exists.

**Syntax**
- `DELDATA <slot>`

**Arguments**
- `<slot>`: integer expression. Must be in `[0, 2147483647]` (32-bit signed non-negative).
  - If omitted, the argument parser supplies `0` (with a warning); this deletes slot `0`.

**Defaults / optional arguments**
- None (but see omitted-argument behavior above).

**Semantics**
- Computes the save file path under `Config.SavDir` as `save{slot:00}.sav`.
- If the file does not exist, does nothing.
- If the file exists:
  - If it has the read-only attribute, raises an error.
  - Otherwise deletes it.
- See also: `save-files.md` (directories, partitions, and on-disk formats)

**Errors & validation**
- Errors if `<slot>` is negative or larger than `int.MaxValue`.
- Error if the file exists and is read-only.

**Examples**
- `DELDATA 3`

**Progress state**
- complete
