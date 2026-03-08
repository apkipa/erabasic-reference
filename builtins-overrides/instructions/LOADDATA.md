**Summary**
- Loads a numbered save slot file (script-controlled load), resets the call stack, and then runs the engine’s post-load system hooks.

**Tags**
- save-system

**Syntax**
- `LOADDATA [<slot>]`

**Arguments**
- `<slot>` (optional, int; default `0`; omission emits a warning): save slot index. Must be in `[0, 2147483647]` (32-bit signed non-negative).

**Semantics**
- Validates the target save file; if the file is missing/corrupt/mismatched, raises a runtime error.
- Before applying the loaded payload, the engine resets the normal non-global runtime buckets to their default state: local stores, static non-global user variables, non-global built-in variables, and the current character list.
- It then loads the save slot payload into the normal-save partitions.
  - `GLOBAL/GLOBALS` and ERH `GLOBAL` user variables are **not** reset by this instruction.
  - Private `STATIC` variables and local stores are **not** restored from the save file; after `LOADDATA` they remain in their reset/default state.
- Within the partitions that are actually stored in a normal save slot, the loaded file contents replace the current runtime values.
- Sets the pseudo variables:
  - `LASTLOAD_NO` to the loaded slot number
  - `LASTLOAD_TEXT` to the saved `<saveText>`
  - `LASTLOAD_VERSION` to the save file’s recorded script version
- Clears the EraBasic call stack, discarding the current call context.
  - Any live private `DYNAMIC` instances or private `REF` bindings from that old stack disappear at this boundary.
- Runs post-load system hooks (if they exist), in this order:
  - `SYSTEM_LOADEND`
  - `EVENTLOAD`
- If `EVENTLOAD` returns normally without performing a `BEGIN`, the engine enters the SHOP main loop fallback: it proceeds to `@SHOW_SHOP` / command input without calling `@EVENTSHOP` and without performing the SHOP-entry autosave.
- See also: `save-files.md` (directories, partitions, and on-disk formats).

**Errors & validation**
- Errors if `<slot>` is negative or larger than `int.MaxValue`.
- Error if the target save file is missing/corrupt/mismatched.
- If loading fails unexpectedly after validation, a runtime error is raised.

**Examples**
- `LOADDATA 0`

**Progress state**
- complete
