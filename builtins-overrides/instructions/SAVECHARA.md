**Summary**
- Saves one or more characters into a `dat/chara_<name>.dat` file (binary only).

**Tags**
- characters
- save-system

**Syntax**
- `SAVECHARA <name>, <saveText>, <charaNo1> [, <charaNo2> ...]`

**Arguments**
- `<name>`: string expression; the file name component.
- `<saveText>`: string expression stored in the file as a description.
- `<charaNo*>`: one or more integer expressions; character indices to save (0-based).

**Semantics**
- Writes a binary file under `Program.DatDir`:
  - Path is `chara_<name>.dat`.
- File format:
  - Binary save format with file type `CharVar`.
  - Includes game unique code and script version checks, `<saveText>`, and the serialized character data.
- Validates the character list:
  - All indices must be within `[0, CHARANUM-1]`.
  - Duplicate indices are rejected.
- See also: `save-files.md` (directories, partitions, and on-disk formats)

**Errors & validation**
- Argument parsing requires at least 3 arguments.
- Errors if any character index is negative, too large, out of range, or duplicated.
- File name validity is ultimately enforced by the OS; invalid names can cause runtime errors.

**Examples**
- `SAVECHARA "party", "Before boss", MASTER, TARGET`

**Progress state**
- complete
