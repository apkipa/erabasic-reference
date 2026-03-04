**Summary**
- Loads characters from `dat/chara_<name>.dat` and appends them to the current character list.

**Tags**
- characters
- save-system

**Syntax**
- `LOADCHARA <name>`

**Arguments**
- `<name>`: string expression; the file name component.

**Semantics**
- Reads `Program.DatDir/chara_<name>.dat`.
- If the file exists and passes validation (file type, unique code, version):
  - Deserializes the characters and appends them to the current character list.
  - Sets `RESULT = 1`.
- Otherwise:
  - Does nothing and sets `RESULT = 0`.
- See also: `save-files.md` (directories, partitions, and on-disk formats)

**Errors & validation**
- No explicit errors are raised for “file not found” / “invalid file”; failures are reported via `RESULT`.

**Examples**
- `LOADCHARA "party"`

**Progress state**
- complete
