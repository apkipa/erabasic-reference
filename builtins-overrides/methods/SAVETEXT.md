**Summary**
- Saves a string either to a numbered text-save slot or to an explicit relative path.

**Tags**
- files
- io

**Syntax**
- `SAVETEXT(text, target [, forceSavdir [, forceUTF8]])`

**Signatures / argument rules**
- `SAVETEXT(text, fileNo)` → `long`
- `SAVETEXT(text, fileNo, forceSavdir)` → `long`
- `SAVETEXT(text, fileNo, forceSavdir, forceUTF8)` → `long`
- `SAVETEXT(text, relativePath)` → `long`
- `SAVETEXT(text, relativePath, forceSavdir)` → `long`
- `SAVETEXT(text, relativePath, forceSavdir, forceUTF8)` → `long`

**Arguments**
- `text` (string): content to write.
- `target` (int or string): numbered save slot or explicit relative path.
- `forceSavdir` (optional, int; default `0`): in numeric-slot mode, non-zero forces the dedicated save-folder path; in explicit-path mode, ignored.
- `forceUTF8` (optional, int; default `0`): legacy compatibility argument with no observable effect in this build.

**Semantics**
- Numeric-slot mode (`target` is int):
  - If `target < 0` or `target > 2147483647`, returns `0`.
  - Resolves the destination filename as `txt{target:00}.txt` in the normal save-text directory, or the forced save-text directory when `forceSavdir != 0`.
  - Creates the chosen destination directory if needed.
- Explicit-path mode (`target` is string):
  - Applies the same safe relative-path normalization used by `EXISTFILE`.
  - So parent-directory segments such as `../` / `..\` are stripped rather than rejected.
  - If normalization fails, returns `0`.
  - If the path's extension is missing or not present in config item `ValidExtension`, rewrites the extension to `.txt`.
  - Creates any missing parent directories under the resolved path.
  - `forceSavdir` is ignored.
- Writing behavior shared by both modes:
  - writes the exact string content without newline normalization or automatic extra terminators,
  - writes using the runtime save-text encoding; in this build that encoding is UTF-8 with BOM,
  - returns `1` on success and `0` on any failure.
- Path-handling family for explicit-path mode: see `filesystem-paths.md` Family A.

**Errors & validation**
- None; failure paths return `0`.

**Examples**
- `SAVETEXT("hello", 2)`
- `SAVETEXT("hello", "notes/memo.txt")`

**Progress state**
- complete
