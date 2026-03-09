**Summary**
- Loads text either from a numbered text-save slot or from an explicit relative path.

**Tags**
- files
- io

**Syntax**
- `LOADTEXT(source [, forceSavdir [, forceUTF8]])`

**Signatures / argument rules**
- `LOADTEXT(fileNo)` → `string`
- `LOADTEXT(fileNo, forceSavdir)` → `string`
- `LOADTEXT(fileNo, forceSavdir, forceUTF8)` → `string`
- `LOADTEXT(relativePath)` → `string`
- `LOADTEXT(relativePath, forceSavdir)` → `string`
- `LOADTEXT(relativePath, forceSavdir, forceUTF8)` → `string`

**Arguments**
- `source` (int or string): numbered save slot or explicit relative path.
- `forceSavdir` (optional, int; default `0`): in numeric-slot mode, non-zero forces the dedicated save-folder path; in explicit-path mode, ignored.
- `forceUTF8` (optional, int; default `0`): legacy compatibility argument with no observable effect in this build.

**Semantics**
- Numeric-slot mode (`source` is int):
  - If `source < 0` or `source > 2147483647`, returns `""`.
  - Resolves the source filename as `txt{source:00}.txt` in the normal save-text directory, or the forced save-text directory when `forceSavdir != 0`.
- Explicit-path mode (`source` is string):
  - Applies the same safe relative-path normalization used by `EXISTFILE`.
  - So parent-directory segments such as `../` / `..\` are stripped rather than rejected.
  - If normalization fails, returns `""`.
  - The path must already have an extension present in config item `ValidExtension`; otherwise returns `""`.
  - `forceSavdir` is ignored.
- Reading behavior shared by both modes:
  - if the resolved file does not exist, returns `""`,
  - reads the entire file,
  - detects encoding as UTF-8 with BOM / UTF-8 when valid, otherwise falls back to Shift-JIS,
  - removes every `` character from the loaded text before returning it,
  - returns `""` on any failure.
- Path-handling family for explicit-path mode: see `filesystem-paths.md` Family A.

**Errors & validation**
- None; failure paths return `""`.

**Examples**
- `text = LOADTEXT(2)`
- `text = LOADTEXT("notes/memo.txt")`

**Progress state**
- complete
