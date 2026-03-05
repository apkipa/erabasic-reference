**Summary**
- Saves global variables to `global.sav`.

**Tags**
- save-system

**Syntax**
- `SAVEGLOBAL`

**Arguments**
- None.

**Semantics**
- Writes the global save file under `SavDir`:
  - Path is `global.sav`.
- Save format:
  - If `SystemSaveInBinary` is enabled, writes Emuera’s binary save format with file type `Global`.
  - Otherwise, writes the legacy text save format.
  - Emuera-private global extension blocks may also be written.
- If a system-level I/O exception occurs during saving, the engine raises a runtime error.
- See also: `save-files.md` (directories, partitions, and on-disk formats)

**Errors & validation**
- Errors if the save directory cannot be created or the file cannot be written.

**Examples**
- `SAVEGLOBAL`

**Progress state**
- complete
