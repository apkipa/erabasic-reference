**Summary**
- Loads a numbered save slot file (script-controlled load), resets the call stack, and then runs the engine’s post-load system hooks.

**Syntax**
- `LOADDATA <slot>`

**Arguments**
- `<slot>`: integer expression. Must be in `[0, 2147483647]` (32-bit signed non-negative).
  - If omitted, the argument parser supplies `0` (with a warning); this effectively loads slot `0`.

**Defaults / optional arguments**
- None (but see omitted-argument behavior above).

**Semantics**
- Validates the target save file via `CheckData(slot, Normal)`; if the file is missing/corrupt/mismatched, raises an error.
- Loads the save file:
  - Resets variable state and reloads characters/variables from the file (implementation detail).
  - Sets the pseudo variables:
    - `LASTLOAD_NO` to the loaded slot number
    - `LASTLOAD_TEXT` to the saved `<saveText>`
    - `LASTLOAD_VERSION` to the save file’s recorded script version
- Clears the EraBasic function stack (`state.ClearFunctionList()`), discarding the current call context.
- Transfers control into the system “data loaded” phase:
  - Sets `SystemState = LoadData_DataLoaded`.
  - System processing then calls (if they exist):
    - `SYSTEM_LOADEND`
    - `EVENTLOAD`
  - If `EVENTLOAD` returns normally without performing a `BEGIN`, the engine proceeds as if `BEGIN SHOP` occurred (implementation detail).
- See also: `save-files.md` (directories, partitions, and on-disk formats)

**Errors & validation**
- Errors if `<slot>` is negative or larger than `int.MaxValue`.
- Error if the file is not considered valid by `CheckData(..., Normal)` (“corrupted save data” path).
- If loading fails after validation, the engine throws an internal execution error.

**Examples**
- `LOADDATA 0`

**Progress state**
- complete
