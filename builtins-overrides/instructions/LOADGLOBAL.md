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
- On success:
  - Loads the global variable data from the file (format depends on file type).
  - Sets `RESULT = 1`.
- On failure:
  - Sets `RESULT = 0`.
- Before attempting to read, the loader removes certain Emuera-private global extension data; if loading then fails, this removal may still have occurred.
- See also: `save-files.md` (directories, partitions, and on-disk formats)

**Errors & validation**
- No explicit errors are raised for load failures; failures are reported via `RESULT`.

**Examples**
- `LOADGLOBAL`

**Progress state**
- complete
