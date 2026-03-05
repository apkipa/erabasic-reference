**Summary**
- Loads a numbered save slot file (script-controlled load), resets the call stack, and then runs the engine’s post-load system hooks.

**Tags**
- save-system

**Syntax**
- `LOADDATA [<slot>]`

**Arguments**
- `<slot>` (optional, int; default `0` with a warning if omitted): save slot index. Must be in `[0, 2147483647]` (32-bit signed non-negative).

**Semantics**
- Validates the target save file; if the file is missing/corrupt/mismatched, raises a runtime error.
- Loads the save slot and replaces the current saveable state (characters and variables) with the loaded contents.
- Sets the pseudo variables:
  - `LASTLOAD_NO` to the loaded slot number
  - `LASTLOAD_TEXT` to the saved `<saveText>`
  - `LASTLOAD_VERSION` to the save file’s recorded script version
- Clears the EraBasic call stack, discarding the current call context.
- Runs post-load system hooks (if they exist), in this order:
  - `SYSTEM_LOADEND`
  - `EVENTLOAD`
- If `EVENTLOAD` returns normally without performing a `BEGIN`, execution proceeds as if `BEGIN SHOP` occurred.
- See also: `save-files.md` (directories, partitions, and on-disk formats).

**Errors & validation**
- Errors if `<slot>` is negative or larger than `int.MaxValue`.
- Error if the target save file is missing/corrupt/mismatched.
- If loading fails unexpectedly after validation, a runtime error is raised.

**Examples**
- `LOADDATA 0`

**Progress state**
- complete
