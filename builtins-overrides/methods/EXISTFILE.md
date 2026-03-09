**Summary**
- Tests whether a file exists under the executable directory using the engine's safe relative-path normalization.

**Tags**
- files

**Syntax**
- `EXISTFILE(relativePath)`

**Signatures / argument rules**
- `EXISTFILE(relativePath)` → `long`

**Arguments**
- `relativePath` (string): file path relative to the executable directory.

**Semantics**
- Normalizes the supplied path before checking:
  - `/` is converted to `\`,
  - literal parent-directory segments are stripped after that slash normalization, so both `../` and `..\` are removed rather than rejected,
  - rooted / absolute paths are rejected.
- The resulting relative path is resolved under the executable directory.
- Returns `1` if the resolved path exists and is a file.
- Returns `0` if normalization fails or the resolved file does not exist.
- This API does **not** apply the `LOADTEXT` / `SAVETEXT` extension allow-list.
- Path-handling family: see `filesystem-paths.md` Family A.

**Errors & validation**
- None.

**Examples**
- `EXISTFILE("csv/VariableSize.csv")` → `1` when that file exists

**Progress state**
- complete
