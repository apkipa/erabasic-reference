**Summary**
- Loads global variables from `global.sav` and reports success via `RESULT`.

**Tags**
- save-system

**Syntax**
- `LOADGLOBAL`

**Arguments**
- None.

**Semantics**
- Attempts to load `global.sav` under `SavDir`.
- This instruction does **not** perform `RESETGLOBAL` first.
  - Built-in `GLOBAL/GLOBALS` are loaded from the file.
  - ERH user variables are reloaded only for the `GLOBAL SAVEDATA` subset.
  - ERH `GLOBAL` variables without `SAVEDATA` keep their current in-memory values across `LOADGLOBAL`.
- On success:
  - Loads the global variable data from the file (format depends on file type).
  - Sets `RESULT = 1`.
- On failure:
  - Sets `RESULT = 0`.
- Before attempting to read, the loader removes certain Emuera-private global extension data; if loading then fails, this removal may still have occurred.
- It does not clear the current call stack, does not run post-load system hooks, and does not touch the current character list or non-global runtime buckets.
- See also: `save-files.md` (directories, partitions, and on-disk formats)

**Errors & validation**
- No explicit errors are raised for load failures; failures are reported via `RESULT`.

**Examples**
- `LOADGLOBAL`

**Progress state**
- complete
