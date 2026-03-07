**Summary**
- Deletes a numbered save slot file (`saveXX.sav`) if it exists.

**Tags**
- save-system

**Syntax**
- `DELDATA [<slot>]`

**Arguments**
- `<slot>` (optional, int; default `0`; omission emits a warning): save slot index. Must be in `[0, 2147483647]` (32-bit signed non-negative).

**Semantics**
- Computes the save file path under `SavDir` as `save{slot:00}.sav`.
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
