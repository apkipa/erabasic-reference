**Summary**
- Saves the current game state to a numbered save slot file (script-controlled save).

**Tags**
- save-system

**Syntax**
- `SAVEDATA <slot>, <saveText>`

**Arguments**
- `<slot>` (int): save slot number. Must satisfy `0 <= slot <= 2147483647` (32-bit signed non-negative).
- `<saveText>` (string): saved into the file and shown by the built-in save/load UI.
  - Must not contain a newline (`'\n'`).

**Semantics**
- Evaluates `<slot>` and `<saveText>`.
- Writes a save file under `SavDir`:
  - Path is `save{slot:00}.sav` (e.g. slot `0` -> `save00.sav`).
- Save format:
  - If config item `SystemSaveInBinary` is enabled, writes Emuera’s binary save format with file type `Normal`.
  - Otherwise, writes the legacy text save format.
  - The save always includes:
    - game unique code and script version checks
    - the `<saveText>` string
    - the current character list and variable data
    - Emuera-private extension blocks (if applicable)
- If saving fails unexpectedly (I/O error, etc.), the engine prints an error message but does not throw.
- See also: `save-files.md` (directories, partitions, and on-disk formats)

**Errors & validation**
- Errors if `<slot>` is negative or larger than `int.MaxValue`.
- Error if `<saveText>` contains `'\n'`.

**Examples**
- `SAVEDATA 0, "Start of day 1"`
- `SAVEDATA 12, SAVEDATA_TEXT`

**Progress state**
- complete
